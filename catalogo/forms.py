from decimal import Decimal

from django import forms

from .models import ConsultaCliente, Producto


class ProductoForm(forms.ModelForm):
    precio = forms.DecimalField(
        min_value=Decimal('0.01'),
        max_digits=10,
        decimal_places=2,
        error_messages={
            'min_value': 'El valor debe ser mayor o igual a %(limit_value)s.',
        },
        widget=forms.NumberInput(attrs={'min': '0.01', 'step': '0.01'}),
    )
    stock = forms.IntegerField(
        min_value=0,
        error_messages={
            'min_value': 'El valor debe ser mayor o igual a %(limit_value)s.',
        },
        widget=forms.NumberInput(attrs={'min': '0', 'step': '1'}),
    )

    class Meta:
        model = Producto
        fields = ('nombre', 'categoria', 'precio', 'stock')
        labels = {
            'nombre': 'Nombre',
            'categoria': 'Categoría',
            'precio': 'Precio',
            'stock': 'Stock',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'autocomplete': 'off'}),
            'categoria': forms.TextInput(attrs={'autocomplete': 'off'}),
        }


class ConsultaClienteForm(forms.ModelForm):
    nombre = forms.CharField(
        min_length=2,
        max_length=150,
        error_messages={
            'min_length': 'El nombre debe tener al menos 2 caracteres.',
            'required': 'Ingresa tu nombre.',
        },
    )
    correo = forms.EmailField(
        error_messages={
            'invalid': 'Ingresa un correo electrónico válido.',
            'required': 'Ingresa tu correo electrónico.',
        },
    )
    mensaje = forms.CharField(
        min_length=10,
        widget=forms.Textarea(attrs={'rows': 5}),
        error_messages={
            'min_length': 'El mensaje debe tener al menos 10 caracteres.',
            'required': 'Escribe tu mensaje.',
        },
    )

    class Meta:
        model = ConsultaCliente
        fields = ('nombre', 'correo', 'mensaje', 'producto_interes')
        labels = {
            'nombre': 'Nombre',
            'correo': 'Correo electrónico',
            'mensaje': 'Mensaje',
            'producto_interes': 'Producto de interés (opcional)',
        }
        widgets = {
            'producto_interes': forms.Select(),
        }
