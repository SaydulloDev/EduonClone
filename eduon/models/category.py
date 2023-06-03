from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.title:
            self.slug = slugify(self.title)
        return super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name_plural = "Category"

    def __str__(self):
        return self.title
