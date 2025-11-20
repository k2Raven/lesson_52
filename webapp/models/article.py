from django.db import models
from django.urls import reverse

from webapp.models import BaseModel



class Article(BaseModel):
    title = models.CharField(max_length=50,
                             null=False,
                             blank=False,
                             verbose_name='Заголовок')
    content = models.TextField(verbose_name='Контент')
    author = models.CharField(max_length=50, default='Anonymous', verbose_name='Автор')
    tags = models.ManyToManyField('webapp.Tag', verbose_name="Теги", related_name='articles', blank=True)

    def __str__(self):
        return f'{self.id} - {self.title}'

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'pk': self.pk})
