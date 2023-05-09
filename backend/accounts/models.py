from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserAccountManager(BaseUserManager):


    def _create_user(self, email, password=None, **kwargs):
        print(kwargs)
        if not email:
            raise ValueError('Users must have an email address')



        is_active     = kwargs.pop('active', True)
        # is_verified   = kwargs.pop('verified', False)
        is_staff      = kwargs.pop('staff', False)
        is_superuser  = kwargs.pop('admin', False)

        user_instance = self.model(
            email        = email,
            # verified        = is_verified,
            is_active       = is_active,
            is_staff        = is_staff,
            is_superuser    = is_superuser,
            **kwargs
        )
        user_instance.set_password(password)
        user_instance.save(using=self._db)
        return user_instance


    # def create_user(self, email, password=None, **extra_fields):
    #     if not email:
    #         raise ValueError('Users must have an email address')

    #     email = self.normalize_email(email)
    #     user = self.model(email=email, **extra_fields)

    #     user.set_password(password)
    #     user.save()
    #     return user

    
    def create_user(self, email, password=None,  **extra_fields):
        extra_staff      = extra_fields.pop('staff', False)
        extra_superuser  = extra_fields.pop('admin', False)

        if extra_staff is True:
            raise ValueError('Invalid Data')
        if extra_superuser is True:
            raise ValueError('Invalid Data')

        return self._create_user(email=email, password=password, **extra_fields)

    
    def create_superuser(self, email, password, **extra_fields):
        extra_staff      = extra_fields.pop('staff', True)
        extra_superuser  = extra_fields.pop('admin', True)

        if extra_staff is not True:
            raise ValueError('Invalid Staff User')
        if extra_superuser is not True:
            raise ValueError('Invalid Super User')

        return self._create_user(email=email, password=password, staff=True, admin=True, **extra_fields)



class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return self.email
