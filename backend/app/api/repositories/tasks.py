from typing import Dict, List, Any, Annotated, Optional

from fastapi import Depends
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID

from backend.app.setup.config import settings
from backend.app.database.base import get_session
from backend.app.database.models.logs import Task
from backend.app.api.repositories.base import BaseRepository


class TaskRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def create(self, task_data: Dict[str, Any]) -> Task:
        try:
            # Check if the task already exists
            existing_task = (
                self.session.execute(
                    select(Task).filter_by(
                        task_name=task_data.get("task_name"),
                        task_type=task_data.get("task_type"),
                    )
                )
                .scalars()
                .first()
            )

            if existing_task:
                # Update the existing task
                return self.update(existing_task.task_id, task_data)

            # Create a new task
            task = Task(**task_data)
            self.session.add(task)
            self.session.commit()
            self.session.refresh(task)
            return task
        except Exception as e:
            self.session.rollback()  # Rollback in case of error
            raise Exception(f"Error creating task: {e}")

    def update(self, task_id: UUID, task_data: Dict[str, Any]) -> Optional[Task]:
        try:
            task = self.get_by_id(task_id)
            if not task:
                return None

            # Update fields from task_data
            for key, value in task_data.items():
                setattr(task, key, value)

            self.session.commit()
            self.session.refresh(task)
            return task
        except Exception as e:
            self.session.rollback()  # Rollback in case of error
            raise Exception(f"Error updating task: {e}")

    def get_by_id(self, task_id: UUID) -> Optional[Task]:
        try:
            return self.session.get(Task, task_id)
        except Exception as e:
            raise Exception(f"Error fetching task by id: {e}")

    def get_all(self, limit: int = 100, offset: int = 0) -> List[Task]:
        try:
            return (
                self.session.execute(select(Task).offset(offset).limit(limit))
                .scalars()
                .all()
            )
        except Exception as e:
            raise Exception(f"Error fetching all tasks: {e}")

    def delete_by_id(self, id: UUID) -> bool:
        try:
            task = self.get_by_id(id)
            if not task:
                return False

            self.session.delete(task)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()  # Rollback in case of error
            raise Exception(f"Error deleting task: {e}")

def get_task_repository():
    with get_session(settings.POSTGRES_DBNAME_AUDIT) as session:
        return TaskRepository(session)


TaskRepositoryDependency = Annotated[TaskRepository, Depends(get_task_repository)]
