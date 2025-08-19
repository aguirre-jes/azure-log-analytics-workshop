# 🐍 Configuración de la Aplicación Python

Este documento te guía para configurar y ejecutar la aplicación Python que enviará logs a Azure Log Analytics.

## 🎯 Objetivo

Configurar la aplicación demo que simula un e-commerce y envía logs estructurados a Azure Log Analytics para demostrar agregación y análisis de logs.

---

## 🏗️ Arquitectura de la Aplicación

### **📊 Flujo de Datos:**

```
Python App (Local)
├── 🛒 E-commerce Simulator
│   ├── User operations
│   ├── Product interactions
│   └── Error scenarios
├── 📝 Structured Logging
│   ├── Info logs (90%)
│   └── Error logs (10%)
└── 📤 OpenCensus Azure Exporter
    ├── Connection String
    └── Custom Dimensions
        ↓
🌩️ Azure Application Insights
    ├── Automatic ingestion
    └── Data transformation
        ↓
📊 Azure Log Analytics
    ├── AppTraces table
    ├── AppEvents table
    └── Query interface (KQL)
```

### **🎭 Operaciones Simuladas:**

La aplicación simula estas operaciones de un e-commerce típico:

- **👤 user_login:** Inicio de sesión de usuario
- **🔍 product_search:** Búsqueda de productos
- **👀 product_view:** Visualización de producto
- **🛒 add_to_cart:** Agregar al carrito
- **💳 checkout:** Proceso de compra
- **💰 payment_process:** Procesamiento de pago
- **🚪 user_logout:** Cierre de sesión

---

## 🔧 Configuración Inicial

### **1. Obtener Connection String**

Desde el directorio de Terraform, obtén la connection string:

```bash
# Navegar al directorio terraform
cd terraform

# Obtener la connection string
terraform output -raw application_insights_connection_string
```

#### **📋 Ejemplo de output:**
```
InstrumentationKey=12345678-1234-1234-1234-123456789012;IngestionEndpoint=https://eastus-8.in.applicationinsights.azure.com/;LiveEndpoint=https://eastus.livediagnostics.monitor.azure.com/
```

### **2. Configurar Variables de Entorno**

```bash
# Navegar de vuelta al workspace
cd ..

# Exportar la variable de entorno
export APPLICATIONINSIGHTS_CONNECTION_STRING="tu-connection-string-aquí"

# Verificar que se configuró correctamente
echo $APPLICATIONINSIGHTS_CONNECTION_STRING
```

#### **💾 Para persistir en la sesión:**

Crear archivo `.env` (opcional):

```bash
# Crear archivo .env
cat > .env << EOF
APPLICATIONINSIGHTS_CONNECTION_STRING="tu-connection-string-aquí"
EOF

# Cargar variables desde .env
source .env
```

### **3. Verificar Configuración**

```bash
# Navegar al directorio de la aplicación
cd src

# Ejecutar script de verificación
python config.py
```

#### **📊 Salida esperada:**
```
🔧 Configuración actual:
   Connection String: ✅ Configurado
```

---

## 📦 Estructura de la Aplicación

### **🗂️ Archivos principales:**

```
src/
├── app.py              # Aplicación principal
├── config.py           # Configuración y verificación
├── requirements.txt    # Dependencias Python
└── .env               # Variables de entorno (opcional)
```

### **📄 Descripción de archivos:**

#### **`app.py` - Aplicación Principal:**
- **ECommerceSimulator:** Clase que simula operaciones
- **Logging configurado:** OpenCensus + Azure handler
- **Datos estructurados:** Custom dimensions en logs
- **Error simulation:** 10% de operaciones fallan

#### **`config.py` - Configuración:**
- **Verificación de variables:** Connection string
- **Debugging helpers:** Info de configuración
- **Validation:** Formato correcto de variables

#### **`requirements.txt` - Dependencias:**
```txt
opencensus-ext-azure==1.1.11    # Azure telemetry
opencensus-context==0.1.3       # Context management
python-dotenv==1.0.0            # Environment variables
flask==3.0.0                    # Web framework (opcional)
```

---

## 🚀 Ejecutar la Aplicación

### **1. Verificar Dependencias**

```bash
# Verificar que las dependencias están instaladas
pip list | grep opencensus

# Si no están, instalar
pip install -r requirements.txt
```

### **2. Test de Conectividad**

