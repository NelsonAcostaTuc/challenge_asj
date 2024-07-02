from celery import Celery
import os
from celery.schedules import crontab
from datetime import timedelta

# Cargar variables de entorno desde el archivo .env
from dotenv import load_dotenv
load_dotenv()

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')

celery_app = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],  
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    beat_schedule={
        'fetch-weather-every-5-seconds': {
            'task': 'app.tasks.fetch_weather_data',
            'schedule': 5.0,  # Ejecuta cada 5 segundos
        },
    },
)

# Importar tareas para asegurarse de que están registradas
import app.tasks
