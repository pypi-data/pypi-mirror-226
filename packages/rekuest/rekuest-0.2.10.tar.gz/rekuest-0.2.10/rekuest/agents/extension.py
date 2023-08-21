from typing import runtime_checkable, Protocol, Optional
from rekuest.api.schema import TemplateFragment
from rekuest.actors.base import Actor, Passport, ActorTransport
from rekuest.messages import Provision
from typing import TYPE_CHECKING
from rekuest.definition.registry import DefinitionRegistry

if TYPE_CHECKING:
    from rekuest.agents.base import BaseAgent


@runtime_checkable
class AgentExtension(Protocol):
    async def aspawn_actor_from_template(
        self,
        template: TemplateFragment,
        passport: Passport,
        transport: ActorTransport,
        agent: "BaseAgent",
    ) -> Optional[Actor]:
        ...

    async def aregister_definitions(
        self, definition_registry: DefinitionRegistry, instance_id: str
    ):
        ...