```bash
# Test básico de configuración
python -c "
from config import get_connection_string
cs = get_connection_string()
print('✅ Connection string OK' if cs else '❌ No connection string')
"
```

### **3. Ejecutar la Demo**

```bash
# Ejecutar aplicación
python app.py
```

#### **📊 Salida esperada:**
```
🚀 Iniciando Azure Log Analytics Workshop Demo
==================================================
✅ Logging configurado correctamente
🔗 Enviando logs a Azure Log Analytics...

🔄 Generando operaciones (Ctrl+C para detener)...
📡 Los logs se están enviando a Azure Log Analytics
⏱️  Espera 2-3 minutos para ver los datos en Azure Portal

✅ OK [  1] alice: user_login
✅ OK [  2] bob: product_search
❌ ERROR [  3] charlie: payment_process
✅ OK [  4] diana: product_view
...
```

### **4. Interpretar la Salida**

#### **🟢 Operación Exitosa:**
```
✅ OK [  5] eve: add_to_cart
```
- **Usuario:** eve
- **Operación:** add_to_cart
- **Resultado:** Exitosa (SeverityLevel: 1)

#### **🔴 Operación con Error:**
```
❌ ERROR [  6] alice: checkout
```
- **Usuario:** alice
- **Operación:** checkout
- **Resultado:** Error (SeverityLevel: 3)
- **Detalles adicionales:** Error code, category, message

---

## 🔍 Datos Enviados a Azure

### **📊 Estructura de Logs - Operación Exitosa:**

```json
{
  "timestamp": "2025-01-15T10:30:45.123Z",
  "message": "Operation successful: product_view",
  "severityLevel": 1,
  "customDimensions": {
    "operation": "product_view",
    "user_id": "bob",
    "session_id": "sess_12345",
    "product_id": 3,
    "product_name": "Keyboard",
    "product_price": 79.99
  }
}
```

### **📊 Estructura de Logs - Error:**

```json
{
  "timestamp": "2025-01-15T10:30:50.456Z",
  "message": "Operation failed: payment_process",
  "severityLevel": 3,
  "customDimensions": {
    "operation": "payment_process",
    "user_id": "charlie",
    "session_id": "sess_67890",
    "error_code": "PAYMENT_FAILED",
    "error_message": "Payment processing failed",
    "error_category": "payment",
    "payment_method": "credit_card",
    "amount": 149.99
  }
}
```

### **🎯 Tipos de Errores Simulados:**

1. **DB_TIMEOUT** (category: database)
2. **PAYMENT_FAILED** (category: payment)
3. **INVALID_SESSION** (category: authentication)
4. **PRODUCT_UNAVAILABLE** (category: inventory)
5. **RATE_LIMIT_EXCEEDED** (category: security)

---

## ⏱️ Timing y Latencia

### **📡 Envío a Azure:**

- **Intervalo:** 1-3 segundos entre operaciones
- **Batching:** OpenCensus agrupa logs automáticamente
- **Latencia:** 30 segundos - 2 minutos para aparecer en Azure

### **🔄 Flujo de Datos:**

```
Python App → OpenCensus → Application Insights → Log Analytics
    (instantáneo)  (30s)           (30s)            (disponible)
```

### **⏳ Tiempos esperados:**

- **Logs en consola:** Inmediato
- **Datos en Application Insights:** 30-60 segundos
- **Datos en Log Analytics:** 1-2 minutos
- **Disponibles para queries:** 2-3 minutos

---

## 📊 Monitoreo en Tiempo Real

### **1. Ver en Azure Portal - Application Insights:**

1. **Ir a Azure Portal**
2. **Resource Group:** `rg-log-analytics-workshop`
3. **Application Insights:** `ai-workshop`
4. **Live Metrics Stream:** Ver datos en tiempo real

### **2. Ver en Azure Portal - Log Analytics:**

1. **Log Analytics Workspace:** `law-workshop`
2. **Logs:** Ejecutar queries básicas
3. **Monitoring:** Dashboard automático

---

## 🔧 Personalización de la Demo

### **⚙️ Modificar Frecuencia de Logs:**

En `app.py`, línea ~150:

```python
# Cambiar el intervalo entre operaciones
time.sleep(random.uniform(1, 3))  # 1-3 segundos

# Para más logs frecuentes:
time.sleep(random.uniform(0.5, 1))  # 0.5-1 segundo

# Para menos logs:
time.sleep(random.uniform(5, 10))  # 5-10 segundos
```

