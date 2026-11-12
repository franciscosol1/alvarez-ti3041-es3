from decimal import Decimal

from django import forms

from .models import Producto


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
