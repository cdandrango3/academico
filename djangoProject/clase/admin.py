from django.contrib import admin
from .models import clase
from .models import profesores
from .models import materia
from .models import Users
from django.contrib.auth.admin import UserAdmin
# Register your models here.
admin.site.register(Users,UserAdmin)
admin.site.register(clase)
admin.site.register(profesores)
admin.site.register(materia)




