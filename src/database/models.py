"""Modelos de la base de datos"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """Modelo de usuario (manager o jugador)"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='manager')  # 'manager' or 'player'
    phone = db.Column(db.String(30))
    city = db.Column(db.String(120))
    birth_date = db.Column(db.Date)
    preferred_position = db.Column(db.String(10))  # for players: PG, DEF, MED, DEL
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    clubs = db.relationship('Club', backref='manager', lazy=True, foreign_keys='Club.manager_id')

    def __repr__(self):
        return f'<User {self.email}>'


class Club(db.Model):
    """Modelo de club de fútbol"""
    __tablename__ = 'clubs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    budget = db.Column(db.Float, default=10_000_000)
    available_budget = db.Column(db.Float, default=10_000_000)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    player_contracts = db.relationship('PlayerContract', backref='club', lazy=True,
                                       foreign_keys='PlayerContract.club_id')
    sent_requests = db.relationship('MarketRequest', backref='from_club', lazy=True,
                                    foreign_keys='MarketRequest.from_club_id')
    received_requests = db.relationship('MarketRequest', backref='to_club', lazy=True,
                                        foreign_keys='MarketRequest.to_club_id')
    transactions = db.relationship('Transaction', backref='club', lazy=True)

    def __repr__(self):
        return f'<Club {self.name}>'


class Player(db.Model):
    """Modelo de jugador"""
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    position = db.Column(db.String(10), nullable=False)  # PG, DEF, MED, DEL
    rating = db.Column(db.Float, default=5.0)
    value = db.Column(db.Float, default=500_000)
    league = db.Column(db.String(80))
    status = db.Column(db.String(20), default='available')  # available, signed, injured
    release_clause = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    contracts = db.relationship('PlayerContract', backref='player', lazy=True)

    def __repr__(self):
        return f'<Player {self.name}>'


class PlayerContract(db.Model):
    """Contrato activo entre jugador y club"""
    __tablename__ = 'player_contracts'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=False)
    contract_type = db.Column(db.String(20), default='standard')  # standard, free_agent, loan
    salary = db.Column(db.Float, default=0)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<PlayerContract player={self.player_id} club={self.club_id}>'


class MarketRequest(db.Model):
    """Solicitud de fichaje entre clubes o de jugador"""
    __tablename__ = 'market_requests'

    id = db.Column(db.Integer, primary_key=True)
    from_club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'))
    to_club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    request_type = db.Column(db.String(20))  # 'sign', 'transfer', 'join'
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # for player join requests
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    player = db.relationship('Player', backref='market_requests', lazy=True)
    requester = db.relationship('User', backref='market_requests', lazy=True)

    def __repr__(self):
        return f'<MarketRequest {self.request_type} status={self.status}>'


class Transaction(db.Model):
    """Historial de movimientos económicos"""
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    transaction_type = db.Column(db.String(20))  # 'sign', 'release', 'transfer'
    amount = db.Column(db.Float, default=0)
    description = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    player = db.relationship('Player', backref='transactions', lazy=True)

    def __repr__(self):
        return f'<Transaction {self.transaction_type} amount={self.amount}>'
