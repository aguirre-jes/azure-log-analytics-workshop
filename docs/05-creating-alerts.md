## 🚀 Crear una Alert Rule Basada en KQL

### 1. Desarrollar la Consulta KQL

Ejemplo para detectar errores recientes:

```kql
AppTraces
| where TimeGenerated > ago(5m)
| where SeverityLevel >= 3
| summarize AggregatedValue = count()
```

- **AggregatedValue** será el campo que Azure usará como medida para la alerta.

---

### 2. Crear la Regla de Alerta en Azure Portal

1. **Ejecuta la consulta en Log Analytics** y haz clic en **"New alert rule"**.
2. **Scope:**  
   - Selecciona el Log Analytics Workspace (por defecto si vienes desde Logs).
3. **Condition:**  
   - **Measurement:** Azure detecta automáticamente el campo de agregación (`AggregatedValue`).
   - **Aggregation type:** Count (o el tipo que uses en tu consulta).
   - **Aggregation granularity:** 1 minute o el valor que prefieras.
   - **Split by dimensions:**  
     - Por defecto: **Don't split** (la alerta se aplica a todo el workspace).
     - Si quieres dividir por dimensión (por ejemplo, usuario), agrega una columna en tu consulta:
       ```kql
       AppTraces
       | where TimeGenerated > ago(5m)
       | where SeverityLevel >= 3
       | extend user_id = tostring(Properties.user_id)
       | where isnotempty(user_id)
       | summarize AggregatedValue = count() by user_id
       ```
     - Luego selecciona `user_id` como dimensión en el portal.
   - **Resource ID column:**  
     - En la mayoría de los casos, no es necesario. Si tu tabla no tiene `ResourceId` ni `$_ResourceId`, la alerta será global al workspace.
4. **Alert logic:**  
   - **Operator:** Greater than
   - **Threshold value:** 5 (o el valor que prefieras)
   - **Frequency of evaluation:** 1 minute (o el valor que prefieras)
   - **Period (lookback window):** 5 minutes

---

### 3. Configurar Action Group y Detalles

- **Action Group:**  
  - Selecciona ag-workshop o crea un grupo de acción (email, SMS, webhook, etc.).
- **Alert rule name:**  
  - Ejemplo: `High Error Rate - Workshop`
- **Description:**  
  - Ejemplo: `Alerta cuando hay más de 5 errores en 5 minutos`
- **Severity:**  
  - Ejemplo: `2 - Warning`
- **Enable upon creation:**  
  - Yes

---

### ℹ️ Notas y Buenas Prácticas

- Si tu consulta **no incluye una columna de tipo Resource ID o dimensión**, la alerta se aplicará a todo el workspace.  
- Para ver las columnas disponibles en tu tabla, ejecuta:
  ```kql
  AppTraces | getschema
  ```
- Si necesitas dividir la alerta por alguna dimensión (usuario, tipo de error, etc.), agrégala explícitamente en tu consulta con `summarize ... by <dimension>`.
- El mensaje "This query doesn't return an Azure resource ID column..." es solo informativo y no es un error.

---
