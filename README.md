# CSV Processor

A Django-based CSV Processing Application that leverages Celery and Redis for asynchronous CSV file processing. The application allows users to upload CSV files, perform calculations (sum, average, count) on numeric columns, compute additional metrics, and dynamically search data by product name.

## Features

- **CSV Upload:** Upload CSV files via a user-friendly web interface.
- **Asynchronous Processing:** Process CSV files in the background using Celery and Redis.
- **In-Memory Calculations:** Compute sum, average, and count for numeric columns.
- **Additional Metrics:** Calculate total revenue, average discount, best-selling product, most profitable product, and product with maximum discount.
- **Dynamic Search:** Filter displayed CSV data by product name without reloading the page.

## Prerequisites

- **Python 3.8+**
- **Redis:** [Install Redis](https://redis.io/download) and ensure it's running.
- **Git:** To clone the repository.

## Getting Started

### 1. Clone the Repository

Clone the repository using SSH:

```
git clone git@github.com:kunalwagh101/csvprocessor.git
```

### Create a virtual environment

**For Linux and macOS**
```
    python3.8 -m venv venv
    source venv/bin/activate
```

**For Windows**
```
    pip install virtualenv
    python -m venv venv
    virtualenv venv
    venv/Scripts/activate
```

### Go inside the project folder

    cd  untill you see manage.py file 

- **Install the necessary modules**

```
    pip install -r requirements.txt
```
    
    

- **If it shows error, run**
```
    pip install django
```

- **Run the redis** - works on most systems
```
    redis-server
```

    

- **Run Celery**
```
    celery -A csvprocessor worker -l info
```

- **Run the application**
```
    python manage.py runserver
```

- **Open the below url on your browser**
```
    http://127.0.0.1:8000/
```

### You can also create a new super user with the following command and login with those credentials.
```
    python manage.py makemigration
    python manage.py migrate
    python manage.py createsuperuser
```
    