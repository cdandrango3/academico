from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class estudiante(models.Model):
    id=models.PositiveBigIntegerField(primary_key=True)
    nombre=models.CharField(max_length=200)
    apellido=models.CharField(max_length=300,default="")
    edad=models.CharField(max_length=3, default="0")
    Telefono=models.CharField(max_length=9,default=0)

    user = models.OneToOneField('Users', on_delete=models.CASCADE)
class curso(models.Model):
    Curso_codigo=models.CharField(max_length=40,primary_key=True)
    Nivel=models.CharField(max_length=40)
    Paralelo=models.CharField(max_length=40)
    docente_curso=models.ManyToManyField('profesores')
    alumno_curso = models.ForeignKey('estudiante',on_delete=models.CASCADE)
class profesores(models.Model):
    cedula_id = models.PositiveBigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=300, default="")
    edad = models.CharField(max_length=3, default="0")
    Telefono=models.CharField(max_length=9,default="0")
    user = models.OneToOneField('Users', on_delete=models.CASCADE)
class materia(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    nombre_materia = models.CharField(max_length=200)
    alumno_materia = models.ManyToManyField('estudiante')
class periodo(models.Model):
    nombre_periodo=models.CharField(max_length=200)
    is_active=models.BooleanField(default=False)
class notas(models.Model):
    nota=models.FloatField()
    alumno = models.ForeignKey('estudiante', on_delete=models.CASCADE)
    profesor = models.ForeignKey('profesores', on_delete=models.CASCADE)
    materia= models.ForeignKey('materia', on_delete=models.CASCADE)
    curso = models.ForeignKey('curso', on_delete=models.CASCADE)


class Users(AbstractUser):
    isTeacher=models.BooleanField(default="False")
    isStudent = models.BooleanField(default="False")
    telefono = models.BooleanField(default="False")
    def is_student(self):
        return self.groups.filter(name='estudiante').exists()
    class Meta:
        db_table = 'auth_user'
