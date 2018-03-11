# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
	author = models.ForeignKey(User, default=None)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.localtime(timezone.now()))
	published_date = models.DateTimeField(blank=True, null=True)

	def publish(self):
	    self.published_date = timezone.now()
	    self.save()

	def __str__(self):
	    return self.text

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
	commenter = models.ForeignKey(User, default=None, related_name='commenter')
	text = models.TextField()
	published_date = models.DateTimeField(blank=True, null=True)

	def publish(self):
	    self.published_date = timezone.now()
	    self.save()

	def __unicode__(self):
	    return 'commenter=' + str(self.commenter) + ', text="' + self.text + '", post='+str(self.post)


class Profile(models.Model):
	profile_user = models.ForeignKey(User, default=None, related_name='profile_user')
	bio = models.CharField(max_length=200)
	picture = models.FileField(upload_to="images", blank=True)
	content_type = models.CharField(max_length=50)
	followers = models.ManyToManyField(User, related_name='followed_by')

	def __unicode__(self):
		return 'id=' + str(self.id) + ', bio="' + self.bio + '", username='+str(self.profile_username)



