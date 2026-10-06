from datetime import datetime
from typing import Dict, List, Optional

from imapclient import IMAPClient
from loguru import logger
from openai import OpenAI

from config import EmailCategory, config
from src.utils.email_parser import parse_email
from src.utils.response_generator import generate_response


class EmailProcessor:
    def __init__(self, client=None):
        self.client = client or OpenAI(
            api_key=config.OPENAI_API_KEY,
            timeout=config.OPENAI_TIMEOUT,
        )
        self.processed_count = 0
        self.categories = {cat.value: 0 for cat in EmailCategory}

    def connect_to_email_server(self) -> IMAPClient:
        try:
            server = IMAPClient(
                host=config.IMAP_SERVER,
                port=config.IMAP_PORT,
                ssl=True,
                timeout=config.OPENAI_TIMEOUT,
            )
            server.login(config.EMAIL_ACCOUNT, config.EMAIL_PASSWORD)
            return server
        except Exception as exc:
            logger.error(f"Error de conexión IMAP: {exc}")
            raise

    def fetch_unread_emails(self, limit: Optional[int] = None) -> List[Dict]:
        limit = config.PROCESSING_LIMIT if limit is None else limit
        folder = config.EMAIL_FOLDERS[0] if config.EMAIL_FOLDERS else "INBOX"
        emails = []
        try:
            with self.connect_to_email_server() as server:
                server.select_folder(folder)
                messages = server.search(["UNSEEN"])[:limit]
                if not messages:
                    return emails
                for _, data in server.fetch(messages, ["RFC822"]).items():
                    emails.append(parse_email(data[b"RFC822"]))
        except Exception as exc:
            logger.error(f"Error al obtener emails: {exc}")
        return emails

    def process_single_email(self, email_data: Dict) -> Optional[Dict]:
        try:
            classification_prompt = (
                f"Clasifica este email en una de estas categorías: "
                f"{[cat.value for cat in EmailCategory]}\n\n"
                f"Asunto: {email_data['subject']}\n"
                f"Contenido: {email_data['body'][:1000]}\n"
                "Respuesta solo con la categoría:"
            )
            response = self.client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[{"role": "user", "content": classification_prompt}],
                temperature=0.3,
                max_tokens=10,
            )
            category = response.choices[0].message.content.strip().lower()
            if category not in [cat.value for cat in EmailCategory]:
                category = EmailCategory.OTHER.value
            self.categories[category] += 1

            response_text = generate_response(
                email_data["body"],
                category,
                self.client,
                config.OPENAI_MODEL,
            )
            return {
                "id": email_data["id"],
                "from": email_data["from"],
                "subject": email_data["subject"],
                "category": category,
                "response": response_text,
                "processed_at": datetime.now().isoformat(),
            }
        except Exception as exc:
            logger.error(f"Error al procesar email: {exc}")
            return None


def process_emails(limit: Optional[int] = None) -> Dict:
    processor = EmailProcessor()
    emails = processor.fetch_unread_emails(limit)
    results = []

    for email_data in emails:
        result = processor.process_single_email(email_data)
        if result:
            results.append(result)
            processor.processed_count += 1

    return {
        "total_processed": processor.processed_count,
        "categories": processor.categories,
        "emails": results,
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    logger.info("Iniciando procesamiento de emails...")
    results = process_emails()
    logger.info(f"Procesamiento completado. Resultados: {results}")
