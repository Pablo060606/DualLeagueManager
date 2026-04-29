"""Rutas del mercado de jugadores"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from src.database.models import Player

bp = Blueprint('market', __name__, url_prefix='/market')


@bp.route('/players')
@login_required
def players():
    position = request.args.get('position', '')
    league = request.args.get('league', '')
    query = Player.query.filter_by(status='available')

    if position:
        query = query.filter_by(position=position)
    if league:
        query = query.filter_by(league=league)

    players_list = query.order_by(Player.rating.desc()).all()
    positions = ['PG', 'DEF', 'MED', 'DEL']
    leagues = ['LaLiga', 'Premier League', 'Serie A', 'Bundesliga', 'Ligue 1']

    return render_template('market.html', players=players_list,
                           positions=positions, leagues=leagues,
                           selected_position=position, selected_league=league)


@bp.route('/api/players')
@login_required
def api_players():
    position = request.args.get('position', '')
    query = Player.query.filter_by(status='available')
    if position:
        query = query.filter_by(position=position)
    players_list = query.order_by(Player.rating.desc()).all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'position': p.position,
        'rating': p.rating,
        'value': p.value,
        'league': p.league,
        'status': p.status,
    } for p in players_list])


@bp.route('/api/player/<int:player_id>')
@login_required
def api_player(player_id):
    player = db.session.get(Player, player_id)
    if player is None:
        from flask import abort
        abort(404)
    return jsonify({
        'id': player.id,
        'name': player.name,
        'position': player.position,
        'rating': player.rating,
        'value': player.value,
        'league': player.league,
        'status': player.status,
    })
