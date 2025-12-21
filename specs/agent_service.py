from pydantic import BaseModel, Field, model_validator
from typing import Literal, Dict, Any, List, Optional
from datetime import date


Protocol = Literal["local", "a2a", "http"]


class IdentitySpec(BaseModel):
    uid: str
    name: str
    namespace: str
    version: str
    owner: str

    @property
    def fqdn(self) -> str:
        return f"{self.namespace}/{self.name}@{self.version}"


class InterfaceSpec(BaseModel):
    input: str
    output: str
    protocols: List[Protocol]


class BehaviorSpec(BaseModel):
    summary: str
    tags: List[str] = Field(default_factory=list)


class ConstraintsSpec(BaseModel):
    pii: bool = True
    max_tokens: Optional[int] = None
    allowed_regions: Optional[List[str]] = None


class MetadataSpec(BaseModel):
    domains: List[str] = Field(default_factory=list)
    suitability: Dict[str, Any] = Field(default_factory=dict)


class DeprecationSpec(BaseModel):
    sunset: Optional[date] = None


class LifecycleSpec(BaseModel):
    stage: Literal["alpha", "beta", "ga", "deprecated"]
    deprecation: Optional[DeprecationSpec] = None

    @model_validator(mode="after")
    def check_deprecation(self):
        if self.stage == "deprecated" and not self.deprecation:
            raise ValueError("Deprecated service must include deprecation info")
        return self


class RuntimeSpec(BaseModel):
    protocol: Protocol
    endpoint: Optional[str] = None
    timeout_ms: int = 3000


class AgentServiceSpec(BaseModel):
    kind: Literal["AgentService"]
    apiVersion: str

    identity: IdentitySpec
    interface: InterfaceSpec
    behavior: BehaviorSpec
    constraints: ConstraintsSpec
    metadata: MetadataSpec
    lifecycle: LifecycleSpec
    runtime: RuntimeSpec

    @model_validator(mode="after")
    def check_protocol_compatibility(self):
        if self.runtime.protocol not in self.interface.protocols:
            raise ValueError(
                f"Runtime protocol '{self.runtime.protocol}' "
                f"not in interface protocols {self.interface.protocols}"
            )
        return self