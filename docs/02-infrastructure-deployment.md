# 🏗️ Deploy de Infraestructura con Terraform

Este documento te guía para desplegar la infraestructura de Azure necesaria para el workshop usando Infrastructure as Code.

## 🎯 Objetivo

Crear automáticamente todos los recursos Azure necesarios usando Terraform, incluyendo Log Analytics Workspace, Application Insights y alertas básicas.

---

## 🏛️ Arquitectura de la Infraestructura

### **📋 Recursos que se crearán:**

```
Azure Subscription
└── Resource Group: rg-log-analytics-workshop
    ├── 📊 Log Analytics Workspace
    │   ├── Retention: 30 days
    │   └── SKU: PerGB2018
    ├── 📈 Application Insights
    │   ├── Linked to: Log Analytics Workspace
    │   └── Type: web
    ├── 🚨 Action Group
    │   └── Email notification
    └── ⚠️  Alert Rule
        ├── Query: Error rate > 5 in 5 minutes
        └── Action: Send email
```

### **💰 Costo estimado:**
- Log Analytics: ~$2/día
- Application Insights: ~$1/día
- **Total: ~$3 USD/día**

---

## 🚀 Proceso de Deployment

### **1. Verificar el Entorno**

Asegúrate de estar en el devcontainer:

```bash
# Verificar que estás en el container
whoami                    # debería ser "vscode"
pwd                      # debería ser "/workspace"

# Verificar herramientas
terraform --version      # Terraform v1.x.x
az --version            # Azure CLI 2.x.x
```

### **2. Login a Azure**

```bash
# Login interactivo
az login

# Verificar la suscripción activa
az account show --query "name" -o tsv

# Si tienes múltiples suscripciones, configurar la correcta
az account set --subscription "nombre-o-id-de-tu-suscripcion"
```

### **3. Obtener tu Subscription ID**

```bash
# Obtener subscription ID
az account show --query "id" -o tsv

# Ejemplo de salida:
# 12345678-1234-1234-1234-123456789012
```

**💾 Guarda este ID, lo necesitarás en el siguiente paso.**

### **4. Configurar Variables de Terraform**

```bash
# Navegar al directorio de Terraform
cd terraform

# Copiar template de variables
cp terraform.tfvars.example terraform.tfvars

# Editar el archivo
code terraform.tfvars
```

#### **📝 Contenido del archivo `terraform.tfvars`:**

```hcl
# Azure Subscription ID (requerido)
subscription_id = "12345678-1234-1234-1234-123456789012"

# Email para notificaciones de alertas (requerido)
admin_email = "tu-email@ejemplo.com"

# Opcional: personalizar nombres de recursos
resource_group_name = "rg-log-analytics-workshop"
location = "East US"
log_analytics_workspace_name = "law-workshop"
application_insights_name = "ai-workshop"

# Opcional: agregar prefix para nombres únicos
prefix = "tu-nombre"
```

> **🔒 Importante:** No subas `terraform.tfvars` a git, contiene información sensible.

---

## 🔧 Comandos de Terraform

### **1. Inicializar Terraform**

```bash
terraform init
```

#### **📊 Salida esperada:**
```
Initializing the backend...
Initializing provider plugins...
- Finding hashicorp/azurerm versions matching "~> 3.0"...
- Installing hashicorp/azurerm v3.x.x...

Terraform has been successfully initialized!
```

### **2. Validar la Configuración**

```bash
# Validar sintaxis
terraform validate

# Formatear código
terraform fmt

# Verificar configuración
terraform plan
```

#### **📊 Plan Output esperado:**
```
Plan: 4 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + application_insights_connection_string = (sensitive value)
  + log_analytics_workspace_id = (known after apply)
  + resource_group_name = "rg-log-analytics-workshop"
```

### **3. Desplegar Infraestructura**

```bash
terraform apply
```

**⚠️ Terraform te pedirá confirmación:**
```
Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes
```

#### **📊 Salida de éxito:**
```
Apply complete! Resources: 4 added, 0 changed, 0 destroyed.

Outputs:
application_insights_connection_string = <sensitive>
log_analytics_workspace_id = "/subscriptions/xxx/resourceGroups/rg-log-analytics-workshop/providers/Microsoft.OperationalInsights/workspaces/law-workshop"
resource_group_name = "rg-log-analytics-workshop"
```

---

## 🔍 Verificación del Deployment

### **1. Verificar Outputs de Terraform**

```bash
# Ver todos los outputs
terraform output

# Ver connection string (será usado en la aplicación)
terraform output -raw application_insights_connection_string
```

### **2. Verificar en Azure Portal**

