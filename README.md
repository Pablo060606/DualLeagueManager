# ⚽ Dual-League Manager

Aplicación web Flask para gestionar clubes de fútbol: fichar jugadores, administrar presupuestos y controlar estadísticas.

## Estructura del proyecto

```
DualLeagueManager/
├── src/                    # Código fuente de la aplicación
│   ├── app.py              # App factory (create_app)
│   ├── config.py           # Configuración (dev/prod/testing)
│   ├── database/
│   │   ├── models.py       # Modelos SQLAlchemy
│   │   └── init_db.py      # Datos de ejemplo
│   ├── routes/
│   │   ├── auth.py         # Autenticación
│   │   ├── clubs.py        # Gestión de clubes
│   │   ├── market.py       # Mercado de jugadores
│   │   ├── transfers.py    # Fichajes y solicitudes
│   │   ├── stats.py        # Estadísticas
│   │   └── public.py       # Rutas públicas
│   └── templates/          # Plantillas HTML
├── static/                 # CSS y JS
│   ├── css/style.css
│   └── js/main.js
├── tests/                  # Pruebas automatizadas
│   ├── conftest.py
│   ├── test_routes.py      # Pruebas de rutas (sin servidor)
│   └── test_funcionalidades.py  # Pruebas Playwright (con servidor)
├── run_app.py              # Punto de entrada
├── requirements.txt        # Dependencias
├── pytest.ini              # Configuración pytest
└── .env.example            # Variables de entorno de ejemplo
```

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/Pablo060606/DualLeagueManager.git
cd DualLeagueManager

# 2. Crear entorno virtual
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. (Opcional) Instalar navegadores Playwright
playwright install chromium
```

## Ejecutar la aplicación

```bash
python run_app.py
```

Accede en: http://localhost:5000

**Credenciales de prueba:**
- Manager: `manager1@example.com` / `password123`
- Jugador: `jugador1@example.com` / `password123`

## Ejecutar los tests

### Tests unitarios (sin servidor)

```bash
pytest
```

### Tests de integración con Playwright (requiere servidor activo)

En una terminal, arrancar el servidor:

```bash
python run_app.py
```

En otra terminal:

```bash
pytest tests/test_funcionalidades.py --headed
```

## Variables de entorno

Copia `.env.example` a `.env` y ajusta los valores:

```bash
cp .env.example .env
```

| Variable | Descripción | Valor por defecto |
|---|---|---|
| `FLASK_ENV` | Entorno (development/production) | `development` |
| `SECRET_KEY` | Clave secreta de sesión | (valor de desarrollo) |
| `DATABASE_URL` | URL de la base de datos SQLite | `sqlite:///football_manager.db` |

## Funcionalidades

- **Registro y login** de managers y jugadores
- **Creación de clubes** con presupuesto configurable
- **Mercado de jugadores** con filtros por posición y liga
- **Fichajes directos** con descuento de presupuesto
- **Liberación de jugadores** de la plantilla
- **Solicitudes de jugadores** para unirse a clubes
- **Estadísticas** del club: valor total, rating promedio, distribución por posición
- **Vista pública** de clubes y estadísticas globales
