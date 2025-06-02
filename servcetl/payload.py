from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class NoSpecPayload(BaseModel):
    tenant_name: str
    app_id: str
    job_id: str


F = TypeVar("F", bound=NoSpecPayload)


class Payload(NoSpecPayload, Generic[T]):
    # token_id: str # TODO: add token_id to enforce tenant isolation
    spec: T


class PartPayload(BaseModel, Generic[F]):
    inputs: F


class PayloadReturn(BaseModel, Generic[T]):
    payload: Optional[T]
    message: Optional[str]
