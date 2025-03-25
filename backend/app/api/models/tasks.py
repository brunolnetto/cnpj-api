from typing import List, Dict, Callable, Optional, Any
from uuid import uuid4

from pydantic import BaseModel, Field, UUID4


class TaskBase(BaseModel):
    """Base model for a task."""

    task_id: UUID4 = Field(
        default_factory=uuid4,
        title="Task ID",
        description="The unique identifier of the task",
    )
    task_schedule_type: str = Field(
        ..., title="Task Schedule Type", description="The type of the task schedule"
    )
    task_schedule_params: Dict[str, Any] = Field(
        ...,
        title="Task Schedule Params",
        description="The parameters for the task schedule",
    )
    task_name: str = Field(..., title="Task Name", description="The name of the task")
    task_callable: str = Field(
        ...,
        title="Task Callable",
        description="The function or method that executes the task logic",
    )
    task_type: str = Field(..., title="Task Type", description="The type of the task")
    task_is_active: Optional[bool] = Field(
        True, title="Task Active", description="Indicates if the task is active"
    )


class TaskCreate(TaskBase):
    """Model for creating a new task."""

    pass


class TaskRead(TaskBase):
    """Model for reading task information."""

    class Config:
        from_attributes = True


class TaskResponse(TaskBase):
    """Model for the task response."""

    class Config:
        from_attributes = True


class TaskConfig(BaseModel):
    """Configuration for a task."""

    task_id: UUID4 = Field(default_factory=uuid4)
    schedule_type: str = Field(..., description="Type of the schedule")
    schedule_params: Dict[str, Any] = Field(
        default_factory=dict, description="Parameters for the schedule"
    )
    task_name: str = Field(..., description="Name of the task")
    task_type: str = Field(..., description="Type of the task")
    task_callable: Callable = Field(..., description="Callable for the task logic")
    task_args: List[Any] = Field(
        default_factory=list, description="Arguments for the task callable"
    )
    task_details: Dict[str, Any] = Field(
        default_factory=dict, description="Additional details about the task"
    )

    def __eq__(self, other):
        if not isinstance(other, TaskConfig):
            return NotImplemented

        return all(
            (
                self.schedule_type == other.schedule_type,
                self.schedule_params == other.schedule_params,
                self.task_name == other.task_name,
                self.task_type == other.task_type,
                self.task_callable == other.task_callable,
                self.task_args == other.task_args,
                self.task_details == other.task_details,
            )
        )

    def __hash__(self):
        return hash(
            (
                self.schedule_type,
                # Using frozenset for hashability
                frozenset(self.schedule_params.items()),
                self.task_name,
                self.task_type,
                self.task_callable,
                tuple(self.task_args),
                # Using frozenset for hashability
                frozenset(self.task_details.items()),
            )
        )
