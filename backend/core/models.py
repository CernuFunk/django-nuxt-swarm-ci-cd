from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserProfileManager(BaseUserManager):
    """
    Define user creation fields and manages to save user
    """
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('password must have to passed')
        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_staffuser(self, email, username, password):
        user = self.create_user(email, username=username, password=password)
        user.is_staff = True
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username=username, password=password)
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    Creates a customized database table for using customized user manager
    """
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    username = models.CharField('username', max_length=150, unique=True,
                                error_messages={'unique': "A user with that username already exist"})
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]
    objects = UserProfileManager()

    def get_full_name(self):
        # TODO: da cambiare quando avremo più dati
        return self.email

    def get_short_name(self):
        # TODO: come sopra
        return self.email

    def __str__(self):
        return self.email

    #  DA RIVEDERE POSSIBILE PROBLEMA TODO: Capirlo bene
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
