# backend/status_checker.py
import requests
import json
from pathlib import Path
import re
import socket
from urllib.parse import urlparse

def is_resolvable(url):
    try:
        domain = urlparse(url).netloc
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False
    
    
# ✅ Detecta sitios que estén activos pero devuelvan HTML de error
def check_url_status(url):
    if not is_resolvable(url):
        return {"url": url, "status": "unresolvable"}
    
    try:
        response = requests.get(url, timeout=8)
        html = response.text.lower()

        # Palabras clave específicas que indican posible inactividad
        offline_keywords = [
            r"\bsitio en mantenimiento\b",
            r"\ben mantenimiento\b",
            r"\bfuera de servicio\b",
            r"\bpágina no encontrada\b",
            r"\bunder maintenance\b",
            r"\btemporarily unavailable\b",
            r"\btemporalmente fuera\b",
            r"\bservice unavailable\b",
            r"\bmaintenance\b"
        ]

        if response.status_code == 200:
            for pattern in offline_keywords:
                if re.search(pattern, html):
                    return {
                        "url": url,
                        "status": "inactive (HTML match)",
                        "matched": pattern  # solo para debug, podés quitarlo
                    }
            return {"url": url, "status": 200}
        else:
            return {"url": url, "status": response.status_code}
    except Exception:
        return {"url": url, "status": "offline"}

# ✅ Llama a la función inteligente para cada URL
def check_status(urls):
    status_list = []
    for url in urls:
        result = check_url_status(url)
        status_list.append(result)
    return status_list

# ✅ Carga el archivo urls.txt desde ruta absoluta
def load_urls(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return []

# ✅ Guarda el resultado
def save_status(status, output_file):
    with open(output_file, 'w') as f:
        json.dump(status, f, indent=2)

# ✅ Punto de entrada
def main():
    urls_file = Path(__file__).resolve().parent / 'urls.txt'
    output_file = Path(__file__).resolve().parent / 'status.json'

    urls = load_urls(urls_file)
    status = check_status(urls)
    save_status(status, output_file)

if __name__ == '__main__':
    main()
    
    

