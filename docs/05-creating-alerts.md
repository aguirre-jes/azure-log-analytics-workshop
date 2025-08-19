# 🚨 Creando Alertas en Azure Monitor

Este documento te guía paso a paso para crear alertas básicas basadas en consultas de Log Analytics, configurar acciones y gestionar notificaciones.

## 🎯 Objetivo

Aprender a crear alertas proactivas que notifiquen automáticamente cuando se detecten condiciones específicas en los logs, como errores frecuentes o comportamientos anómalos.

---

## 📋 Conceptos Fundamentales

### **🔧 Componentes de una Alerta:**

```
Alert Rule (Regla de Alerta)
├── 🎯 Scope (Alcance)
│   └── Log Analytics Workspace
├── 📊 Condition (Condición)
│   ├── Query (Consulta KQL)
│   ├── Threshold (Umbral)
│   └── Evaluation Period (Período de evaluación)
├── 🚨 Action (Acción)
│   ├── Action Group
│   └── Notification methods
└── ⚙️ Alert Details
    ├── Name & Description
    ├── Severity
    └── Auto-resolve settings
```

### **📊 Tipos de Alertas:**

1. **Log Search Alerts:** Basadas en consultas KQL
2. **Metric Alerts:** Basadas en métricas numéricas
3. **Activity Log Alerts:** Basadas en eventos de Azure
4. **Resource Health Alerts:** Estado de recursos Azure

**En este workshop nos enfocamos en Log Search Alerts.**

---

## 🚀 Crear tu Primera Alerta

### **1. Navegar a Log Analytics**

1. **Azure Portal** → Resource Groups → `rg-log-analytics-workshop`
2. **Log Analytics Workspace** → `law-workshop`
3. **Menú izquierdo** → Logs

### **2. Desarrollar la Query de la Alerta**

Primero desarrollamos y testemos la query que detectará la condición:

```kql
// Alerta: Más de 5 errores en los últimos 5 minutos
AppTraces
| where TimeGenerated > ago(5m)
| where SeverityLevel >= 3
| summarize ErrorCount = count()
```

#### **🧪 Test de la Query:**

```kql
// Test con ventana más amplia para verificar funcionamiento
AppTraces
| where TimeGenerated > ago(30m)
| where SeverityLevel >= 3
| summarize ErrorCount = count() by bin(TimeGenerated, 5m)
| order by TimeGenerated desc
```

### **3. Crear la Alert Rule**

1. **En la ventana de query**, después de ejecutar tu consulta
2. **Hacer clic en** "New Alert Rule" (arriba de los resultados)
3. **O alternativamente:** Monitor → Alerts → Create → Alert rule

#### **📋 Configuración Step-by-Step:**

---

## 🎯 Configuración Detallada de Alert Rules

### **Paso 1: Scope (Alcance)**

```
Scope Configuration:
├── Resource Type: Log Analytics Workspace
├── Subscription: Tu suscripción
├── Resource Group: rg-log-analytics-workshop
└── Resource: law-workshop
```

**✅ Ya está pre-configurado si vienes desde Log Analytics**

### **Paso 2: Condition (Condición)**

#### **🔍 Signal Configuration:**

1. **Signal Type:** Logs
2. **Signal Name:** Custom log search

#### **📊 Search Query:**

```kql
AppTraces
| where TimeGenerated > ago(5m)
| where SeverityLevel >= 3
| summarize AggregatedValue = count()
```

#### **⚙️ Alert Logic:**

```
Based on: Number of results
Condition: Greater than
Threshold value: 5

Period: 5 minutes
Frequency: 5 minutes
```

**🎯 Significado:**
- Evalúa la query cada 5 minutos
- Mira los logs de los últimos 5 minutos
- Si encuentra más de 5 errores → dispara alerta

### **Paso 3: Action Groups**

#### **🔄 ¿Qué es un Action Group?**
Conjunto de acciones que se ejecutan cuando se dispara una alerta:
- Email notifications
- SMS
- Push notifications
- Azure Functions
- Logic Apps
- Webhooks

#### **📧 Configurar Email Notification:**

