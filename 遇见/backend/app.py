from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from datetime import datetime
import bcrypt
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///coffee_app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    school = db.Column(db.String(100))
    department = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_title = db.Column(db.String(50))
    major = db.Column(db.String(100))
    research_area = db.Column(db.String(200))
    expertise = db.Column(db.String(200))
    bio = db.Column(db.Text)
    available_time = db.Column(db.Text)
    rating = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    student_feedback = db.Column(db.Text)
    teacher_feedback = db.Column(db.Text)
    rating = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    new_user = User(
        username=data['username'],
        password=hashed_password.decode('utf-8'),
        role=data['role'],
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        school=data.get('school'),
        department=data.get('department')
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
        
        if data['role'] == 'teacher':
            new_teacher = Teacher(
                user_id=new_user.id,
                professional_title=data.get('professional_title'),
                major=data.get('major'),
                research_area=data.get('research_area'),
                expertise=data.get('expertise'),
                bio=data.get('bio'),
                available_time=data.get('available_time')
            )
            db.session.add(new_teacher)
            db.session.commit()
        
        return jsonify({'message': '注册成功'}), 201
    except Exception as e:
        return jsonify({'message': '注册失败', 'error': str(e)}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
        access_token = create_access_token(identity={'id': user.id, 'username': user.username, 'role': user.role})
        return jsonify({'access_token': access_token, 'user': {'id': user.id, 'username': user.username, 'role': user.role, 'name': user.name}}), 200
    else:
        return jsonify({'message': '用户名或密码错误'}), 401

@app.route('/api/teachers', methods=['GET'])
def get_teachers():
    teachers = Teacher.query.all()
    teacher_list = []
    for teacher in teachers:
        user = User.query.get(teacher.user_id)
        teacher_list.append({
            'id': teacher.id,
            'name': user.name,
            'professional_title': teacher.professional_title,
            'major': teacher.major,
            'research_area': teacher.research_area,
            'expertise': teacher.expertise,
            'bio': teacher.bio,
            'available_time': teacher.available_time,
            'rating': teacher.rating
        })
    return jsonify(teacher_list), 200

@app.route('/api/teachers/<int:teacher_id>', methods=['GET'])
def get_teacher(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        return jsonify({'message': '老师不存在'}), 404
    
    user = User.query.get(teacher.user_id)
    return jsonify({
        'id': teacher.id,
        'name': user.name,
        'professional_title': teacher.professional_title,
        'major': teacher.major,
        'research_area': teacher.research_area,
        'expertise': teacher.expertise,
        'bio': teacher.bio,
        'available_time': teacher.available_time,
        'rating': teacher.rating,
        'email': user.email,
        'phone': user.phone
    }), 200

@app.route('/api/appointments', methods=['POST'])
@jwt_required()
def create_appointment():
    data = request.get_json()
    new_appointment = Appointment(
        student_id=data['student_id'],
        teacher_id=data['teacher_id'],
        appointment_time=datetime.strptime(data['appointment_time'], '%Y-%m-%d %H:%M:%S'),
        location=data['location'],
        reason=data['reason']
    )
    
    try:
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify({'message': '预约成功', 'appointment_id': new_appointment.id}), 201
    except Exception as e:
        return jsonify({'message': '预约失败', 'error': str(e)}), 400

@app.route('/api/appointments/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def update_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({'message': '预约不存在'}), 404
    
    data = request.get_json()
    if 'status' in data:
        appointment.status = data['status']
    
    try:
        db.session.commit()
        return jsonify({'message': '预约更新成功'}), 200
    except Exception as e:
        return jsonify({'message': '预约更新失败', 'error': str(e)}), 400

@app.route('/api/appointments/student/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_appointments(student_id):
    appointments = Appointment.query.filter_by(student_id=student_id).all()
    appointment_list = []
    for appointment in appointments:
        teacher = Teacher.query.get(appointment.teacher_id)
        teacher_user = User.query.get(teacher.user_id)
        appointment_list.append({
            'id': appointment.id,
            'teacher_name': teacher_user.name,
            'appointment_time': appointment.appointment_time.strftime('%Y-%m-%d %H:%M:%S'),
            'location': appointment.location,
            'reason': appointment.reason,
            'status': appointment.status
        })
    return jsonify(appointment_list), 200

@app.route('/api/appointments/teacher/<int:teacher_id>', methods=['GET'])
@jwt_required()
def get_teacher_appointments(teacher_id):
    appointments = Appointment.query.filter_by(teacher_id=teacher_id).all()
    appointment_list = []
    for appointment in appointments:
        student = User.query.get(appointment.student_id)
        appointment_list.append({
            'id': appointment.id,
            'student_name': student.name,
            'appointment_time': appointment.appointment_time.strftime('%Y-%m-%d %H:%M:%S'),
            'location': appointment.location,
            'reason': appointment.reason,
            'status': appointment.status
        })
    return jsonify(appointment_list), 200

@app.route('/api/expenses', methods=['POST'])
@jwt_required()
def create_expense():
    data = request.get_json()
    new_expense = Expense(
        appointment_id=data['appointment_id'],
        amount=data['amount']
    )
    
    try:
        db.session.add(new_expense)
        db.session.commit()
        return jsonify({'message': '费用申请成功', 'expense_id': new_expense.id}), 201
    except Exception as e:
        return jsonify({'message': '费用申请失败', 'error': str(e)}), 400

@app.route('/api/expenses/<int:expense_id>', methods=['PUT'])
@jwt_required()
def update_expense(expense_id):
    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({'message': '费用申请不存在'}), 404
    
    data = request.get_json()
    if 'status' in data:
        expense.status = data['status']
    
    try:
        db.session.commit()
        return jsonify({'message': '费用申请更新成功'}), 200
    except Exception as e:
        return jsonify({'message': '费用申请更新失败', 'error': str(e)}), 400

@app.route('/api/feedbacks', methods=['POST'])
@jwt_required()
def create_feedback():
    data = request.get_json()
    new_feedback = Feedback(
        appointment_id=data['appointment_id'],
        student_feedback=data.get('student_feedback'),
        teacher_feedback=data.get('teacher_feedback'),
        rating=data.get('rating')
    )
    
    try:
        db.session.add(new_feedback)
        db.session.commit()
        return jsonify({'message': '反馈提交成功', 'feedback_id': new_feedback.id}), 201
    except Exception as e:
        return jsonify({'message': '反馈提交失败', 'error': str(e)}), 400

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)
