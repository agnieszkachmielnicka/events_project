from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Profile(models.Model):   
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

	@receiver(post_save, sender=CustomUser)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=CustomUser)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()