# Dual-League Manager

Una aplicación web de gestión de clubes de fútbol profesional basada en las grandes ligas europeas. Gestiona tu presupuesto, ficha estrellas en el mercado y compite por tener la mejor plantilla.

---

## Guía de Inicio Rápido (Instalación desde cero)

Sigue estos pasos en orden para configurar el proyecto en tu ordenador local:

### 1. Descomprimir y Abrir
1. Localiza el archivo `.zip` del proyecto.
2. Haz clic derecho y selecciona **Extraer todo...**.
3. Abre **Visual Studio Code**.
4. Ve a `Archivo > Abrir carpeta...` y selecciona la carpeta que acabas de descomprimir (`DualLeagueManager3`).

### 2. Configurar el Entorno Virtual (venv)
Es fundamental que el entorno esté configurado correctamente para tu usuario de Windows.

* **Si ya existe una carpeta `venv` o `mi_entorno`:**
    Debes borrarla antes de empezar, ya que las rutas internas están ligadas al ordenador original.
    1. Haz clic derecho sobre la carpeta `venv` en VS Code y selecciona **Eliminar**.
    
* **Crear el nuevo entorno:**
    Abre una terminal en VS Code (`Ctrl + Ñ`) y escribe:
    ```powershell
    python -m venv venv
    ```

* **Activar el entorno:**
    Si recibes un error de "script bloqueado", primero ejecuta:
    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
    ```
    Luego actívalo con:
    ```powershell
    .\venv\Scripts\activate
    ```
    *(Sabrás que está activo porque aparecerá `(venv)` en verde al inicio de la línea).*

### 3. Instalar Dependencias
Con el entorno activo, instala todas las librerías necesarias (Flask, SQLAlchemy, Playwright, etc.):
```powershell
pip install -r requirements.txt
```

### 4. Instalar Navegadores para Tests
Para que las pruebas automatizadas funcionen, instala los motores de navegación:´
´´´
pip install pytest-playwright 
´´´

pip
```powershell
playwright install
```

---

## Ejecución de la Aplicación

Para poner en marcha el servidor web:

1. Asegúrate de estar en la carpeta raíz.
2. Ejecuta el archivo de inicio:
   ```powershell
   python run_app.py
   ```
3. Si tienes una versión superior a python 3.12 utliza este comando 
    ```
    pip install --upgrade SQLAlchemy 
    ´´

4. Abre tu navegador y ve a: `http://127.0.0.1:5000`

---

## Pruebas de Testeo (Playwright)

Hemos incluido una suite de pruebas para asegurar que el mercado de fichajes y el login funcionan correctamente.

### Cómo ejecutar los tests:
**Importante:** El servidor (`run_app.py`) debe estar encendido en una terminal mientras ejecutas los tests en otra terminal diferente.

* **Ejecución estándar (rápida):**
    ```powershell
    pytest
    ```
* **Modo Visual (ver al robot navegar):**
    ```powershell
    python -m pytest --headed --slowmo 2000
    ```
* **Ejecutar un test específico:**
    ```powershell
    pytest tests/test_funcionalidades.py
    ```

---

## Características Principales

- **Doble Rol**: Regístrate como **Manager** (para gestionar un club) o como **Jugador** (para recibir ofertas).
- **Mercado Dinámico**: Filtra jugadores por posición (PG, DEF, MED, DEL) y liga.
- **Sistema de Fichajes**: Control de presupuesto, cláusulas de rescisión y contratos de agentes libres.
- **Gestión de Plantilla**: Límite de 18 jugadores por equipo para mantener la competitividad.
- **Estadísticas Avanzadas**: Cálculo automático de valor de mercado y media de valoración (rating) del equipo.

---

## Estructura Técnica

### Árbol de Directorios
```text
DualLeagueManager3/
├── src/
│   ├── database/       # Modelos de SQLAlchemy (User, Club, Player)
│   ├── routes/         # Lógica de negocio (auth, market, transfers...)
│   └── templates/      # Archivos HTML (Jinja2)
├── tests/              # Pruebas automatizadas de Playwright
├── run_app.py          # Punto de entrada de la aplicación
├── requirements.txt    # Librerías necesarias
└── football_manager.db # Base de Datos SQLite
```

### Tecnologías utilizadas
- **Backend**: Python 3.8+ con Flask.
- **Base de Datos**: SQLite3 con SQLAlchemy ORM.
- **Frontend**: HTML5, CSS3 (Bootstrap) y Jinja2.
- **Testing**: Playwright y Pytest.

---

## API Endpoints principales
- `POST /auth/register` - Registro de nuevos usuarios.
- `GET /market/players` - Mercado de fichajes.
- `POST /transfers/sign` - Ejecutar un fichaje.
- `GET /stats/club` - Estadísticas de rendimiento.
