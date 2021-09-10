from django.contrib import admin
from .models import estudiante
from .models import profesores
from .models import materia
from .models import Users

from .models import curso
from .models import notas
from .models import periodo
from django.contrib.auth.admin import UserAdmin

admin.site.register(Users,UserAdmin)
admin.site.register(curso)
admin.site.register(estudiante)
admin.site.register(profesores)
admin.site.register(materia)
admin.site.register(notas)
admin.site.register(periodo)