1. **Ir a [portal.azure.com](https://portal.azure.com)**
2. **Buscar tu Resource Group:** `rg-log-analytics-workshop`
3. **Verificar recursos creados:**
   - ✅ Log Analytics workspace
   - ✅ Application Insights
   - ✅ Action group
   - ✅ Alert rule

### **3. Verificar con Azure CLI**

```bash
# Listar recursos en el resource group
az resource list --resource-group rg-log-analytics-workshop --output table

# Verificar Log Analytics Workspace
az monitor log-analytics workspace show \
  --resource-group rg-log-analytics-workshop \
  --workspace-name law-workshop \
  --query "name" -o tsv

# Verificar Application Insights
az monitor app-insights component show \
  --resource-group rg-log-analytics-workshop \
  --app ai-workshop \
  --query "name" -o tsv
```

---

## 📋 Estructura de Archivos Terraform

### **🗂️ Archivos incluidos:**

```
terraform/
├── main.tf                    # Recursos principales
├── variables.tf              # Definición de variables
├── outputs.tf               # Outputs del deployment
├── terraform.tfvars.example # Template de variables
└── terraform.tfvars         # Tus variables (no en git)
```

### **📄 Contenido de cada archivo:**

#### **`main.tf` - Recursos principales:**
- Provider configuration
- Resource Group
- Log Analytics Workspace
- Application Insights
- Action Group
- Alert Rule

#### **`variables.tf` - Variables:**
- `subscription_id`: Tu Azure subscription
- `admin_email`: Email para alertas
- `resource_group_name`: Nombre del RG
- `location`: Región de Azure
- Nombres personalizables para cada recurso

#### **`outputs.tf` - Información importante:**
- Connection string de Application Insights
- ID del Log Analytics Workspace
- Nombre del Resource Group

---

## 🔒 Configuraciones de Seguridad

### **🛡️ Provider Configuration:**

```hcl
provider "azurerm" {
  features {}
  subscription_id                 = var.subscription_id
  resource_provider_registrations = "none"
}
```

**🎯 Beneficios:**
- **`resource_provider_registrations = "none"`:** Evita registros automáticos de RPs
- **Subscription explícita:** Control total sobre la suscripción usada

### **🔐 Sensitive Outputs:**

Los outputs sensibles están marcados como `sensitive = true`:
- Application Insights connection string
- Log Analytics workspace key

---

## ⚠️ Gestión de Estado

### **📁 Estado Local:**

El workshop usa estado local de Terraform (`terraform.tfstate`). 

**🚨 Importante:**
- No subir `terraform.tfstate` a git
- El archivo contiene información sensible
- Para uso personal/workshop está bien

### **🏗️ Para Producción:**

En entornos reales, usar remote state:

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "terraformstate"
    container_name       = "tfstate"
    key                  = "workshop.terraform.tfstate"
  }
}
```

---

## 🚨 Troubleshooting

### **❌ Error: "Error building ARM Config"**

#### **🔍 Causa común:**
```
Error: building AzureRM Client: Authenticating using the Azure CLI is supported, however no Azure CLI
```

#### **🛠️ Solución:**
```bash
# Re-login a Azure
az logout
az login

# Verificar suscripción
az account show
```

### **❌ Error: "subscription not found"**

#### **🔍 Causa:**
Subscription ID incorrecto en `terraform.tfvars`

#### **🛠️ Solución:**
```bash
# Obtener el subscription ID correcto
az account show --query "id" -o tsv

# Verificar que está en terraform.tfvars
grep subscription_id terraform.tfvars
```

### **❌ Error: "email address is invalid"**

#### **🔍 Causa:**
Email mal formateado en la variable `admin_email`

#### **🛠️ Solución:**
```bash
# Verificar el email en terraform.tfvars
grep admin_email terraform.tfvars

# Debe tener formato: "nombre@dominio.com"
```

### **❌ Error: "resource already exists"**

#### **🔍 Causa:**
Nombres de recursos no únicos

#### **🛠️ Solución:**
```bash
# Agregar prefix único en terraform.tfvars
prefix = "tu-nombre-unico"

# Re-ejecutar plan
terraform plan
```

---

## 🧹 Limpieza de Recursos

### **🗑️ Destruir todo con Terraform:**

```bash
# Ver qué se eliminará
terraform plan -destroy

# Eliminar todos los recursos
terraform destroy
```

**⚠️ Confirmación requerida:**
```
Do you really want to destroy all resources?
  Enter a value: yes
```

### **🔍 Verificar limpieza:**

```bash
# Verificar que el resource group fue eliminado
az group exists --name rg-log-analytics-workshop
# Debería retornar: false
```

---

## 📊 Monitoreo de Costos

### **💰 Ver costos actuales:**

```bash
# Costo del resource group
az consumption usage list \
  --billing-period-name $(az billing period list --query "[0].name" -o tsv) \
  --query "[?contains(resourceGroup, 'rg-log-analytics-workshop')]"
```

### **🔔 Configurar alertas de costo:**

En Azure Portal:
1. Cost Management + Billing
2. Budgets
3. Create budget: $10 USD
4. Alert: 80% of budget

---

## ➡️ Siguiente Paso

Una vez que la infraestructura esté desplegada exitosamente:

**👉 Continúa con: [03-application-setup.md](03-application-setup.md)**

---

## 📚 Referencias

### **📖 Documentación:**
- [Terraform AzureRM Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Azure Log Analytics](https://docs.microsoft.com/azure/azure-monitor/logs/log-analytics-overview)
- [Application Insights](https://docs.microsoft.com/azure/azure-monitor/app/app-insights-overview)

### **🛠️ Herramientas:**
- [Terraform CLI](https://learn.hashicorp.com/terraform)
- [Azure CLI](https://docs.microsoft.com/cli/azure/)
- [Azure Portal](https://portal.azure.com)

**¡Tu infraestructura está lista!** 🎉