1. **Create New Action Group**
2. **Basics:**
   ```
   Action group name: ag-workshop-alerts
   Display name: Workshop Alerts
   Resource group: rg-log-analytics-workshop
   ```

3. **Notifications:**
   ```
   Notification type: Email/SMS message/Push/Voice
   Name: Admin Email
   Details: tu-email@ejemplo.com
   ```

4. **Actions (Opcional):**
   - Azure Function
   - Logic App
   - Webhook
   - ITSM Connector

### **Paso 4: Alert Rule Details**

```
Alert rule name: High Error Rate - Workshop
Description: Alerta cuando hay más de 5 errores en 5 minutos
Severity: 2 - Warning
Resource group: rg-log-analytics-workshop
Enable upon creation: Yes
Auto-resolve alerts: Yes
```

### **Paso 5: Review y Create**

1. **Review** todas las configuraciones
2. **Validate** que la query sea correcta
3. **Create** la alert rule

---

## 📊 Alertas Útiles para el Workshop

### **🚨 Alerta 1: High Error Rate**

```kql
// Detectar cuando hay muchos errores
AppTraces
| where TimeGenerated > ago(5m)
| where SeverityLevel >= 3
| summarize AggregatedValue = count()
```

**Configuración:**
- Threshold: > 5
- Period: 5 minutes
- Frequency: 5 minutes
- Severity: Warning (2)

### **🚨 Alerta 2: Error Rate Percentage**

```kql
// Detectar cuando el % de errores es alto
AppTraces
| where TimeGenerated > ago(10m)
| summarize 
    Total = count(),
    Errors = countif(SeverityLevel >= 3)
| extend ErrorRate = (Errors * 100.0) / Total
| project AggregatedValue = ErrorRate
```

**Configuración:**
- Threshold: > 20 (20% error rate)
- Period: 10 minutes
- Frequency: 5 minutes
- Severity: Warning (2)

### **🚨 Alerta 3: Specific Error Type**

```kql
// Detectar errores específicos de payment
AppTraces
| where TimeGenerated > ago(15m)
| where SeverityLevel >= 3
| extend error_category = tostring(Properties.error_category)
| where error_category == "payment"
| summarize AggregatedValue = count()
```

**Configuración:**
- Threshold: > 2
- Period: 15 minutes
- Frequency: 5 minutes
- Severity: Critical (0)

### **🚨 Alerta 4: No Activity Detection**

```kql
// Detectar cuando no hay logs (aplicación caída)
AppTraces
| where TimeGenerated > ago(10m)
| summarize AggregatedValue = count()
```

**Configuración:**
- Threshold: < 1 (menos de 1 log)
- Period: 10 minutes
- Frequency: 5 minutes
- Severity: Critical (0)

---

## 🔧 Configuración Avanzada de Alertas

### **⏱️ Frequency vs Period**

```
Frequency: Cada cuánto evalúa la query
Period: Ventana de tiempo de datos a evaluar

Ejemplos:
├── Frequency: 5min, Period: 5min  → Evalúa cada 5min los últimos 5min
├── Frequency: 5min, Period: 15min → Evalúa cada 5min los últimos 15min
└── Frequency: 1min, Period: 5min  → Evalúa cada 1min los últimos 5min
```

### **🎯 Dimensiones (Split by Dimensions)**

Permite crear alertas granulares:

```kql
// Alerta por usuario específico
AppTraces
| where TimeGenerated > ago(10m)
| where SeverityLevel >= 3
| extend user_id = tostring(Properties.user_id)
| where isnotempty(user_id)
| summarize AggregatedValue = count() by user_id
```

**Configuración:**
- Split by dimensions: user_id
- Threshold: > 3
- **Resultado:** Una alerta separada por cada usuario

### **🔄 Aggregation Settings**

```
Aggregation Type:
├── Count          → count()
├── Average        → avg(column)
├── Minimum        → min(column)
├── Maximum        → max(column)
├── Total          → sum(column)
└── Standard Deviation → stdev(column)
```

### **⚙️ Advanced Options**

#### **Auto-resolution:**
```
Auto-resolve alerts: Yes/No
└── Si Yes: La alerta se resuelve automáticamente cuando la condición ya no se cumple
```

