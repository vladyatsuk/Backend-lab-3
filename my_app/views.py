from my_app import app
from flask import request
from datetime import datetime
import uuid

users = {}
categories = {}
records = {}

@app.route('/healthcheck')
def healthcheck():
    current_time = datetime.now().isoformat()
    status = 'OK'

    response_data = {
        'status': status,
        'timestamp': current_time
    }

    return response_data, 200

@app.get('/user/<user_id>')
def user_get(user_id):
    if user_id not in users:
        return {'error': f'No user found with id {user_id}'}, 404
    else:
        return users[user_id]

@app.delete('/user/<user_id>')
def user_delete(user_id):
    if user_id not in users:
        return {'error': f'No user found with id {user_id}'}, 404
    else:
        del users[user_id]
        return {'message': f'User {user_id} deleted successfully'}

@app.post('/user')
def user_add():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        name = request.json['name']
    else:
        name = request.args.get('name') 
    if not name:
        return {'error': 'Name is required'}, 400
    id = uuid.uuid4().hex
    user = {'id': id, 'name': name}
    users[id] = user
    return user

@app.get('/users')
def users_get():
    return list(users.values())

@app.get('/category')
def categories_get():
    return list(categories.values())

@app.post('/category')
def category_add():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        name = request.json['name']
    else:
        name = request.args.get('name')
    id = uuid.uuid4().hex
    category = {'id': id, 'name': name}
    categories[id] = category
    return category

@app.delete('/category')
def category_delete():
    category_id = request.args.get('category_id')
    if not category_id:
        return {'error', 'Category id is required'}, 400
    if category_id not in categories:
        return {'error': f'No category found with id {category_id}'}, 404
    else:
        del categories[category_id]
        return {'message': f'Category {category_id} deleted successfully'}

@app.get('/record/<record_id>')
def record_get(record_id):
    if record_id not in records:
        return {'error': f'No record found with id {record_id}'}, 404
    else:
        return records[record_id]

@app.delete('/record/<record_id>')
def record_delete(record_id):
    if record_id not in records:
        return {'error': f'No record found with id {record_id}'}, 404
    else:
        del records[record_id]
        return {'message': f'Category {record_id} deleted successfully'}

@app.post('/record')
def record_add():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        user_id = request.json['user_id']
        category_id = request.json['category_id']
        amount = request.json['amount']
    else:
        user_id = request.args.get('user_id')
        category_id = request.args.get('category_id')
        amount = request.args.get('amount')
    if not user_id or not category_id or not amount:
        return {'error': 'User id, Category id, and Amount are required'}, 400
    if user_id not in users:
        return {'error': 'User not found'}, 404
    if category_id not in categories:
        return {'error': 'Category not found'}, 404 
    record_id = uuid.uuid4().hex
    timestamp = datetime.now().isoformat()
    record = {
        'id': record_id,
        'user_id': user_id,
        'category_id': category_id,
        'timestamp': timestamp,
        'amount': amount
    }
    records[record_id] = record
    return record

@app.get('/record')
def records_get():
    user_id = request.args.get('user_id')
    category_id = request.args.get('category_id')
    if user_id and user_id not in users:
        return {'error': 'User not found'}, 404
    if category_id and category_id not in categories:
        return {'error': 'Category not found'}, 404
    if user_id and category_id:
        user_category_records = [
                record for record in records.values() if
                record['user_id'] == user_id and 
                record['category_id'] == category_id
            ]
        return user_category_records
    elif user_id:
        user_records = [
            record for record in records.values() if record['user_id'] == user_id
        ]
        return user_records
    elif category_id:
        category_records = [
            record for record in records.values() if
            record['category_id'] == category_id
        ]
        return category_records
    else:
        return {'error': 'At least one of User id or Category id is required'}, 400