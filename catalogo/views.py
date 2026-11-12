import json
from pathlib import Path
from urllib.parse import quote

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404

from .models import Producto


DATOS_PATH = Path(__file__).parent / 'data' / 'productos.json'

IMAGENES_PRODUCTOS = {
  1: 'martillo.png',
  2: 'destornillador.png',
  3: 'set de llaves allen 9.png',
  4: 'alicate.png',
  5: 'cinta metrica.png',
  6: 'nivel de burbuja.png',
  7: 'taladro percutor.png',
  8: 'brocas para concreto.png',
  9: 'cierra circular.png',
  10: 'disco de corte metal.png',
  11: 'lijadora orbital.png',
  12: 'guantes.png',
  13: 'lentes.png',
  14: 'casco.png',
  16: 'tornillo madera.png',
  17: 'tarugo.png',
  18: 'clavos.png',
  19: 'pernos.png',
  20: 'silicona.png',
  21: 'adecibos.png',
  22: 'cinta hasliadora.png',
  23: 'enchufe.png',
  25: 'cable electrico.png',
  26: 'llave de paso.png',
  27: 'flexibles.png',
  28: 'cinta teflon.png',
  29: 'rodillo.png',
  30: 'brocha.png',
}


def preparar_producto(producto):
    if isinstance(producto, Producto):
        producto_data = {
            'id': producto.pk,
            'nombre': producto.nombre,
            'categoria': producto.categoria,
            'precio': float(producto.precio),
            'stock': producto.stock,
        }
    else:
        producto_data = dict(producto)

    imagen = IMAGENES_PRODUCTOS.get(producto_data.get('id'))
    if imagen:
        ruta_imagen = f'/static/catalogo/productos(imageness)/{quote(imagen)}'
        producto_con_imagen = {**producto_data, 'imagen': ruta_imagen, 'sprite': ruta_imagen}
    else:
        producto_con_imagen = {**producto_data, 'imagen': generar_imagen_producto(producto_data), 'sprite': generar_imagen_producto(producto_data)}

    producto_con_imagen['bg_x'] = 50
    producto_con_imagen['bg_y'] = 50
    return producto_con_imagen


