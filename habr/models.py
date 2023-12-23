from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {'null': True, 'blank': True}


class Author(models.Model):
    name = models.CharField(
        _('Author name'), max_length=255, unique=True, **NULLABLE
    )
    profile_url = models.URLField(_('Author profile url'), **NULLABLE)

    def __str__(self):
        return f'Author name: {self.name}, author profile url: {self.profile_url}.'

    def __repr__(self) -> str:
        return str(self)

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Author')


class Article(models.Model):
    header = models.TextField(_('Header'), **NULLABLE)
    content = models.TextField(_('Content'), **NULLABLE)
    posted_at = models.DateTimeField(_('Posted at'), **NULLABLE)
    url = models.URLField(_('Url'), **NULLABLE)

    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='articles',
        **NULLABLE
    )

    def __str__(self):
        return f'Article header: {self.header}, article url {self.url}.'

    def __repr__(self) -> str:
        return str(self)

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Article')
