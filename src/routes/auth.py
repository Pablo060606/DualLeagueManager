"""Rutas de autenticación: registro, login y logout"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from src.database.models import db, User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('public.landing'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        role = request.form.get('role', 'manager')
        preferred_position = request.form.get('preferred_position', '')

        if not name or not email or not password:
            flash('Todos los campos son obligatorios.', 'danger')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('El email ya está registrado.', 'danger')
            return render_template('register.html')

        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            role=role,
            preferred_position=preferred_position if role == 'player' else None,
        )
        db.session.add(user)
        db.session.commit()

        flash('Cuenta creada correctamente. ¡Inicia sesión!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.landing'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.role == 'manager':
                from src.database.models import Club
                club = Club.query.filter_by(manager_id=user.id).first()
                if not club:
                    return redirect(url_for('clubs.create'))
                return redirect(url_for('clubs.dashboard'))
            else:
                return redirect(url_for('transfers.requests'))
        else:
            flash('Email o contraseña incorrectos.', 'danger')

    return render_template('login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('public.landing'))