def generar_imagen_producto(producto):
    nombre = str(producto.get('nombre', 'Producto')).strip()
    categoria = str(producto.get('categoria', 'General')).strip() or 'General'
    nombre_corto = nombre[:34]
    nombre_lower = nombre.lower()
    numero = int(producto.get('id', 1))

    palette = [
        ('#dfe7e2', '#9bb0a2', '#2f4f46', '#1a2d28', '#b7d96a'),
        ('#edf1f5', '#a7bcd8', '#3d5c7a', '#1f2d3d', '#f0b653'),
        ('#f6eee7', '#ddb08f', '#7c4a2c', '#351b14', '#ebb16d'),
        ('#edf2f3', '#c7d8dd', '#4e6475', '#1d2a34', '#77b8ca'),
        ('#f5f3ed', '#d9d4c7', '#5d534c', '#2a2520', '#d6b77a'),
    ]
    bg, mid, dark, deep, accent = palette[numero % len(palette)]

    if any(k in nombre_lower for k in ['martillo', 'llave', 'alicate', 'destornillador']):
        object_svg = f"""
        <g transform='translate(110,118)'>
          <ellipse cx='220' cy='300' rx='220' ry='38' fill='rgba(0,0,0,0.18)'/>
          <g>
            <path d='M130 40 L210 40 C238 40 260 62 260 90 L260 180 L198 180 L198 151 L169 151 L169 198 L130 198 Z' fill='url(#metal)'/>
            <path d='M132 80 L210 80 L210 150 L132 150 Z' fill='rgba(255,255,255,0.18)'/>
            <path d='M110 235 L270 235 L290 285 L90 285 Z' fill='url(#metalDark)'/>
            <path d='M164 218 L150 285 L188 285 L198 218 Z' fill='rgba(255,255,255,0.18)'/>
            <rect x='148' y='0' width='42' height='70' rx='16' fill='url(#steel)'/>
            <rect x='155' y='62' width='28' height='90' rx='12' fill='rgba(255,255,255,0.3)'/>
            <path d='M174 232 Q180 265 192 290' stroke='rgba(255,255,255,0.45)' stroke-width='8' fill='none' stroke-linecap='round'/>
          </g>
        </g>
        """
    elif any(k in nombre_lower for k in ['taladro', 'sierra', 'lijadora', 'broca']):
        object_svg = f"""
        <g transform='translate(130,120)'>
          <ellipse cx='170' cy='310' rx='200' ry='34' fill='rgba(0,0,0,0.18)'/>
          <g>
            <rect x='80' y='40' width='210' height='120' rx='26' fill='url(#body)'/>
            <rect x='180' y='120' width='56' height='150' rx='16' fill='url(#metalDark)'/>
            <path d='M100 175 L110 235 L95 290 L145 290 L160 235 L170 175 Z' fill='url(#dark)'/>
            <path d='M215 175 L225 235 L240 290 L195 290 L180 235 L170 175 Z' fill='url(#dark)'/>
            <circle cx='245' cy='120' r='68' fill='url(#metal)'/>
            <circle cx='245' cy='120' r='30' fill='url(#dark)'/>
            <path d='M55 82 L82 82 L82 150 L55 150 Z' fill='rgba(255,255,255,0.18)'/>
            <path d='M60 158 L82 158 L82 230 L60 230 Z' fill='rgba(255,255,255,0.12)'/>
            <path d='M160 220 L210 220' stroke='rgba(255,255,255,0.42)' stroke-width='10' stroke-linecap='round'/>
          </g>
        </g>
        """
    elif any(k in nombre_lower for k in ['cinta', 'metro', 'nivel', 'medicion']):
        object_svg = f"""
        <g transform='translate(110,120)'>
          <ellipse cx='210' cy='310' rx='210' ry='36' fill='rgba(0,0,0,0.16)'/>
          <rect x='20' y='35' width='300' height='180' rx='22' fill='url(#panel)'/>
          <rect x='50' y='70' width='240' height='112' rx='12' fill='rgba(255,255,255,0.7)'/>
          <line x1='82' y1='90' x2='262' y2='90' stroke='{dark}' stroke-width='8' stroke-linecap='round'/>
          <line x1='82' y1='120' x2='262' y2='120' stroke='{dark}' stroke-width='8' stroke-linecap='round'/>
          <line x1='82' y1='150' x2='262' y2='150' stroke='{dark}' stroke-width='8' stroke-linecap='round'/>
          <line x1='170' y1='66' x2='170' y2='182' stroke='{deep}' stroke-width='10' stroke-linecap='round'/>
          <circle cx='170' cy='222' r='54' fill='rgba(255,255,255,0.9)'/>
          <circle cx='170' cy='222' r='20' fill='{accent}'/>
          <rect x='120' y='242' width='100' height='32' rx='14' fill='{dark}' opacity='0.8'/>
        </g>
        """
    elif any(k in nombre_lower for k in ['guante', 'casco', 'lente', 'mascarilla', 'seguridad']):
        object_svg = f"""
        <g transform='translate(118,120)'>
          <ellipse cx='200' cy='300' rx='190' ry='36' fill='rgba(0,0,0,0.16)'/>
          <path d='M120 50 C130 20, 265 18, 290 60 L310 200 C313 226, 294 246, 268 246 H122 C97 246, 78 225, 82 198 L120 50 Z' fill='url(#softMetal)'/>
          <circle cx='182' cy='124' r='74' fill='rgba(255,255,255,0.8)'/>
          <path d='M138 112 L180 158 L225 112' stroke='{deep}' stroke-width='18' fill='none' stroke-linecap='round' stroke-linejoin='round'/>
          <path d='M177 100 L200 200' stroke='{deep}' stroke-width='18' stroke-linecap='round'/>
          <path d='M105 246 L150 215' stroke='{deep}' stroke-width='18' stroke-linecap='round'/>
          <path d='M255 246 L210 215' stroke='{deep}' stroke-width='18' stroke-linecap='round'/>
        </g>
        """
    elif any(k in nombre_lower for k in ['tornillo', 'tuerca', 'clavo', 'tarugo', 'perno', 'fijacion', 'fijaciones']):
        object_svg = f"""
        <g transform='translate(140,92)'>
          <ellipse cx='180' cy='330' rx='170' ry='28' fill='rgba(0,0,0,0.18)'/>
          <g>
            <circle cx='180' cy='85' r='84' fill='url(#metal)'/>
            <circle cx='180' cy='85' r='38' fill='url(#deep)'/>
            <rect x='150' y='140' width='60' height='170' rx='20' fill='url(#metalDark)'/>
            <path d='M138 168 H222' stroke='rgba(255,255,255,0.35)' stroke-width='12' stroke-linecap='round'/>
            <path d='M138 206 H222' stroke='rgba(255,255,255,0.35)' stroke-width='12' stroke-linecap='round'/>
          </g>
        </g>
        """
    elif any(k in nombre_lower for k in ['silicona', 'adhesivo', 'pegamento', 'sellante']):
        object_svg = f"""
        <g transform='translate(150,82)'>
          <ellipse cx='170' cy='330' rx='170' ry='28' fill='rgba(0,0,0,0.16)'/>
          <g>
            <rect x='25' y='55' width='260' height='210' rx='26' fill='url(#tube)'/>
            <path d='M105 0 L195 0 L220 54 L80 54 Z' fill='url(#accentMetal)'/>
            <path d='M90 110 H215' stroke='rgba(255,255,255,0.72)' stroke-width='16' stroke-linecap='round'/>
            <path d='M90 150 H215' stroke='rgba(255,255,255,0.72)' stroke-width='16' stroke-linecap='round'/>
            <path d='M90 190 H215' stroke='rgba(255,255,255,0.72)' stroke-width='16' stroke-linecap='round'/>
            <circle cx='210' cy='255' r='34' fill='rgba(255,255,255,0.18)'/>
          </g>
        </g>
        """
    elif any(k in nombre_lower for k in ['cable', 'enchufe', 'interruptor', 'electric', 'flexible']):
        object_svg = f"""
        <g transform='translate(110,116)'>
          <ellipse cx='210' cy='310' rx='200' ry='30' fill='rgba(0,0,0,0.18)'/>
          <g>
            <rect x='80' y='70' width='210' height='140' rx='28' fill='url(#panel)'/>
            <circle cx='132' cy='142' r='25' fill='{accent}'/>
            <circle cx='240' cy='142' r='25' fill='{accent}'/>
            <path d='M132 142 L240 142' stroke='{deep}' stroke-width='18' stroke-linecap='round'/>
            <rect x='126' y='200' width='180' height='60' rx='18' fill='url(#metalDark)'/>
            <path d='M160 215 L160 248' stroke='rgba(255,255,255,0.5)' stroke-width='13' stroke-linecap='round'/>
            <path d='M220 215 L220 248' stroke='rgba(255,255,255,0.5)' stroke-width='13' stroke-linecap='round'/>
          </g>
        </g>
        """
    elif any(k in nombre_lower for k in ['rodillo', 'brocha', 'pintura']):
        object_svg = f"""
        <g transform='translate(126,120)'>
          <ellipse cx='180' cy='316' rx='180' ry='32' fill='rgba(0,0,0,0.17)'/>
          <g>
            <rect x='82' y='0' width='160' height='52' rx='18' fill='rgba(255,255,255,0.82)'/>
            <rect x='150' y='44' width='24' height='170' rx='12' fill='url(#metalDark)'/>
            <path d='M110 110 C145 90, 220 90, 250 110 L250 208 C220 225, 145 225, 110 208 Z' fill='url(#paint)'/>
            <ellipse cx='180' cy='160' rx='72' ry='45' fill='rgba(255,255,255,0.68)'/>
            <circle cx='180' cy='160' r='16' fill='{accent}'/>
          </g>
        </g>
        """
    else:
        object_svg = f"""
        <g transform='translate(130,120)'>
          <ellipse cx='170' cy='310' rx='180' ry='30' fill='rgba(0,0,0,0.16)'/>
          <g>
            <rect x='40' y='80' width='260' height='180' rx='28' fill='url(#box)'/>
            <rect x='70' y='110' width='200' height='120' rx='18' fill='rgba(255,255,255,0.18)'/>
            <path d='M120 80 L120 260 M200 80 L200 260' stroke='rgba(255,255,255,0.22)' stroke-width='10'/>
            <path d='M40 130 L300 130 M40 190 L300 190' stroke='rgba(255,255,255,0.22)' stroke-width='10'/>
          </g>
        </g>
        """

    svg = f"""
    <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 560'>
      <defs>
        <linearGradient id='bgGrad' x1='0' x2='1' y1='0' y2='1'>
          <stop offset='0%' stop-color='{bg}'/>
          <stop offset='100%' stop-color='{mid}'/>
        </linearGradient>
        <linearGradient id='metal' x1='0' x2='1' y1='0' y2='1'>
          <stop offset='0%' stop-color='#f5f7fa'/>
          <stop offset='25%' stop-color='#dfe7ee'/>
          <stop offset='65%' stop-color='#a7afba'/>
          <stop offset='100%' stop-color='#6a7482'/>
        </linearGradient>
        <linearGradient id='metalDark' x1='0' x2='0' y1='0' y2='1'>
          <stop offset='0%' stop-color='{dark}'/>
          <stop offset='100%' stop-color='{deep}'/>
        </linearGradient>
        <linearGradient id='steel' x1='0' x2='1' y1='0' y2='1'>
          <stop offset='0%' stop-color='#eef3f6'/>
          <stop offset='100%' stop-color='#9eaab5'/>
        </linearGradient>
        <linearGradient id='softMetal' x1='0' x2='1' y1='0' y2='1'>
          <stop offset='0%' stop-color='#f4f2f0'/>
          <stop offset='100%' stop-color='{mid}'/>
        </linearGradient>
        <linearGradient id='panel' x1='0' x2='1' y1='0' y2='1'>
          <stop offset='0%' stop-color='white'/>
          <stop offset='100%' stop-color='{mid}'/>
        </linearGradient>
        <linearGradient id='tube' x1='0' x2='1' y1='0' y2='1'>
          <stop offset='0%' stop-color='#f9f2d6'/>
          <stop offset='100%' stop-color='{accent}'/>
        </linearGradient>
        <linearGradient id='accentMetal' x1='0' x2='1' y1='0' y2='1'>
          <stop offset='0%' stop-color='{accent}'/>
          <stop offset='100%' stop-color='{dark}'/>
        </linearGradient>
        <linearGradient id='paint' x1='0' x2='0' y1='0' y2='1'>
          <stop offset='0%' stop-color='white'/>
          <stop offset='100%' stop-color='{accent}'/>
        </linearGradient>
        <linearGradient id='body' x1='0' x2='1' y1='0' y2='1'>
          <stop offset='0%' stop-color='white'/>
          <stop offset='100%' stop-color='{mid}'/>
        </linearGradient>
        <linearGradient id='box' x1='0' x2='1' y1='0' y2='1'>
          <stop offset='0%' stop-color='{mid}'/>
          <stop offset='100%' stop-color='{dark}'/>
        </linearGradient>
        <linearGradient id='dark' x1='0' x2='0' y1='0' y2='1'>
          <stop offset='0%' stop-color='{deep}'/>
          <stop offset='100%' stop-color='#1a1d24'/>
        </linearGradient>
      </defs>

      <rect width='800' height='560' fill='url(#bgGrad)' rx='32'/>
      <circle cx='125' cy='120' r='145' fill='rgba(255,255,255,0.12)'/>
      <circle cx='700' cy='450' r='185' fill='rgba(255,255,255,0.10)'/>
      <path d='M0 432 C180 370, 270 410, 380 444 C560 500, 700 440, 800 392 L800 560 L0 560 Z' fill='rgba(255,255,255,0.08)'/>
      <rect x='56' y='46' width='190' height='46' rx='14' fill='rgba(255,255,255,0.18)'/>
      <text x='82' y='76' font-size='22' font-family='Segoe UI, Arial, sans-serif' fill='white' font-weight='700'>FERROSUR</text>
      {object_svg}
      <text x='72' y='498' font-size='28' font-family='Segoe UI, Arial, sans-serif' fill='white' font-weight='700'> {categoria[:23]} </text>
      <text x='72' y='532' font-size='18' font-family='Segoe UI, Arial, sans-serif' fill='rgba(255,255,255,0.92)'>{nombre_corto}</text>
    </svg>
    """
    return 'data:image/svg+xml;charset=UTF-8,' + quote(svg)


