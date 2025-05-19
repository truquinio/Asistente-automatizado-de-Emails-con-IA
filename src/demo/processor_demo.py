from typing import List, Dict, Optional
from datetime import datetime
from loguru import logger
from random import choice
from time import sleep

from config import EmailCategory, Config

class DemoEmailProcessor:
    """Simulador completo del procesador de emails para entornos de prueba"""
    
    DEMO_EMAILS = [
        {
            "id": 1,
            "from": "cliente@empresa.com",
            "subject": "Problema con mi pedido reciente",
            "body": "Hola, tengo un problema con el pedido #12345 que hice la semana pasada. "
                    "El producto llegó dañado. ¿Cómo puedo solicitar un reemplazo?",
            "date": "2023-05-15T10:30:00"
        },
        {
            "id": 2,
            "from": "prospecto@otraempresa.com",
            "subject": "Consulta sobre sus servicios",
            "body": "Buen día, estoy interesado en sus servicios empresariales. "
                    "¿Podrían enviarme información sobre sus planes y precios?",
            "date": "2023-05-15T11:45:00"
        },
        {
            "id": 3,
            "from": "soporte@terceros.com",
            "subject": "Colaboración entre empresas",
            "body": "Nos gustaría explorar oportunidades de colaboración. "
                    "¿Estarían disponibles para una reunión la próxima semana?",
            "date": "2023-05-16T09:15:00"
        }
    ]
    
    def __init__(self):
        self.processed_count = 0
        self.categories = {cat.value: 0 for cat in EmailCategory}
    
    def fetch_unread_emails(self, limit: int = 3) -> List[Dict]:
        """Simula la obtención de emails no leídos"""
        sleep(1)  # Simular retardo de red
        return self.DEMO_EMAILS[:limit]
    
    def process_single_email(self, email_data: Dict) -> Optional[Dict]:
        """Simula el procesamiento de un email con IA"""
        try:
            sleep(0.5)  # Simular tiempo de procesamiento
            
            # Simular clasificación
            if "problema" in email_data["body"].lower() or "dañado" in email_data["body"].lower():
                category = EmailCategory.SUPPORT.value
            elif "consulta" in email_data["subject"].lower() or "información" in email_data["body"].lower():
                category = EmailCategory.INQUIRY.value
            elif "colaboración" in email_data["body"].lower() or "reunión" in email_data["body"].lower():
                category = EmailCategory.SALES.value
            else:
                category = EmailCategory.OTHER.value
            
            self.categories[category] += 1
            
            # Simular generación de respuesta
            responses = {
                EmailCategory.SUPPORT.value: (
                    f"Estimado cliente,\n\n"
                    f"Hemos recibido su reporte sobre '{email_data['subject']}'. "
                    f"Nuestro equipo de soporte se contactará con usted en las próximas 24 horas.\n\n"
                    f"Atentamente,\nEl equipo de soporte"
                ),
                EmailCategory.INQUIRY.value: (
                    f"Gracias por su interés en nuestros servicios.\n\n"
                    f"Hemos recibido su consulta sobre '{email_data['subject']}'. "
                    f"Adjunto encontrará información detallada sobre nuestros productos.\n\n"
                    f"Quedamos atentos a sus comentarios.\n\n"
                    f"Cordialmente,\nEl equipo comercial"
                ),
                EmailCategory.SALES.value: (
                    f"Estimado/a,\n\n"
                    f"Agradecemos su interés en colaborar con nosotros. "
                    f"Nos encantaría programar una reunión para discutir oportunidades. "
                    f"¿Estaría disponible el próximo miércoles a las 2pm?\n\n"
                    f"Saludos cordiales,\nEl equipo de alianzas"
                ),
                EmailCategory.OTHER.value: (
                    f"Hemos recibido su mensaje con asunto: '{email_data['subject']}'.\n\n"
                    f"Nos pondremos en contacto con usted pronto.\n\n"
                    f"Atentamente,\nEl equipo de atención al cliente"
                )
            }
            
            return {
                'id': email_data['id'],
                'from': email_data['from'],
                'subject': email_data['subject'],
                'category': category,
                'response': responses[category],
                'processed_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error en procesamiento simulado: {str(e)}")
            return None

def demo_process_emails(limit: int = 3) -> Dict:
    """Función principal para la demo"""
    processor = DemoEmailProcessor()
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
        'timestamp': datetime.now().isoformat(),
        'note': 'ESTOS SON RESULTADOS DE DEMOSTRACIÓN - NO SE PROCESARON EMAILS REALES'
    }

if __name__ == "__main__":
    logger.info("Iniciando DEMO de procesamiento de emails...")
    results = demo_process_emails()
    logger.info(f"Procesamiento completado. Resultados:\n{results}")