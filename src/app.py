#!/usr/bin/env python3
"""
Azure Log Analytics Workshop Demo Application

Esta aplicación simula operaciones de una aplicación web típica
y envía logs estructurados a Azure Log Analytics.
"""

import logging
import time
import random
import json
import os
from datetime import datetime
from opencensus.ext.azure.log_exporter import AzureLogHandler
from config import get_connection_string

# Configuración de logging
logger = logging.getLogger(__name__)

def setup_logging():
    """Configura el logging para enviar a Azure Log Analytics"""
    connection_string = get_connection_string()
    
    if not connection_string:
        print("❌ Error: No se encontró la connection string de Application Insights")
        print("📝 Asegúrate de configurar las variables de entorno correctamente")
        exit(1)
    
    # Handler para Azure
    azure_handler = AzureLogHandler(connection_string=connection_string)
    azure_handler.setLevel(logging.INFO)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    # Configurar logger
    logger.addHandler(azure_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)
    
    print("✅ Logging configurado correctamente")
    print(f"🔗 Enviando logs a Azure Log Analytics...")

class ECommerceSimulator:
    """Simulador de operaciones de e-commerce"""
    
    def __init__(self):
        self.users = ['alice', 'bob', 'charlie', 'diana', 'eve']
        self.products = [
            {'id': 1, 'name': 'Laptop', 'price': 999.99},
            {'id': 2, 'name': 'Mouse', 'price': 29.99},
            {'id': 3, 'name': 'Keyboard', 'price': 79.99},
            {'id': 4, 'name': 'Monitor', 'price': 299.99},
            {'id': 5, 'name': 'Headphones', 'price': 149.99}
        ]
        self.operations = [
            'user_login',
            'product_search',
            'product_view',
            'add_to_cart',
            'checkout',
            'payment_process',
            'user_logout'
        ]
    
    def generate_operation(self):
        """Genera una operación aleatoria"""
        operation = random.choice(self.operations)
        user = random.choice(self.users)
        
        # Datos base de la operación
        operation_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'operation': operation,
            'user_id': user,
            'session_id': f"sess_{random.randint(10000, 99999)}"
        }
        
        # Agregar datos específicos según la operación
        if operation == 'product_search':
            operation_data['search_term'] = random.choice([
                'laptop', 'gaming', 'office', 'wireless', 'portable'
            ])
            operation_data['results_count'] = random.randint(0, 25)
        
        elif operation == 'product_view':
            product = random.choice(self.products)
            operation_data['product_id'] = product['id']
            operation_data['product_name'] = product['name']
            operation_data['product_price'] = product['price']
        
        elif operation == 'add_to_cart':
            product = random.choice(self.products)
            operation_data['product_id'] = product['id']
            operation_data['quantity'] = random.randint(1, 3)
            operation_data['cart_total'] = product['price'] * operation_data['quantity']
        
        elif operation == 'checkout':
            operation_data['cart_items'] = random.randint(1, 5)
            operation_data['total_amount'] = round(random.uniform(50, 2000), 2)
        
        elif operation == 'payment_process':
            operation_data['payment_method'] = random.choice(['credit_card', 'paypal', 'debit_card'])
            operation_data['amount'] = round(random.uniform(50, 2000), 2)
        
        return operation_data
    
    def should_generate_error(self):
        """Determina si se debe generar un error (10% de probabilidad)"""
        return random.random() < 0.1
    
    def generate_error(self, operation_data):
        """Genera diferentes tipos de errores"""
        error_types = [
            {
                'error_code': 'DB_TIMEOUT',
                'error_message': 'Database connection timeout',
                'error_category': 'database'
            },
            {
                'error_code': 'PAYMENT_FAILED',
                'error_message': 'Payment processing failed',
                'error_category': 'payment'
            },
            {
                'error_code': 'INVALID_SESSION',
                'error_message': 'Session expired or invalid',
                'error_category': 'authentication'
            },
            {
                'error_code': 'PRODUCT_UNAVAILABLE',
                'error_message': 'Product out of stock',
                'error_category': 'inventory'
            },
            {
                'error_code': 'RATE_LIMIT_EXCEEDED',
                'error_message': 'Too many requests from user',
                'error_category': 'security'
            }
        ]
        
        error = random.choice(error_types)
        operation_data.update(error)
        return operation_data

def log_operation(operation_data, is_error=False):
    """Registra una operación en los logs"""
    if is_error:
        logger.error(
            f"Operation failed: {operation_data['operation']}",
            extra={'custom_dimensions': operation_data}
        )
    else:
        logger.info(
            f"Operation successful: {operation_data['operation']}",
            extra={'custom_dimensions': operation_data}
        )

def print_stats(operations_count, errors_count):
    """Imprime estadísticas de la sesión"""
    success_rate = ((operations_count - errors_count) / operations_count) * 100
    print(f"\n📊 Estadísticas de la sesión:")
    print(f"   Total operaciones: {operations_count}")
    print(f"   Operaciones exitosas: {operations_count - errors_count}")
    print(f"   Errores: {errors_count}")
    print(f"   Tasa de éxito: {success_rate:.1f}%")

def main():
    """Función principal"""
    print("🚀 Iniciando Azure Log Analytics Workshop Demo")
    print("=" * 50)
    
    # Configurar logging
    setup_logging()
    
    # Crear simulador
    simulator = ECommerceSimulator()
    
    # Enviar log inicial
    logger.info("Application started", extra={
        'custom_dimensions': {
            'timestamp': datetime.utcnow().isoformat(),
            'operation': 'app_start',
            'version': '1.0.0',
            'environment': 'workshop'
        }
    })
    
    operations_count = 0
    errors_count = 0
    
    try:
        print("\n🔄 Generando operaciones (Ctrl+C para detener)...")
        print("📡 Los logs se están enviando a Azure Log Analytics")
        print("⏱️  Espera 2-3 minutos para ver los datos en Azure Portal\n")
        
        while True:
            # Generar operación
            operation_data = simulator.generate_operation()
            operations_count += 1
            
            # Determinar si es error
            is_error = simulator.should_generate_error()
            if is_error:
                operation_data = simulator.generate_error(operation_data)
                errors_count += 1
            
            # Registrar en logs
            log_operation(operation_data, is_error)
            
            # Mostrar progreso
            status = "❌ ERROR" if is_error else "✅ OK"
            print(f"{status} [{operations_count:3d}] {operation_data['user_id']}: {operation_data['operation']}")
            
            # Pausa entre operaciones
            time.sleep(random.uniform(1, 3))
    
    except KeyboardInterrupt:
        print(f"\n\n🛑 Deteniendo aplicación...")
        
        # Log de cierre
        logger.info("Application stopped", extra={
            'custom_dimensions': {
                'timestamp': datetime.utcnow().isoformat(),
                'operation': 'app_stop',
                'session_operations': operations_count,
                'session_errors': errors_count
            }
        })
        
        print_stats(operations_count, errors_count)
        print("🎉 Demo completado! Revisa Azure Log Analytics para ver los datos")

if __name__ == "__main__":
    main()