from django.db import models


class Comment(models.Model):
    post = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('users.CustomUserModel', on_delete=models.CASCADE)
    content = models.TextField()

    class Meta:
        verbose_name_plural = 'Comment'

    def __str__(self):
        return self.user.get_full_name()
