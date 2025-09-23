import os
import subprocess
import threading
import shutil
import fitz  # PyMuPDF
from datetime import datetime
from functools import wraps

from flask import (Flask, render_template, request, redirect, url_for, flash,
                   send_from_directory)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from flask_login import (LoginManager, UserMixin, login_user, logout_user,
                         login_required, current_user)
from flask_bcrypt import Bcrypt

# --- App Initialization & Configuration ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-very-secret-and-long-random-string-for-security'

# --- Folder and Path Configurations ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOADS_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['COURSES_FOLDER'] = os.path.join(BASE_DIR, 'courses')

# Create folders if they don't exist
os.makedirs(app.config['UPLOADS_FOLDER'], exist_ok=True)
os.makedirs(app.config['COURSES_FOLDER'], exist_ok=True)

# --- IMPORTANT: Configure your LibreOffice Path ---
# Update this path to match your system's installation
LIBREOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"

# --- Database Configuration ---
instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_path, 'platform.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Extension Initialization ---
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# --- Database Models ---
role_permissions = db.Table('role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    superior_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    subordinates = db.relationship('User', backref=db.backref('superior', remote_side=[id]), lazy='dynamic')
    enrollments = db.relationship('Enrollment', backref='learner', lazy='dynamic', foreign_keys='Enrollment.user_id')
    uploaded_courses = db.relationship('Course', backref='uploader', lazy='dynamic', foreign_keys='Course.user_id')

    @property
    def role(self):
        return Role.query.get(self.role_id)

    def has_permission(self, permission_name):
        for perm in self.role.permissions:
            if perm.name == permission_name:
                return True
        return False

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    users = db.relationship('User', backref='role_info', lazy='dynamic')
    permissions = db.relationship('Permission', secondary=role_permissions, backref=db.backref('roles', lazy='dynamic'))

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    original_filename = db.Column(db.String(150), nullable=False)
    folder_name = db.Column(db.String(150), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Changed from created_by_id
    course_type = db.Column(db.String(100), nullable=False, default='Security Information')
    enrollments = db.relationship('Enrollment', backref='course', lazy='dynamic', cascade="all, delete-orphan")

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    assigned_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expiration_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), nullable=False, default='Not Started')
    completion_date = db.Column(db.DateTime)

# --- Flask-Login Configuration ---
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Conversion Function ---
def convert_ppt_to_images(pptx_path, output_folder):
    """Converts a .pptx file to a series of PNG images using LibreOffice."""
    print(f"Starting conversion for: {pptx_path}")
    if not os.path.exists(LIBREOFFICE_PATH):
        print(f"FATAL ERROR: LibreOffice not found at '{LIBREOFFICE_PATH}'. Conversion failed.")
        return

    pdf_path = os.path.join(output_folder, 'temp.pdf')
    
    try:
        # Step 1: Convert PPTX to PDF using LibreOffice
        command = [
            LIBREOFFICE_PATH,
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', output_folder,
            pptx_path
        ]
        print(f"Running command: {' '.join(command)}")
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Successfully converted {pptx_path} to PDF.")

        # Step 2: Convert PDF to PNG images using PyMuPDF
        doc = fitz.open(pdf_path)
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=150) # Set DPI for better image quality
            output_image_path = os.path.join(output_folder, f'slide_{i+1}.png')
            pix.save(output_image_path)
        doc.close()
        print(f"Successfully converted PDF to {len(doc)} PNG images.")

    except subprocess.CalledProcessError as e:
        print(f"FATAL ERROR: LibreOffice conversion failed for {pptx_path}.")
        print(f"Stderr: {e.stderr}")
    except Exception as e:
        print(f"An unexpected error occurred during conversion: {e}")
    finally:
        # Step 3: Clean up the temporary PDF and original upload
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            print("Temporary PDF file cleaned up.")
        if os.path.exists(pptx_path):
            os.remove(pptx_path)
            print(f"Cleaned up uploaded file: {pptx_path}")

