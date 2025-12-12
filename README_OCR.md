Guía rápida: extraer precios de las imágenes (OCR) y aplicarlos a la tienda

Resumen
-------
Este proyecto incluye `ocr_extract_prices.py`, un script que intenta leer los precios incrustados en las imágenes dentro de la carpeta `imagenes/`.
El script genera dos archivos:
 - `saved_prices.json` — mapeo filename -> precio detectado (JSON legible)
 - `saved_prices.js` — script JS que escribe los precios en localStorage (clave `savedPrices`).

Pasos para ejecutar en Windows (PowerShell)
-----------------------------------------
1) Instala Tesseract OCR (si no lo tienes)
   - Descarga el instalador desde: https://github.com/tesseract-ocr/tesseract/releases
   - O usa Chocolatey (si lo tienes):
     choco install -y tesseract
   - Anota la ruta de instalación (por ejemplo: C:\Program Files\Tesseract-OCR\tesseract.exe)

2) Asegúrate de tener Python 3 instalado (Windows: `py -3`)

3) Instala dependencias Python (en PowerShell):

```powershell
py -3 -m pip install --upgrade pip
py -3 -m pip install pillow pytesseract opencv-python
```

4) (Opcional) Si Tesseract no está en tu PATH, edita `ocr_extract_prices.py` y descomenta esta línea en la parte superior, ajustando la ruta si es necesario:

```python
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

5) Ejecuta el script desde la carpeta del proyecto (donde está `ocr_extract_prices.py`):

```powershell
py -3 ocr_extract_prices.py
```

6) Resultados:
 - `saved_prices.json` con el mapeo filename->precio.
 - `saved_prices.js` que contiene una instrucción `localStorage.setItem('savedPrices', ...)`.

7) Abrir `Index.html` en el navegador (si lo sirves con un servidor local o lo abres directamente). El archivo `Index.html` ya incluye una referencia a `saved_prices.js` (si existe). Si lo abres después de ejecutar el script, la página cargará los precios automáticamente.

Notas y recomendaciones
-----------------------
- El OCR no es perfecto sobre fotografías con tipografías decorativas o sobre fondos muy cargados. Revisa el resultado en el modal "Editar precios" y corrige manualmente los errores.
- Si prefieres, puedes pegar aquí el JSON generado y yo puedo aplicarlo manualmente por ti.
- Si quieres, te doy comandos de PowerShell preparados para automatizar la instalación y ejecución (con tu permiso).

Si quieres que ejecute el OCR por ti desde aquí, confírmame que puedo intentar instalar/ejecutar herramientas en tu sistema (necesitaré permiso explícito para ejecutar instalaciones).