#### **Mute Actions:**
```
Mute actions for: 1 hour
└── Después de disparar, no envía más notificaciones por 1 hora
```

---

## 📧 Gestión de Action Groups

### **📋 Tipos de Notifications:**

#### **📨 Email/SMS:**
```
Email: tu-email@ejemplo.com
SMS: +1234567890
Common Schema: Yes (Recommended)
```

#### **📱 Push Notifications:**
```
Azure Mobile App: Yes
Account: usuario@azure.com
```

#### **🔊 Voice Call:**
```
Country/Region: United States
Phone number: +1234567890
```

### **⚡ Actions Avanzadas:**

#### **🔗 Webhook:**
```json
{
  "webhookUrl": "https://tu-servidor.com/webhook",
  "customProperties": {
    "severity": "high",
    "environment": "workshop"
  }
}
```

#### **⚙️ Azure Function:**
```
Function App: func-workshop-alerts
Function: ProcessAlert
```

#### **🔄 Logic App:**
```
Logic App: logic-alert-processor
Resource Group: rg-log-analytics-workshop
```

---

## 🧪 Testing de Alertas

### **1. Triggering Manual**

Para testear tu alerta, genera errores intencionalmente:

```python
# En tu aplicación Python (app.py), modificar temporalmente:
def should_generate_error(self):
    return random.random() < 0.8  # 80% errores por unos minutos
```

### **2. Verificar en Azure Portal**

1. **Monitor → Alerts → Alert rules**
2. **Buscar tu alerta:** "High Error Rate - Workshop"
3. **Ver history:** Fired alerts

### **3. Verificar Notificaciones**

#### **📧 Email Notification:**
```
Subject: Microsoft Azure Alert - High Error Rate - Workshop has been activated
Body: 
- Alert Rule: High Error Rate - Workshop
- Severity: Warning
- Condition: AggregatedValue > 5.0
- Actual Value: 12
- Time: 2025-01-15 14:30:45 UTC
```

#### **📊 Portal Notifications:**
- Bell icon (🔔) en Azure Portal
- Alert details con query results
- Links to Log Analytics

---

## 📊 Monitoreo de Alertas

### **🔍 Alert Management**

#### **Ver Alertas Activas:**
1. **Monitor → Alerts → Alert instances**
2. **Filtrar por:** Resource Group, Time Range, Severity
3. **Actions:** Acknowledge, Close, Change State

#### **Alert States:**
```
States:
├── New        → Recién disparada
├── Acknowledged → Reconocida por alguien
└── Closed     → Resuelta
```

### **📈 Alert Metrics**

```kql
// Query para ver estadísticas de alertas
AlertsManagementResources
| where type == "microsoft.alertsmanagement/alerts"
| where properties.essentials.startDateTime > ago(7d)
| extend 
    AlertName = properties.essentials.alertRule,
    Severity = properties.essentials.severity,
    State = properties.essentials.alertState
| summarize AlertCount = count() by AlertName, Severity, State
| order by AlertCount desc
```

### **📊 Dashboard de Alertas**

Crear un workbook con:

```kql
// Widget 1: Alertas por severidad (últimos 7 días)
AlertsManagementResources
| where type == "microsoft.alertsmanagement/alerts"
| where properties.essentials.startDateTime > ago(7d)
| extend Severity = properties.essentials.severity
| summarize count() by Severity
| render piechart

// Widget 2: Timeline de alertas
AlertsManagementResources
| where type == "microsoft.alertsmanagement/alerts"
| where properties.essentials.startDateTime > ago(24h)
| extend StartTime = properties.essentials.startDateTime
| summarize AlertCount = count() by bin(StartTime, 1h)
| render timechart
```

---

## 🔧 Troubleshooting de Alertas

### **❌ "Alert not firing"**

#### **🔍 Diagnóstico:**

1. **Verificar query manualmente:**
   ```kql
   // Ejecutar la query de la alerta directamente
   AppTraces
   | where TimeGenerated > ago(5m)
   | where SeverityLevel >= 3
   | summarize AggregatedValue = count()
   ```

2. **Verificar Alert Rule configuration:**
   - Scope correcto
   - Query sintácticamente correcta
   - Threshold apropiado
   - Frequency/Period configurados

