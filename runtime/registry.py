from typing import Dict
from runtime.service import AgentService


class AgentRegistry:
    def __init__(self):
        self._services: Dict[str, AgentService] = {}

    def register(self, service: AgentService):
        self._services[service.identity.fqdn] = service

    def get(self, fqdn: str) -> AgentService:
        return self._services[fqdn]
