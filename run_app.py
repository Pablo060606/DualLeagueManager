#!/usr/bin/env python
"""Ejecutor de aplicación Dual-League Manager desde raíz del proyecto"""
import os
import sys

# Asegurar que la raíz del proyecto esté en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.app import create_app

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("  🚀 INICIANDO DUAL-LEAGUE MANAGER")
    print("=" * 70)

    try:
        app = create_app(os.getenv('FLASK_ENV', 'development'))

        print("  ✓ Aplicación creada exitosamente")
        print("\n  📍 Accede a: http://localhost:5000")
        print("  👤 Usuario de prueba: manager1@example.com")
        print("  🔑 Contraseña: password123")
        print("  ⏹️  Para detener: Ctrl + C")
        print("=" * 70 + "\n")

        app.run(debug=True, host='127.0.0.1', port=5000)

    except Exception as e:
        print(f"\n  ❌ Error al iniciar: {e}")
        print("\n  Intenta:")
        print("  1. Verifica que estés en la carpeta DualLeagueManager")
        print("  2. Activa el entorno virtual: venv/Scripts/activate (Windows)")
        print("     o: source venv/bin/activate (Linux/Mac)")
        print("  3. Instala dependencias: pip install -r requirements.txt")
        print("  4. Ejecuta nuevamente: python run_app.py")
        sys.exit(1)
