from typing import Dict, Optional
from config import Config, EmailCategory
from openai import OpenAI

client = OpenAI(api_key=Config.OPENAI_API_KEY)

def generate_response(email_body: str, category: str, client: OpenAI, model: str) -> str:
    """Genera una respuesta adecuada según la categoría del email"""
    try:
        prompt = build_response_template(email_body, category)
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=Config.OPENAI_TEMPERATURE,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generando respuesta: {str(e)}")
        return build_fallback_response(category)

def build_response_template(email_body: str, category: str) -> str:
    """Construye el prompt adecuado para cada tipo de respuesta"""
    base_prompt = (
        "Eres un asistente automatizado de respuestas por email. "
        "Genera una respuesta profesional y adecuada en español. "
        f"El email recibido es clasificado como '{category}'. "
        "El contenido del email es:\n\n"
        f"{email_body[:2000]}\n\n"
        "Por favor genera una respuesta adecuada que incluya:\n"
        "- Saludo personalizado\n"
        "- Reconocimiento del tema\n"
        "- Solución o siguiente paso\n"
        "- Despedida cordial\n"
        "- Nombre del equipo/firma\n\n"
        "Respuesta:"
    )
    
    category_specific = {
        EmailCategory.SUPPORT.value: (
            "El cliente está reportando un problema. "
            "Ofrece disculpas si corresponde, explica los próximos pasos "
            "y asegura que el equipo de soporte se contactará pronto."
        ),
        EmailCategory.SALES.value: (
            "Es una consulta comercial. Responde de manera persuasiva, "
            "destaca los beneficios y ofrece continuar la conversación."
        ),
        EmailCategory.INQUIRY.value: (
            "Es una consulta general. Proporciona información clara y concisa, "
            "y ofrece ayuda adicional si es necesario."
        )
    }
    
    return base_prompt + "\n" + category_specific.get(category, "")

def build_fallback_response(category: str) -> str:
    """Respuesta predeterminada en caso de error"""
    responses = {
        EmailCategory.SUPPORT.value: (
            "Estimado cliente,\n\n"
            "Hemos recibido su solicitud de soporte. "
            "Nuestro equipo se contactará con usted pronto.\n\n"
            "Atentamente,\nEl equipo de soporte"
        ),
        EmailCategory.SALES.value: (
            "Estimado/a,\n\n"
            "Gracias por su interés en nuestros productos. "
            "Pronto nos comunicaremos con usted.\n\n"
            "Cordialmente,\nEl equipo comercial"
        ),
        EmailCategory.INQUIRY.value: (
            "Estimado/a,\n\n"
            "Hemos recibido su consulta y le responderemos a la brevedad.\n\n"
            "Atentamente,\nEl equipo de atención al cliente"
        )
    }
    return responses.get(category, 
        "Hemos recibido su mensaje. Nos pondremos en contacto pronto.\n\n"
        "Atentamente,\nEl equipo de atención al cliente"
    )