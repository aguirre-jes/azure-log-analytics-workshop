# Azure Log Analytics Workshop

Este workshop te enseña los fundamentos de Azure Log Analytics a través de una aplicación práctica que demuestra la agregación de logs y creación de alertas básicas.

## 🎯 Objetivos del Workshop

Al completar este workshop, habrás aprendido:

- ✅ Cómo configurar Azure Log Analytics y Application Insights
- ✅ Enviar logs estructurados desde una aplicación Python
- ✅ Ejecutar consultas KQL para analizar logs
- ✅ Crear alertas básicas basadas en consultas
- ✅ Usar Infrastructure as Code (Terraform) para Azure

## 📋 Prerrequisitos

Para instrucciones detalladas y recomendaciones, consulta la guía:  [docs/01-prerequisites.md](docs/01-prerequisites.md)

- **Cuenta de Azure** con permisos para crear recursos
- **Docker Desktop o Podman Desktop** instalado y funcionando
- **Visual Studio Code** con extensión Dev Containers
- **Azure CLI** instalado (opcional, se incluye en el devcontainer)

## ⚙️ Configuración Inicial Crítica

### **🚨 IMPORTANTE: Configurar tu Container Engine**

Para instrucciones detalladas y recomendaciones, consulta la guía:  [docs/01-devcontainer-setup](docs/01-devcontainer-setup)

Antes de abrir el devcontainer, **debes configurar VS Code** para usar tu engine de contenedores:

#### **Si usas Docker Desktop:**
1. Abre VS Code
2. Ve a **Settings** (`Cmd/Ctrl + ,`)
3. Busca: `dev.containers.dockerPath`
4. Configura el valor como: `docker`

#### **Si usas Podman Desktop:**
1. Abre VS Code
2. Ve a **Settings** (`Cmd/Ctrl + ,`)
3. Busca: `dev.containers.dockerPath` 
4. Configura el valor como: `podman`

**📸 Captura Visual:**
```
Settings > Extensions > Dev Containers
├── Docker Path: [docker] o [podman]
└── ✅ Restart Required: Reinicia VS Code después de cambiar
```

> **💡 Sin esta configuración, el devcontainer fallará al construirse.**

## 🚀 Inicio Rápido

### 1. Configurar VS Code para tu Container Engine

**🔧 PASO OBLIGATORIO ANTES DE CONTINUAR:**

1. **Abre VS Code**
2. **Abre Settings**: `Cmd/Ctrl + ,` o `File > Preferences > Settings`
3. **Busca**: `dev.containers.dockerPath`
4. **Configura según tu setup**:
   - Si tienes **Docker Desktop**: escribe `docker`
   - Si tienes **Podman Desktop**: escribe `podman`
5. **Reinicia VS Code** completamente

**🖼️ Ubicación Visual:**
```
VS Code Settings
└── Extensions
    └── Dev Containers
        └── Docker Path: [tu-engine-aquí]
```

### 2. Clonar y Abrir el Proyecto

```bash
git clone https://github.com/aguirre-jes/azure-log-analytics-workshop
cd azure-log-analytics-workshop
code .
```

### 3. Abrir en Dev Container

1. **VS Code te preguntará** si quieres reabrir en container - **acepta**
2. **O manualmente**: `Cmd/Ctrl + Shift + P` → "Dev Containers: Reopen in Container"
3. **Espera** a que se construya el container (primera vez toma 5-10 minutos)

**🚨 Si el container falla al construirse:**
- Verifica que configuraste correctamente `dev.containers.dockerPath`
- Asegúrate que Docker/Podman Desktop esté corriendo
- Reinicia VS Code completamente
- Intenta: `Cmd/Ctrl + Shift + P` → "Dev Containers: Rebuild Container"

**✅ Sabrás que funciona cuando veas:**
- Terminal con prompt del container (usualmente `vscode@...`)
- Las extensiones de Python y Azure cargadas automáticamente

### 4. Configurar Variables de Azure

**En el terminal del devcontainer** (debería mostrar `vscode@...:`):

```bash
# Copiar template de variables
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
```

Edita `terraform/terraform.tfvars` con tus valores:

```hcl
subscription_id = "tu-azure-subscription-id"
admin_email = "tu-email@ejemplo.com"
```

### 4. Deploy de Infraestructura

Para instrucciones detalladas y recomendaciones, consulta la guía:  [docs/02-infrastructure-deployment.md](docs/02-infrastructure-deployment.md)

```bash
# Login a Azure
az login

# Deploy con Terraform
cd terraform
terraform init
terraform plan
terraform apply
```

### 5. Configurar la Aplicación

Para instrucciones detalladas y recomendaciones, consulta la guía:  
[docs/03-application-setup](docs/03-application-setup)