def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin:index')
    return redirect('admin:login')


@login_required(login_url='admin:login')
@user_passes_test(lambda user: user.is_staff, login_url='admin:login')
def admin_logout(request):
    logout(request)
    return redirect('admin:login')


@login_required(login_url='admin:login')
@user_passes_test(lambda user: user.is_staff, login_url='admin:login')
def panel_admin(request):
    return redirect('admin:index')


@login_required(login_url='admin:login')
@user_passes_test(lambda user: user.is_staff, login_url='admin:login')
def crear_producto(request):
    if request.method != 'POST':
        return redirect('admin:index')

    nombre = (request.POST.get('nombre') or '').strip()
    categoria = (request.POST.get('categoria') or '').strip()

    try:
        precio = float(request.POST.get('precio', 0) or 0)
        stock = int(request.POST.get('stock', 0) or 0)
    except ValueError:
        messages.error(request, 'Precio y stock deben ser valores válidos.')
        return redirect('admin:index')

    if not nombre or not categoria or precio <= 0:
        messages.error(request, 'Completa nombre, categoría y un precio válido.')
        return redirect('admin:index')

    producto = Producto.objects.create(
        nombre=nombre,
        categoria=categoria,
        precio=round(precio, 2),
        stock=max(0, stock),
    )
    messages.success(request, f'Se creó el producto "{producto.nombre}" correctamente.')
    return redirect('admin:index')


