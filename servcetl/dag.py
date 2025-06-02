from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class ProvisionerComponent(BaseModel):
    type: str
    name: str

    model_config = ConfigDict(
        extra="allow",
    )


class Step(BaseModel):
    name: str
    type: str
    queue: str
    method: str


class Notifier(BaseModel):
    complete: Optional[List[Step]]
    failure: Optional[List[Step]]


class Dag(BaseModel):
    steps: List[Step]
    notifiers: Notifier
    provisioner: List[ProvisionerComponent]
