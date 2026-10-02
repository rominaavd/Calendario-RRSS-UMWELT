# ⚡ Sincronización en Tiempo Real - Calendario RRSS UMWELT

Con este sistema, **cualquier persona de tu equipo que abra el calendario podrá agregar o editar tareas y tú las verás reflejadas inmediatamente en tu dispositivo**, sin pagar por servidores ni depender de software complicado.

---

## 🚀 Pasos para activar la sincronización (1 minuto):

### Paso 1: Crear una planilla en Google Drive
1. En tu navegador abre: [https://sheets.new](https://sheets.new)
2. Ponle de nombre a la planilla: `Base de Datos - Calendario RRSS UMWELT`

### Paso 2: Pegar el código sincronizador
1. En el menú superior de tu planilla, haz clic en **Extensiones** > **Apps Script**.
2. Borra el código que aparece por defecto (`function myFunction() { ... }`).
3. Abre el archivo [`codigo_google_sheets.js`](file:///Users/romiheresmann/Desktop/UMWELT/Calendario%20RRSS/codigo_google_sheets.js), copia todo su contenido y pégalo en el editor de Apps Script.
4. Guarda los cambios con el icono de disquete (o `Ctrl + S` / `Cmd + S`).

### Paso 3: Publicar como Aplicación Web
1. En la esquina superior derecha, haz clic en el botón azul **Implementar** (*Deploy*) > **Nueva implementación**.
2. En el engranaje de la izquierda, selecciona **Aplicación web**.
3. Configura exactamente estos 3 campos:
   * **Descripción**: `Sincronizador Calendario`
   * **Ejecutar como**: `Yo (tu correo de Google)`
   * **Quién tiene acceso**: **`Cualquier persona`** (*Anyone*) *(⚠️ Es crucial para que tu equipo pueda guardar tareas sin pedirles permisos especiales)*.
4. Haz clic en **Implementar**. Si te pide autorizar permisos, acéptalos (*Avanzado > Ir a proyecto*).
5. **Copia la URL de la aplicación web** que termina en `/exec`.

### Paso 4: Conectar en tu Calendario
1. Abre tu calendario: [calendario-ig-standalone.html](file:///Users/romiheresmann/Desktop/UMWELT/Calendario%20RRSS/calendario-ig-standalone.html).
2. En la barra superior, haz clic en **"⚡ Conectar Sincronización en Vivo"**.
3. Pega la URL que copiaste y presiona **"Guardar y Conectar"**.
4. ¡Listo! El indicador cambiará a **`🟢 Sincronizado en Vivo con el Equipo`**.

---

## 👥 ¿Cómo lo usan los demás?
Una vez conectada la URL en tu calendario, haz clic en **"💾 Guardar Archivo HTML"**. 
Ese archivo ya llevará la conexión integrada de forma permanente. Puedes enviárselo a quien quieras (por WhatsApp, Slack, correo o Drive):
* Cuando otra persona agregue una publicación o cambie un estado a "Listo" o "En progreso", **se guardará en la base de datos**.
* Tu calendario actualizará los cambios automáticamente en tu pantalla cada pocos segundos.
* Además, podrás abrir la planilla de Google Sheets cuando quieras y verás todas las tareas organizadas en filas y columnas ordenadas.
