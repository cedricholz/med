import bleach
from django.db import models
class HtmlField(models.TextField):
    description = "Clean HTML field"

    def to_python(self, value):
        value = super().to_python(value)
        if value is None:
            return None
        allowed_tags = [
            "a",
            "abbr",
            "acronym",
            "address",
            "b",
            "br",
            "div",
            "dl",
            "dt",
            "em",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "hr",
            "i",
            "img",
            "li",
            "ol",
            "p",
            "pre",
            "q",
            "s",
            "small",
            "strike",
            "strong",
            "span",
            "sub",
            "sup",
            "table",
            "tbody",
            "td",
            "tfoot",
            "th",
            "thead",
            "tr",
            "tt",
            "u",
            "ul",
        ]

        allowed_attrs = {
            "a": ["href", "target", "title"],
            "img": ["src", "alt", "width", "height"],
        }
        return bleach.clean(
            value,
            tags=allowed_tags,
            attributes=allowed_attrs,
            strip=True,
        )