```bash
# Obtener connection string
export APPLICATIONINSIGHTS_CONNECTION_STRING=$(terraform output -raw application_insights_connection_string)

# Verificar configuración
cd ../src
python config.py
```

### 6. Ejecutar la Demo

```bash
# Ejecutar aplicación
python app.py

# Deja correr por 3-5 minutos para generar datos
# Usa Ctrl+C para detener
```

### 7. Explorar en Azure Portal

Para instrucciones detalladas y recomendaciones, consulta la guía:  [docs/04-exploring-logs](docs/04-exploring-logs)

1. Ve a [Azure Portal](https://portal.azure.com)
2. Busca tu Log Analytics Workspace
3. Ve a "Logs" y ejecuta las consultas del archivo `queries/basic-queries.kql`

## 📚 Estructura del Proyecto

```
azure-log-analytics-workshop/
├── .devcontainer/          # Configuración del desarrollo en container
├── terraform/              # Infraestructura como código
├── src/                    # Aplicación Python
├── queries/                # Consultas KQL de ejemplo
├── docs/                   # Documentación detallada del workshop
└── scripts/                # Scripts de utilidad
```

## 🔍 Consultas KQL Incluidas

El archivo `queries/basic-queries.kql` contiene ejemplos de:

- Ver todos los logs recientes
- Filtrar por nivel de error
- Agrupar operaciones por usuario
- Crear gráficos de timeline
- Detectar patrones de errores

## 🚨 Crear tu Primera Alerta

Para instrucciones detalladas y recomendaciones, consulta la guía: [docs/05-creating-alerts](docs/05-creating-alerts)

1. En Azure Portal → Log Analytics → Logs
2. Ejecuta esta consulta:
   ```kql
   AppTraces
   | where TimeGenerated > ago(5m)
   | where SeverityLevel >= 3
   | summarize error_count = count()
   ```
3. Haz clic en "New Alert Rule"
4. Configura condición: `count > 5`
5. Agrega acción: Email notification

## 🧹 Limpieza

Para eliminar todos los recursos creados:

```bash
cd terraform
terraform destroy
```

## 📖 Documentación Detallada

- [Prerrequisitos](docs/00-prerequisites.md)
- [Configuración del Dev Container](docs/01-devcontainer-setup.md)
- [Deploy de Infraestructura](docs/02-infrastructure-deployment.md)
- [Configuración de la Aplicación](docs/03-application-setup.md)
- [Explorando Logs](docs/04-exploring-logs.md)
- [Creando Alertas](docs/05-creating-alerts.md)

## ❓ Troubleshooting

### ❌ Error: "No such file or directory" al construir container
**Causa:** Error de configuración en `dev.containers.dockerPath`
**Solución:**
1. Ve a VS Code Settings → `dev.containers.dockerPath`
2. Asegúrate que dice `docker` o `podman` según tu setup
3. Reinicia VS Code completamente
4. `Cmd/Ctrl + Shift + P` → "Dev Containers: Rebuild Container"

### ❌ Container no se construye o falla
**Verificaciones:**
1. **Docker/Podman Desktop está corriendo** ✅
2. **VS Code tiene la extensión "Dev Containers"** instalada ✅
3. **Configuraste `dev.containers.dockerPath`** correctamente ✅
4. **Tienes permisos** para ejecutar containers ✅

**Comandos de debug:**
```bash
# Verificar que tu engine está funcionando
docker version   # Si usas Docker
podman version   # Si usas Podman

# Ver configuración actual de VS Code
code --list-extensions | grep containers
```

### ❌ Error: "Connection string not configured"
**Causa:** Variables de entorno no configuradas correctamente
**Solución:**
- Verifica que la variable `APPLICATIONINSIGHTS_CONNECTION_STRING` esté exportada
- Ejecuta `python src/config.py` para verificar configuración
- Asegúrate de estar en el terminal del devcontainer

### ❌ No veo logs en Azure Portal
**Posibles causas:**
- Espera **2-3 minutos** después de ejecutar la app (hay delay normal)
- Verifica que la connection string sea correcta
- Revisa que no haya errores en la consola de la aplicación
- Confirma que los recursos de Azure se crearon correctamente

### 🆘 Comandos de Emergencia

Si todo falla, ejecuta en orden:

```bash
# 1. Verificar engine
docker --version    # o podman --version

# 2. Reconstruir container desde cero
# En VS Code: Cmd/Ctrl + Shift + P
# → "Dev Containers: Rebuild Container (No Cache)"

# 3. Si persiste, eliminar y recrear
# → "Dev Containers: Clean Up Dev Containers..."
```

## 🤝 Contribuir

¿Encontraste un error o tienes una mejora? ¡Crea un issue o PR!

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

**¡Feliz aprendizaje! 🎉**