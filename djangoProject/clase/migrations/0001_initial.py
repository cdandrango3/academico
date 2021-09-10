# Generated by Django 3.2.4 on 2021-09-09 00:17

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('isTeacher', models.BooleanField(default='False')),
                ('isStudent', models.BooleanField(default='False')),
                ('telefono', models.BooleanField(default='False')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'auth_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='curso',
            fields=[
                ('Curso_codigo', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('Nivel', models.CharField(max_length=40)),
                ('Paralelo', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='estudiante',
            fields=[
                ('id', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('apellido', models.CharField(default='', max_length=300)),
                ('edad', models.CharField(default='0', max_length=3)),
                ('Telefono', models.CharField(default=0, max_length=9)),
                ('curso_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clase.curso')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='materia',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre_materia', models.CharField(max_length=200)),
                ('curso_materia', models.ForeignKey(default='no hay', on_delete=django.db.models.deletion.CASCADE, to='clase.curso')),
            ],
        ),
        migrations.CreateModel(
            name='periodo',
            fields=[
                ('periodoid', models.CharField(default='PRI1Q', max_length=200, primary_key=True, serialize=False)),
                ('nombre_periodo', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='profesores',
            fields=[
                ('cedula_id', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('apellido', models.CharField(default='', max_length=300)),
                ('edad', models.CharField(default='0', max_length=3)),
                ('Telefono', models.CharField(default='0', max_length=9)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='notas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.FloatField()),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clase.estudiante')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clase.curso')),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clase.materia')),
                ('periodo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clase.periodo')),
                ('profesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clase.profesores')),
            ],
        ),
        migrations.AddField(
            model_name='materia',
            name='id_profesor',
            field=models.ManyToManyField(to='clase.profesores'),
        ),
    ]
