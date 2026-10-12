# Aula IA — Tutor virtual inteligente

Proyecto 2 de la lección LLM: una aplicación local para aprender inteligencia artificial con la API de OpenAI. Explica conceptos, genera ejercicios, revisa respuestas y propone planes de estudio según el nivel del estudiante.

## Funcionalidades

- Cuatro modos: Explícame, Quiero practicar, Revisa mi respuesta y Organiza mi estudio.
- Niveles principiante, intermedio y avanzado.
- Conversación con contexto de los últimos cuatro intercambios.
- Ejemplos iniciales sobre aprendizaje automático, recomendadores y LLM.
- Reinicio de conversación, indicador de espera y mensajes claros ante errores.
- Interfaz adaptable a teléfonos y computadoras, sin recursos externos.

## Requisitos

Python 3.10 o superior, conexión a internet y una clave de API de OpenAI con acceso al modelo configurado y saldo o cuota disponible. Las llamadas a la API pueden generar cargos; una suscripción a ChatGPT no configura la API de este proyecto.

## Instalar y ejecutar en Windows

Abre una terminal en la carpeta donde quieras guardar el proyecto:

```powershell
git clone https://github.com/PM-O-SD/llm.git
cd llm
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Abre `.env` en tu editor y completa la clave **solo en tu computadora**:

```dotenv
OPENAI_API_KEY=tu_clave_personal
OPENAI_MODEL=gpt-4.1-mini
```

Obtén tu clave desde [la plataforma de OpenAI](https://platform.openai.com/api-keys). No la publiques en GitHub ni la pegues en capturas. Puedes cambiar `OPENAI_MODEL` por un modelo compatible con Responses API al que tenga acceso tu cuenta.

Inicia el tutor desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -m tutor_virtual.app
```

Abre **http://127.0.0.1:8000** en tu navegador. El servidor se cierra con Ctrl+C. Si el puerto está ocupado, ejecuta `python -m tutor_virtual.app --port 8001` usando el Python de tu entorno virtual.

## Instalar y ejecutar en macOS o Linux

```bash
git clone https://github.com/PM-O-SD/llm.git
cd llm
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
# Edita .env y configura OPENAI_API_KEY antes de continuar.
.venv/bin/python -m tutor_virtual.app
```

## Recorrido de demostración

1. Selecciona Principiante y Explícame. Consulta: «¿Qué diferencia hay entre aprendizaje supervisado y no supervisado?».
2. Cambia a Quiero practicar y pide tres ejercicios sobre ese tema.
3. Intenta responder uno; cambia a Revisa mi respuesta y pega tu intento para recibir orientación.
4. Cambia a Organiza mi estudio y pide un plan de una semana para estudiar recomendadores, con 30 minutos diarios.
5. Pulsa Nueva conversación para borrar el contexto local.

Las respuestas son generadas por OpenAI; no hay respuestas prefabricadas ni modo de simulación en la aplicación. Sin clave puedes abrir la interfaz, pero las consultas mostrarán el aviso de configuración pendiente.

## Diseño e integración

`tutor_virtual/app.py` sirve la interfaz y recibe consultas en el servidor local. `tutor_virtual/tutor.py` valida los datos, adapta las instrucciones educativas y llama a `client.responses.create`. La clave permanece en el servidor. `tutor_virtual/static/` contiene la interfaz HTML, CSS y JavaScript.

La conversación se mantiene en memoria de la pestaña; al recargar se borra. Se envían la pregunta y hasta ocho mensajes previos a OpenAI para generar cada respuesta. Se usa `store=False`, lo que desactiva el almacenamiento de respuestas para recuperación mediante la API; no implica ausencia de todos los registros del proveedor. No se guardan conversaciones en archivos.

## Pruebas

Desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Las pruebas usan respuestas y errores simulados de la API; no requieren clave ni generan cargos. Comprueban validación, instrucciones por modo, contexto, errores, integración con el SDK mediante un transporte simulado y rutas HTTP.

Para verificar el servicio real, configura tu clave y ejecuta el recorrido de demostración. Las pruebas automáticas no certifican la calidad pedagógica de las respuestas ni el acceso de tu cuenta al modelo.

## Límites y mejoras

El tutor puede cometer errores y no consulta fuentes externas. No tiene cuentas, seguimiento persistente, integración con plataformas educativas ni documentos propios del curso. Es una aplicación para uso local y un estudiante por instancia; el servidor de desarrollo no está pensado para publicación en internet.

Como mejoras se proponen recuperación de material del curso, evaluación con preguntas de referencia y seguimiento del aprendizaje con consentimiento del usuario.

## Repositorio de origen

Este proyecto se entrega en un fork de [mendiolaleonel2002-debug/llm](https://github.com/mendiolaleonel2002-debug/llm). Se conserva la licencia y la carpeta `asistente_escritura/` del repositorio base. Esa carpeta usa Gemini y corresponde al ejemplo original; la entrega seleccionada es el tutor con OpenAI. La documentación original se conserva en `README_BASE.md`.

Documentación consultada: [Responses API y generación de texto](https://developers.openai.com/api/docs/guides/text?lang=python), [modelo GPT-4.1 mini](https://developers.openai.com/api/docs/models/gpt-4.1-mini).
