from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

from .models import Autor, Libro, Prestamo, Multa

def index(request):
    title = settings.TITLE
    return render(request, 'gestion/templates/home.html', {'titulo': title})

def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, 'gestion/templates/libros.html', {'autores': libros})
    pass

def crear_libro(request):
    autores = Autor.objects.all()
    
    if request.method == "POST":
        titulo = request.POST.get('titulo')
        autor_id = request.POST.get('autor')
        
        if titulo and autor_id:
            autor = get_object_or_404(Autor, id=autor_id)
            Libro.objects.create(titulo=titulo, autor=autor)
            return redirect('lista_libros')
    return render(request='gestion/templates/crear_libros.html')
    

def lista_autores(request):
    autores = Autor.objects.all()
    return render(request, 'gestion/templates/autores.html', {'autores': autores})
    pass

def crear_autor(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        bibliografia = request.POST.get('bibliografia')
        Autor.objects.create(nombre=nombre, apellido=apellido, bibliografia=bibliografia)
        return redirect(lista_autores)
    return render(request='gestion/templates/crear_autores.html')

def lista_prestamo(request):
    prestamo = Prestamo.objects.all()
    return render(request, 'gestion/templates/prestamo.html', {'prestamo': prestamo})
    pass

def crear_prestamo(request):
    
    if request.method == 'POST':
        libro = request.POST.get('libro')
        usuario = request.POST.get('usuario')
        fecha_prestamos = request.POST.get('fecha_prestamos')
        fecha_maxima = request.POST.get('fecha_maxima')
        fecha_devolucion = request.POST.get('fecha_devolucion')
        Prestamo.objects.create(libro=libro, usuario=usuario, fecha_prestamos=fecha_prestamos,
                                fecha_maxima=fecha_maxima, fecha_devolucion=fecha_devolucion)
        return redirect(detalle_prestamo)
    return render(request='gestion/templates/crear_prestamos.html')

def detalle_prestamo(request):
    pass

def lista_multas(request):
    multas = Multa.objects.all()
    return render(request, 'gestion/templates/prestamo.html', {'multas': multas})
    pass

def crear_multas(request):
    
    if request.method == 'POST':
        prestamo = request.POST.get('prestamo')
        tipo = request.POST.get('tipo')
        monto = request.POST.get('monto')
        pagada = request.POST.get('pagada')
        fecha = request.POST.get('fecha')
        Prestamo.objects.create(prestamo=prestamo, tipo=tipo, monto=monto,
                                pagada=pagada, fecha=fecha)
        return redirect(lista_multas)
    return render(request='gestion/templates/crear_multas.html')

