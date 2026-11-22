from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .forms import TaskForm
from django.db import IntegrityError
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def vPaginaInicio(request):
    return render(request,'paginainicial.html')

def vPaginaRegistro(request):
    if request.method == 'GET':
        return render (request, 'paginaregistro.html',
                       {'consulta' : UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username = request.POST["username"],
                    password = request.POST["password1"]
                )
                user.save()
                login(request, user)
                return redirect('TAREA')
            except IntegrityError:
                return render(
                    request, 
                    "paginaregistro.html",
                    {"consulta" : UserCreationForm, "error" : "Nombre de usuario ya existe"},
                )
        else:
            return render(
                request, 
                "paginaregistro.html",
                {"consulta" : UserCreationForm, "error" : "Las contraseñas no coinciden"},
            )

# Create your views here.
@login_required
def singout(request):
    logout(request)
    return redirect('INICIO')

def sesion(request):
    if request.method == 'GET':
        return render(request, 'sesion.html', 
                    {'sesion': AuthenticationForm})
    else: 
        user = authenticate(request, username = request.POST['username'],
                            password = request.POST['password'])
        if user is None:
            return render(request, 'sesion.html', {
                'sesion': AuthenticationForm,
                'error' : 'Usuario o contraseña incorrectos'
            })
        else:
            login(request, user)
            return redirect('TAREA')

@login_required
def vPaginaTareas(request):
    mistareas = Task.objects.filter(user=request.user, datecompleted__isnull= True)
    return render (request, 'paginatarea.html',{'tareas': mistareas, 'tipopagina': 'TAREAS PENDIENTES DE LOS CHAMOS SIX SEVENCITOS'})

@login_required
def creatarea(request):
    if request.method == 'GET':
        return render(request, 'creartarea.html', {'consulta': TaskForm})
    else:
        try:
            consulta = TaskForm(request.POST)
            tarea_nueva = consulta.save(commit=False)
            tarea_nueva.user = request.user
            tarea_nueva.save()
            return redirect('TAREA')
        except ValueError:
            return render(request, 'creartarea.html', 
                          {'sesion':TaskForm,
                           'error': 'Ingrese tipo de datos correctos'
                           })

@login_required
def tarea_detalle(request, id_tarea):
    if request.method == 'GET':
        mitarea = get_object_or_404(Task, pk = id_tarea, user = request.user)
        form = TaskForm(instance=mitarea)
        return render(request, 'detallestarea.html',
                    {'tarea':mitarea,
                    'consulta' : form,
                    'usuario': mitarea.user.username
                    })
    else:
        try:
            #print(request.POST)
            mitarea = get_object_or_404(Task, pk=id_tarea, user=request.user)
            form = TaskForm(request.POST, instance=mitarea)
            form.save()
            return redirect('TAREA')
        except ValueError:
            return render(request,'detallestarea.html',{
            'tarea':mitarea,
            'consulta': form,
            'error':'Error actualizar tarea'
        })

@login_required
def tarea_completada(request, id_tarea):
    mitarea = get_object_or_404(Task, pk = id_tarea, user = request.user)
    if request.method == 'POST':
        mitarea.datecompleted = timezone.now()
        mitarea.save()
        return redirect('TAREA')

@login_required
def tarea_eliminada(request, id_tarea):
    mitarea = get_object_or_404(Task, pk = id_tarea, user = request.user)
    if request.method == 'POST':
        mitarea.delete()
        return redirect('TAREA')

@login_required
def tareas_completas(request):
    tarea = Task.objects.filter(user= request.user, datecompleted__isnull = False).order_by('-datecompleted')
    return render (request, 'paginatarea.html',{'tareas': tarea, 'tipopagina': 'TAREAS COMPLETADAS DE 6 O 7 CHAMOS'})