# 📧 Asistente Automatizado de Emails con IA

![Banner del Proyecto](image.png)  
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT-4-12990.svg)
![IMAP](https://img.shields.io/badge/Protocol-IMAP-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Sistema automatizado que clasifica y responde correos electrónicos utilizando inteligencia artificial. Ideal para gestionar consultas, soporte técnico o ventas. Este es un proyecto personal orientado a optimizar la administración de bandejas de entrada.

---

## 🚀 Características Principales

- ✨ **Clasificación inteligente** de correos (consulta, soporte, ventas, spam)
- 🤖 **Generación de respuestas** con GPT-3.5-turbo o GPT-4
- 🔒 Conexión segura vía **IMAP con SSL** (compatible con Gmail, Outlook, Exchange)
- 📊 **Dashboard de métricas en tiempo real**
- 🧪 **Modo demo** incluido para pruebas sin conexión
- ⚡ **Procesamiento rápido** (hasta 50 correos por ejecución)
- 📁 **Soporte multi-carpeta** (INBOX, Important, etc.)
- 🔄 **Reintentos automáticos** ante errores de conexión

---

## ⚙️ Configuración Rápida

```bash
# Clonar el repositorio
git clone https://github.com/tuusuario/Asistente-Automatizado-de-Emails-con-IA.git
cd Asistente-Automatizado-de-Emails-con-IA

# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate      # En Linux/Mac
.\venv\Scripts\activate       # En Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Edita el archivo .env con tus credenciales



## 🔍 Diagrama de Flujo
sequenceDiagram
    participant Sistema
    participant Gmail
    participant OpenAI

    Sistema->>Gmail: Conexión IMAP segura
    Gmail-->>Sistema: Obtener correos no leídos
    Sistema->>OpenAI: Clasificar correo
    OpenAI-->>Sistema: Categoría (consulta, soporte, ventas)
    Sistema->>OpenAI: Generar respuesta
    OpenAI-->>Sistema: Texto de respuesta
    Sistema->>Gmail: Marcar correo como leído


## 🛠️ Uso avanzado
# Procesar 5 correos
python src/real/processor.py --limit 5

# Procesar una carpeta específica
python src/real/processor.py --folder "INBOX/Important"

# Ejecutar en modo verbose (depuración)
python src/real/processor.py --verbose

# Ejecutar versión demo con retardo simulado
python src/demo/processor_demo.py --simulate-delay



## 🏗️ Estructura del Proyecto
Asistente-Automatizado-de-Emails-con-IA/
├── .env.example
├── requirements.txt
├── config.py
└── src/
    ├── demo/               # Modo simulado para pruebas
    │   ├── __init__.py
    │   └── processor_demo.py
    ├── real/               # Implementación funcional
    │   ├── __init__.py
    │   └── processor.py
    └── utils/              # Funciones auxiliares
        ├── email_parser.py
        └── response_generator.py



## 🤝 ¿Cómo contribuir?
- Haz fork del proyecto.
- Crea una rama: `git checkout -b feature/mi-mejora`
- Realiza tus cambios y haz commit: `git commit -am 'Agrega nueva funcionalidad'`
- Sube la rama: `git push origin feature/mi-mejora`
- Abre un Pull Request.

**Recomendaciones:**
- Documenta nuevas funcionalidades.
- Mantén cobertura de pruebas >90%.
- Sigue el estilo de código PEP8.

## 📜 Licencia
Este proyecto está licenciado bajo la [Licencia MIT](LICENSE.md).