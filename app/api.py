from flask import Blueprint, jsonify, request

from app.models import db, News, Category, User

api = Blueprint('api', __name__)

@api.route('/')
def default():
    response = {
        'msg': 'Good Test!'
    }

    return jsonify(response), 200


@api.route('/news', methods=('GET', 'POST'))
def allNews():
    data = {
        'errorMessage': 'Method Not Implemented'
    }
    code = 403

    if request.method == 'GET':
        category_id = request.args.get('category_id')
        page = int(request.args.get('page', default=1))

        try:
            if category_id:                
                results = Category.query.get(category_id).news.paginate(page, 10)
            else:
                results = News.query.order_by(News.created_at.desc()).paginate(page, 10)
            data['has_next'] = results.has_next
            results = results.items
        except:
            results = []
        
        # in case there are enormous content body, just show the titles
        data['result'] = [
            {
                'id': r.id,
                'title': r.title,
                'created_at': r.created_at.strftime('%Y-%m-%d')
            } 
            for r in results]
        code = 200

    elif request.method == 'POST':
        req_body = request.get_json()
        news = News(req_body['title'], req_body['content'], req_body['category_id'])

        db.session.add(news)
        db.session.commit()

        data = {
            'result': news.serialize()
        }
        code = 201

    return jsonify(data), code


@api.route('/news/<int:id>', methods=('GET', 'DELETE', 'PUT'))
def news(id):
    data = {
        'errorMessage': 'Method Not Implemented'
    }
    code = 403

    news = News.query.get(id)

    if not news:
        data = {
                'errorMessage': 'News not found!'
            }    
        code = 200

    else:
        if request.method == 'GET':
            result = News.query.get(id)
            data = {
                'result': result.serialize()
            }    
            code = 200
        
        elif request.method == 'DELETE':
            db.session.delete(news)
            db.session.commit()

            data = {
                'successMessage': 'Deleted Successfully!'
            }
            code = 201
            
        elif request.method == 'PUT':
            req_body = request.get_json()
            news.title = req_body['title']
            news.content = req_body['content']
            news.category_id = req_body['category_id']

            db.session.commit()
            
            data = {
                'result': News.query.get(req_body['id']).serialize()
            }
            code = 201

    return jsonify(data), code


@api.route('/categories', methods=('GET', 'POST'))
def allCategories():
    data = {
        'errorMessage': 'Method Not Implemented'
    }
    code = 403

    if request.method == 'GET':
        data = {
            'result': [c.serialize() for c in Category.query.all()]
        }                
        code = 200

    elif request.method == 'POST':
        req_body = request.get_json()
        category = Category(req_body['name'])

        db.session.add(category)
        db.session.commit()

        data = {
            'result': category.serialize()
        }
        code = 201

    return jsonify(data), code


@api.route('/categories/<int:id>', methods=('GET', 'DELETE', 'PUT'))
def category(id):
    data = {
        'errorMessage': 'Method Not Implemented'
    }
    code = 403

    category = Category.query.get(id)
    
    if not category:
        data = {
            'errorMessage': 'Category not found!'
        }
        code = 200

    else:        
        if request.method == 'GET':
            data = {
                'result': category.serialize()
            }
            code = 200
            
        elif request.method == 'DELETE':

            db.session.delete(category)
            db.session.commit()

            data = {
                'successMessage': 'Deleted Successfully!'
            }
            code = 201
            
        elif request.method == 'PUT':
            req_body = request.get_json()
            category.name = req_body['name']

            db.session.commit()
            
            updated_category =  Category.query.get(id)
            if updated_category:
                data = {
                    'result': Category.query.get(category.id).serialize()
                }
                code = 201
     
            else:
                data = {
                    'errorMessage': 'Category not updated!'
                }
                code = 200

    return jsonify(data), code


@api.route('/login', methods=['POST'])
def login():
    data = {
        'errorMessage': 'Method Not Implemented'
    }
    code = 403

    req_body = request.get_json()
    user = User.query.filter_by(username=req_body['username']).first()
    if not user or not user.check_password(req_body['password']):        
        data = {
            'errorMessage': 'Wrong Authentication!'
        }
        code = 200

    else:
        data = {
            'successMessage': 'Success Login!'
        }
        code = 200
    
    return jsonify(data), code

