from django.db import models
from webapp.models import BaseModel


class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name
