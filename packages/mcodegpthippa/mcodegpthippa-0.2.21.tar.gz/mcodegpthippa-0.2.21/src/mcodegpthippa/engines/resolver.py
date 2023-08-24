"""Resolver engine."""
from typing import Optional, Type, Union

from class_resolver import ClassResolver

from mcodegpthippa.engines.enrichment import EnrichmentEngine
from mcodegpthippa.engines.halo_engine import HALOEngine
from mcodegpthippa.engines.knowledge_engine import KnowledgeEngine
from mcodegpthippa.engines.spires_engine import SPIRESEngine

resolver = ClassResolver([SPIRESEngine, HALOEngine, EnrichmentEngine], base=KnowledgeEngine)


def create_engine(
    template: str, engine: Optional[Union[str, Type]] = None, **kwargs
) -> KnowledgeEngine:
    """Create a knowledge engine."""
    if engine is None:
        engine = SPIRESEngine
    if isinstance(engine, str):
        engine = resolver.get_class(engine)(**kwargs)
    return engine(template, **kwargs)
