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
from .utils import render_to_pdf


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
         periodos=periodo.objects.get(is_active=True)

         list_alumnos = [listas for listas in alumnos.values()]
         existe=[]

         for listas in list_alumnos:
             estudiantes=listas['id']
             criterio1 = Q(alumno=estudiantes)
             criterio2 = Q(materia=materi)
             criterio3 = Q(periodo=periodos)
             c = calificacion.objects.filter(criterio1 & criterio2 & criterio3).exists()
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
            periodos = periodo.objects.get(is_active=True)

            criterio1=Q(alumno=estudiantes)
            criterio2 = Q(materia=materi)
            criterio3 = Q(periodo=periodos)
            c=calificacion.objects.filter(criterio1 & criterio2 & criterio3).exists()
            if c:
                h = calificacion.objects.get(criterio1 & criterio2 & criterio3)
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

                        consulta=calificacion.objects.filter(criterio1 & criterio2 & criterio3).update(nota=nota)



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
    return render(request,"academico/ver_alumno.html",{"periodo":periodos.nombre_periodo,"curso":materi.curso_materia.Nivel + " ' " + materi.curso_materia.Paralelo + " ' " ,"info":dato,"existe":exits})
def promedio_general(request,materias):
    materi = materia.objects.get(id=materias)
    codigo_curso = materi.curso_materia.Curso_codigo
    alumnos = estudiante.objects.filter(curso_id__Curso_codigo=codigo_curso)
    periodos = periodo.objects.get(is_active=True)
    criterio2 = Q(materia=materi)
    criterio3 = Q(periodo=periodos)
    promedio=[]
    datos=[]
    for alumno in alumnos:
        criterio1 = Q(alumno=alumno)
        h=calificacion.objects.filter(criterio1 & criterio2 & criterio3).exists()
        if h:
            listas={}
            c = calificacion.objects.get(criterio1 & criterio2 & criterio3)
            promedio.append(c.nota)
            listas["nombre"]=alumno.nombre
            listas["apellido"]=alumno.apellido
            listas["id"] = alumno.id
            listas["nota"] = c.nota
            datos.append(listas)
        else:
            listas = {}
            listas["nombre"] = alumno.nombre
            listas["apellido"] = alumno.apellido
            listas["id"] = alumno.id
            listas["nota"] = "-"
            datos.append(listas)
    print(datos)
    notas_prom=0
    for promedios in promedio:
        notas_prom+=promedios

    promf=notas_prom/len(promedio)
    print(promf)


    return render(request, "academico/ver_alumno.html",{"periodo":periodos.nombre_periodo,"curso":materi.curso_materia.Nivel + " ' " + materi.curso_materia.Paralelo + " ' ","datos":datos,"is_prom":True,"promedio":promf,"materia":materias})
def notas_estudiante(request):
    if request.user.is_authenticated:
        userGroup = Group.objects.get(user=request.user).name
        print(userGroup)
        if userGroup == 'estudiante':
            fr=estudiante.objects.get(id=request.user.username)
            f=curso.objects.get(Curso_codigo=fr.curso_id.Curso_codigo)

            vc=materia.objects.filter(curso_materia=f)
            print(vc.values())
            g=[]
            promedio_final=[]
            for mate in vc:
                dato={}
                dato["materia"]=mate.nombre_materia
                criterio1 = Q(materia=mate)
                criterio2 = Q(alumno=request.user.username)
                is_exists=calificacion.objects.filter(criterio1 & criterio2).exists()
                print(is_exists)
                if(is_exists):
                    periodos=periodo.objects.all()
                    print(periodos)
                    for period in periodos:
                      criterio3=Q(periodo=period)
                      cali = calificacion.objects.filter(criterio1 & criterio2 & criterio3)
                      if cali.exists():
                          nota=calificacion.objects.get(criterio1 & criterio2 & criterio3)
                          dato[period.periodoid]=nota.nota
                      else:

                          dato[period.periodoid] = "-"
                if dato["PRI1Q"]=="-" or dato["PRI2Q"]=="-":
                    promedio="-"
                else:
                    promedio = (dato["PRI1Q"] + dato["PRI2Q"]) / 2
                    promedio_final.append(promedio)
                dato["final"]=promedio




                g.append(dato)




            print(g)
            print(promedio)
        prof=0
        for promediof in promedio_final:
            prof += promediof
        profi=prof/len(promedio_final)
        print(profi)

        return render(request,"academico/nota_alumno.html" ,{"curso":f.Nivel+ " ' "+ f.Paralelo + " ", "nombre": fr.nombre + " "+ fr.apellido,"datos":g,"profi":profi})

def export_pdf(request,materias):
    materi = materia.objects.get(id=materias)
    codigo_curso = materi.curso_materia.Curso_codigo
    alumnos = estudiante.objects.filter(curso_id__Curso_codigo=codigo_curso)
    periodos = periodo.objects.get(is_active=True)
    criterio2 = Q(materia=materi)
    criterio3 = Q(periodo=periodos)
    promedio = []
    datos = []
    for alumno in alumnos:
        criterio1 = Q(alumno=alumno)
        h = calificacion.objects.filter(criterio1 & criterio2 & criterio3).exists()
        if h:
            listas = {}
            c = calificacion.objects.get(criterio1 & criterio2 & criterio3)
            promedio.append(c.nota)
            listas["nombre"] = alumno.nombre
            listas["apellido"] = alumno.apellido
            listas["id"] = alumno.id
            listas["nota"] = c.nota
            datos.append(listas)
        else:
            listas = {}
            listas["nombre"] = alumno.nombre
            listas["apellido"] = alumno.apellido
            listas["id"] = alumno.id
            listas["nota"] = "-"
            datos.append(listas)
    pdf = render_to_pdf('academico/nota_alumno.html', {
        "dato":datos
    })
    return HttpResponse(pdf, content_type='application/pdf')