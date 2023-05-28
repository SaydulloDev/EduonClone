from django.db import models
from users.models import CustomUserModel


class Comment(models.Model):
    post = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.user.get_full_name()


