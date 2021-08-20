from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from djangoProject.clase.models import profesores
from django.contrib.auth import authenticate
from django.contrib.auth import login as lg
from django.contrib.auth import logout as cerrar
from djangoProject.clase.models import estudiante
from djangoProject.clase.models import materia
from django.contrib.auth.models import Group
def c(request):
     return render(request,"academico/index.html")
def login(request):
    # Se ubica el request con el metodo Post
    if request.method== 'POST':
        username=request.POST['username']
        password=request.POST['password']
        if username=="":
            return HttpResponse("no hay usuario")
        if password=="":
            return HttpResponse("No hay contraseña")
        user=authenticate(request,username=username,password=password)
        if user is None:
            return HttpResponse("not exits")
        else:



          lg(request,user)
          return redirect("/profesores")

        return HttpResponse(username)
    return render(request, "academico/login.html")

def allprofe(request):
    if request.user.is_authenticated:
        d=estudiante.objects.filter(user__username__contains=request.user.username)
        perfil = [perf for perf in d.values()]
        return render(request, "academico/profeall.html", {"authe": "perro", "name": perfil})

    else:
        return redirect("/login")



def about(request):
    return HttpResponse("about ")
def logout(request):
    cerrar(request)
    return redirect('/')
def perfil(request):
    userGroup = Group.objects.get(user=request.user).name
    print(userGroup)
    if userGroup == 'estudiante':
        d = estudiante.objects.filter(user__username__contains=request.user.username)
        perfil = [perf for perf in d.values()]
    elif userGroup == 'profesor':
        d = profesores.objects.filter(user__username__contains=request.user.username)
        perfil = [perf for perf in d.values()]
    else:
        perfil="no existe"
    return render(request, "academico/Perfil.html", {"authe": "profesor", "name": perfil})


def elegir_curso(request):
    if request.user.is_authenticated:
      userGroup = Group.objects.get(user=request.user).name
      if userGroup=='estudiante':
          return redirect("/profesores")
      elif userGroup == 'profesor':
          d = request.user.username
          print(d)
          lis=materia.objects.filter(id_profesor__cedula_id__contains=d)
          lista = [listas for listas in lis.values()]
          print(lista)
          return render(request, "academico/cursosescoger.html", {"name": lista})

    else:
        return redirect("/login")

def editar_curso(request,materias):
    if request.user.is_authenticated:
      userGroup = Group.objects.get(user=request.user).name
      if userGroup=='estudiante':
          return redirect("/profesores")
      elif userGroup == 'profesor':

         materi=materia.objects.get(id=materias)
         codigo_curso=materi.curso_materia.Curso_codigo
         print(codigo_curso)
         alumnos = estudiante.objects.filter(curso_id__Curso_codigo=codigo_curso)
         print(alumnos)
         list_alumnos = [listas for listas in alumnos.values()]
         return render(request,"academico/editar_alumnos.html",{"alumnos":list_alumnos})

def editar_curso(request,notas):
    pass

