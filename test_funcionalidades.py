import pytest
import re
from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:5000"

# Datos de prueba dinámicos para evitar errores de "Email ya registrado"
import time
TIMESTAMP = int(time.time())
MANAGER_EMAIL = f"manager_{TIMESTAMP}@test.com"
PLAYER_EMAIL = f"player_{TIMESTAMP}@test.com"

class TestFootballManager:
    
    # 1. FLUJO DE AUTENTICACIÓN (auth.py)
    def test_01_registration_and_login_flows(self, page: Page):
        # Registro de Manager
        page.goto(f"{BASE_URL}/auth/register")
        page.fill("input[name='name']", "Arturo Manager")
        page.fill("input[name='email']", MANAGER_EMAIL)
        page.fill("input[name='password']", "pass123")
        page.select_option("select[name='role']", value="manager")
        page.click("button[type='submit']")
        
        expect(page).to_have_url(f"{BASE_URL}/auth/login")
        
        # Registro de Jugador
        page.goto(f"{BASE_URL}/auth/register")
        page.fill("input[name='name']", "Pepito Jugador")
        page.fill("input[name='email']", PLAYER_EMAIL)
        page.fill("input[name='password']", "pass123")
        page.select_option("select[name='role']", value="player")
        page.select_option("select[name='preferred_position']", value="MED")
        page.click("button[type='submit']")
        
        expect(page).to_have_url(f"{BASE_URL}/auth/login")

    # 2. GESTIÓN DE CLUBES (clubs.py)
    def test_02_club_creation_and_dashboard(self, page: Page):
        # Login como Manager
        page.goto(f"{BASE_URL}/auth/login")
        page.fill("input[name='email']", MANAGER_EMAIL)
        page.fill("input[name='password']", "pass123")
        page.click("button[type='submit']")
        
        # Detectar redirección a creación de club
        expect(page).to_have_url(f"{BASE_URL}/clubs/create")
        
        page.fill("input[name='name']", f"Nebrija FC {TIMESTAMP}")
        page.fill("input[name='budget']", "10000000")
        page.click("button[type='submit']")
        
        # Comprobar Dashboard
        expect(page).to_have_url(f"{BASE_URL}/clubs/dashboard")
        expect(page.locator("text=Nebrija FC")).to_be_visible()

    # 3. MERCADO Y FICHAJES DIRECTOS (market.py & transfers.py)
    def test_03_market_interaction_and_signing(self, page: Page):
        # Login Manager
        page.goto(f"{BASE_URL}/auth/login")
        page.fill("input[name='email']", MANAGER_EMAIL)
        page.fill("input[name='password']", "pass123")
        page.click("button[type='submit']")
        
        # Ir al mercado
        page.goto(f"{BASE_URL}/market/players")
        
        # Probar filtros
        page.select_option("select[name='position']", value="DEL")
        page.click("button:has-text('Filtrar'), button[type='submit']")
        
        # Fichar al primer jugador disponible (Botón en transfers.sign)
        # Buscamos el formulario de fichaje
        first_player_form = page.locator("form[action='/transfers/sign']").first
        player_name = first_player_form.locator("xpath=..//h5").inner_text() # Asumiendo estructura de card
        
        first_player_form.locator("button[type='submit']").click()
        
        # Verificar que está en la plantilla
        expect(page).to_have_url(re.compile(r".*/clubs/\d+/squad"))
        expect(page.get_by_text(player_name)).to_be_visible()

    # 4. SOLICITUDES JUGADOR -> CLUB (transfers.py - requests)
    def test_04_player_to_club_request(self, page: Page):
        # Login como Jugador
        page.goto(f"{BASE_URL}/auth/login")
        page.fill("input[name='email']", PLAYER_EMAIL)
        page.fill("input[name='password']", "pass123")
        page.click("button[type='submit']")
        
        # El jugador va a solicitudes
        page.goto(f"{BASE_URL}/transfers/requests")
        
        # Selecciona el club creado antes y solicita unirse
        page.select_option("select[name='club_id']", label=re.compile(f"Nebrija FC.*"))
        page.click("button:has-text('Solicitar unirse')")
        
        expect(page.get_by_text("Solicitud enviada al club")).to_be_visible()

    # 5. RESPONDER SOLICITUDES (transfers.py - respond)
    def test_05_manager_accepts_player(self, page: Page):
        # Login como Manager para aceptar al jugador del test anterior
        page.goto(f"{BASE_URL}/auth/login")
        page.fill("input[name='email']", MANAGER_EMAIL)
        page.fill("input[name='password']", "pass123")
        page.click("button[type='submit']")
        
        page.goto(f"{BASE_URL}/transfers/requests")
        
        # Buscar la solicitud recibida y aceptarla
        solicitud = page.locator("tr:has-text('Pepito Jugador')")
        solicitud.locator("button:has-text('Aceptar')").click()
        
        expect(page.get_by_text("Solicitud actualizada")).to_be_visible()

    # 6. ESTADÍSTICAS (stats.py)
    def test_06_check_stats(self, page: Page):
        # Login Manager
        page.goto(f"{BASE_URL}/auth/login")
        page.fill("input[name='email']", MANAGER_EMAIL)
        page.fill("input[name='password']", "pass123")
        page.click("button[type='submit']")
        
        page.goto(f"{BASE_URL}/stats/club")
        
        # Verificar que se muestran números (no error 0)
        expect(page.locator("text=Presupuesto disponible")).to_be_visible()
        expect(page.locator("text=Valor Total")).not_to_contain_text("$0")

    # 7. VISTA PÚBLICA (public.py)
    def test_07_public_access(self, page: Page):
        page.goto(f"{BASE_URL}/logout") # Asegurar estar fuera
        page.goto(f"{BASE_URL}/")
        
        expect(page.locator("text=Clubes registrados")).to_be_visible()
        
        # Exploración pública de clubes
        page.goto(f"{BASE_URL}/clubs")
        expect(page.locator(f"text=Nebrija FC {TIMESTAMP}")).to_be_visible()