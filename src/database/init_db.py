"""Inicialización y seed de la base de datos"""
from werkzeug.security import generate_password_hash
from .models import db, User, Player


def seed_data():
    """Poblar la base de datos con datos iniciales de prueba."""
    # Solo insertar si no hay usuarios
    if User.query.first():
        return

    # Crear usuarios de prueba
    manager = User(
        email='manager1@example.com',
        password=generate_password_hash('password123'),
        name='Manager Demo',
        role='manager',
    )
    player_user = User(
        email='jugador1@example.com',
        password=generate_password_hash('password123'),
        name='Jugador Demo',
        role='player',
        preferred_position='DEL',
    )
    db.session.add_all([manager, player_user])
    db.session.commit()

    # Crear jugadores disponibles
    players = [
        Player(name='Carlos Gómez', position='PG', rating=8.5, value=3_000_000, league='LaLiga', status='available'),
        Player(name='Miguel Torres', position='DEF', rating=7.8, value=2_000_000, league='LaLiga', status='available'),
        Player(name='Sergio Medina', position='MED', rating=8.0, value=2_500_000, league='LaLiga', status='available'),
        Player(name='Andrés López', position='DEL', rating=9.0, value=5_000_000, league='LaLiga', status='available'),
        Player(name='Raúl Martínez', position='DEF', rating=7.5, value=1_800_000, league='LaLiga', status='available'),
        Player(name='Diego Fernández', position='MED', rating=7.2, value=1_500_000, league='LaLiga', status='available'),
        Player(name='Pablo Ruiz', position='DEL', rating=8.3, value=3_500_000, league='LaLiga', status='available'),
        Player(name='Javier Sánchez', position='PG', rating=7.9, value=2_200_000, league='LaLiga', status='available'),
        Player(name='Álvaro Jiménez', position='DEF', rating=8.1, value=2_800_000, league='LaLiga', status='available'),
        Player(name='Roberto García', position='MED', rating=8.6, value=4_000_000, league='LaLiga', status='available'),
        Player(name='Luis Herrero', position='DEL', rating=7.7, value=1_900_000, league='LaLiga', status='available'),
        Player(name='Fernando Vega', position='DEF', rating=7.3, value=1_600_000, league='LaLiga', status='available'),
        Player(name='Marcos Blanco', position='MED', rating=8.4, value=3_200_000, league='LaLiga', status='available'),
        Player(name='Iván Moreno', position='DEL', rating=9.2, value=6_000_000, league='LaLiga', status='available'),
        Player(name='Alberto Castillo', position='PG', rating=8.0, value=2_600_000, league='LaLiga', status='available'),
    ]
    db.session.add_all(players)
    db.session.commit()
