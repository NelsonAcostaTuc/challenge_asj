from celery import shared_task, chain
import requests
import json
from datetime import datetime
import logging


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

"""
Extracto del ejercicio: Desarrollar un **conjunto** de tareas

Es decir, se requería mas de una task, siendo la primera la encargada de recolectar los datos de la API
y la segunda, tomando los datos recolectados por la primera, almacenar dichos datos en un archivo .json. 

"""

@shared_task(bind=True, max_retries=3, default_retry_delay=5, name='app.tasks.fetch_weather_data')
def fetch_weather_data(self):
    try:
        response = requests.get('https://api.open-meteo.com/v1/forecast', params={
            'latitude': 35.6895,
            'longitude': 139.6917,
            'current_weather': 'true'
        }, timeout=5)
        response.raise_for_status()
        data = response.json()
        # Encadenar la tarea de guardar datos después de la de extracción
        logger.info(f'Retrieved cars: {data}')
        filename = "/app/data/weather_data.json"
        with open(filename, 'w') as json_file:
            json.dump(data, json_file)

    # Este manejo de exceptions no toma en cuenta qué podría suceder si el usuario del SO que 
    # está ejecutando el archivo tiene acceso de esctritura al path indicado. 
    # Dado ese caso, la función json.dump fallará y ésta tarea no dará ninguna información al respecto sobre su fallo. 
    # En general, una buena práctica para lidiar con Exceptions es declarar exceptions custom de manera tal que cada tarea pueda raisear solamente esas exceptions. 
    except requests.exceptions.RequestException as exc:
        self.retry(exc=exc)