@login_required(login_url='admin:login')
@user_passes_test(lambda user: user.is_staff, login_url='admin:login')
def actualizar_stock(request, producto_id):
    if request.method != 'POST':
        return redirect('admin:index')

    producto = get_object_or_404(Producto, pk=producto_id)

    try:
        nuevo_stock = int(request.POST.get('stock', producto.stock) or producto.stock)
    except ValueError:
        messages.error(request, 'El stock debe ser un número entero.')
        return redirect('admin:index')

    producto.stock = max(0, nuevo_stock)
    producto.save(update_fields=['stock'])
    messages.success(request, f'Se actualizó el stock de "{producto.nombre}" a {producto.stock}.')
    return redirect('admin:index')


def landing(request):
    productos_destacados = [preparar_producto(producto) for producto in Producto.objects.order_by('id')[:3]]
    return render(request, 'catalogo/landing.html', {'productos_destacados': productos_destacados})


def lista_productos(request):
    productos = [preparar_producto(producto) for producto in Producto.objects.order_by('id')]
    contexto = {
        'productos': productos,
        'total_productos': len(productos),
        'productos_con_stock': sum(producto['stock'] > 0 for producto in productos),
    }
    return render(request, 'catalogo/lista.html', contexto)


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    return render(request, 'catalogo/detalle.html', {'producto': preparar_producto(producto)})


def simular_compra(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    producto_data = preparar_producto(producto)

    if request.method != 'POST':
        return render(
            request,
            'catalogo/compra.html',
            {
                'producto': producto_data,
                'error': 'Esta compra debe realizarse desde el formulario del producto.',
            },
        )

    try:
        cantidad = int(request.POST.get('cantidad', 1) or 1)
    except ValueError:
        cantidad = 1

    cantidad = max(1, cantidad)

    if producto.stock == 0 or cantidad > producto.stock:
        return render(
            request,
            'catalogo/compra.html',
            {
                'producto': producto_data,
                'cantidad': cantidad,
                'error': 'No hay stock suficiente para completar esta compra.',
            },
        )

    producto.stock -= cantidad
    producto.save(update_fields=['stock'])
    producto_data = preparar_producto(producto)

    return render(
        request,
        'catalogo/compra.html',
        {
            'producto': producto_data,
            'cantidad': cantidad,
            'total': float(producto.precio) * cantidad,
            'exito': True,
        },
    )