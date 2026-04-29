"""Pruebas unitarias de la aplicación Dual-League Manager"""
import pytest
from werkzeug.security import generate_password_hash

from src.app import create_app
from src.database.models import db, User, Club, Player, PlayerContract


@pytest.fixture()
def app():
    app = create_app("testing")
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        WTF_CSRF_ENABLED=False,
    )

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def app_ctx(app):
    with app.app_context():
        yield


@pytest.fixture()
def create_user(app_ctx):
    def _create_user(email="manager@test.com", password="secret123", name="Manager Test", role="manager"):
        user = User(
            email=email,
            password=generate_password_hash(password),
            name=name,
            role=role,
        )
        db.session.add(user)
        db.session.commit()
        return user

    return _create_user


@pytest.fixture()
def create_club(app_ctx):
    def _create_club(manager_id, name="Test FC", budget=10_000_000):
        club = Club(
            name=name,
            manager_id=manager_id,
            budget=budget,
            available_budget=budget,
        )
        db.session.add(club)
        db.session.commit()
        return club

    return _create_club


@pytest.fixture()
def create_player(app_ctx):
    def _create_player(
        name="Jugador Test",
        position="DEL",
        rating=8.0,
        value=1_000_000,
        league="LaLiga",
        status="available",
    ):
        player = Player(
            name=name,
            position=position,
            rating=rating,
            value=value,
            league=league,
            status=status,
        )
        db.session.add(player)
        db.session.commit()
        return player

    return _create_player
