from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import os
from girlsDay import settings
from image_cropping.fields import ImageRatioField, ImageCropField


class UserManager(BaseUserManager):
    def create_user(self, username, email, name, password, image=None):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=UserManager.normalize_email(email),
            username=username,
            name=name,
            is_admin=False)
        if image:
            user.image = image
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, name='admin'):
        user = self.create_user(
            email=email,
            username=username,
            name=name,
            password=password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True, unique=True)
    username = models.CharField(max_length=50, unique=True, db_index=True)
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=50, db_index=True, unique=True)
    image = ImageCropField(
        upload_to='avatar/',
        default=os.path.join('', 'default.jpg').replace('\\', '/')
    )
    cropping = ImageRatioField('image', '200x200', allow_fullsize=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class Girl(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=10)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey('User')
    girl = models.ForeignKey('Girl')
    content = models.CharField(max_length=500)

    def __str__(self):
        return "FROM:" + str(self.sender) + " TO:" + str(self.girl) + " CONTENT:"+ self.content