3. **Verificar data availability:**
   ```kql
   // ¿Hay datos recientes?
   AppTraces
   | where TimeGenerated > ago(1h)
   | count
   ```

### **❌ "Too many alerts firing"**

#### **🛠️ Soluciones:**

1. **Ajustar threshold:**
   ```
   Antes: > 5 errores
   Después: > 10 errores
   ```

2. **Aumentar period:**
   ```
   Antes: 5 minutos
   Después: 15 minutos
   ```

3. **Configurar mute actions:**
   ```
   Mute actions for: 1 hour
   ```

### **❌ "Notifications not received"**

#### **🔍 Verificaciones:**

1. **Action Group configurado correctamente**
2. **Email address correcto**
3. **Check spam folder**
4. **Verify in Activity Log:**
   ```
   Monitor → Activity Log
   Filter by: Action Groups
   ```

### **❌ "Query timeout/performance issues"**

#### **🛠️ Optimizaciones:**

```kql
// ❌ Query lenta
AppTraces
| where SeverityLevel >= 3
| where TimeGenerated > ago(5m)

// ✅ Query optimizada
AppTraces
| where TimeGenerated > ago(5m)  // Filtro temporal primero
| where SeverityLevel >= 3
| summarize AggregatedValue = count()
```

---

## 📋 Best Practices para Alertas

### **🎯 Naming Convention:**

```
Alert Rule Names:
├── [Environment]-[Component]-[Condition]
├── PROD-WebApp-HighErrorRate
├── DEV-API-SlowResponse
└── Workshop-App-NoActivity
```

### **📊 Severity Guidelines:**

```
Severity Levels:
├── 0 - Critical  → Sistema caído, pérdida de servicio
├── 1 - Error     → Funcionalidad afectada, require atención
├── 2 - Warning   → Problema potencial, monitorear
├── 3 - Informational → FYI, no requiere acción inmediata
└── 4 - Verbose   → Detalles técnicos, debugging
```

### **⏱️ Timing Best Practices:**

```
Para diferentes tipos de issues:
├── Critical issues: 1-2min frequency, 5min period
├── Error rates: 5min frequency, 10min period
├── Performance: 15min frequency, 30min period
└── Business metrics: 1h frequency, 4h period
```

### **🔄 Alert Lifecycle:**

1. **Design:** Query + threshold thoughtful
2. **Test:** Verify firing conditions
3. **Deploy:** Enable with proper action group
4. **Monitor:** Check for false positives/negatives
5. **Tune:** Adjust thresholds based on experience
6. **Maintain:** Regular review and updates

---

## 🎯 Alertas Avanzadas

### **🔍 Multi-dimensional Alerts:**

```kql
// Alerta por combinación de usuario + tipo de error
AppTraces
| where TimeGenerated > ago(15m)
| where SeverityLevel >= 3
| extend 
    user_id = tostring(Properties.user_id),
    error_category = tostring(Properties.error_category)
| where isnotempty(user_id) and isnotempty(error_category)
| summarize AggregatedValue = count() by user_id, error_category
```

### **📊 Composite Alerts:**

Combinar múltiples condiciones:

```kql
// Alerta cuando hay errores Y baja actividad
let ErrorCount = AppTraces
| where TimeGenerated > ago(10m)
| where SeverityLevel >= 3
| count;
let TotalCount = AppTraces
| where TimeGenerated > ago(10m)
| count;
ErrorCount
| extend TotalLogs = toscalar(TotalCount)
| extend ErrorRate = Count * 100.0 / TotalLogs
| where Count > 3 and TotalLogs < 50  // Errores altos Y actividad baja
| project AggregatedValue = ErrorRate
```

### **🎛️ Dynamic Thresholds:**

```kql
// Threshold basado en baseline histórico
let Baseline = AppTraces
| where TimeGenerated between(ago(7d) .. ago(1d))
| where SeverityLevel >= 3
| summarize HistoricalAvg = avg(todouble(1));
AppTraces
| where TimeGenerated > ago(10m)
| where SeverityLevel >= 3
| summarize CurrentErrors = count()
| extend Threshold = toscalar(Baseline) * 3  // 3x el promedio histórico
| where CurrentErrors > Threshold
| project