import asyncio
from pathlib import Path
from runtime.registry import AgentRegistry
from runtime.builder import build_agent_service
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),          # console
    ]
)

async def main():
    # registry = AgentRegistry()
    # service = build_agent_service(Path("agents/weather_agent"))
    # registry.register(service)

    service = build_agent_service("agents/weather_agent")
    try:
        result = await service.call("What will the weather be like in Paris tomorrow?")
        print(result)
    except (Exception) as e:
        # 达到重试上限或发生其他错误时，返回你定义的特定信息
        print(f"The agent tried its best, but still failed. Error details:{e}")

if __name__ == "__main__":
    asyncio.run(main())