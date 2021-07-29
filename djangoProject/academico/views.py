from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from djangoProject.clase.models import profesores
from django.contrib.auth import authenticate
from django.contrib.auth import login as lg
from django.contrib.auth import logout as cerrar
from djangoProject.clase.models import estudiante
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
    d=estudiante.objects.filter(user__username__contains=request.user.username)
    perfil = [perf for perf in d.values()]
    return render(request, "academico/profeall.html", {"authe":"perro","name":perfil})

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



