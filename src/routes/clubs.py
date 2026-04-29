"""Rutas de gestión de clubes"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from src.database.models import db, Club, PlayerContract, Player

bp = Blueprint('clubs', __name__, url_prefix='/clubs')


@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'manager':
        return redirect(url_for('transfers.requests'))

    club = Club.query.filter_by(manager_id=current_user.id).first()
    if not club:
        return redirect(url_for('clubs.create'))

    contracts = PlayerContract.query.filter_by(club_id=club.id).all()
    players = [c.player for c in contracts]
    return render_template('dashboard.html', club=club, players=players)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.role != 'manager':
        return redirect(url_for('transfers.requests'))

    existing = Club.query.filter_by(manager_id=current_user.id).first()
    if existing:
        return redirect(url_for('clubs.dashboard'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        budget_str = request.form.get('budget', '10000000').strip()

        if not name:
            flash('El nombre del club es obligatorio.', 'danger')
            return render_template('create_club.html')

        if Club.query.filter_by(name=name).first():
            flash('Ya existe un club con ese nombre.', 'danger')
            return render_template('create_club.html')

        try:
            budget = float(budget_str)
        except ValueError:
            budget = 10_000_000

        club = Club(
            name=name,
            manager_id=current_user.id,
            budget=budget,
            available_budget=budget,
        )
        db.session.add(club)
        db.session.commit()

        flash(f'Club "{name}" creado correctamente.', 'success')
        return redirect(url_for('clubs.dashboard'))

    return render_template('create_club.html')


@bp.route('/<int:club_id>/squad')
@login_required
def squad(club_id):
    club = db.session.get(Club, club_id)
    if club is None:
        from flask import abort
        abort(404)
    contracts = PlayerContract.query.filter_by(club_id=club.id).all()
    players = [c.player for c in contracts]
    return render_template('squad.html', club=club, players=players)


@bp.route('/')
def list_clubs():
    clubs = Club.query.all()
    return render_template('clubs_list.html', clubs=clubs)
