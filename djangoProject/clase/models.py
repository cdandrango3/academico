from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class clase(models.Model):
    id=models.PositiveBigIntegerField(primary_key=True)
    nombre=models.CharField(max_length=200)
    apellido=models.CharField(max_length=300,default="")
    edad=models.CharField(max_length=3, default="0")
class profesores(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=300, default="")
    edad = models.CharField(max_length=3, default="0")
class materia(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    nombre_materia = models.CharField(max_length=200)
    docentes=models.ManyToManyField(profesores)
