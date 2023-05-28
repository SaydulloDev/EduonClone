from django.db import models

from .category import Category
from .comment import Comment


class Course(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField()
    tutorial_video = models.FileField(upload_to='tutorial_video/')
    language = models.CharField(max_length=32)
    hours = models.TimeField()
    discount = models.IntegerField(null=True, blank=True)
    price = models.IntegerField()
    sales_price = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.discount:
            self.sales_price = int(self.price - ((self.price / 100) * self.discount))

        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.title


class CourseMaterials(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=128)
    video = models.FileField(upload_to='course_material/video/')
    file = models.FileField(upload_to='course_material/pdf/')

    def __str__(self):
        return self.title
