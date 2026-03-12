"""
Configuración global de pytest.
Este archivo asegura que el módulo 'app' sea importable desde los tests.
"""
import sys
from pathlib import Path

# Añade el directorio raíz del proyecto al PYTHONPATH
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