### **⚙️ Modificar Rate de Errores:**

En `app.py`, línea ~135:

```python
# Cambiar probabilidad de error
is_error = simulator.should_generate_error()  # Actual: 10%

# En la clase ECommerceSimulator:
def should_generate_error(self):
    return random.random() < 0.2  # Cambiar a 20% errores
```

### **⚙️ Agregar Nuevas Operaciones:**

```python
# En la clase ECommerceSimulator, agregar a self.operations:
self.operations = [
    'user_login',
    'product_search',
    'product_view',
    'add_to_cart',
    'checkout',
    'payment_process',
    'user_logout',
    'wishlist_add',      # Nueva operación
    'review_product',    # Nueva operación
    'support_ticket'     # Nueva operación
]
```

---

## 🚨 Troubleshooting

### **❌ Error: "Connection string not configured"**

#### **🔍 Diagnóstico:**
```bash
python config.py
```

#### **🛠️ Soluciones:**
```bash
# 1. Verificar variable de entorno
echo $APPLICATIONINSIGHTS_CONNECTION_STRING

# 2. Re-obtener desde Terraform
cd terraform && terraform output -raw application_insights_connection_string

# 3. Re-exportar variable
export APPLICATIONINSIGHTS_CONNECTION_STRING="nueva-connection-string"
```

### **❌ Error: "ModuleNotFoundError: No module named 'opencensus'"**

#### **🛠️ Solución:**
```bash
# Verificar que estás en el devcontainer
whoami  # debería ser "vscode"

# Instalar dependencias
pip install -r src/requirements.txt

# Verificar instalación
pip list | grep opencensus
```

### **❌ La aplicación ejecuta pero no veo datos en Azure**

#### **🔍 Verificaciones:**

1. **Connection string correcta:**
   ```bash
   python -c "from config import get_connection_string; print(get_connection_string())"
   ```

2. **Conectividad de red:**
   ```bash
   curl -I https://dc.applicationinsights.azure.com/
   ```

3. **Esperar el tiempo de latencia:** 2-3 minutos mínimo

4. **Verificar en Application Insights Live Metrics**

### **❌ Logs llegan pero con campos faltantes**

#### **🔍 Causa:**
Estructura de `custom_dimensions` incorrecta

#### **🛠️ Solución:**
Verificar que todos los campos en `operation_data` son serializables:
- Strings, numbers, booleans ✅
- Objects, arrays complejos ❌

---

## 📊 Métricas y Estadísticas

### **📈 Al finalizar la sesión:**

La aplicación mostrará estadísticas:

```
📊 Estadísticas de la sesión:
   Total operaciones: 150
   Operaciones exitosas: 135
   Errores: 15
   Tasa de éxito: 90.0%
```

### **🎯 Volumen de datos típico:**

- **5 minutos:** ~100-150 logs
- **1 hora:** ~1,200-1,800 logs
- **Tamaño:** ~500KB de datos

---

## 🧪 Testing Avanzado

### **🔬 Generar Burst de Errores:**

```python
# Modificar temporalmente en app.py para testing
def should_generate_error(self):
    return random.random() < 0.8  # 80% errores por unos minutos
```

### **🔬 Generar Datos para Usuario Específico:**

```python
# Modificar para generar solo logs de un usuario
self.users = ['test-user']  # Solo un usuario para testing
```

### **🔬 Stress Test:**

```python
# Reducir tiempo entre operaciones para stress test
time.sleep(0.1)  # 10 operaciones por segundo
```

---

## ➡️ Siguiente Paso

Una vez que la aplicación esté ejecutándose y enviando logs:

**👉 Continúa con: [04-exploring-logs.md](04-exploring-logs.md)**

---

## 📚 Referencias Técnicas

### **🔗 Documentación:**
- [OpenCensus Python Azure](https://github.com/census-instrumentation/opencensus-python/tree/master/contrib/opencensus-ext-azure)
- [Application Insights Python](https://docs.microsoft.com/azure/azure-monitor/app/python)
- [Custom Telemetry](https://docs.microsoft.com/azure/azure-monitor/app/api-custom-events-metrics)

### **🛠️ Herramientas de Debug:**
- **Application Insights Live Metrics:** Datos en tiempo real
- **Application Insights Search:** Buscar eventos específicos
- **Log Analytics Queries:** Análisis avanzado

**¡Tu aplicación está enviando logs!** 🎉