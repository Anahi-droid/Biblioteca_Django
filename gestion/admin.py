from django.contrib import admin
<<<<<<< HEAD
from .models import *

# Register your models here.

admin.site.register(Autor)
admin.site.register(Prestamo)
admin.site.register(Libro)
=======
from .models import * # debemos importar para que salga en la interfaz grafica

# Register your models here.

admin.site.register(Autor) # aqui llamamos, aparece en la interfaz grafica
admin.site.register(Prestamos)
admin.site.register(Libro)
admin.site.register(Multa)
>>>>>>> 1ff34db8ae80ff69bb1af0619381edf623b73fc6
