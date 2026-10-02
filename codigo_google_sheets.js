// ==============================================================================
// CÓDIGO DE SINCRONIZACIÓN EN VIVO - CALENDARIO RRSS UMWELT
// ==============================================================================
// Este script convierte una planilla de Google Sheets en una base de datos en vivo.
// Cualquier persona que tenga el archivo HTML podrá agregar o editar tareas y
// tú verás los cambios en tiempo real desde tu dispositivo (y viceversa).
//
// PASOS DE INSTALACIÓN (Toma menos de 1 minuto):
// ------------------------------------------------------------------------------
// 1. Ve a https://sheets.new en tu navegador (creará una planilla nueva en tu Google Drive).
// 2. Nombra la planilla: "Base de Datos - Calendario RRSS UMWELT".
// 3. En el menú superior haz clic en: Extensiones > Apps Script.
// 4. Borra todo el código que aparece por defecto y PEGA este archivo completo.
// 5. Haz clic en el botón azul superior: "Implementar" (Deploy) > "Nueva implementación".
// 6. En la ventana que aparece:
//    - Selecciona el tipo (icono de engranaje): "Aplicación web".
//    - Descripción: "Sincronizador Calendario RRSS".
//    - Ejecutar como: "Yo (tu_correo@gmail.com)".
//    - Quién tiene acceso: "Cualquier persona" (Anyone) -> ¡MUY IMPORTANTE para que tu equipo pueda conectar sin pedir login!
// 7. Haz clic en "Implementar", autoriza los permisos de Google.
// 8. Copia la "URL de la aplicación web" (termina en /exec).
// 9. Ve a tu Calendario HTML, haz clic en "⚡ Conectar en Vivo" y pega esa URL.
// ==============================================================================

function doGet(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var rawJson = sheet.getRange("A1").getValue();
  var responseData;
  
  try {
    responseData = rawJson ? JSON.parse(rawJson) : { posts: [], _selMonth: "2026-09" };
  } catch(err) {
    responseData = { posts: [], _selMonth: "2026-09" };
  }
  
  return ContentService.createTextOutput(JSON.stringify(responseData))
    .setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var contents = e.postData ? e.postData.contents : "";
  
  if (contents) {
    // 1. Guardar el JSON crudo en A1 para lectura ultrarrápida del HTML
    sheet.getRange("A1").setValue(contents);
    
    // 2. Formatear automáticamente filas legibles en la hoja de cálculo
    try {
      var parsed = JSON.parse(contents);
      if (parsed && parsed.posts && Array.isArray(parsed.posts)) {
        updateSpreadsheetTable(sheet, parsed.posts);
      }
    } catch(err) {
      Logger.log("Error al tabular datos: " + err);
    }
  }
  
  return ContentService.createTextOutput(JSON.stringify({ status: "success", timestamp: new Date().toISOString() }))
    .setMimeType(ContentService.MimeType.JSON);
}

function updateSpreadsheetTable(sheet, posts) {
  // Limpiar filas anteriores desde la fila 3
  var lastRow = sheet.getLastRow();
  if (lastRow >= 3) {
    sheet.getRange(3, 1, lastRow - 2, 8).clearContent();
  }
  
  // Encabezados con estilo UMWELT
  var headers = [["Fecha", "Día", "Formato", "Título / Tema", "Estado", "Obligatoria", "Hora / Notas", "ID"]];
  var headerRange = sheet.getRange("A3:H3");
  headerRange.setValues(headers);
  headerRange.setFontWeight("bold");
  headerRange.setBackground("#ef6c1a"); // Naranja UMWELT
  headerRange.setFontColor("#ffffff");
  headerRange.setHorizontalAlignment("center");
  
  if (posts.length === 0) return;
  
  // Ordenar por fecha
  var sorted = posts.slice().sort(function(a, b) {
    return (a.date || "").localeCompare(b.date || "");
  });
  
  var DAYS_ES = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"];
  
  var rows = sorted.map(function(p) {
    var d = new Date(p.date + "T00:00:00");
    var dayName = isNaN(d.getTime()) ? "" : DAYS_ES[(d.getDay() + 6) % 7];
    var statusLabels = {
      "pendiente": "⏳ Pendiente",
      "en_progreso": "🔄 En progreso",
      "listo": "✅ Listo",
      "no_realizado": "❌ No realizado"
    };
    
    return [
      p.date || "",
      dayName,
      p.type || "",
      p.title || "",
      statusLabels[p.status] || p.status || "",
      p.mandatory ? "Sí (Historia diaria)" : "No",
      (p.time ? p.time + " | " : "") + (p.notes || ""),
      p.id || ""
    ];
  });
  
  var dataRange = sheet.getRange(4, 1, rows.length, 8);
  dataRange.setValues(rows);
  
  // Estilo alternado sutil
  for (var i = 0; i < rows.length; i++) {
    var rowBg = (i % 2 === 0) ? "#ffffff" : "#fdfbf7";
    sheet.getRange(4 + i, 1, 1, 8).setBackground(rowBg);
  }
  
  sheet.autoResizeColumns(1, 8);
}
