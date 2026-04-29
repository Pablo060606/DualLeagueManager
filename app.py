"""Aplicación principal Flask"""
import os
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from sqlalchemy import text
from src.config import config
from src.database.models import db, User
from src import routes

def _ensure_schema_compatibility():
    """Aplica alteraciones mínimas para bases SQLite existentes sin migraciones."""
    if db.engine.url.get_backend_name() != 'sqlite':
        return

    column_statements = {
        'users': [
            ('phone', 'ALTER TABLE users ADD COLUMN phone VARCHAR(30)'),
            ('city', 'ALTER TABLE users ADD COLUMN city VARCHAR(120)'),
            ('birth_date', 'ALTER TABLE users ADD COLUMN birth_date DATE')
        ],
        'players': [
            ('user_id', 'ALTER TABLE players ADD COLUMN user_id INTEGER'),
            ('release_clause', 'ALTER TABLE players ADD COLUMN release_clause FLOAT')
        ]
    }

    for table_name, changes in column_statements.items():
        existing_columns = {
            row[1] for row in db.session.execute(text(f'PRAGMA table_info({table_name})')).fetchall()
        }
        for column_name, alter_sql in changes:
            if column_name not in existing_columns:
                db.session.execute(text(alter_sql))

    db.session.commit()


def create_app(config_name='development'):
    """Factory para crear la aplicación Flask"""
    
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
                static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    
    # Inicializar login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
    
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except (TypeError, ValueError):
            return None
    
    # Registrar blueprints
    app.register_blueprint(routes.public.bp)
    app.register_blueprint(routes.auth.bp)
    app.register_blueprint(routes.clubs.bp)
    app.register_blueprint(routes.market.bp)
    app.register_blueprint(routes.transfers.bp)
    app.register_blueprint(routes.stats.bp)
    
    # Crear contexto para comandos
    with app.app_context():
        db.create_all()
        _ensure_schema_compatibility()
    
    @app.route('/')
    def index():
        """Página de inicio"""
        return redirect(url_for('public.landing'))
    
    return app
