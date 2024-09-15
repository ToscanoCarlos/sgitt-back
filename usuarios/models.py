from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El Email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Alumno(models.Model):
    class Carrera(models.TextChoices):
        SISTEMAS = 'ISC', 'sistemas_computacionales'
        LICDATOS = 'LCD', 'licencia_datos'
        IA = 'IIA', 'inteligencia_artificial'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    apellido_materno = models.CharField(max_length=50)
    boleta = models.CharField(unique=True, max_length=255)
    carrera = models.CharField(max_length=3, choices=Carrera.choices, default=Carrera.SISTEMAS)
    plan_estudios = models.CharField(max_length=50)

    class Meta:
        ordering = ['boleta']
        indexes = [models.Index(fields=['boleta']), ]

class Profesor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    matricula = models.CharField(unique=True, max_length=255)
    materias = models.CharField(max_length=255)
    es_profesor = models.BooleanField(default=True)

    class Meta:
        ordering = ['matricula']
        indexes = [models.Index(fields=['matricula']), ]