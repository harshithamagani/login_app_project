from django.db import models
import re




class UserManager(models.Manager):
    def basic_validator(self , postData):
        errors = {}
        email = postData['email']
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if postData['form'] != 'login':
            if len(postData['first_name']) == 0:
                errors['first_name_empty'] = "First name should not be empty"
            elif len(postData['first_name']) < 2:
                errors['first_name'] = "First name should be at least 2 characters"
            if len(postData['last_name']) == 0:
                errors['last_name_empty'] = "Last name should not be empty"
            elif len(postData['last_name']) < 2:
                errors['last_name'] = "Last name should be at least 2 characters"
        if len(postData['email']) == 0:
            errors['email_empty'] = "Email should not be empty"
        elif not EMAIL_REGEX.match(email):
            errors['email'] = "Invalid email address!"
        if len(postData['password']) == 0:
            errors['password_empty'] = "Password should not be empty"
        elif len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        return errors



# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="user_messages")

class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="user_comments")
    message = models.ForeignKey(Message , related_name="message_comments")


