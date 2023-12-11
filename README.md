
# Recipes API

A simple API to manage recipes


## Stack used

**Back-end:** [Python](https://www.python.org/), [Django](https://www.djangoproject.com/), [Django-Rest-Framework](https://www.django-rest-framework.org/)


## Installation

1. Ensure [Python](https://www.python.org/downloads/) is installed. You can download it from the official Python website: https://www.python.org/downloads/
2. Clone the repository by executing the following command:
```bash
git clone https://github.com/ViniciusMeireles/recipe_api.git
```
3. Navigate to the project directory:
```bash
cd recipe_api
```
4. Create a virtualenv:
* Linux
```bash
python -m pip install virtualenv
python -m venv venv
source venv/bin/activate
```
* Windows
```bash
python -m pip install virtualenv
python -m venv venv
.\venv\Scripts\activate
```
5. Install the required packages:
```bash
pip install -r requirements.txt
```
6. Configure the database:
```bash
python manage.py makemigrations
python manage.py migrate
```
7. Create a superuser account:
```bash
python manage.py createsuperuser
```
8. Run the development server:
```bash
python manage.py runserver 8000
```

## Access

Now that everything is installed and configured, click the link below or enter the URL in your browser.

http://127.0.0.1:8000/


## API Documentation 
[![documentation](https://img.shields.io/badge/Documentation-blue)](http://127.0.0.1:8000/api/schema/swagger-ui/#/)

To explore the complete API documentation, please visit [http://127.0.0.1:8000/api/schema/swagger-ui/#/](http://127.0.0.1:8000/api/schema/swagger-ui/#/). This page provides details on endpoints, parameters, and allows you to interactively test various features offered by the API.

Make sure you have the server running locally to access the documentation.

