import email
from email.header import decode_header
from bs4 import BeautifulSoup
from typing import Dict, Optional
import re

def parse_email(raw_email: bytes) -> Dict:
    """Parsea un email en formato raw a un diccionario estructurado"""
    msg = email.message_from_bytes(raw_email)
    
    # Decodificar asunto
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or "utf-8", errors="replace")
    
    # Decodificar remitente
    from_, encoding = decode_header(msg.get("From"))[0]
    if isinstance(from_, bytes):
        from_ = from_.decode(encoding or "utf-8", errors="replace")
    
    # Extraer dirección de email del remitente
    from_email = re.search(r'<(.+?)>', from_)
    if from_email:
        from_email = from_email.group(1)
    else:
        from_email = from_.strip()
    
    # Procesar cuerpo del email
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                body = part.get_payload(decode=True).decode(
                    part.get_content_charset() or "utf-8", 
                    errors="replace"
                )
                break
            elif content_type == "text/html":
                html_body = part.get_payload(decode=True).decode(
                    part.get_content_charset() or "utf-8", 
                    errors="replace"
                )
                body = extract_text_from_html(html_body)
                break
    else:
        body = msg.get_payload(decode=True).decode(
            msg.get_content_charset() or "utf-8", 
            errors="replace"
        )
        if msg.get_content_type() == "text/html":
            body = extract_text_from_html(body)
    
    return {
        "id": msg["Message-ID"],
        "from": from_email,
        "subject": subject,
        "body": body.strip(),
        "date": msg["Date"],
        "content_type": msg.get_content_type()
    }

def extract_text_from_html(html: str) -> str:
    """Extrae texto legible de contenido HTML"""
    soup = BeautifulSoup(html, "html.parser")
    
    # Eliminar scripts y estilos
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Obtener texto
    text = soup.get_text(separator="\n", strip=True)
    
    # Limpiar múltiples saltos de línea
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    return text