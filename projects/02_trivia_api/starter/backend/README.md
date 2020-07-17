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
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
Endpoints
GET '/api/categories'
GET '/api/questions'
GET '/api/categories/<category_id>/questions'
POST '/api/questions'
POST '/api/questions/search/'
POST '/api/quizzes'
DELETE '/apit/questions/<questions_id>'

GET '/api/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/api/questions'
- Fetches a paginated set of questions, their number, the categories, and the current category
- Request Arguments: None
- Returns: A list of question objects, their number, the categories' names, and the name of the current category
{
  'questions': list of question objects,
  'total_questions': the size of the list of question objects,
  'categories': list of strings for all categories' names,
  'current_category': name of the current category
}

GET '/api/categories/<category_id>/questions'
- Fetches questions based on the selected category
- Request Argument: None
- Returns: A list of questions with the same category as requested, their number, and the category itself
{
  'questions': list of questions based on the requested category,
  'total_questions': the size of the list,
  'current_category': the category's name of the requested category
}

POST '/api/questions'
- Create a new question with the question itself, the answer, the level of difficulty, and the category it belongs in
- Request Argument: question, answer, difficulty, category
- Returns: None

POST '/api/questions/search/'
- Fetches questions based on a search term, their number, and the current category
- Request Argument: searchTerm
- Returns: a list of questions with the pattern of the search term, their numbers, and the current category
{
  'questions': list of questions based on the search term,
  'total_questions': the size of the list,
  'current_category': the current category's name
}

POST '/api/quizzes'
- Fetch a single random question based on all or a category that the app has not asked the player yet in a game
- Request Argument: previous_questions, quiz_category
- Returns: a question based on the category given
{
  'question': list of question based on the category given
}

DELETE '/apit/questions/<questions_id>'
- Delete a question with the given id
- Request Argument: None
- Returns: None

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
