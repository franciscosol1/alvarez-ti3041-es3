from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.nombre


class ConsultaCliente(models.Model):
    nombre = models.CharField(max_length=150)
    correo = models.EmailField()
    mensaje = models.TextField()
    producto_interes = models.ForeignKey(
        Producto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='consultas_clientes',
    )
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Consulta de cliente'
        verbose_name_plural = 'Consultas de clientes'
        ordering = ('-fecha',)

    def __str__(self):
        return f'{self.nombre} - {self.correo}'