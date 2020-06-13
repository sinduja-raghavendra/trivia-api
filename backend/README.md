# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
1. Create "trivia_user" with the command "createuser trivia_user"
2. Create a database with the command "createdb trivia"
3. If database already exist run "dropdb trivia && createdb trivia" to drop the database and recreate it
4. Run psql file with the command "psql trivia < trivia.psql"
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Backend server will be running at 
```
http://localhost:5000
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


## Endpoints
```
GET '/categories'
```
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category

Curl Syntax
```
curl http://localhost:5000/categories
```

- Request Arguments: None
- Returns: An object with a Success flag and list of categories, that contains a object of id: category_string key:value pairs. 
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```
**************
```
GET '/questions'
```
- Fetches a dictionary of categories and questions

Curl Syntax
```
curl  http://localhost:5000/questions
```

- Request Arguments: None
- Returns: 
``` 
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, ....
  ], 
  "success": true, 
  "total_questions": 58
}
```
**************
```
GET '/categories/<int:category_id>/questions'
```
- Fetches a dictionary of questions based on category

Curl Syntax
```
curl  http://localhost:5000/categories/1/questions
```

- Request Arguments: None
- Returns: 
``` 
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "Sports", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, ...
```
**************
```
POST '/questions'
```
- When Search term is present in the request it fetches all the questions that contains the search term as a substring

curl Syntax
```
curl -d '{"searchTerm":"Movie"}' -H "Content-Type: application/json" -X POST http://localhost:5000/questions
```

- Returns: 
```
{
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```
**************
```
POST '/questions'
```
- When the Request has Question, Answer, Difficulty and Category parameters, It creates a new question record in the database 

curl Syntax
```
curl -d '{"question": "What is H2O?", "answer": "Water", "difficulty": 1, "category": 1}' -H "Content-Type: application/json" -X POST http://localhost:5000/questions
```

- Returns: 
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, ...
  ], 
  "success": true, 
  "total_questions": 58
}
```
**************
```
POST '/quizzes'
```
- Fetches all the questions from the database based on the category provided in the request, Picks a random question based on the previous question id that is provided in the request. 

curl Syntax
```
curl -d '{"previous_questions": [37], "quiz_category": {"type": "Science", "id": "1"}}' -H "Content-Type: application/json" -X POST http://localhost:5000/quizzes
```

- Returns: 
```
{
  "question": {
    "answer": "1", 
    "category": 1, 
    "difficulty": 1, 
    "id": 48, 
    "question": "1"
  }, 
  "success": true
}
```
**************
```
DELETE '/questions/<int:question_id>'
```
- Deletes the question based on ID. 

curl Syntax
```
curl -X DELETE http://localhost:5000/questions/45
```

- Request Arguments: None
- Returns: 
```
{
  "question": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, ...
  ], 
  "deleted": 45, 
  "success": true, 
  "total_books": 56
}
```

## Testing
To run the tests,
```
1. Create "trivia_user" with the command "createuser trivia_user"
2. Create a database with the command "createdb trivia_test"
3. If database already exist run "dropdb trivia_test && createdb trivia_test" to drop the database and recreate it
4. Run psql file with the command "psql trivia_test < trivia.psql"
5. python test_flaskr.py
```