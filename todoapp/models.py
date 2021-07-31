from ToDoApp.settings import TIME_ZONE
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields.proxy import OrderWrt
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            instance.profile.save()

class Tasks(models.Model):
    user=models.ForeignKey(User,on_delete=CASCADE,null=True,blank=True)
    task_title=models.CharField(max_length=50,null=True)
    description=models.TextField(null=True)
    completed=models.BooleanField(default=False,null=True)
    created=models.DateTimeField(auto_now_add=True,null=True)
  

    def __str__(self):
        return self.task_title

    class Meta:
        order_with_respect_to='completed'