# Arquitectura del Sistema - Dual-League Manager

## 📐 Descripción General

Dual-League Manager sigue una arquitectura cliente-servidor de tres capas:

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (Cliente)                     │
│                  (HTML, CSS, JavaScript)                    │
│              Interfaz Web en el Navegador                   │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP/REST
                             ↓
┌─────────────────────────────────────────────────────────────┐
│              BACKEND (Servidor - Flask/Python)              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Capa de Presentación (Routes)           │   │
│  │  - auth.py    (Autenticación)                        │   │
│  │  - clubs.py   (Gestión de clubes)                    │   │
│  │  - market.py  (Mercado de jugadores)                 │   │
│  │  - transfers.py (Fichajes)                           │   │
│  │  - stats.py   (Estadísticas)                         │   │
│  │  - public.py  (Rutas públicas)                       │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Capa de Lógica de Negocio                  │   │
│  │  - Validaciones de fichajes                          │   │
│  │  - Cálculo de presupuestos                           │   │
│  │  - Autenticación y autorización                      │   │
│  │  - Estadísticas del equipo                           │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │        Capa de Acceso a Datos (ORM - SQLAlchemy)    │   │
│  │  - Modelos de datos                                  │   │
│  │  - Consultas a la base de datos                      │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────┘
                             │ SQL
                             ↓
┌─────────────────────────────────────────────────────────────┐
│              BASE DE DATOS (SQLite)                         │
│  - users                 (Usuarios del sistema)             │
│  - clubs                 (Clubes de fútbol)                 │
│  - players               (Base de datos de jugadores)       │
│  - player_contracts      (Contratos activos)                │
│  - market_requests       (Solicitudes de fichaje)           │
│  - transactions          (Historial de movimientos)         │
└─────────────────────────────────────────────────────────────┘
```

## 🏗️ Componentes Principales

### 1. **Frontend (src/templates/)**

Interfaz web basada en HTML puro, sin frameworks JavaScript. Responsable de:
- Formularios de autenticación y registro
- Visualización de datos
- Interacción del usuario

**Vistas principales:**
- `login.html` / `register.html` - Autenticación
- `dashboard.html` - Panel principal del club
- `market.html` - Exploración de jugadores disponibles
- `squad.html` - Gestión de plantilla
- `stats.html` - Estadísticas del equipo
- `requests.html` - Solicitudes de fichaje
- `public/landing.html` - Página de inicio pública

### 2. **Backend (src/)**

Aplicación Flask con estructura modular:

**Rutas (src/routes/):**
- `auth.py` - Login/Registro
- `clubs.py` - Operaciones de clubes
- `market.py` - Mercado de jugadores
- `transfers.py` - Fichajes y transferencias
- `stats.py` - Cálculos de estadísticas
- `public.py` - Acceso sin autenticación

**Modelos (src/database/models.py):**

```
User
├── id (PK)
├── email (unique)
├── password (hashed)
├── name
├── role (manager/player)
└── 1-to-N: clubs

Club
├── id (PK)
├── name (unique)
├── manager_id (FK to User)
├── budget
├── available_budget
└── relationships
    ├── 1-to-N: player_contracts
    ├── 1-to-N: market_requests (sent)
    ├── 1-to-N: market_requests (received)

Player
├── id (PK)
├── name
├── position (PG, DEF, MED, DEL)
├── rating (1-10)
├── value ($)
├── league
├── status (available, signed, injured)
└── 1-to-N: player_contracts

PlayerContract
├── id (PK)
├── player_id (FK)
├── club_id (FK)
├── contract_type
├── salary
├── start_date
└── end_date

MarketRequest
├── id (PK)
├── from_club_id (FK)
├── to_club_id (FK)
├── player_id (FK)
├── request_type
├── status
└── timestamps

Transaction
├── id (PK)
├── club_id (FK)
├── player_id (FK)
├── transaction_type
├── amount
└── description
```

### 3. **Base de Datos (SQLite)**

Almacenamiento relacional con las siguientes tablas:

- **users**: Información de usuarios autenticados
- **clubs**: Datos de los clubes gestionados por managers
- **players**: Base de datos global de jugadores disponibles
- **player_contracts**: Relación activa entre jugadores y clubes
- **market_requests**: Solicitudes de fichaje pendientes
- **transactions**: Historial de movimientos económicos

## 🔄 Flujos Principales

### Flujo de Autenticación

```
Usuario → Formulario de Registro → Backend (auth.py)
   ↓
Validar datos → Hashear contraseña → Insertar en BD
   ↓
