from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import Group


from .models import Autor, Libro, Prestamo, Multa

def index(request):
    titulo2 = "Hola Mundo"
    title = settings.TITLE
    return render(request, 'gestion/templates/home.html', {'titulo': title, 't': titulo2})

def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, 'gestion/templates/libros.html', {'libros': libros} )

def crear_libro(request):
    autores = Autor.objects.all()
    if request.method == "POST":
        titulo =  request.POST.get('titulo')
        autor_id =  request.POST.get('autor')

from .models import Autor, Libro, Prestamos, Multa

def index(request):
    title = settings.TITLE
    return render(request, 'gestion/templates/home.html', {'titulo': title})

def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, 'gestion/templates/libros.html', {'libros': libros})

def crear_libro(request):
    autores = Autor.objects.all()
    
    if request.method == "POST":
        titulo = request.POST.get('titulo')
        autor_id = request.POST.get('autor')

        
        if titulo and autor_id:
            autor = get_object_or_404(Autor, id=autor_id)
            Libro.objects.create(titulo=titulo, autor=autor)
            return redirect('lista_libros')
    return render(request, 'gestion/templates/crear_libros.html', {'autores': autores})


def lista_autores(request):
    autores = Autor.objects.all()
    return render(request, 'gestion/templates/autores.html', {'autores': autores} )

@login_required
def crear_autor(request, id=None):
    if id == None:
        autor = None

     
    
def lista_autores(request):
    autores = Autor.objects.all()
    return render(request, 'gestion/templates/autores.html', {'autores': autores})


@ login_required # ponemos antes esto de todas las funciones que querramos que antes de que ingrese aparezca un login
def crear_autor(request, id=None):
    if id == None:
        autor = None 
        modo = 'crear'
    else:
        autor = get_object_or_404(Autor, id=id)
        modo = 'editar'
        
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        bibliografia = request.POST.get('bibliografia')
        if autor == None:
            Autor.objects.create(nombre=nombre, apellido=apellido, bibliografia=bibliografia)
        else:

            autor.apellido = apellido

            autor.apellido = apellido # nuevo valor seran los datos que capturo desde el formulario
            autor.nombre = nombre
            autor.bibliografia = bibliografia
            autor.save()
        return redirect('lista_autores')
    context = {'autor': autor,
               'titulo': 'Editar Autor' if modo == 'editar' else 'Crear Autor',
               'texto_boton': 'Guardar cambios' if modo == 'editar' else 'Crear'}

    return render(request, 'gestion/templates/crear_autores.html', context)

def lista_prestamos(request):
    prestamos = Prestamo.objects.all()
    return render(request, 'gestion/templates/prestamos.html', {'prestamos': prestamos} )


def crear_prestamo(request):
    if not request.user.has_perm('gestion.gestionar_prestamos'):
        return HttpResponseForbidden()
    libro = Libro.objects.filter(disponible=True)
    usuario = User.objects.all()
    if request.method == 'POST':
        libro_id = request.POST.get('libro')
        usuario_id = request.POST.get('usuario')
        fecha_prestamos = request.POST.get('fecha_prestamos')
        fecha_max = request.POST.get('fecha_max')

        if libro_id and usuario_id and fecha_prestamos and fecha_max:
            libro = get_object_or_404(Libro, id=libro_id)
            usuario = get_object_or_404(User, id=usuario_id)
            prestamo = Prestamo.objects.create(libro = libro,
                                               usuario=usuario,
                                               fecha_prestamos=fecha_prestamos,
                                               fecha_max=fecha_max)
            libro.disponible = False
            libro.save()
            return redirect('lista_prestamo', id=prestamo.id)
    fecha = (timezone.now().date()).isoformat() # YYYY-MM-DD
    return render(request, 'gestion/templates/crear_prestamo.html', {'libros': libro,
                                                                     'usuarios': usuario,
                                                                     'fecha': fecha})

    return render(request,'gestion/templates/crear_autores.html', context)

def lista_prestamo(request):
    prestamo = Prestamos.objects.all()
    return render(request, 'gestion/templates/prestamo.html', {'prestamo': prestamo}) # se manda para que se visualice 

@ login_required
def crear_prestamo(request):
    
    if not request.user.has.perm('gestion.gestionar_prestamos'): # aqui gestionamos el permiso, si no tiene este permiso tata
        return HttpResponseForbidden()
    libro = Libro.objects.filter(disponible=True)
    usuario = User.objects.all()
        
    if request.method == 'POST':
        libro_id = request.method.POST.get('libro')
        usuario_id = request.method.POST.get('usuario')
        fecha_prestamo = request.method.POST.get('fecha_prestamo')
        if libro_id and usuario_id and fecha_prestamo:
            libro = get_object_or_404(Libro, id=libro_id)
            usuario = get_object_or_404(User, id=usuario_id)
            prestamo = Prestamos.objects.create(libro=libro, usuario=usuario,
                                fecha_prestamo=fecha_prestamo)
            libro.disponible = False 
            libro.save()
            return redirect('detalle_prestamo', id=prestamo.id)
    fecha = (timezone.now().date()).isoformat() # fromato iso es YYY-MM-DD
    return render(request,'gestion/templates/crear_prestamos.html', {'libros': libro, 'usuario': usuario,
                                                                     'fecha': fecha })


def detalle_prestamo(request):
    pass

def lista_multas(request):
    multas = Multa.objects.all()

    return render(request, 'multas.html', {'multas': multas} )

def crear_multa(request):
    pass


def registro(request):

    return render(request, 'gestion/templates/prestamo.html', {'multas': multas})

def crear_multas(request):
    pass

def registro(request):
    

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()


            grupo = Group.objects.get(name="UsuariosBiblioteca")
            usuario.groups.add(grupo)


            login(request, usuario)
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'gestion/templates/registration/registro.html', {'form': form})

# Create your views here.

    return render(request, 'gestion/templates/registration/registro.html', {'form':form})
        
    

