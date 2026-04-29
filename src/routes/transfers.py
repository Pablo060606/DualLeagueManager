"""Rutas de fichajes y solicitudes de transferencia"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from src.database.models import db, Club, Player, PlayerContract, MarketRequest, Transaction

bp = Blueprint('transfers', __name__, url_prefix='/transfers')

MAX_SQUAD_SIZE = 18


@bp.route('/sign', methods=['POST'])
@login_required
def sign():
    """Fichar directamente un jugador disponible en el mercado."""
    if current_user.role != 'manager':
        flash('Solo los managers pueden fichar jugadores.', 'danger')
        return redirect(url_for('market.players'))

    player_id = request.form.get('player_id')
    player = db.session.get(Player, player_id)
    if player is None:
        from flask import abort
        abort(404)
    club = Club.query.filter_by(manager_id=current_user.id).first()

    if not club:
        flash('Debes crear un club primero.', 'danger')
        return redirect(url_for('clubs.create'))

    if player.status != 'available':
        flash('El jugador no está disponible.', 'warning')
        return redirect(url_for('market.players'))

    squad_count = PlayerContract.query.filter_by(club_id=club.id).count()
    if squad_count >= MAX_SQUAD_SIZE:
        flash(f'La plantilla está llena (máx. {MAX_SQUAD_SIZE} jugadores).', 'warning')
        return redirect(url_for('market.players'))

    if club.available_budget < player.value:
        flash('Presupuesto insuficiente.', 'danger')
        return redirect(url_for('market.players'))

    # Realizar el fichaje
    player.status = 'signed'
    club.available_budget -= player.value

    contract = PlayerContract(player_id=player.id, club_id=club.id, contract_type='standard', salary=0)
    db.session.add(contract)

    transaction = Transaction(
        club_id=club.id,
        player_id=player.id,
        transaction_type='sign',
        amount=player.value,
        description=f'Fichaje de {player.name}',
    )
    db.session.add(transaction)
    db.session.commit()

    flash(f'¡{player.name} fichado con éxito!', 'success')
    return redirect(url_for('clubs.squad', club_id=club.id))


@bp.route('/release/<int:player_id>', methods=['POST'])
@login_required
def release(player_id):
    """Liberar un jugador de la plantilla."""
    if current_user.role != 'manager':
        flash('Solo los managers pueden liberar jugadores.', 'danger')
        return redirect(url_for('clubs.dashboard'))

    club = Club.query.filter_by(manager_id=current_user.id).first()
    if not club:
        flash('No tienes un club.', 'danger')
        return redirect(url_for('clubs.dashboard'))

    player = db.session.get(Player, player_id)
    if player is None:
        from flask import abort
        abort(404)
    contract = PlayerContract.query.filter_by(player_id=player.id, club_id=club.id).first()
    if not contract:
        flash('Este jugador no pertenece a tu club.', 'danger')
        return redirect(url_for('clubs.squad', club_id=club.id))

    player.status = 'available'
    db.session.delete(contract)

    transaction = Transaction(
        club_id=club.id,
        player_id=player.id,
        transaction_type='release',
        amount=0,
        description=f'Liberación de {player.name}',
    )
    db.session.add(transaction)
    db.session.commit()

    flash(f'{player.name} ha sido liberado.', 'info')
    return redirect(url_for('clubs.squad', club_id=club.id))


@bp.route('/requests', methods=['GET', 'POST'])
@login_required
def requests():
    """Vista de solicitudes de unirse a un club (para jugadores) o recibidas (para managers)."""
    if current_user.role == 'player':
        if request.method == 'POST':
            club_id = request.form.get('club_id')
            club = Club.query.get(club_id)
            if not club:
                flash('Club no encontrado.', 'danger')
            else:
                existing = MarketRequest.query.filter_by(
                    user_id=current_user.id, to_club_id=club.id, status='pending'
                ).first()
                if existing:
                    flash('Ya tienes una solicitud pendiente para ese club.', 'warning')
                else:
                    req = MarketRequest(
                        to_club_id=club.id,
                        user_id=current_user.id,
                        request_type='join',
                        status='pending',
                    )
                    db.session.add(req)
                    db.session.commit()
                    flash('Solicitud enviada al club.', 'success')

        clubs = Club.query.all()
        my_requests = MarketRequest.query.filter_by(user_id=current_user.id).order_by(
            MarketRequest.created_at.desc()
        ).all()
        return render_template('requests.html', clubs=clubs, my_requests=my_requests)

    else:  # manager
        club = Club.query.filter_by(manager_id=current_user.id).first()
        if not club:
            flash('Debes crear un club primero.', 'warning')
            return redirect(url_for('clubs.create'))

        received = MarketRequest.query.filter_by(to_club_id=club.id, request_type='join').order_by(
            MarketRequest.created_at.desc()
        ).all()
        return render_template('requests_manager.html', club=club, received=received)


@bp.route('/requests/<int:request_id>/respond', methods=['POST'])
@login_required
def respond(request_id):
    """Aceptar o rechazar una solicitud de un jugador."""
    if current_user.role != 'manager':
        flash('Solo los managers pueden responder solicitudes.', 'danger')
        return redirect(url_for('transfers.requests'))

    club = Club.query.filter_by(manager_id=current_user.id).first()
    req = db.session.get(MarketRequest, request_id)
    if req is None:
        from flask import abort
        abort(404)

    if req.to_club_id != club.id:
        flash('No tienes permiso para responder esta solicitud.', 'danger')
        return redirect(url_for('transfers.requests'))

    action = request.form.get('action')
    if action == 'accept':
        req.status = 'accepted'
        flash('Solicitud actualizada: aceptada.', 'success')
    elif action == 'reject':
        req.status = 'rejected'
        flash('Solicitud actualizada: rechazada.', 'info')

    db.session.commit()
    return redirect(url_for('transfers.requests'))
