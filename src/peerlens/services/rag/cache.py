from collections import OrderedDict

from peerlens.models.context import AnalysisContext

_CONTEXT_CACHE: OrderedDict[str, AnalysisContext] = OrderedDict()
_CACHE_LIMIT = 24


def cache_context(identifier: str, context: AnalysisContext) -> None:
    _CONTEXT_CACHE[identifier] = context
    _CONTEXT_CACHE.move_to_end(identifier)
    while len(_CONTEXT_CACHE) > _CACHE_LIMIT:
        _CONTEXT_CACHE.popitem(last=False)


async def get_analysis_context(identifier: str) -> AnalysisContext:
    if identifier in _CONTEXT_CACHE:
        _CONTEXT_CACHE.move_to_end(identifier)
        return _CONTEXT_CACHE[identifier]

    from peerlens.services.reports import build_analysis_context

    context = await build_analysis_context(identifier)
    cache_context(identifier, context)
    return context
