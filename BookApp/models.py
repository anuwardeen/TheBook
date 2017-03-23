from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    topic_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    image = models.FileField(null=True, blank=True, default="default.jpeg")
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    min_accessing_level = models.IntegerField()

    def __str__(self):
        return self.title

class AccessLevel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_level = models.IntegerField(default=2)


    def __str__(self):
        return str(self.user)


class Comment(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return self.comment