from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, nickname, email, password=None):
        if not email:
            raise ValueError('O email é obrigatório')
        if not nickname:
            raise ValueError('O nickname é obrigatório')

        email = self.normalize_email(email)
        user = self.model(nickname=nickname, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, email, password):
        user = self.create_user(nickname, email, password)
        user.is_admin = True
        user.is_staff = True  # Necessário para o painel admin
        user.is_superuser = True  # Necessário para o painel admin
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    nickname = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Necessário para acesso ao painel admin
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
