from celery import shared_task, chain
import requests
import json
from datetime import datetime


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
        save_weather_data.apply_async((data,))
    except requests.exceptions.RequestException as exc:
        self.retry(exc=exc)


@shared_task(name='app.tasks.save_weather_data')
def save_weather_data(data):
    filename = "/app/data/weather_data.json"
    with open(filename, 'w') as json_file:
        json.dump(data, json_file)
    return filename  # Devolver la ruta del archivo JSON

