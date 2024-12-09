import os
from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response
from models.book_model import db
from auth_routes import auth_bp
from book_routes import books_bp
from utils.logger import configure_logger
from models import db

# Load environment variables from .env file
load_dotenv()


def create_app() -> Flask:
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)

    configure_logger(app.logger)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///books.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(books_bp, url_prefix='/api')

    # Create tables
    with app.app_context():
        db.create_all()

    return app

app = create_app()


####################################################
#
# Healthchecks
#
####################################################


@app.route('/api/health', methods=['GET'])
def healthcheck() -> Response:
    """
    Health check route to verify the service is running.

    Returns:
        JSON response indicating the health status of the service.
    """
    app.logger.info('Health check')
    return make_response(jsonify({'status': 'healthy'}), 200)

@app.route('/api/db-check', methods=['GET'])
def db_check() -> Response:
    """
    Route to check if the database connection and tables are functional.

    Returns:
        JSON response indicating the database health status.
    Raises:
        error if there is an issue with the database.
    """
    try:
        from models.user_model import User
        _ = User.query.first()
        return make_response(jsonify({'database_status': 'healthy'}), 200)
    except Exception as e:
        app.logger.error(f"Database check failed: {e}")
        return make_response(jsonify({'error': str(e)}), 500)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)