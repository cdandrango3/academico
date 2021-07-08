from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from djangoProject.clase.models import profesores
from django.contrib.auth import authenticate
def c(request):
     return render(request,"academico/index.html")
def login(request):
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
            return redirect('/profesores')

        return HttpResponse(username)
    return render(request, "academico/login.html")
def allprofe(request):
    return render(request, "academico/profeall.html", {"profe": profesores.objects.all()})
def about(request):
    return HttpResponse("about ")

