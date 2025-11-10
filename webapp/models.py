from django.db import models

status_choices = [('new', 'Новая'), ('in_progress', 'В процессе'), ('done', 'Сделано')]


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        abstract = True


class Article(BaseModel):
    title = models.CharField(max_length=50,
                             null=False,
                             blank=False,
                             verbose_name='Заголовок')
    content = models.TextField(verbose_name='Контент')
    author = models.CharField(max_length=50, default='Anonymous', verbose_name='Автор')
    tags = models.ManyToManyField('webapp.Tag',
                                  verbose_name='Теги',
                                  related_name='articles',
                                  blank=True,
                                  through='webapp.ArticleTag',
                                  through_fields=('article', 'tag'))



    def __str__(self):
        return f'{self.id} - {self.title}'


class Comment(BaseModel):
    article = models.ForeignKey('webapp.Article', related_name='comments', on_delete=models.CASCADE,
                                verbose_name='Статья')
    text = models.TextField(max_length=400, verbose_name='Комментарий')
    author = models.CharField(max_length=40, null=True, blank=True, default='Аноним', verbose_name='Автор')

    def __str__(self):
        return self.text[:20]

class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    # articles = models.ManyToManyField('webapp.Article',
    #                                   verbose_name='Статьи',
    #                                   related_name='tags',
    #                                   blank=True)

    def __str__(self):
        return self.name

class ArticleTag(BaseModel):
    article = models.ForeignKey('webapp.Article', related_name='article_tags',
                                on_delete=models.CASCADE,
                                verbose_name='Статья')
    tag = models.ForeignKey('webapp.Tag', related_name='tag_articles',
                            on_delete=models.CASCADE,
                            verbose_name='Тег')
