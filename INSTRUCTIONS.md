# Instrucciones del Sistema Admin Naturita

## 1. Iniciar el Sistema
Para abrir el panel de administración, ejecuta el siguiente comando en la terminal:

```bash
python app.py
```

Luego, abre tu navegador y ve a:
**http://127.0.0.1:5000/admin**

## 2. Iniciar Sesión
Usa las credenciales que proporcionaste:
- **Usuario**: Naturita
- **Contraseña**: Lacalera25@

## 3. Gestión de Productos
- **Agregar**: Desde el Panel de Control, haz clic en "Nuevo Producto". Completa todos los campos (Nombre, Precio, Info Extra para el pop-up, etc.).
- **Editar**: Haz clic en el ícono de lápiz al lado de cualquier producto en la lista.

## 4. Sincronizar con la Web
Cuando hayas terminado de hacer cambios (agregar o editar productos), haz clic en el botón **"Sincronizar Web"** en el Panel de Control.
- Esto generará automáticamente las páginas del catálogo con los nuevos datos.
- Subirá los cambios a GitHub automáticamente.
- Tu sitio web (https://naturita.github.io/Naturita/) se actualizará en unos minutos.

## Notas Importantes
- Asegúrate de tener conexión a internet para que la sincronización con GitHub funcione.
- Las imágenes deben estar en la carpeta `imagenes` y debes poner la ruta correcta (ej: `../../../imagenes/mi_foto.jpg`).
