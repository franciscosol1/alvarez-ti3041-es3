usuario:fran
contraseña:gatadoris2

1.-Implemente las operaciones desde el sitio (no solo desde /admin): crear un registro con
formulario, editar un registro existente y eliminar con confirmación.
Tras cada operación, redirija al listado principal para ver el cambio reflejado desde la BD

1:en este prom creo el editar_producto.html para mostrar el foms.py y el CRUD  puedes acceder a este después de ingresar como administrador 

2.-Reporte 1, resumen por agrupación: cantidad de registros y algún cálculo (promedio de precio,
total de stock) por categoría, marca o laboratorio, usando aggregate o annotate del ORM.
Reporte 2, listado filtrado: registros bajo un umbral (stock crítico, no disponibles, o que
requieren receta), usando filter y order_by.
Cada reporte tiene su template, ambos accesibles desde la navegación de base.html, con los
cálculos resueltos en la vista con el ORM

2:

3.-Cree el modelo ConsultaCliente (nombre, correo, mensaje, producto de interés opcional, fecha
automática), registrado en /admin.
Implemente el formulario con ModelForm, con validaciones (campos obligatorios, correo válido,
largo mínimo); la vista guarda en la BD y muestra confirmación.
Implemente una funcionalidad simple con sesiones (últimos 3 productos visitados o contador de
visitas) y verifique CSRF y validaciones con datos inválidos.
