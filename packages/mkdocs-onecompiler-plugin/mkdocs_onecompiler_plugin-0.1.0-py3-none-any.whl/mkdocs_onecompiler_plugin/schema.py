from typing import Literal
from urllib.parse import urlencode

from pydantic import BaseModel  # noqa: E0611

IFRAME_TEMPLATE = """
<iframe id="{id_value}" referrerpolicy="no-referrer" name="{id_value}" class="{classes}" src="{src}" height="{height}" width="{width}" onload='this.contentWindow.postMessage({{
        eventType: "populateCode",
        language: "{lang}",
        files: [
            {{
                "name": "{filename}",
                "content": String.raw`{content}`
            }}
        ]
    }}, "*");'>
</iframe>
"""


class OneCompiler(BaseModel):
    """Schema to build a valid OneCompiler iframe"""

    # lang
    lang: str
    # file name
    filename: str = "untitled"
    # content
    content: str = ""
    # api
    baseUrl: str = "https://onecompiler.com/embed/"
    # html
    width: str = "100%"
    height: str = "450px"
    id_value: str = ""
    classes: str = ""
    # options
    availableLanguages: bool = (
        True  # To limit the languages in the Language selection popup
    )
    hideLanguageSelection: bool = (
        False  # To hide the language selection button
    )
    hideNew: bool = False  # To hide the 'New' button
    hideNewFileOption: bool = False  # Disables new file creation button
    disableCopyPaste: bool = False  # Disables copy/paste functionality
    hideStdin: bool = False  # To hide the STDIN section
    hideResult: bool = False  # To hide the Result section including STDIN
    hideTitle: bool = False  # To hide the Title/Code ID
    listenToEvents: bool = True  # Editor will keep listening for events like code change/ run from parent website
    theme: Literal["light", "dark"] = "light"  # For Darkmode editor

    @property
    def query_params(self) -> str:
        """Return the url query params"""

        # dump the model
        raw = self.model_dump(
            exclude=[
                "width",
                "height",
                "id_value",
                "classes",
                "baseUrl",
                "content",
                "filename",
                "lang",
            ]
        )

        # correct the dict because we need lowercase boolean ("true" and "false")
        # but urlencode keep them uppercase...
        corrected = dict(
            (k, f"{v}".lower()) if isinstance(v, bool) else (k, v)
            for k, v in raw.items()
        )

        return urlencode(corrected)

    def html(self) -> str:
        """Output the formatted iframe that can directly be inserted into html"""
        src = f"{self.baseUrl}{self.lang}?{self.query_params}"
        return IFRAME_TEMPLATE.format(
            src=src,
            width=self.width,
            height=self.height,
            filename=self.filename,
            content=self.content,
            lang=self.lang,
            id_value=self.id_value,
            classes=self.classes,
        )
