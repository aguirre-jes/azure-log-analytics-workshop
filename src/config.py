#!/usr/bin/env python3
"""
Configuración para la aplicación del workshop
"""

import os
from typing import Optional

def get_connection_string() -> Optional[str]:
    """
    Obtiene la connection string de Application Insights desde variables de entorno
    
    Prioridad:
    1. APPLICATIONINSIGHTS_CONNECTION_STRING (recomendado)
    2. AI_CONNECTION_STRING (alternativo)
    """
    connection_string = (
        os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING') or 
        os.getenv('AI_CONNECTION_STRING')
    )
    
    if not connection_string:
        print("⚠️  Variables de entorno disponibles:")
        env_vars = [key for key in os.environ.keys() if 'INSIGHT' in key.upper() or 'AI_' in key.upper()]
        if env_vars:
            for var in env_vars:
                print(f"   {var}")
        else:
            print("   No se encontraron variables relacionadas con Application Insights")
        
        print("\n💡 Para configurar correctamente:")
        print("   export APPLICATIONINSIGHTS_CONNECTION_STRING='tu_connection_string'")
        print("   o crea un archivo .env con la variable")
    
    return connection_string

def print_config_info():
    """Imprime información de configuración para debugging"""
    print("🔧 Configuración actual:")
    print(f"   Connection String: {'✅ Configurado' if get_connection_string() else '❌ No configurado'}")

if __name__ == "__main__":
    print_config_info()