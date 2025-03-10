from sqlalchemy.orm import Session
from typing import List
from collections import defaultdict
import re
from .models import Task


def generate_smart_suggestions(db: Session) -> List[str]:
    tasks = db.query(Task).all()

    for task in tasks:
        match = re.match(
            r"Project (.+?) (Review|Follow-up Meeting|Finalization)", task.title, re.I
        )
        if match:
            project_name, stage = match.groups()
            project_name = project_name.strip()
            stage = stage.strip().lower()
            project_stages = project_stage_map[project_name]
            project_stages.add(stage)

    suggestions = []
    for project, stages in project_stage_map.items():
        if "review" in stages and "follow-up meeting" not in stages:
            suggestions.append(f"Project {project} Follow-up Meeting")
        if "follow-up meeting" in stages and "finalization" not in stages:
            suggestions.append(f"Project {project} Finalization")

    return suggestions


project_stage_map = defaultdict(set)
