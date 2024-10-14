from typing import List, Dict, Callable, Optional, Any
from uuid import uuid4

from pydantic import BaseModel, Field, UUID4

class TaskBase(BaseModel):
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
    pass


class TaskRead(TaskBase):
    class ConfigDict:
        from_atributes = True


class TaskResponse(TaskBase):
    class ConfigDict:
        from_atributes = True


class TaskConfig(BaseModel):
    task_id: UUID4 = Field(default_factory=uuid4)
    schedule_type: str
    schedule_params: Dict[str, Any] = Field(default_factory=dict)
    task_name: str
    task_type: str
    task_callable: Callable
    task_args: List[Any] = Field(default_factory=list)
    task_details: Dict[str, Any] = Field(default_factory=dict)

    def __eq__(self, other):
        if not isinstance(other, TaskConfig):
            return NotImplemented

        return (
            self.schedule_type == other.schedule_type
            and self.schedule_params == other.schedule_params
            and self.task_name == other.task_name
            and self.task_type == other.task_type
            and self.task_callable == other.task_callable
            and self.task_args == other.task_args
            and self.task_details == other.task_details
        )

    def __hash__(self):
        # Implementing __hash__ allows TaskConfig to be used in sets or as dict
        # keys
        return hash(
            (
                self.schedule_type,
                tuple(sorted(self.schedule_params.items())),
                self.task_name,
                self.task_type,
                self.task_callable,
                self.task_args,
                tuple(sorted(self.task_details.items())),
            )
        )
