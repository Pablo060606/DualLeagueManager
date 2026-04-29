"""Aplicación principal Flask – app factory"""
import os
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from src.config import config
from src.database.models import db, User
from src.routes import auth, clubs, market, transfers, stats, public


def create_app(config_name='development'):
    """Factory para crear la aplicación Flask."""
    src_dir = os.path.dirname(__file__)
    root_dir = os.path.dirname(src_dir)

    app = Flask(
        __name__,
        template_folder=os.path.join(src_dir, 'templates'),
        static_folder=os.path.join(root_dir, 'static'),
    )

    # Cargar configuración
    app.config.from_object(config[config_name])

    # Inicializar extensiones
    db.init_app(app)

    # Inicializar login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except (TypeError, ValueError):
            return None

    # Registrar blueprints
    app.register_blueprint(public.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(clubs.bp)
    app.register_blueprint(market.bp)
    app.register_blueprint(transfers.bp)
    app.register_blueprint(stats.bp)

    # Crear tablas y poblar datos iniciales
    with app.app_context():
        db.create_all()
        if config_name != 'testing':
            try:
                from src.database.init_db import seed_data
                seed_data()
            except Exception:
                pass

    @app.route('/')
    def index():
        return redirect(url_for('public.landing'))

    return app
