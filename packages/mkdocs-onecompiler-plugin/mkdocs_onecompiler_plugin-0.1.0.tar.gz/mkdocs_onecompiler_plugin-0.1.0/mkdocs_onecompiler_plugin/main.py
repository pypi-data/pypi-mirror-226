from typing import Dict, List

from markdown.core import Markdown
from mkdocs.plugins import get_plugin_logger

from .schema import OneCompiler

logger = get_plugin_logger(__name__)


def formatter(
    source: str,
    language: str = "onecompiler",  # pylint: disable=W0613
    css_class: str = "onecompiler",
    options: Dict[str, str] | None = None,  # pylint: disable=W0613
    md: Markdown = Markdown(),  # pylint: disable=W0613,C0103
    attrs: Dict[str, str] | None = None,
    classes: List[str] | None = None,
    id_value: str = "",
    **kwargs,
) -> str:
    """Turn the fence into onecompiler iframe"""

    # debug
    debug = attrs.pop("debug", "false") == "true"

    if debug:
        for k in formatter.__code__.co_varnames:
            if k in ["k", "oc"]:
                continue
            logger.debug(f"{k}: {locals().get(k)}")

    # add parameters to schema
    attrs |= {
        "id_value": id_value,
        "classes": " ".join([css_class] + classes) if classes else css_class,
        "content": source,
    }
    oc = OneCompiler(**attrs)

    # print result if debug
    if debug:
        logger.debug(oc.html())
    return oc.html()
