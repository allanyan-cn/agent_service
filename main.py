import asyncio
from pathlib import Path
from runtime.registry import AgentRegistry
from runtime.builder import build_agent_service

async def main():
    # registry = AgentRegistry()
    # service = build_agent_service(Path("agents/weather_agent"))
    # registry.register(service)

    service = build_agent_service("agents/weather_agent")
    result = await service.call("How is the weather today?")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())