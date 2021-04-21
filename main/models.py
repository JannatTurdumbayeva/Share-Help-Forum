from django.db import models

from account.models import MyUser
from django.dispatch import receiver
from django.db.models.signals import post_save


class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    author = models.ForeignKey(MyUser, on_delete=models.CASCADE,
                               related_name='problems')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created',)


class CodeImage(models.Model):
    image = models.ImageField(upload_to='images')
    problem = models.ForeignKey(Problem,
                                on_delete=models.CASCADE,
                                related_name='images')


class Reply(models.Model):
    problem = models.ForeignKey(Problem,
                                on_delete=models.CASCADE,
                                related_name='replies')
    body = models.TextField()
    image = models.ImageField(upload_to='replies',
                              blank=True)
    author = models.ForeignKey(MyUser,
                               on_delete=models.DO_NOTHING,
                               related_name='replies')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body

    class Meta:
        ordering = ('-created',)


class Comment(models.Model):
    comment = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(MyUser,
                               on_delete=models.DO_NOTHING,
                               related_name='comments')
    reply = models.ForeignKey(Reply,
                              on_delete=models.CASCADE,
                              related_name='comments')

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ('created',)


class Favorite(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='favorites')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='favorites')
    favorite = models.BooleanField(default=False)


class Like(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='likes')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=False)


class Rating(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='ratings')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(default=0)


class History(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='histories')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='histories')
    created = models.DateTimeField(auto_now_add=True, blank=True)


