from enum import Enum
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


class ProvisionerType(Enum):
    DEPLOYMENT = "deployment"
    CRON = "cron"


class Resource(BaseModel):
    cpu: str
    memory: str


class Resources(BaseModel):
    requests: Resource
    limits: Resource


class EnvVariable(BaseModel):
    name: str
    value: str


class Deployment(ProvisionerComponent):
    image: str
    resources: Resources
    pullSecret: List[str]
    env: List[EnvVariable]
    queueName: str
    maxReplicas: int


class CronTrigger(ProvisionerComponent):
    image: str
    resources: Resources
    pullSecret: List[str]
    env: List[EnvVariable]
    cron: str
    cmd: List[str]
