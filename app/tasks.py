from celery import shared_task, chain
import requests
import json
from datetime import datetime
import logging


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


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
    except requests.exceptions.RequestException as exc:
        self.retry(exc=exc)



