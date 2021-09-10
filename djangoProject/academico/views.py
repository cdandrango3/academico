from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from djangoProject.clase.models import profesores
from django.contrib.auth import authenticate
from django.contrib.auth import login as lg
from django.contrib.auth import logout as cerrar
from djangoProject.clase.models import estudiante
from djangoProject.clase.models import materia,curso,periodo
from djangoProject.clase.models import notas as calificacion
from django.contrib.auth.models import Group
from django.db.models import Q
from .form import Nota
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
         alumnos = estudiante.objects.filter(curso_id__Curso_codigo=codigo_curso)

         list_alumnos = [listas for listas in alumnos.values()]
         existe=[]

         for listas in list_alumnos:
             estudiantes=listas['id']
             criterio1 = Q(alumno=estudiantes)
             criterio2 = Q(materia=materi)
             c = calificacion.objects.filter(criterio1 & criterio2).exists()
             listas['status']=c
             existe.append(listas)
         if request.method == 'POST':
             search = request.POST['search']
             nom= request.POST.get('ca')
             print(nom)

             if nom!=False:
                 criterio2 = Q(id__contains=search)
             else:
                 criterio2 = Q(nombre__contains=search)

             materi = materia.objects.get(id=materias)
             codigo_curso = materi.curso_materia.Curso_codigo
             criterio1 = Q(curso_id__Curso_codigo=codigo_curso)
             alumnos = estudiante.objects.filter(criterio1 & criterio2)
             list_alumnos = [listas for listas in alumnos.values()]
             existe=[]
             for listas in list_alumnos:
                 estudiantes = listas['id']
                 criterio1 = Q(alumno=estudiantes)
                 criterio2 = Q(materia=materi)
                 c = calificacion.objects.filter(criterio1 & criterio2).exists()
                 listas['status'] = c
                 existe.append(listas)





         return render(request,"academico/editar_alumnos.html",{"alumnos":existe,"materia":materi.id})

def notas(request,materias,alum):
    print(materias)
    print(estudiante)

    if request.user.is_authenticated:
        userGroup = Group.objects.get(user=request.user).name
        if userGroup == 'estudiante':
            return redirect("/profesores")
        elif userGroup == 'profesor':
            estudiantes = estudiante.objects.get(id=alum)
            materi = materia.objects.get(id=materias)


            criterio1=Q(alumno=estudiantes)
            criterio2 = Q(materia=materi)
            c=calificacion.objects.filter(criterio1 & criterio2).exists()
            if c:
                h = calificacion.objects.get(criterio1 & criterio2)
                print(h.nota)
            print(c)
            if request.method == 'POST':
                form=Nota(request.POST)
                user = request.GET.get('nota')
                print(user)
                if form.is_valid():
                    # obtiene la nota del formulario
                    nota = form.cleaned_data['nota']

                    if c:

                        consulta=calificacion.objects.filter(criterio1 & criterio2).update(nota=nota)



                    else:
                        # obtiene todos los datos
                        periodos = periodo.objects.get(is_active=True)
                        materi = materia.objects.get(id=materias)
                        codigo= materi.curso_materia.Curso_codigo
                        cursos=curso.objects.get(Curso_codigo=codigo)
                        profesor= profesores.objects.get(cedula_id=request.user.username)
                        estudiantes=estudiante.objects.get(id=alum)
                        print(estudiante)
                        # se pone el modelo
                        califi=calificacion(nota=nota,alumno=estudiantes,profesor=profesor,materia=materi,curso=cursos,periodo=periodos)
                        califi.save()

                        print(nota)



                    return redirect("/thank")
            else:
                form=Nota()

    return render(request,"academico/Notas.html",{"form":form})
def thank(request):

    return render(request,"academico/thank.html", {"metodo":request.GET.get('metodo')})

def eliminar(request,materias,alum):
    estudiantes = estudiante.objects.get(id=alum)
    materi = materia.objects.get(id=materias)
    criterio1 = Q(alumno=estudiantes)
    criterio2 = Q(materia=materi)
    c = calificacion.objects.filter(criterio1 & criterio2).exists()
    if c:
        calificacion.objects.filter(criterio1 & criterio2).delete()
        return redirect('/thank/?metodo=eliminar')

    return HttpResponse("eliminar")
def ver(request,materias,alum):
    estudiantes = estudiante.objects.get(id=alum)
    materi = materia.objects.get(id=materias)
    periodos = periodo.objects.get(is_active=True)
    criterio1 = Q(alumno=estudiantes)
    criterio2 = Q(materia=materi)
    criterio3 =  Q(periodo=periodos)
    c = calificacion.objects.filter(criterio1 & criterio2 & criterio3).exists()
    print(c)
    if c:
        notas=calificacion.objects.get(criterio1 & criterio2 & criterio3)
        exits=True
        dato={"id":estudiantes.id,"nombre":estudiantes.nombre,"apellido":estudiantes.apellido,"nota":notas.nota}
        print(dato)
    else:
        dato={}
        exits=False
    return render(request,"academico/ver_alumno.html",{"info":dato,"existe":exits})

