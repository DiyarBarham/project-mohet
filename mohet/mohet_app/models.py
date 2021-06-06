from datetime import datetime
from django.db import models
import re 
from enum import Enum
# Create your models here.

class ContactManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['description']) < 50:
            errors["description"] = "description should be at least 50 characters"
        if len(postData['title'])< 2:
            errors["title"] = "title should be at least 50 characters"
        if len(postData['name'])< 2:
            errors["name"] = "Name should be at least 50 characters"
        return errors
class Contact(models.Model):
    title = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    number= models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField()
    objects = ContactManager()


class SubscriptionManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):  # test whether a field matches the pattern
            errors['email'] = "Invalid email address!"
        return errors

class sub(Enum):
    active = 'active'
    unactive = 'unactive'

class Subscription(models.Model):
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255, default=None)
    status = models.CharField(max_length=10, choices=[(tag, tag.value) for tag in sub])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SubscriptionManager()

class Role(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):  # test whether a field matches the pattern
            errors['email'] = "Invalid email address!"
        if len(postData['first_name']) < 2:
            errors["first_name"] = "first name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "first name should be at least 2 characters"
        if len(postData['password']) < 8 or postData['password']!=postData['confirmpass']:
            errors["password"] = "Password should be at least 8 characters"
        dop = self.cleaned_data[postData['birthday']]
        age = (datetime.now() - dop).days/365
        if age<18:
            errors["birthday"] = "You need to be 18 years old to register"
        return errors
class gender(Enum):
    male = 'male'
    female = 'female'

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=8, choices=[(tag, tag.value) for tag in gender])
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role_id = models.ForeignKey(Role, related_name='user', on_delete=models.CASCADE)
    object = UserManager()

class ArticleManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['title']) < 2:
            errors["title"] = "title should be at least 2 characters"
        if len(postData['description']) < 300:
            errors["description"] = "description should be at least 300 characters"
        return errors

class status(Enum):
    Pending = 'Pending'
    Published = 'Published'
    Removed = 'Removed'
    Refused = 'Refused'
class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=[(tag, tag.value) for tag in status])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_id = models.ManyToManyField(User, related_name='article')
    object = ArticleManager()

class CommentManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors["name"] = "name should be at least 2 characters"
        if len(postData['description']) < 2:
            errors["description"] = "description should be at least 2 characters"
        return errors
class Comment(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    object = CommentManager()

class Mediatype(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MediaManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors["name"] = "name should be at least 2 characters"
        return errors
class Media(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    article = models.ForeignKey(Article, related_name='media', on_delete=models.CASCADE)
    mediatype = models.ForeignKey(Mediatype, related_name='media', on_delete=models.CASCADE)
    object = MediaManager()