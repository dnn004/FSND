import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(':5433', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            "question": "Is this a question?",
            "answer": "Yes that is a question.",
            "difficulty": 2,
            "category": 1
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get("/api/categories")
        data = json.loads(res.data)

        categories = {
            '1' : "Science",
            '2' : "Art",
            '3' : "Geography",
            '4' : "History",
            '5' : "Entertainment",
            '6' : "Sports"
        }

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['categories'], categories)

    def test_get_paginated_questions(self):
        res = self.client().get("/api/questions?page=2")
        data = json.loads(res.data)

        categories = ["Science", "Art", "Geography", "History", "Entertainment", "Sports"]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['categories'], categories)

    def test_404_sent_requesting_beyond_valid_pate(self):
        res = self.client().get("/api/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_create_question(self):
        res = self.client().post("/api/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        return data['question_id']
    
    def test_400_sent_bad_question_request(self):
        empty_question = {
            "question": "",
            "answer": "",
            "difficulty": 1,
            "category": 1
        }
        res = self.client().post("/api/questions", json=empty_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_delete_question(self):
        question_id = self.test_create_question()
        res = self.client().delete("/api/questions/%d" % question_id)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(int(data['deleted_id']), question_id)

    def test_404_beyond_valid_question_delete(self):
        question_id = 1000
        res = self.client().delete("/api/questions/%d" % question_id)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_search_question(self):
        self.test_create_question()
        searchTerm = {
            "searchTerm": "thIS a QuEStiON"
        }
        res = self.client().post("/api/questions/search", json=searchTerm)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['questions'][0]['question'], self.new_question['question'])
        self.assertEqual(data['questions'][0]['answer'], self.new_question['answer'])
        self.assertEqual(data['questions'][0]['difficulty'], self.new_question['difficulty'])
        self.assertTrue(data['total_questions'] > 0)

    def test_questions_by_category(self):
        res = self.client().get("/api/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        for question in data['questions']:
            self.assertEqual(question['category'], 1)
        self.assertEqual(data['current_category'], "Science")

    def test_404_category_not_available(self):
        res = self.client().get("/api/categories/100/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_play_quiz_question_by_category(self):
        quiz = {
            "previous_questions": [5],
            "quiz_category": {
                "id": 1,
                "type": "Science"
            }
        }
        res = self.client().post("/api/quizzes", json=quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question']['category'], 1)
    
    def test_end_of_quiz(self):
        all_questions = Question.query.all()
        ids = []
        for question in all_questions:
            ids.append(question.id)

        # The previous_question are all questions, so no question left
        # to ask for the quiz
        quiz = {
            "previous_questions": ids,
            "quiz_category": {
                "id": 0,
                "type": "Unknown Category"
            }
        }
        res = self.client().post("/api/quizzes", json=quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question'], None)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()