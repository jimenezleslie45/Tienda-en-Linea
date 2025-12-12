"""
OCR helper to extract prices from images in the `imagenes/` folder.
Generates two output files in the project root:
 - saved_prices.json  -> mapping filename -> price string (example: "$240")
 - saved_prices.js    -> small JS that sets localStorage['savedPrices'] to the JSON mapping

How it works (simple heuristic):
 - loads each image, applies grayscale, optional threshold and dilation to improve text
 - runs pytesseract (with config to look for digits and $), extracts candidate strings
 - picks the most likely candidate that contains a currency symbol or looks like a price
 - fallback: empty string (you can edit manually in the "Editar precios" modal)

Run (after installing requirements and Tesseract):
    py -3 ocr_extract_prices.py

Note: OCR on product photos may fail for stylized text. Always review results in the modal and correct any mistakes.
"""

import os
import json
import re
from PIL import Image, ImageFilter, ImageOps
import pytesseract

IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'imagenes')
OUTPUT_JSON = os.path.join(os.path.dirname(__file__), 'saved_prices.json')
OUTPUT_JS = os.path.join(os.path.dirname(__file__), 'saved_prices.js')

# You may need to set pytesseract.pytesseract.tesseract_cmd to the tesseract.exe path on Windows
# Example (uncomment and edit if needed):
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

CURRENCY_REGEX = re.compile(r'(?:\$|€|¢|₡|£|¥)?\s*[0-9]{1,3}(?:[\.,][0-9]{2})?')
DIGITS_REGEX = re.compile(r'[0-9]{2,4}(?:[\.,][0-9]{1,2})?')


def preprocess_image(img_path):
    img = Image.open(img_path).convert('RGB')
    # Resize if very large
    max_dim = 1200
    if max(img.size) > max_dim:
        img.thumbnail((max_dim, max_dim), Image.LANCZOS)
    # convert to grayscale and increase contrast
    gray = ImageOps.grayscale(img)
    # slight sharpening
    gray = gray.filter(ImageFilter.SHARPEN)
    return gray


def extract_price_from_text(text):
    if not text:
        return ''
    # look for currency-like tokens first
    matches = CURRENCY_REGEX.findall(text)
    if matches:
        # pick the first that contains a digit
        for m in matches:
            if re.search(r'\d', m):
                s = m.strip()
                # normalize comma decimal to dot (keep original style)
                s = s.replace(' ', '')
                return s
    # fallback: find any digit group that looks like price
    m2 = DIGITS_REGEX.search(text)
    if m2:
        return '$' + m2.group(0)
    return ''


def process_image_file(filename):
    path = os.path.join(IMAGES_DIR, filename)
    try:
        img = preprocess_image(path)
        # try raw OCR
        text = pytesseract.image_to_string(img, lang='spa+eng')
        price = extract_price_from_text(text)
        if price:
            return price, text
        # try with a binary threshold to catch more
        bw = img.point(lambda p: p > 180 and 255)
        text2 = pytesseract.image_to_string(bw, lang='spa+eng')
        price2 = extract_price_from_text(text2)
        if price2:
            return price2, text2
        # final fallback: try single-line digits config
        text3 = pytesseract.image_to_string(img, config='--psm 6 digits')
        price3 = extract_price_from_text(text3)
        if price3:
            return price3, text3
        return '', text
    except Exception as e:
        return '', ''


def main():
    if not os.path.isdir(IMAGES_DIR):
        print('No se encontró la carpeta "imagenes" en el proyecto. Asegúrate de ejecutar desde la carpeta del proyecto.')
        return
    files = [f for f in os.listdir(IMAGES_DIR) if os.path.isfile(os.path.join(IMAGES_DIR, f)) and f.lower() != 'logo.png']
    results = {}
    details = {}
    for f in files:
        print('Procesando', f)
        price, text = process_image_file(f)
        if price:
            print('  -> detectado:', price)
        else:
            print('  -> no detectado')
        results[f] = price
        details[f] = text
    # save JSON
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as fh:
        json.dump(results, fh, ensure_ascii=False, indent=2)
    # save JS that sets localStorage for the site (so the site can load prices automatically)
    # Escape JSON string for insertion in JS
    json_str = json.dumps(results, ensure_ascii=False)
    js_content = f"localStorage.setItem('savedPrices', JSON.stringify({json_str}));\nconsole.log('savedPrices loaded from saved_prices.js');\n"
    with open(OUTPUT_JS, 'w', encoding='utf-8') as fh:
        fh.write(js_content)
    print('\nResultados guardados en:')
    print(' -', OUTPUT_JSON)
    print(' -', OUTPUT_JS)
    print('\nRevisa los precios en el modal "Editar precios" dentro de la web y corrige en caso de errores.')


if __name__ == '__main__':
    main()
