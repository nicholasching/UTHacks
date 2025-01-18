from flask import Blueprint, request, jsonify
from firebase_admin import credentials, firestore
from datetime import datetime

firebase_bp = Blueprint('firebase', __name__)

def get_db_refs():
    db = firestore.client()
    return db.collection('users'), db.collection('activity')

@firebase_bp.route('/user', methods=['POST'])
def create_user():
    users_ref, _ = get_db_refs()
    try:
        data = request.json
        user_id = data.get('user_id')
        user_data = {
            'name': data.get('name'),
            'auth0_id': user_id,
            'created_at': datetime.now()
        }
        users_ref.document(user_id).set(user_data)
        return jsonify({'message': 'User created successfully', 'user_id': user_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@firebase_bp.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    users_ref, _ = get_db_refs()
    try:
        user = users_ref.document(user_id).get()
        if user.exists:
            return jsonify(user.to_dict()), 200
        return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@firebase_bp.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.json
        users_ref.document(user_id).update(data)
        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@firebase_bp.route('/activity', methods=['POST'])
def create_activity():
    _, activity_ref = get_db_refs()
    try:
        data = request.json
        activity_data = {
            'user_id': data.get('user_id'),
            'productive_time': firestore.Increment(data.get('productive_time', 0)),
            'updated_at': datetime.now()
        }
        
        activity_ref.document(data.get('user_id')).set(activity_data, merge=True)
        
        return jsonify({
            'message': 'Activity updated successfully',
            'user_id': data.get('user_id')
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@firebase_bp.route('/activity/<user_id>', methods=['GET'])
def get_user_activities(user_id):
    _, activity_ref = get_db_refs()
    try:
        activities = activity_ref.where('user_id', '==', user_id).stream()
        activities_list = [{'id': doc.id, **doc.to_dict()} for doc in activities]
        return jsonify(activities_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@firebase_bp.route('/activity/<activity_id>', methods=['PUT'])
def update_activity(activity_id):
    _, activity_ref = get_db_refs() 
    try:
        data = request.json
        activity_ref.document(activity_id).update(data)
        return jsonify({'message': 'Activity updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@firebase_bp.route('/activity/<activity_id>', methods=['DELETE'])
def delete_activity(activity_id):
    _, activity_ref = get_db_refs()  
    try:
        activity_ref.document(activity_id).delete()
        return jsonify({'message': 'Activity deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


