"""Pruebas de rutas de la aplicación (sin necesidad de servidor externo)"""
import pytest
from werkzeug.security import generate_password_hash

from src.database.models import db, User, Club, Player, PlayerContract


class TestAuthRoutes:
    """Pruebas para el módulo de autenticación."""

    def test_register_get(self, client):
        """La página de registro devuelve 200."""
        response = client.get('/auth/register')
        assert response.status_code == 200

    def test_login_get(self, client):
        """La página de login devuelve 200."""
        response = client.get('/auth/login')
        assert response.status_code == 200

    def test_register_and_login(self, client, app):
        """Registro y login de un usuario manager."""
        with app.app_context():
            response = client.post('/auth/register', data={
                'name': 'Test Manager',
                'email': 'test@example.com',
                'password': 'pass123',
                'role': 'manager',
            }, follow_redirects=True)
            assert response.status_code == 200

            response = client.post('/auth/login', data={
                'email': 'test@example.com',
                'password': 'pass123',
            }, follow_redirects=True)
            assert response.status_code == 200

    def test_login_wrong_password(self, client, app):
        """Login con contraseña incorrecta muestra error."""
        with app.app_context():
            user = User(
                email='user@test.com',
                password=generate_password_hash('correct'),
                name='Test',
                role='manager',
            )
            db.session.add(user)
            db.session.commit()

        response = client.post('/auth/login', data={
            'email': 'user@test.com',
            'password': 'wrong',
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'incorrectos' in response.data or b'password' in response.data.lower()

    def test_duplicate_email_registration(self, client, app):
        """Registrar dos veces el mismo email devuelve error."""
        with app.app_context():
            user = User(
                email='dup@test.com',
                password=generate_password_hash('pass'),
                name='Dup',
                role='manager',
            )
            db.session.add(user)
            db.session.commit()

        response = client.post('/auth/register', data={
            'name': 'Dup2',
            'email': 'dup@test.com',
            'password': 'pass',
            'role': 'manager',
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'registrado' in response.data


class TestPublicRoutes:
    """Pruebas para rutas públicas."""

    def test_landing_page(self, client):
        """La página de inicio carga correctamente."""
        response = client.get('/')
        assert response.status_code in (200, 302)

    def test_public_landing(self, client):
        """La ruta /public/landing carga correctamente."""
        # La ruta raíz redirige a la landing
        response = client.get('/', follow_redirects=True)
        assert response.status_code == 200

    def test_clubs_list(self, client):
        """La lista de clubes es accesible públicamente."""
        response = client.get('/clubs/')
        assert response.status_code == 200


class TestClubRoutes:
    """Pruebas para rutas de clubes."""

    def _login(self, client, app, email='mgr@test.com', password='pass123', role='manager'):
        """Helper: crear usuario y hacer login."""
        with app.app_context():
            user = User(
                email=email,
                password=generate_password_hash(password),
                name='Test Manager',
                role=role,
            )
            db.session.add(user)
            db.session.commit()

        client.post('/auth/login', data={'email': email, 'password': password})

    def test_dashboard_requires_login(self, client):
        """El dashboard requiere autenticación."""
        response = client.get('/clubs/dashboard', follow_redirects=False)
        assert response.status_code == 302

    def test_create_club(self, client, app):
        """Un manager puede crear un club."""
        self._login(client, app)
        response = client.post('/clubs/create', data={
            'name': 'My Test FC',
            'budget': '10000000',
        }, follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            assert Club.query.filter_by(name='My Test FC').first() is not None


class TestMarketRoutes:
    """Pruebas para rutas del mercado."""

    def _login_manager(self, client, app):
        with app.app_context():
            user = User(
                email='mgr2@test.com',
                password=generate_password_hash('pass123'),
                name='Manager2',
                role='manager',
            )
            db.session.add(user)
            db.session.commit()
        client.post('/auth/login', data={'email': 'mgr2@test.com', 'password': 'pass123'})

    def test_market_requires_login(self, client):
        """El mercado requiere autenticación."""
        response = client.get('/market/players', follow_redirects=False)
        assert response.status_code == 302

    def test_market_page_loads(self, client, app):
        """El mercado carga para un usuario autenticado."""
        self._login_manager(client, app)
        response = client.get('/market/players')
        assert response.status_code == 200

    def test_market_api(self, client, app):
        """La API del mercado devuelve JSON."""
        with app.app_context():
            player = Player(name='API Player', position='DEL', rating=8.0,
                            value=1_000_000, league='LaLiga', status='available')
            db.session.add(player)
            db.session.commit()
        self._login_manager(client, app)
        response = client.get('/market/api/players')
        assert response.status_code == 200
        assert response.content_type.startswith('application/json')


class TestTransferRoutes:
    """Pruebas para rutas de fichajes."""

    def _setup_manager_with_club(self, client, app):
        """Crear manager con club."""
        with app.app_context():
            user = User(
                email='mgr3@test.com',
                password=generate_password_hash('pass123'),
                name='Manager3',
                role='manager',
            )
            db.session.add(user)
            db.session.commit()
            club = Club(
                name='Transfer FC',
                manager_id=user.id,
                budget=10_000_000,
                available_budget=10_000_000,
            )
            db.session.add(club)
            db.session.commit()
        client.post('/auth/login', data={'email': 'mgr3@test.com', 'password': 'pass123'})

    def test_sign_player(self, client, app):
        """Un manager puede fichar un jugador disponible."""
        self._setup_manager_with_club(client, app)
        with app.app_context():
            player = Player(name='Signable', position='DEL', rating=7.0,
                            value=500_000, league='LaLiga', status='available')
            db.session.add(player)
            db.session.commit()
            player_id = player.id

        response = client.post('/transfers/sign', data={'player_id': player_id},
                               follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            player = db.session.get(Player, player_id)
            assert player.status == 'signed'

    def test_requests_page_manager(self, client, app):
        """El manager ve la página de solicitudes recibidas."""
        self._setup_manager_with_club(client, app)
        response = client.get('/transfers/requests', follow_redirects=True)
        assert response.status_code == 200


class TestStatsRoutes:
    """Pruebas para estadísticas."""

    def test_stats_requires_login(self, client):
        """Las estadísticas requieren autenticación."""
        response = client.get('/stats/club', follow_redirects=False)
        assert response.status_code == 302

    def test_stats_page(self, client, app):
        """Las estadísticas cargan para un manager con club."""
        with app.app_context():
            user = User(
                email='mgr4@test.com',
                password=generate_password_hash('pass123'),
                name='Manager4',
                role='manager',
            )
            db.session.add(user)
            db.session.commit()
            club = Club(
                name='Stats FC',
                manager_id=user.id,
                budget=10_000_000,
                available_budget=10_000_000,
            )
            db.session.add(club)
            db.session.commit()
        client.post('/auth/login', data={'email': 'mgr4@test.com', 'password': 'pass123'})
        response = client.get('/stats/club', follow_redirects=True)
        assert response.status_code == 200
        assert b'Presupuesto disponible' in response.data
