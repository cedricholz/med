from django.db import models

from base.base import BaseModel


# ----------------------------------------
# Media Storage
# ----------------------------------------

class File(BaseModel):
    url = models.URLField(max_length=2048, blank=True, null=True)

    def __str__(self):
        file = self
        return f"{file.url}"