# --- Custom Decorator for Permission Checking ---
def permission_required(permission_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if not any(p.name == permission_name for p in current_user.role.permissions):
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_all_subordinates_recursive(user_id):
    all_subordinates = []
    direct_subordinates = User.query.filter_by(superior_id=user_id).all()
    for sub in direct_subordinates:
        all_subordinates.append(sub)
        all_subordinates.extend(get_all_subordinates_recursive(sub.id))
    return all_subordinates

# --- Authentication Routes ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- Main Application Routes ---
@app.route('/')
@login_required
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    role_name = current_user.role.name
    if role_name == 'Learner':
        enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
        return render_template('dashboards/learner_dashboard.html', enrollments=enrollments)
    if role_name in ['Trainer', 'Admin', 'Super Admin']:
        team_members = get_all_subordinates_recursive(current_user.id)
        if role_name == 'Trainer':
             team_members.append(current_user)
        team_member_ids = [user.id for user in team_members]
        stats = {
            'total_users': len(team_members),
            'completed': 0,
            'in_progress': 0,
            'not_started': 0
        }
        if team_member_ids:
            stats['completed'] = Enrollment.query.filter(
                Enrollment.user_id.in_(team_member_ids), 
                Enrollment.status == 'Completed'
            ).distinct(Enrollment.user_id, Enrollment.course_id).count()
            stats['in_progress'] = Enrollment.query.filter(
                Enrollment.user_id.in_(team_member_ids), 
                Enrollment.status == 'In Progress'
            ).distinct(Enrollment.user_id, Enrollment.course_id).count()
            stats['not_started'] = Enrollment.query.filter(
                Enrollment.user_id.in_(team_member_ids), 
                Enrollment.status == 'Not Started'
            ).distinct(Enrollment.user_id, Enrollment.course_id).count()
        chart_data = {
            'pie': {
                'labels': ['Completed', 'In Progress', 'Not Started'],
                'values': [stats['completed'], stats['in_progress'], stats['not_started']]
            },
            'bar': {
                'labels': [],
                'values': []
            }
        }
        roles_in_team = {}
        for member in team_members:
            role_name = member.role.name
            if role_name not in roles_in_team:
                roles_in_team[role_name] = {'completed': 0}
            completed_count = member.enrollments.filter_by(status='Completed').count()
            roles_in_team[role_name]['completed'] += completed_count
        chart_data['bar']['labels'] = list(roles_in_team.keys())
        chart_data['bar']['values'] = [data['completed'] for data in roles_in_team.values()]
        return render_template(
            'dashboards/manager_dashboard.html', 
            stats=stats, 
            team_members=team_members,
            chart_data=chart_data
        )
    else:
        return "<h1>Error: Unknown user role.</h1>", 500

@app.route('/settings')
@login_required
@permission_required('manage_roles_and_permissions')
def settings():
    return render_template('settings.html')

# --- User Management Routes ---
@app.route('/users')
@login_required
@permission_required('manage_all_users')
def manage_users():
    users = User.query.order_by(User.name).all()
    return render_template('manage_users.html', users=users)

@app.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
@app.route('/user/create', methods=['GET', 'POST'])
@login_required
@permission_required('manage_all_users')
def edit_user(user_id=None):
    if user_id:
        user = User.query.get_or_404(user_id)
        form_title = "Edit User"
    else:
        user = None
        form_title = "Create New User"
    potential_superiors = User.query.join(Role).filter(Role.name != 'Learner').order_by(User.name).all()
    all_roles = Role.query.order_by(Role.name).all()
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role_id = request.form.get('role_id')
        superior_id = request.form.get('superior_id')
        superior_id = int(superior_id) if superior_id else None
        email_conflict = User.query.filter(User.email == email, User.id != user_id).first()
        if email_conflict:
            flash('Another user with this email already exists.', 'danger')
            return render_template('edit_user.html', user=user, superiors=potential_superiors, roles=all_roles, form_title=form_title)
        if user:
            user.name = name
            user.email = email
            user.role_id = role_id
            user.superior_id = superior_id
            if password:
                user.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            flash(f'User "{user.name}" updated successfully!', 'success')
        else:
            if not password:
                flash('Password is required for new users.', 'danger')
                return render_template('edit_user.html', user=user, superiors=potential_superiors, roles=all_roles, form_title=form_title)
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(
                name=name,
                email=email,
                password_hash=hashed_password,
                role_id=role_id,
                superior_id=superior_id
            )
            db.session.add(new_user)
            flash(f'User "{name}" created successfully!', 'success')
        db.session.commit()
        return redirect(url_for('manage_users'))
    return render_template('edit_user.html', user=user, superiors=potential_superiors, roles=all_roles, form_title=form_title)

@app.route('/user/delete/<int:user_id>', methods=['POST'])
@login_required
@permission_required('manage_all_users')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role.name == 'Super Admin' and user.id == 1:
        flash('Cannot delete the primary Super Admin.', 'danger')
        return redirect(url_for('manage_users'))
    if user.id == current_user.id:
        flash('You cannot delete yourself.', 'danger')
        return redirect(url_for('manage_users'))
    for subordinate in user.subordinates:
        subordinate.superior_id = user.superior_id
    db.session.delete(user)
    db.session.commit()
    flash(f'User "{user.name}" has been deleted.', 'success')
    return redirect(url_for('manage_users'))

# --- Team & Course Management Routes ---

# THIS ROUTE IS NOW REMOVED AND REPLACED BY THE ONES BELOW
# @app.route('/upload_course', methods=['GET', 'POST'])
# @login_required
# @permission_required('upload_course')
# def upload_course():
#     ...

# --- NEW COURSE MANAGEMENT HUB ---
@app.route('/manage_courses', methods=['GET', 'POST'])
@login_required
@permission_required('upload_course')
def manage_courses():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        
        if file and file.filename.endswith('.pptx'):
            # Sanitize name and create a unique folder name to prevent conflicts
            sanitized_name = "".join(c for c in os.path.splitext(file.filename)[0] if c.isalnum() or c in (' ', '_')).rstrip()
            folder_name = f"{sanitized_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            course_folder_path = os.path.join(app.config['COURSES_FOLDER'], folder_name)
            os.makedirs(course_folder_path, exist_ok=True)
            
            # Save the uploaded file to a temporary location for conversion
            upload_path = os.path.join(app.config['UPLOADS_FOLDER'], f"{folder_name}.pptx")
            file.save(upload_path)

            new_course = Course(
                name=sanitized_name,
                original_filename=file.filename,
                folder_name=folder_name,
                user_id=current_user.id
            )
            db.session.add(new_course)
            db.session.commit()
            
            # Start the conversion in a background thread so the UI doesn't freeze
            threading.Thread(target=convert_ppt_to_images, args=(upload_path, course_folder_path)).start()
            
            flash(f'Course "{file.filename}" uploaded successfully! Conversion has started in the background.', 'success')
            return redirect(url_for('manage_courses'))
        else:
            flash('Invalid file type. Please upload a .pptx file.', 'danger')
            return redirect(request.url)

    # Logic for GET request (displaying the page)
    view_course_id = request.args.get('view_course_id', type=int)
    slides, course_name, course_folder = [], None, None

    if view_course_id:
        course_to_view = Course.query.get(view_course_id)
        if course_to_view:
            course_name = course_to_view.name
            course_folder = course_to_view.folder_name
            course_path = os.path.join(app.config['COURSES_FOLDER'], course_to_view.folder_name)
            if os.path.exists(course_path):
                slides = sorted([f for f in os.listdir(course_path) if f.lower().endswith('.png')])

    # Fetch all courses and their stats for the table
    courses_with_stats = []
    all_courses = Course.query.options(joinedload(Course.uploader)).order_by(Course.id.desc()).all()
    
    for course in all_courses:
        total_users = Enrollment.query.filter_by(course_id=course.id).count()
        completed = Enrollment.query.filter_by(course_id=course.id, status='Completed').count()
        courses_with_stats.append({
            'course': course,
            'total_users': total_users,
            'completed': completed
        })

    return render_template('manage_courses.html', 
                           courses_with_stats=courses_with_stats, 
                           slides=slides, 
                           view_course_id=view_course_id,
                           course_name=course_name,
                           course_folder=course_folder)

@app.route('/courses/<path:course_folder>/<path:filename>')
def course_files(course_folder, filename):
    """Serves the slide images for the course viewer."""
    return send_from_directory(os.path.join(app.config['COURSES_FOLDER'], course_folder), filename)

@app.route('/course/delete/<int:course_id>', methods=['POST'])
@login_required
@permission_required('manage_all_courses') # Make sure relevant roles have this permission
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    
    # Delete the course's folder from the filesystem
    course_folder_path = os.path.join(app.config['COURSES_FOLDER'], course.folder_name)
    if os.path.exists(course_folder_path):
        shutil.rmtree(course_folder_path)
        
    # Delete the course from the database (enrollments are deleted by cascade)
    db.session.delete(course)
    db.session.commit()
    
    flash(f'Course "{course.name}" and all its data have been successfully deleted.', 'success')
    return redirect(url_for('manage_courses'))

# --- Original Routes (Unchanged) ---
@app.route('/assign_course', methods=['GET', 'POST'])
@login_required
@permission_required('assign_course_to_subordinates')
def assign_course():
    if request.method == 'POST':
        course_id = request.form.get('course_id')
        user_ids = request.form.getlist('user_ids')
        if not course_id or not user_ids:
            flash('You must select a course and at least one user.', 'warning')
            return redirect(url_for('assign_course'))
        course = Course.query.get(course_id)
        for user_id in user_ids:
            user = User.query.get(user_id)
            existing_enrollment = Enrollment.query.filter_by(user_id=user.id, course_id=course.id).first()
            if not existing_enrollment:
                enrollment = Enrollment(
                    user_id=user.id,
                    course_id=course.id,
                    assigned_by_id=current_user.id
                )
                db.session.add(enrollment)
        db.session.commit()
        flash(f'Successfully assigned "{course.name}" to {len(user_ids)} user(s).', 'success')
        return redirect(url_for('assign_course'))
    courses = Course.query.order_by(Course.name).all()
    users = User.query.order_by(User.name).all()
    return render_template('assign_course.html', courses=courses, users=users)

@app.route('/team_progress', methods=['GET', 'POST'])
@login_required
@permission_required('view_subordinate_progress')
def team_progress():
    subordinates = current_user.subordinates.order_by(User.name).all()
    selected_user_enrollments = None
    selected_user_name = None
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        if user_id:
            selected_user = User.query.get(user_id)
            if selected_user and selected_user.superior_id == current_user.id:
                selected_user_enrollments = selected_user.enrollments.all()
                selected_user_name = selected_user.name
            else:
                flash("You do not have permission to view this user's progress.", "warning")
    return render_template(
        'team_progress.html', 
        subordinates=subordinates, 
        enrollments=selected_user_enrollments,
        selected_user_name=selected_user_name
    )

# --- Initial Database Setup Function ---
def setup_database(app):
    with app.app_context():
        db.create_all()
        if Role.query.first() is None:
            print("--- Seeding database with initial roles, permissions, and super admin ---")
            roles_permissions = {
                'Learner': ['view_assigned_courses', 'view_own_progress'],
                'Trainer': ['upload_course', 'assign_course_to_subordinates', 'view_subordinate_progress', 'manage_all_courses'],
                'Admin': ['view_all_trainer_dashboards', 'manage_all_courses', 'manage_users_below_admin', 'upload_course', 'assign_course_to_subordinates', 'view_subordinate_progress'],
                'Super Admin': [
                    'view_all_dashboards', 'manage_all_users', 
                    'manage_roles_and_permissions', 'view_system_logs',
                    'upload_course', 'manage_all_courses', 'assign_course_to_subordinates', 'view_subordinate_progress'
                ]
            }
            all_perms = set()
            for perms in roles_permissions.values():
                all_perms.update(perms)
            
            for perm_name in all_perms:
                if not Permission.query.filter_by(name=perm_name).first():
                    db.session.add(Permission(name=perm_name))
            db.session.commit()

            for role_name, perm_names in roles_permissions.items():
                if not Role.query.filter_by(name=role_name).first():
                    role = Role(name=role_name)
                    db.session.add(role)
                    for perm_name in perm_names:
                        perm = Permission.query.filter_by(name=perm_name).first()
                        if perm:
                            role.permissions.append(perm)
            db.session.commit()

            if User.query.first() is None:
                hashed_password = bcrypt.generate_password_hash('superadmin123').decode('utf-8')
                super_admin_role = Role.query.filter_by(name='Super Admin').first()
                super_admin_user = User(
                    name='Super Admin',
                    email='superadmin@app.com',
                    password_hash=hashed_password,
                    role_id=super_admin_role.id
                )
                db.session.add(super_admin_user)
                db.session.commit()
            print("--- Database seeded successfully! ---")
            print("Super Admin created with email: superadmin@app.com, password: superadmin123")

# --- Main Execution ---
if __name__ == '__main__':
    setup_database(app)
    app.run(debug=True)
