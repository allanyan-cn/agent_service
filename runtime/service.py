from dataclasses import dataclass
from pydantic import BaseModel
from pydantic_ai import Agent


@dataclass
class AgentService:
    identity: object        # IdentitySpec
    interface: object       # InterfaceSpec
    runtime: object         # RuntimeSpec
    agent: Agent            # Executot (point to an agent instance)

    def call(self, input: BaseModel):
        return self.agent.run(input)
