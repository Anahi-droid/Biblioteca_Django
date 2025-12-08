from django.contrib import admin
from .models import * # debemos importar para que salga en la interfaz grafica

# Register your models here.

admin.site.register(Autor) # aqui llamamos, aparece en la interfaz grafica
admin.site.register(Prestamos)
admin.site.register(Libro)