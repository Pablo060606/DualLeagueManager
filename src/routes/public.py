"""Rutas públicas (sin autenticación requerida)"""
from flask import Blueprint, render_template
from src.database.models import Club, Player, PlayerContract

bp = Blueprint('public', __name__)


@bp.route('/')
def landing():
    clubs = Club.query.all()
    total_players = Player.query.count()
    total_clubs = Club.query.count()
    return render_template('public/landing.html', clubs=clubs,
                           total_players=total_players, total_clubs=total_clubs)
