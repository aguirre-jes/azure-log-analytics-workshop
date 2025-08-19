# 🔍 Explorando Logs en Azure Log Analytics

Este documento te guía para explorar y analizar los logs enviados por tu aplicación usando Azure Log Analytics y KQL (Kusto Query Language).

## 🎯 Objetivo

Aprender a consultar, filtrar y visualizar los datos de logs usando KQL para obtener insights valiosos sobre el comportamiento de la aplicación.

---

## 🚀 Acceder a Log Analytics

### **1. Navegar al Portal**

1. **Abrir:** [portal.azure.com](https://portal.azure.com)
2. **Buscar:** Tu resource group `rg-log-analytics-workshop`
3. **Hacer clic en:** Log Analytics Workspace (`law-workshop`)
4. **En el menú izquierdo:** Logs

### **2. Interfaz de Log Analytics**

```
Azure Log Analytics - Logs
├── 📊 Query Editor (centro)
├── 📋 Tables Panel (izquierda)
├── ⏱️ Time Range Selector (arriba)
└── 🎯 Results Panel (abajo)
```

---

## 🗃️ Entendiendo las Tablas de Datos

### **📊 Principales tablas para nuestro workshop:**

#### **`AppTraces` - Logs de aplicación**
- **Contiene:** Todos los logs enviados desde Python
- **Campos clave:**
  - `TimeGenerated`: Timestamp del evento
  - `Message`: Mensaje del log
  - `SeverityLevel`: 1 (Info), 3 (Error)
  - `Properties`: Custom dimensions (JSON)

#### **`AppEvents` - Eventos custom**
- **Contiene:** Eventos específicos de aplicación
- **Uso:** Menos común en nuestro caso

#### **`AppExceptions` - Excepciones**
- **Contiene:** Excepciones no manejadas
- **Uso:** Errores críticos de aplicación

### **🔍 Verificar qué tablas tienen datos:**

```kql
// Ver todas las tablas con datos recientes
search "*" 
| where TimeGenerated > ago(2h)
| distinct $table 
| sort by $table asc
```

---

## 🚦 Primeras Consultas - Paso a Paso

### **1. Query Básica - Ver Todos los Logs**

```kql
AppTraces
| where TimeGenerated > ago(1h)
| project TimeGenerated, Message, SeverityLevel, Properties
| order by TimeGenerated desc
| limit 100
```

#### **📊 Resultado esperado:**
- Lista de logs ordenados por tiempo
- Mensajes como "Operation successful: product_view"
- Properties con datos JSON estructurados

### **2. Contar Logs por Severidad**

```kql
AppTraces
| where TimeGenerated > ago(1h)
| extend SeverityName = case(
    SeverityLevel == 1, "Information", 
    SeverityLevel == 3, "Error",
    "Other"
)
| summarize Count = count() by SeverityName
| order by Count desc
```

#### **📊 Resultado esperado:**
```
SeverityName    Count
Information     135
Error          15
```

### **3. Timeline de Actividad**

```kql
AppTraces
| where TimeGenerated > ago(1h)
| summarize count() by bin(TimeGenerated, 5m)
| render timechart
```

#### **📊 Resultado esperado:**
- Gráfico de líneas mostrando actividad cada 5 minutos
- Picos y valles según la actividad de la aplicación

---

## 🎯 Queries Funcionales Avanzadas

### **4. Top Operaciones Más Frecuentes**

```kql
AppTraces
| where TimeGenerated > ago(1h)
| extend operation = tostring(Properties.operation)
| where isnotempty(operation)
| summarize count() by operation
| order by count_ desc
| limit 10
```

### **5. Análisis de Errores por Categoría**

```kql
AppTraces
| where TimeGenerated > ago(2h) and SeverityLevel >= 3
| extend error_category = tostring(Properties.error_category)
| where isnotempty(error_category)
| summarize ErrorCount = count() by error_category
| render barchart
```

### **6. Actividad por Usuario**

```kql
AppTraces
| where TimeGenerated > ago(1h)
| extend user_id = tostring(Properties.user_id)
| where isnotempty(user_id)
| summarize 
    TotalOperations = count(),
    ErrorCount = countif(SeverityLevel >= 3),
    SuccessRate = round((count() - countif(SeverityLevel >= 3)) * 100.0 / count(), 1)
by user_id
| order by TotalOperations desc
```

### **7. Análisis de E-commerce - Productos Más Vistos**

```kql
AppTraces
| where TimeGenerated > ago(1h)
| extend operation = tostring(Properties.operation)
| extend product_name = tostring(Properties.product_name)
| where operation == "product_view" and isnotempty(product_name)
| summarize Views = count() by product_name
| order by Views desc
```

---

## 📊 Visualizaciones Disponibles

### **🎨 Tipos de gráficos (`render`):**

#### **`timechart` - Gráfico de líneas temporal:**
```kql
AppTraces
| where TimeGenerated > ago(4h)
| summarize count() by bin(TimeGenerated, 15m)
| render timechart
```

#### **`barchart` - Gráfico de barras:**
```kql
AppTraces
| where TimeGenerated > ago(1h) and SeverityLevel >= 3
| extend error_code = tostring(Properties.error_code)
| where isnotempty(error_code)
| summarize count() by error_code
| render barchart
```

#### **`piechart` - Gráfico circular:**
```kql
AppTraces
| where TimeGenerated > ago(1h)
| extend operation = tostring(Properties.operation)
| where isnotempty(operation)
| summarize count() by operation
| render piechart
```

#### **`columnchart` - Gráfico de columnas:**
```kql
AppTraces
| where TimeGenerated > ago(1h)
| extend user_id = tostring(Properties.user_id)
| where isnotempty(user_id)
| summarize count() by user_id
| render columnchart
```

---

## 🔬 Análisis Profundo - Casos de Uso Reales

### **8. Detección de Patrones de Error**

```kql
AppTraces
| where TimeGenerated > ago(2h) and SeverityLevel >= 3
| extend 
    user_id = tostring(Properties.user_id),
    error_category = tostring(Properties.error_category),
    operation = tostring(Properties.operation)
| summarize 
    ErrorCount = count(),
    UniqueUsers = dcount(user_id),
    Operations = make_set(operation)
by error_category
| order by ErrorCount desc
```

### **9. Análisis de Sesiones de Usuario**

```kql
AppTraces
| where TimeGenerated > ago(1h)
| extend 
    user_id = tostring(Properties.user_id),
    operation = tostring(Properties.operation),
    session_id = tostring(Properties.session_id)
| where isnotempty(user_id) and isnotempty(session_id)
| summarize 
    SessionDuration = max(TimeGenerated) - min(TimeGenerated),
    Operations = count(),
    UniqueOperations = dcount(operation),
    OperationsList = make_list(operation)
by user_id, session_id
| order by SessionDuration desc
```

### **10. Performance Analysis - Búsquedas**

```kql
AppTraces
| where TimeGenerated > ago(1h)
| extend 
    operation = tostring(Properties.operation),
    search_term = tostring(Properties.search_term),
    results_count = toint(Properties.results_count)
| where operation == "product_search"
| summarize 
    Searches = count(),
    AvgResults = avg(results_count),
    MaxResults = max(results_count),
    MinResults = min(results_count)
by search_term
| where Searches > 1
| order by Searches desc
```

---

## 🎛️ Funciones KQL Útiles

### **📅 Funciones de Tiempo:**
```kql
// Últimas 4 horas
| where TimeGenerated > ago(4h)

// Hoy desde medianoche
| where TimeGenerated >= startofday(now())

// Entre dos fechas específicas
| where TimeGenerated between(datetime(2025-01-15 10:00) .. datetime(2025-01-15 15:00))

// Agrupar por intervalos
| summarize count() by bin(TimeGenerated, 1h)  // Por hora
| summarize count() by bin(TimeGenerated, 15m) // Por 15 minutos
```

### **🔢 Funciones de Agregación:**
```kql
// Contar
| summarize count()
| summarize count() by column_name

// Promedios
| summarize avg(numeric_column)

// Valores únicos
| summarize dcount(column_name)

// Estadísticas completas
| summarize 
    Count = count(),
    Avg = avg(numeric_column),
    Min = min(numeric_column),
    Max = max(numeric_column),
    StdDev = stdev(numeric_column)
```

### **🎯 Funciones de Cadenas:**
```kql
// Extraer de JSON
| extend operation = tostring(Properties.operation)
| extend amount = todouble(Properties.amount)

// Filtros de texto
| where Message contains "error"
| where Message startswith "Operation"
| where Message matches regex ".*login.*"

// Case-insensitive
| where Message contains_cs "ERROR"  // Case sensitive
| where Message !contains "success"  // No contiene
```

---

## 🚨 Queries de Monitoreo y Alertas

### **11. Health Check - Rate de Errores**

```kql
AppTraces
| where TimeGenerated > ago(15m)
| summarize 
    Total = count(),
    Errors = countif(SeverityLevel >= 3)
| extend ErrorRate = round((Errors * 100.0) / Total, 2)
| project ErrorRate, Total, Errors
```

### **12. Spike Detection - Volumen de Logs**

```kql
AppTraces
| where TimeGenerated > ago(1h)
| summarize LogCount = count() by bin(TimeGenerated, 5m)
| extend AvgCount = avg(LogCount)
| where LogCount > AvgCount * 2  // Spikes > 200% del promedio
| project TimeGenerated, LogCount, AvgCount
```

### **13. Error Burst Detection**

```kql
AppTraces
| where TimeGenerated > ago(30m) and SeverityLevel >= 3
| summarize ErrorCount = count() by bin(TimeGenerated, 1m)
| where ErrorCount > 5  // Más de 5 errores por minuto
| project TimeGenerated, ErrorCount
```

---

## 💡 Tips y Mejores Prácticas

### **⚡ Performance:**

1. **Usar filtros de tiempo primero:**
   ```kql
   // ✅ Correcto
   AppTraces
   | where TimeGenerated > ago(1h)  // Filtrar tiempo primero
   | where SeverityLevel >= 3
   
   // ❌ Lento
   AppTraces
   | where SeverityLevel >= 3
   | where TimeGenerated > ago(1h)  // Filtrar tiempo después
   ```

2. **Limitar resultados:**
   ```kql
   AppTraces
   | where TimeGenerated > ago(1h)
   | limit 1000  // Evitar queries que retornen millones de filas
   ```

3. **Usar `project` para seleccionar columnas específicas:**
   ```kql
   AppTraces
   | where TimeGenerated > ago(1h)
   | project TimeGenerated, Message, Properties.operation  // Solo columnas necesarias
   ```

### **🎯 Debugging de Queries:**

```kql
// Verificar estructura de datos
AppTraces
| where TimeGenerated > ago(1h)
| take 1
| evaluate bag_unpack(Properties)  // Ver todas las propiedades

// Ver tipos de datos
AppTraces
| where TimeGenerated > ago(1h)
| take 1
| project getschema()
```

### **📊 Queries Modulares:**

```kql
// Definir variables para reutilizar
let timeRange = ago(1h);
let errorThreshold = 3;
AppTraces
| where TimeGenerated > timeRange and SeverityLevel >= errorThreshold
| summarize count() by bin(TimeGenerated, 5m)
```

---

## 🔍 Búsqueda y Filtrado Avanzado

### **🔎 Search vs Where:**

```kql
// Search - busca en todas las columnas
AppTraces
| where TimeGenerated > ago(1h)
| search "payment"  // Busca "payment" en cualquier campo

// Where - filtro específico
AppTraces
| where TimeGenerated > ago(1h)
| where Properties.operation == "payment_process"  // Filtro específico
```

### **🎛️ Filtros Complejos:**

```kql
AppTraces
| where TimeGenerated > ago(1h)
| where (SeverityLevel >= 3 and Properties.error_category == "payment")
    or (Properties.operation in ("checkout", "payment_process"))
| extend user_id = tostring(Properties.user_id)
| where user_id !in ("test", "admin")  // Excluir usuarios de test
```

---

## 🎨 Personalizar y Exportar

### **💾 Guardar Queries:**

1. **En Log Analytics:** Pin to Dashboard
2. **En Azure Portal:** Save as Function
3. **Exportar a:** Excel, CSV, Power BI

### **📊 Crear Workbooks:**

1. **Azure Monitor > Workbooks**
2. **New > Empty Workbook**
3. **Add Query > Paste KQL**
4. **Configure Visualization**

---

## 🚨 Troubleshooting de Queries

### **❌ "No data found"**

#### **🔍 Diagnóstico:**
```kql
// Verificar si hay datos en general
AppTraces
| where TimeGenerated > ago(24h)
| count

// Verificar estructura
AppTraces
| where TimeGenerated > ago(1h)
| take 1
```

### **❌ "Syntax error"**

#### **🛠️ Errores comunes:**
```kql
// ❌ Incorrecto - pipes sin continuación
AppTraces
| where TimeGenerated > ago(1h)
|  // Línea vacía causa error

// ✅ Correcto
AppTraces
| where TimeGenerated > ago(1h)
| summarize count()

// ❌ Comillas incorrectas
| where operation == 'login'  // Usar comillas dobles

// ✅ Correcto
| where operation == "login"
```

### **❌ "Column not found"**

#### **🔍 Verificar estructura:**
```kql
AppTraces
| where TimeGenerated > ago(1h)
| take 1