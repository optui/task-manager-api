import torch
from transformers import AutoTokenizer, pipeline
from sqlalchemy.orm import Session
from .models import Task

device = 0 if torch.cuda.is_available() else -1

tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
tokenizer.pad_token = tokenizer.eos_token

generator = pipeline(
    "text-generation",
    model="distilgpt2",
    tokenizer=tokenizer,
    device=0 if torch.cuda.is_available() else -1,
)


def generate_suggestions(prompts, max_suggestions=5):
    results = generator(
        prompts,
        max_length=50,
        do_sample=True,
        temperature=0.9,
        top_p=0.9,
        num_return_sequences=max_suggestions,
        truncation=True,
    )

    suggestions = []
    for item in results:
        if isinstance(item, list):
            suggestions.extend([entry["generated_text"] for entry in item])
        else:
            suggestions.append(item["generated_text"])

    return suggestions


def generate_smart_suggestions_ai(db: Session):
    completed_tasks = (
        db.query(Task)
        .filter(Task.status == "completed")
        .order_by(Task.creation_date.desc())
        .limit(10)
        .all()
    )

    existing_titles = {task.title.lower() for task in completed_tasks}

    task_list = "\n".join([task.title for task in completed_tasks])
    prompt = f"Existing tasks:\n{task_list}\n\nRelated new task:"

    outputs = generate_suggestions([prompt])

    new_tasks = set()
    for output in outputs:
        if prompt in output:
            output = output.replace(prompt, "").strip()

        for line in output.split("\n"):
            task = line.strip("-1234567890. ").strip()
            if (
                task
                and len(task) > 5
                and task.lower() not in existing_titles
                and ":" not in task
            ):
                new_tasks.add(task.title())

    return list(new_tasks)[:5]
