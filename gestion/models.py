from django.db import models
from django.conf import settings 
from django.utils import timezone

# Create your models here.
# por defecto todos los campos serán obligatorios, solo puedo hacer que no sean obligatorio


class Autor(models.Model): 
    nombre = models.CharField(max_length=50) # aqui el char es para caracteres, definimos longitud con el max_length
    apellido = models.CharField(max_length=50)
    bibliografia = models.CharField(max_length=200, blank=True, null= True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}" # devolver nombre y apellido con espacio
    
class Libro(models.Model):
    titulo = models.CharField(max_length=20)
    autor = models.ForeignKey(Autor, related_name="Libros", on_delete=models.PROTECT ) # ForeignKey usamos para relacion 
    #  related_name es como el string
    disponible = models.BooleanField(default=True)
    
    def __str__(self): # nunca olvisar el __str__
        return self.titulo

class Prestamos(models.Model):
    libro = models.ForeignKey(Libro, related_name="Prestamos" , on_delete=models.PROTECT)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="Prestamos" , on_delete=models.PROTECT) # usamos usuarios propios de django, importamos libreria settings 
    fecha_prestamos = models.DateField(default=timezone.now) # aqui es para la fecha de ese dia, importamos libreria
    fecha_maxima= models.DateField()
    fecha_devolucion = models.DateField(blank=True, null= True) # aqui defino que no sea obligatorio
    
    class Meta: # permisos, lo que puede hacer en cada una de las clases
        permissions = (("Ver_prestamos", "Puede ver prestamos"),
                       ("gestionar_prestamos", "Puede gestionar prestamos"),)

    def __str__(self):
        return f"Prestamo de {self.libro} a {self.usuario}"
    
    @property # constructor nos permite trabajar con las propiedades de nuestra clase, como el computer de odoo
    def dias_retraso(self):
        hoy = timezone.now().date()
        fecha_ref = self.fecha_devolucion or hoy #  el propery convierte en atributos, a traves de una funcion
        if fecha_ref > self.fecha_maxima:
            return (fecha_ref - self.fecha_devolucion).days
        
    @property
    def multa_retraso(self):
        tarifa_diaria = 0.5
        return self.dias_retraso * tarifa_diaria
    
class Multa(models.Model):
    prestamo = models.ForeignKey(Prestamos, related_name="Multa" , on_delete=models.PROTECT)
    tipo = models.CharField(max_length=10, choices=(('r', 'retraso'),
                                                        ('p', 'perdida'),
                                                        ('d', 'deterioro'))) # el choices se tiene que definir como tupla de tuplas
    monto= models.DecimalField(max_digits=3, decimal_places=2, default=0)
    pagada= models.BooleanField(default=False)
    fecha = models.DateField(default=timezone.now)
        
    def __str__(self):
            return f"Multa {self.tipo} - {self.monto} - {self.prestamos}"
        
    def save(self, *args, **kwargs):  # args podemos o no mandar parametros, solo es con el *, puedo decir *pepo
            # y cumple con la misma funcion tranforma a una lista
            # **kwargs aqui mando con clave, valor, mando parametros con clave y valor, por eso es que al **kwargs llega como diccionario
            # los dos con opcionales, sino mandamos esos parametros no ecistira error
            if self.tipo == 'r' and self.monto == 0:
                self.monto = self.prestamo.multa_retraso
            super().save(*args **kwargs) # el super llama a la funcion padre, para no perder datos, o se que redefino
            
            