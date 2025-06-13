from flask import Flask, send_from_directory, abort, send_file, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
from .config import Config
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail
from flasgger import Swagger
import os

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
api = Api()
cors = CORS()
mail = Mail()
def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object(Config)
    swagger = Swagger(app)
    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    cors.init_app(app, 
        resources={r"/api/*": {
            "origins": ["http://localhost:3000", "http://192.168.1.83:3000", "https://eventify-kr4t53kyi-otakugod0s-projects.vercel.app", "https://rotracteventify.vercel.app"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }}
    )
    mail.init_app(app)
    
    # Configure upload folder for media files
    MEDIA_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'media'))
    app.config['MEDIA_FOLDER'] = MEDIA_FOLDER

    # Ensure the media folder exists
    if not os.path.exists(MEDIA_FOLDER):
        os.makedirs(MEDIA_FOLDER)

    @app.route('/api/image/<filename>', methods=['GET', 'POST'])
    def get_image(filename):
        if request.method == 'POST':
            # Handle image upload
            if 'image' not in request.files:
                return {'message': 'No image file provided'}, 400
                
            file = request.files['image']
            if file.filename == '':
                return {'message': 'No selected file'}, 400
                
            # Check if the file extension is allowed
            file_ext = os.path.splitext(file.filename)[1].lower()
            if file_ext not in ['.jpg', '.jpeg', '.png']:
                return {'message': 'File type not allowed'}, 400
                
            # Save the file
            file_path = os.path.join(app.config['MEDIA_FOLDER'], filename)
            file.save(file_path)
            return {'filename': filename, 'message': 'success'}, 200
            
        else:
            # Handle GET request
            # Construct the file path using absolute path
            file_path = os.path.join(app.config['MEDIA_FOLDER'], filename)
            
            # Check if the file exists
            if not os.path.isfile(file_path):
                abort(404, description="Image not found")
            
            # Get file extension to determine mimetype
            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext in ['.jpg', '.jpeg']:
                mimetype = 'image/jpeg'
            elif file_ext == '.png':
                mimetype = 'image/png'
            else:
                mimetype = 'image/jpeg'  # Default to jpeg
                
            # Serve the image
            return send_file(file_path, mimetype=mimetype)

    # Optional: Serve images from the media folder directly
    @app.route('/media/<filename>')
    def serve_media(filename):
        return send_from_directory(app.config['MEDIA_FOLDER'], filename)

    
    # Register blueprints
    # from api.routes.events import events_bp
    # from api.routes.users import users_bp
    # from api.routes.branches import branches_bp
    # app.register_blueprint(events_bp, url_prefix="/api/events")
    # app.register_blueprint(users_bp, url_prefix="/api/users")
    # app.register_blueprint(branches_bp, url_prefix="/api/branches")
    from .routes.test import test_bp
    from .routes.auth import auth_bp
    from .routes.user import user_bp
    from .routes.event import event_bp
    from .routes.branch import branch_bp
    from .routes.registration import registration_bp
    from .routes.contact import contact_bp
    from .routes.payment import payment_bp
    from .routes.newsLetter import news_letter_bp

    
    app.register_blueprint(contact_bp, url_prefix="/api/contact/")
    app.register_blueprint(branch_bp, url_prefix="/api/branch/")
    app.register_blueprint(event_bp, url_prefix='/api/event')
    app.register_blueprint(test_bp, url_prefix='/api/test')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(registration_bp, url_prefix='/api/registration')
    app.register_blueprint(payment_bp, url_prefix='/api/payment')
    app.register_blueprint(news_letter_bp, url_prefix='/api/newsletter')
    
    with app.app_context():
        db.create_all()  # Create database tables

    return app