<div align="center">

# 📧 Asistente Automatizado de Emails con IA

**Demo interactiva de clasificación y respuesta asistida, acompañada por un prototipo backend en Python/OpenAI/IMAP.**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white)
![OpenAI API](https://img.shields.io/badge/OpenAI-API-412991?style=flat&logo=openai&logoColor=white)
![IMAP](https://img.shields.io/badge/Email-IMAP-EA4335?style=flat)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

[**🖥️ Abrir demo**](https://truquinio.github.io/Asistente-automatizado-de-Emails-con-IA/) ·
[**📂 Ver código**](https://github.com/truquinio/Asistente-automatizado-de-Emails-con-IA)

</div>

---

## Qué muestra el proyecto

El repositorio tiene dos partes diferenciadas:

1. **Dashboard demo** en HTML/CSS/JavaScript, publicado mediante GitHub Pages y alimentado con datos simulados.
2. **Prototipo Python** para recuperar correo no leído por IMAP, clasificar mensajes con la API de OpenAI y generar una respuesta propuesta.

La separación es deliberada: la demo puede explorarse sin credenciales ni acceso a una cuenta de correo.

## 📸 Capturas

| Bandeja | Clasificación + respuesta | Vista de enviados |
| --- | --- | --- |
| ![Bandeja de entrada](screenshots/01-bandeja.png) | ![Clasificación y respuesta generada](screenshots/02-clasificacion.png) | ![Pestaña de enviados](screenshots/03-enviados.png) |

## ✨ Capacidades verificables

- categorías de correo definidas para **soporte, ventas, consulta, spam y otros**;
- conexión IMAP configurada para SSL;
- recuperación de mensajes no leídos;
- clasificación mediante Chat Completions;
- generación de respuesta según categoría;
- respuesta fallback cuando falla la generación;
- límite de procesamiento configurable, acotado a un máximo de 50 en la configuración;
- demo frontend independiente del correo real.

## 🧱 Arquitectura

```text
Cuenta de correo
      │
      ▼
    IMAP
      │
      ▼
EmailProcessor
      │
      ├── clasificación ──► OpenAI API
      │
      └── respuesta ──────► OpenAI API
                               │
                               ▼
                     respuesta propuesta

GitHub Pages demo
└── HTML + CSS + JavaScript + datos simulados
```

## 🗂️ Estructura

```text
.
├── index.html
├── style.css
├── script.js
├── screenshots/
├── .env.example
├── requirements.txt
├── config.py
└── src/
    ├── demo/
    ├── real/
    │   └── processor.py
    └── utils/
        ├── email_parser.py
        └── response_generator.py
```

## ⚙️ Preparación del entorno

```bash
git clone https://github.com/truquinio/Asistente-automatizado-de-Emails-con-IA.git
cd Asistente-automatizado-de-Emails-con-IA
python -m venv venv
```

Linux/macOS:

```bash
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edita `.env` con credenciales propias y nunca lo subas al repositorio.

## ⚠️ Estado del backend

**Prototype / work in progress.**

Durante la revisión documental se detectó que el backend actual no está completamente alineado con su módulo de configuración: `src/real/processor.py` importa `Config`, mientras que `config.py` expone `Settings` y una instancia `config`.

Por ese motivo este README **no presenta el procesador real como listo para producción ni como flujo validado end-to-end**. La demo de GitHub Pages es independiente de ese desajuste.

## 🔐 Seguridad

- `.env.example` sirve como plantilla; no debe contener secretos reales.
- El acceso IMAP requiere credenciales propias.
- Las respuestas del modelo deben considerarse propuestas y revisarse antes de cualquier uso real.

## 📜 Licencia

[MIT](LICENSE)

---

**Federico Trucco / [@truquinio](https://github.com/truquinio)**
