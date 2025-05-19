import email
from imapclient import IMAPClient
from openai import OpenAI
from loguru import logger
from typing import List, Dict, Optional
from datetime import datetime, timedelta

from config import Config, EmailCategory
from src.utils.email_parser import parse_email
from src.utils.response_generator import generate_response

class EmailProcessor:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.processed_count = 0
        self.categories = {cat.value: 0 for cat in EmailCategory}
    
    def connect_to_email_server(self) -> IMAPClient:
        """Establece conexión segura con el servidor IMAP"""
        try:
            server = IMAPClient(
                host=Config.IMAP_SERVER,
                port=Config.IMAP_PORT,
                ssl=True,
                timeout=30
            )
            server.login(Config.EMAIL_ACCOUNT, Config.EMAIL_PASSWORD)
            return server
        except Exception as e:
            logger.error(f"Error de conexión IMAP: {str(e)}")
            raise

    def fetch_unread_emails(self, limit: int = Config.DEFAULT_LIMIT) -> List[Dict]:
        """Obtiene emails no leídos del servidor"""
        emails = []
        try:
            with self.connect_to_email_server() as server:
                server.select_folder(Config.DEFAULT_FOLDER)
                messages = server.search(["UNSEEN"])[:limit]
                
                for msg_id, data in server.fetch(messages, ["RFC822"]).items():
                    raw_email = data[b"RFC822"]
                    parsed_email = parse_email(raw_email)
                    emails.append(parsed_email)
                    
        except Exception as e:
            logger.error(f"Error al obtener emails: {str(e)}")
        
        return emails

    def process_single_email(self, email_data: Dict) -> Optional[Dict]:
        """Procesa un email individual con OpenAI"""
        try:
            # Clasificar el email
            classification_prompt = (
                f"Clasifica este email en una de estas categorías: {[cat.value for cat in EmailCategory]}\n\n"
                f"Asunto: {email_data['subject']}\n"
                f"Contenido: {email_data['body'][:1000]}\n"
                "Respuesta solo con la categoría:"
            )
            
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[{"role": "user", "content": classification_prompt}],
                temperature=0.3,
                max_tokens=10
            )
            
            category = response.choices[0].message.content.strip().lower()
            if category not in [cat.value for cat in EmailCategory]:
                category = EmailCategory.OTHER.value
            
            self.categories[category] += 1
            
            # Generar respuesta
            response_text = generate_response(
                email_data['body'],
                category,
                self.client,
                Config.OPENAI_MODEL
            )
            
            return {
                'id': email_data['id'],
                'from': email_data['from'],
                'subject': email_data['subject'],
                'category': category,
                'response': response_text,
                'processed_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error al procesar email: {str(e)}")
            return None

def process_emails(limit: int = Config.DEFAULT_LIMIT) -> Dict:
    """Función principal para procesar lotes de emails"""
    processor = EmailProcessor()
    emails = processor.fetch_unread_emails(limit)
    results = []
    
    for email_data in emails:
        result = processor.process_single_email(email_data)
        if result:
            results.append(result)
            processor.processed_count += 1
    
    return {
        'total_processed': processor.processed_count,
        'categories': processor.categories,
        'emails': results,
        'timestamp': datetime.now().isoformat()
    }

if __name__ == "__main__":
    logger.info("Iniciando procesamiento de emails...")
    results = process_emails()
    logger.info(f"Procesamiento completado. Resultados: {results}")