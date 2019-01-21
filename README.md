# Hello Flask Restful API
---
A simple Restful API, implemented using Flask a microframework for Python based on Werkzeug. 

It showcases the classic programming "Hello World" in different languages.

# Design
---
The design is implemented leveraging SQLAlchemy ORM(Object Relational Mapper) with a SQLite DB Back-End which holds the data fetched by the API. The implementation supports CRUD(Create, Read, Update, Delete) Operations by using the HTTP verbs/methods.

Self URIs are returned with the data which helps a developer consuming the API with the discovery of other resources provided. 

# How to Run Tool
---

**Prerequisites**:

- BackEnd Database:
- SQLite
Flask and a number of extensions

Step 0:
### Install Flask and extensions
Run the following within the project's root folder:

**Command Line run:**

```pip install -r requirements.txt```

Step 1:
### Create Database Schema:
Run the following within the project's root folder:

**Command Line run:**
```python api.py --setup```
>Note: There is an exisitng database "greetings" with sample data within the project;s root folder. So only run the above command if you want to start with a clean fresh database.

Step 2:

- The Hello Flask RESTful API:

Run the following within the project's root folder:

**Command Line run:**
```python api.py```

This is set to run by default at the **following Address: http://localhost:8000**


## How to consume the API:
---
You can use the curl command or httpie, which can be installed by:

**Command Line run:**
```pip install httpie```

### Example of using the API to execute CRUD Operations:

- **POST - Create a Message in English:**

>By specifying the language "english" and message below the API will create "Hello World" in "english". 

```http --ignore-stdin POST http://localhost:8000/api/v1/greetings language=english message="Hello World"```

- **GET - Fetch a message in English:**

>By specifying the language "english" below the API will fetch the message "Hello World"

```http http://localhost:8000/api/v1/greetings/english```

- **PUT - Edit a message in English:**

>By specifying the language "english" and message below the API will edit/update the language and message

```http --ignore-stdin PUT http://localhost:8000/api/v1/greetings/english language=english message="Hello Worldsss"```

- **DELETE - Delete a message in English:**

>By specifying the language "english" below the API will delete the english greeting with a message "Hello World"

```http --ignore-stdin DELETE http://localhost:8000/api/v1/greetings/english```

### Sample data return of a Greetings Collection in a plethora of languages:
```{
    "greetings": [
        {
            "id": 1,
            "language": "english",
            "message": "Hello World",
            "self_uri": "/api/v1/greetings/english"
        },
        {
            "id": 2,
            "language": "french",
            "message": "Bonjour le monde",
            "self_uri": "/api/v1/greetings/french"
        },
        {
            "id": 3,
            "language": "spanish",
            "message": "Hola Mundo",
            "self_uri": "/api/v1/greetings/spanish"
        },
        {
            "id": 4,
            "language": "yoruba",
            "message": "Mo ki O Ile Aiye",
            "self_uri": "/api/v1/greetings/yoruba"
        },
        {
            "id": 5,
            "language": "swahili",
            "message": "Salamu, Dunia",
            "self_uri": "/api/v1/greetings/swahili"
        }
    ]
}```