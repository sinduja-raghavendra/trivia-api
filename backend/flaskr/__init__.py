import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  cors = CORS(app, resources={'/': {"origins": "*"}})

  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  @app.route('/categories')
  def retrieve_categories():
    categories = Category.query.order_by(Category.id).all()

    categories_dict = {}
    for category in categories:
      categories_dict[category.id] = category.type

    if (len(categories_dict) == 0):
      abort(404)

    return jsonify({
      'success': True,
      'categories': categories_dict
    })

  @app.route('/questions')
  def get_questions():
    questions = Question.query.order_by(Question.id).all()
    total_questions = len(questions)
    current_questions = paginate_questions(request, questions)

    categories = Category.query.all()
    categories_dict = {}
    for category in categories:
        categories_dict[category.id] = category.type

    if (len(current_questions) == 0):
        abort(404)

    return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': total_questions,
        'categories': categories_dict
      })
      
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''


  @app.route('/questions', methods=['POST'])
  def add_questions():
    body = request.get_json()
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_difficulty = body.get('difficulty', None)
    new_category = body.get('category', None)

    try:
      question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
      question.insert()

      questions = Question.query.order_by(Question.id).all()
      total_questions = len(questions)
      current_questions = paginate_questions(request, questions)

      categories = Category.query.all()
      categories_dict = {}
      for category in categories:
          categories_dict[category.id] = category.type

      if (len(current_questions) == 0):
          abort(404)

      return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': total_questions,
          'categories': categories_dict
        })
    except:
        abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/categories/<int:category_id>/questions')
  def get_questions_based_on_category(category_id):
    category = Category.query.filter_by(id=category_id).one_or_none()
    if (category is None):
      abort(400)

    questions = Question.query.filter(Question.category == category_id).order_by(Question.id).all()
    total_questions = len(questions)
    current_questions = paginate_questions(request, questions)

    categories = Category.query.all()
    categories_dict = {}
    for category in categories:
        categories_dict[category.id] = category.type

    if (len(current_questions) == 0):
        abort(404)

    return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': total_questions,
        'categories': categories_dict,
        'current_category': category.type
      })


  @app.route('/quizzes', methods=['POST'])
  def get_questions_for_quiz():
    body = request.get_json()
    category = body.get('quiz_category', None)
    previous = body.get('previous_questions')
    try:
      if category['id'] == 0:
        questions = Question.query.all()
      else:
        questions = Question.query.filter(Question.category == category['id']).all()

      totalQuestions = len(questions) 

      def get_random_question():
        return questions[random.randrange(0, len(questions), 1)]

      def check_if_used(question):
        used = False
        for q in previous:
            if (q == question.id):
                used = True
        return used

      question = get_random_question()

      while (check_if_used(question)):
        question = get_random_question()

        if (len(previous) == totalQuestions):
          return jsonify({
              'success': True
          })

      return jsonify({
        'success': True,
        'question': question.format()
      })
    except:
        abort(422)

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False, 
          "error": 404,
          "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False, 
          "error": 422,
          "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False, 
          "error": 400,
          "message": "bad request"
      }), 400

  return app

    