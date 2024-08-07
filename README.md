# Desafío San Jorge - Nelson Acosta

Este proyecto es una aplicación FastAPI con tareas de Celery y almacenamiento de resultados en Redis. La aplicación incluye endpoints para gestionar información sobre automóviles y extraer datos de una API de clima.

## Tecnologías utilizadas

- FastAPI
- Celery
- Redis
- Docker
- Docker Compose
- MySQL
- SQLAlchemy
- Pydantic

## Requisitos previos

Asegúrate de tener Docker y Docker Compose instalados en tu máquina.

- [Instalar Docker](https://docs.docker.com/get-docker/)
- [Instalar Docker Compose](https://docs.docker.com/compose/install/)

## Configuración

1. Clona este repositorio:

   ```sh
   git clone https://github.com/NelsonAcostaTuc/challenge_asj.git
   cd challenge_asj

2. Crea un archivo .env en la raíz del proyecto con el siguiente contenido:

    ```sh
        MYSQL_USER=your_username
        MYSQL_PASSWORD=your_password
        MYSQL_HOST=db
        MYSQL_PORT=3306
        MYSQL_DB=your_database_name

        CELERY_BROKER_URL=redis://redis:6379/0
        CELERY_RESULT_BACKEND=redis://redis:6379/0


3. Construye y levanta los contenedores de Docker:
```sh
    docker-compose up --build
    La aplicación estará disponible en http://localhost:8000.

    Endpoints
        GET /cars: Obtiene una lista de autos.

    Query Parameters:
        brand: Filtra por marca.
        subsidiaryName: Filtra por nombre de sucursal.

    POST /cars: Crea un nuevo auto.

    POST /fetch-weather: Inicia la tarea de extracción de datos de clima.

    
