from django.contrib import admin
from .models import clase
from .models import profesores
from .models import materia

# Register your models here.
admin.site.register(clase)
admin.site.register(profesores)
admin.site.register(materia)




