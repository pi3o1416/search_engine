
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# Create your models here.


class SearchHistory(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name='user_searched',
        on_delete=models.CASCADE,
    )

    search_text = models.CharField(
        verbose_name=_('User search text'),
        max_length=200,
        blank=False,
    )

    search_time = models.DateTimeField(
        verbose_name=_('Search Time'),
    )

    search_result = models.JSONField(
        verbose_name=_('Search Result Appeared for that perticular search'),
    )

    def __str__(self):
        return self.search_text





