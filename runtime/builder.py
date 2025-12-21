import importlib
import yaml
from pathlib import Path

from specs.agent_service import AgentServiceSpec
from runtime.service import AgentService


def load_spec(spec_path: Path) -> AgentServiceSpec:
    raw = yaml.safe_load(spec_path.read_text())
    return AgentServiceSpec.model_validate(raw)


def load_agent(agent_dir: Path):
    module_path = ".".join(agent_dir.parts)
    module = importlib.import_module(f"{module_path}.agent")

    if hasattr(module, "agent"):
        return module.agent

    agents = [
        v for v in vars(module).values()
        if v.__class__.__name__ == "Agent"
    ]

    if len(agents) != 1:
        raise RuntimeError("agent.py must expose exactly one Agent")

    return agents[0]


def build_agent_service(agent_dir: Path) -> AgentService:
    agent_dir = Path(agent_dir)
    spec_path = agent_dir / "spec.yaml"

    spec = load_spec(spec_path)

    agent = load_agent(agent_dir)

    return AgentService(
        identity=spec.identity,
        interface=spec.interface,
        runtime=spec.runtime,
        agent=agent,
    )
