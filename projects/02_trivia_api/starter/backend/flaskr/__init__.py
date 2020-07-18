import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    app.secret_key = "THIS IS A SECRET KEY"
    '''
    @DONE: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
    @DONE: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS'
        )
        return response

    '''
    @DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/api/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.all()
            formatted_categories = [
                category.format() for category in categories
            ]
            return_categories = {}
            for category in formatted_categories:
                return_categories[category["id"]] = category["type"]
            return jsonify({
                'success': True,
                'categories': return_categories
            })
        except:
            abort(404)
    '''
    @DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of
    the screen for three pages. Clicking on the page numbers
    should update the questions.
    '''
    @app.route('/api/questions', methods=['GET'])
    def get_questions():
        # Pagination of questions with 10 questions per page
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        try:
            questions = Question.query.all()
            formatted_questions = [question.format() for question in questions]
            categories = Category.query.all()
            formatted_categories = [
                category.format()["type"] for category in categories
            ]
            current_category = Category.query.get(
                formatted_questions[start]['category']
            ).format()
            return jsonify({
                'success': True,
                'questions': formatted_questions[start:end],
                'total_questions': len(formatted_questions),
                'categories': formatted_categories,
                'current_category': current_category["type"]
            })
        except:
            abort(404)

    '''
    @DONE:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question
    will be removed. This removal will persist in the database and when
    you refresh the page.
    '''
    @app.route('/api/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
        # Delete question with question_id
        question = Question.query.get(question_id)
        try:
            question.delete()
            return jsonify({
                "success": True,
                "deleted_id": question_id
            })
        except:
            abort(404)

    '''
    @DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the
    end of the last page of the questions list in the "List" tab.
    '''
    @app.route('/api/questions', methods=['POST'])
    def post_question():
        question = request.json['question']
        answer = request.json['answer']
        difficulty = request.json['difficulty']
        category = request.json['category']

        # Question input without question or answer is unacceptable
        if not question or not answer:
            abort(400)
        try:
            question = Question(
                question=question,
                answer=answer,
                difficulty=difficulty,
                category=category
            )
            question.insert()
            return jsonify({
                "success": True,
                "question_id": question.id
            })
        except:
            abort(422)

    '''
    @DONE:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/api/questions/search', methods=['POST'])
    def search():
        searchTerm = request.json['searchTerm']
        questions = Question.query.filter(
            Question.question.ilike(f"%{searchTerm}%")
        )
        formatted_questions = [question.format() for question in questions]
        current_category = Category.query.get(1)
        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(formatted_questions),
            'current_category': current_category.format()
        })

    '''
    @DONE:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/api/categories/<category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            questions = Question.query.filter_by(category=category_id)
            current_category = Category.query.get(category_id)
            formatted_questions = [question.format() for question in questions]
            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions),
                'current_category': current_category.type
            })
        except:
            abort(404)

    '''
    @DONE:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route('/api/quizzes', methods=['POST'])
    def post_quizzes():
        previous_questions = request.json['previous_questions']
        quiz_category = request.json['quiz_category']
        return_question = None

        if int(quiz_category["id"]) != 0:
            # If quiz_category is all of the categories
            questions = Question.query.filter_by(
                category=int(quiz_category["id"])
            )
            indices = list(range(questions.count()))
        else:
            # If quiz_category is a specific category
            questions = Question.query.all()
            indices = list(range(Question.query.count()))

        random.shuffle(indices)

        # Get a question that is not previously asked
        for i in indices:
            if questions[i].id not in previous_questions:
                return_question = questions[i]
                break
        if return_question:
            return jsonify({
                "success": True,
                "question": return_question.format()
            })
        else:
            return jsonify({
                "success": True,
                "question": None
            })

    '''
    @DONE:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request!"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found!"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable!"
        }), 422

    @app.errorhandler(500)
    def internal_server(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error!"
        }), 500

    return app