Redirigir a Login → Login → Validar credenciales
   ↓
Crear sesión → Redirect a Dashboard
```

### Flujo de Fichaje

```
Usuario accede Mercado → Ver jugadores disponibles (GET /market/players)
   ↓
Selecciona jugador → Botón "Fichar"
   ↓
Backend valida:
  - ¿Jugador disponible?
  - ¿Cupo en plantilla? (<18)
  - ¿Presupuesto suficiente?
   ↓
Crear PlayerContract → Actualizar presupuesto → Cambiar estado jugador
   ↓
Crear Transaction (registro) → Response a usuario
```

### Flujo de Estadísticas

```
Usuario accede Stats → Backend consulta (stats.py)
   ↓
Query: JOIN players + contracts filtrado por club
   ↓
Calcular:
  - Cantidad de jugadores
  - Valor total de plantilla
  - Rating promedio
  - Distribución por posición
   ↓
Renderizar vista con datos
```

## 🔐 Seguridad

- **Autenticación**: Contraseñas hasheadas con Werkzeug
- **Sesiones**: Flask-Login con cookies seguras
- **Autorización**: Verificación de propietario en operaciones sensibles
- **CSRF**: Habilitado por defecto en formularios Flask
- **Datos sensibles**: Almacenados en `.env`, no commitados

## 📊 Escalabilidad

**Mejoras futuras:**
- Migrar de SQLite a PostgreSQL para producción
- Implementar caché con Redis
- Agregar paginación a listados
- Implementar API GraphQL
- Agregar pruebas unitarias e integración
- Containerizar con Docker

## 🔌 API Endpoints

### Autenticación
- `POST /auth/register` - Registro
- `POST /auth/login` - Login
- `GET /auth/logout` - Logout

### Clubes
- `GET /clubs/dashboard` - Dashboard
- `GET /clubs/create` - Crear club
- `POST /clubs/create` - Crear club (POST)
- `GET /clubs/<id>/squad` - Ver plantilla
- `GET /clubs/<id>/stats` - Estadísticas

### Mercado
- `GET /market/players` - Listar jugadores
- `GET /market/api/players` - API JSON
- `GET /market/api/player/<id>` - Detalle de jugador

### Fichajes
- `POST /transfers/sign` - Fichar jugador
- `POST /transfers/release/<id>` - Liberar jugador
- `GET /transfers/requests` - Ver solicitudes

### Estadísticas
- `GET /stats/club` - Estadísticas del club

## 🧪 Configuración para Desarrollo

```python
# config.py selecciona automáticamente según FLASK_ENV
Development:  DEBUG=True, Templates auto-reload
Production:   DEBUG=False, Cookies HTTPS
Testing:      TESTING=True, BD en memoria
```

## 📦 Dependencias Principales

```
Flask==2.3.3              # Framework web
Flask-SQLAlchemy==3.0.5  # ORM
Flask-Login==0.6.2       # Autenticación
python-dotenv==1.0.0     # Variables de entorno
Werkzeug==2.3.7          # Utilidades, hashing
```

## 🗂️ Estructura de Carpetas Final

```
DualLeagueManager/
├── src/
│   ├── app.py                    # Punto de entrada
│   ├── config.py                 # Configuración
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py             # Modelos SQLAlchemy
│   │   └── init_db.py            # Seed de datos
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py               # Autenticación
│   │   ├── clubs.py              # Clubes
│   │   ├── market.py             # Mercado
│   │   ├── transfers.py          # Fichajes
│   │   ├── stats.py              # Estadísticas
│   │   └── public.py             # Rutas públicas
│   ├── logic/                    # Lógica de negocio (futuro)
│   └── templates/
│       ├── base.html             # Base heredable
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── market.html
│       ├── squad.html
│       ├── stats.html
│       ├── requests.html
│       └── public/
│           └── landing.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── data/
│   └── football_manager.db       # Base de datos (no comitida)
├── requirements.txt              # Dependencias
├── .env.example                  # Template de variables
├── .gitignore
├── README.md
├── SETUP.md
└── ARCHITECTURE.md
```

## 📝 Notas de Desarrollo

1. **Los modelos heredan de SQLAlchemy**: Las relaciones se definen en ambos lados
2. **Las sesiones Flask-Login automáticas**: `current_user` disponible en templates y vistas
3. **Las rutas usan blueprints**: Modularización limpia y fácil de mantener
4. **Los templates heredan de base.html**: Consistencia visual y navegación
5. **Las bases de datos se inicializan automáticamente**: `create_all()` en `app.py`
