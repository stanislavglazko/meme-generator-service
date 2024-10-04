# Meme Generator API

This project is a Meme Generator API that allows users to create, view, 
and rate memes based on predefined templates. 
Users can interact with the service through a set of RESTful API endpoints 
to create their own memes, retrieve a list of memes, rate them, 
and get a random or top-rated meme. 
Meme templates can be managed via the Django Admin Panel.

## Features
- Create memes using predefined templates.
- View and retrieve specific memes.
- Rate memes (from 1 to 5).
- Get a random meme.
- Retrieve the top 10 memes based on average rating.
- Manage meme templates via the admin panel.

## API Endpoints

- **GET** `/api/templates/`: List all meme templates.
- **GET** `/api/memes/`: List all memes (with pagination).
- **POST** `/api/memes/`: Create a new meme.
- **GET** `/api/memes/<id>/`: Retrieve a specific meme by ID.
- **POST** `/api/memes/<id>/rate/`: Rate a meme (1 to 5). If the user has already rated it, the rating is updated.
- **GET** `/api/memes/random/`: Get a random meme.
- **GET** `/api/memes/top/`: Get the top 10 rated memes based on the average rating.

## Running the Project

To set up and run the project locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone <repository-url>
    ```

2. Create a `.env` file and provide necessary environment variables such as `DJANGO_SECRET_KEY`.

3. Build and initialize the Docker containers and apply the migrations by running:
    ```bash
    make init
    ```

4. You can now access the API at `http://localhost:8000` and the admin panel at `http://localhost:8000/admin`.

5. To add meme templates, use the Django Admin panel.

## Requirements

- Python 3.10
- Django 4.2
- PostgreSQL
- Docker and Docker-Compose

## How to contribute

Feel free to open an issue or submit a pull request if you have suggestions or improvements.
