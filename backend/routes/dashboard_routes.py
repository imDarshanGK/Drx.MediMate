from flask import Blueprint, render_template
from backend.utils.role_decorator import role_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/index.html')
def index():
    return render_template('index.html')

# Alternative route for index
@dashboard_bp.route('/dashboard')
def dashboard():
    return render_template('index.html')


# Role-specific Dashboard Routes
@dashboard_bp.route('/doctor-dashboard.html')
@role_required('doctor')
def doctor_dashboard():
    return render_template('doctor-dashboard.html')

@dashboard_bp.route('/pharmacist-dashboard.html')
@role_required('pharmacist')
def pharmacist_dashboard():
    return render_template('pharmacist-dashboard.html')

@dashboard_bp.route('/student-dashboard.html')
@role_required('student')
def student_dashboard():
    return render_template('student-dashboard.html')

@dashboard_bp.route('/patient-dashboard.html')
@role_required('patient')
def patient_dashboard():
    return render_template('patient-dashboard.html')

@dashboard_bp.route('/my-account')
def my_account():
    return render_template('my_account.html', user={
        "name": "Demo User",
        "email": "demo@example.com",
        "notifications": True
    })
