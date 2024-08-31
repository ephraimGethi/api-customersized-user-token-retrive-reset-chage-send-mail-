from typing import Any
from django.db import models

from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,UserManager


class CustomUserManager(BaseUserManager):
    def create_user(self,name,email,tc,password=None,password2=None):
        if not email:
            raise ValueError("you have not specified a valid email address")
        email = self.normalize_email(email)
        user = self.model(email= email,name=name,tc=tc)
        user.set_password(password)
        user.save(using = self._db)

        return user
    def create_superuser(self,name, email,tc, password=None):
        if not email:
            raise ValueError("you have not specified a valid email address")
       
        if not email:
            raise ValueError("you have not specified a valid email address")
        email = self.normalize_email(email)
        user = self.model(email= email,name=name,tc=tc)
        user.set_password(password)
        user.is_admin =True
        user.save(using = self._db)

        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True
    )
    date_of_birth = models.DateField(null=True,blank=True)
    name = models.CharField(max_length=200)
    tc = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['name','tc']

    def __str__(self) -> str:
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True
    

    @property
    def is_staff(self):
        return self.is_admin