from config import EmailCategory, config
from openai import OpenAI


def generate_response(email_body: str, category: str, client: OpenAI, model: str) -> str:
    try:
        prompt = build_response_template(email_body, category)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=config.OPENAI_TEMPERATURE,
            max_tokens=config.OPENAI_MAX_TOKENS,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        print(f"Error generando respuesta: {exc}")
        return build_fallback_response(category)


def build_response_template(email_body: str, category: str) -> str:
    base_prompt = (
        "Eres un asistente automatizado de respuestas por email. "
        "Genera una respuesta profesional y adecuada en español. "
        f"El email recibido es clasificado como '{category}'. "
        "El contenido del email es:\n\n"
        f"{email_body[:2000]}\n\n"
        "Incluye saludo, reconocimiento del tema, siguiente paso, despedida y firma.\n\n"
        "Respuesta:"
    )
    category_specific = {
        EmailCategory.SUPPORT.value: (
            "El cliente reporta un problema. Explica los próximos pasos y evita prometer "
            "plazos que no estén confirmados."
        ),
        EmailCategory.SALES.value: (
            "Es una consulta comercial. Responde con claridad y propone un siguiente paso."
        ),
        EmailCategory.INQUIRY.value: (
            "Es una consulta general. Proporciona información clara y ofrece ayuda adicional."
        ),
    }
    return base_prompt + "\n" + category_specific.get(category, "")


def build_fallback_response(category: str) -> str:
    responses = {
        EmailCategory.SUPPORT.value: (
            "Estimado cliente,\n\nHemos recibido su solicitud de soporte. "
            "Nuestro equipo la revisará.\n\nAtentamente,\nEl equipo de soporte"
        ),
        EmailCategory.SALES.value: (
            "Estimado/a,\n\nGracias por su interés. Revisaremos su consulta y "
            "continuaremos la conversación.\n\nCordialmente,\nEl equipo comercial"
        ),
        EmailCategory.INQUIRY.value: (
            "Estimado/a,\n\nHemos recibido su consulta y la revisaremos.\n\n"
            "Atentamente,\nEl equipo de atención al cliente"
        ),
    }
    return responses.get(
        category,
        "Hemos recibido su mensaje. Lo revisaremos.\n\n"
        "Atentamente,\nEl equipo de atención al cliente",
    )
