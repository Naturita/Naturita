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



si hay algun error lanzar estos comandos para volver al estado que funciona 
## PS C:\Users\DaNi\Naturita> git reset --hard 9398f39
HEAD is now at 9398f39 Update products from Admin Panel
## PS C:\Users\DaNi\Naturita> git push --force
fatal: You are not currently on a branch.
To push the history leading to the current (detached HEAD)
state now, use

    git push origin HEAD:<name-of-remote-branch>

## PS C:\Users\DaNi\Naturita> git checkout main
Previous HEAD position was 9398f39 Update products from Admin Panel
Switched to branch 'main'
Your branch is behind 'origin/main' by 2 commits, and can be fast-forwarded.
  (use "git pull" to update your local branch)
## PS C:\Users\DaNi\Naturita> git push --force
Total 0 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
To https://github.com/Naturita/Naturita.git
 + 13f5722...4c6ed4d main -> main (forced update)
## PS C:\Users\DaNi\Naturita> git log --oneline -5
4c6ed4d (HEAD -> main, origin/main, origin/HEAD) Update products from Admin Panel
63e9636 Update products from Admin Panel
63b15d2 Update products from Admin Panel
6e23f8c Update products from Admin Panel
b05886e centrado buscadores y sin scroll horizontal
## PS C:\Users\DaNi\Naturita> 