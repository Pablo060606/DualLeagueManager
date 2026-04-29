"""Rutas de estadísticas del club"""
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from src.database.models import Club, PlayerContract, Player

bp = Blueprint('stats', __name__, url_prefix='/stats')


@bp.route('/club')
@login_required
def club_stats():
    if current_user.role != 'manager':
        flash('Solo los managers pueden ver estadísticas del club.', 'warning')
        return redirect(url_for('public.landing'))

    club = Club.query.filter_by(manager_id=current_user.id).first()
    if not club:
        return redirect(url_for('clubs.create'))

    contracts = PlayerContract.query.filter_by(club_id=club.id).all()
    players = [c.player for c in contracts]

    total_value = sum(p.value for p in players)
    avg_rating = (sum(p.rating for p in players) / len(players)) if players else 0
    position_count = {}
    for p in players:
        position_count[p.position] = position_count.get(p.position, 0) + 1

    stats = {
        'total_players': len(players),
        'total_value': total_value,
        'avg_rating': round(avg_rating, 2),
        'available_budget': club.available_budget,
        'total_budget': club.budget,
        'spent': club.budget - club.available_budget,
        'position_count': position_count,
    }

    return render_template('stats.html', club=club, stats=stats, players=players)
