# 🐳 Configuración del Dev Container

Este documento te guía paso a paso para configurar correctamente el entorno de desarrollo usando Dev Containers.

## 🎯 Objetivo

Configurar un entorno de desarrollo estandarizado y reproducible que incluya todas las herramientas necesarias para el workshop.

---

## 🚨 CONFIGURACIÓN CRÍTICA INICIAL

### **⚠️ PASO OBLIGATORIO: Configurar Container Engine**

Antes de hacer cualquier cosa, **DEBES** configurar VS Code para usar tu container engine.

#### **🔧 Configuración paso a paso:**

1. **Abrir VS Code Settings:**
   - `Cmd/Ctrl + ,` 
   - O `File > Preferences > Settings`

2. **Buscar la configuración:**
   - En la barra de búsqueda escribir: `dev.containers.dockerPath`

3. **Configurar según tu setup:**
   
   **Si tienes Docker Desktop:**
   ```
   dev.containers.dockerPath: docker
   ```
   
   **Si tienes Podman Desktop:**
   ```
   dev.containers.dockerPath: podman
   ```

4. **Reiniciar VS Code completamente**

#### **🖼️ Ubicación Visual:**
```
VS Code Settings
├── 🔍 Search: "dev.containers.dockerPath"
└── 📂 Extensions
    └── 📦 Dev Containers
        └── ⚙️ Docker Path: [tu-engine-aquí]
```

> **💡 Sin esta configuración, el devcontainer fallará al construirse con errores crípticos.**

---

## 🏗️ Arquitectura del Dev Container

### **📦 ¿Qué incluye nuestro devcontainer?**

```dockerfile
Base Image: mcr.microsoft.com/devcontainers/python:3.11
├── 🐍 Python 3.11 + pip
├── 🌩️  Azure CLI (latest)
├── 🏗️  Terraform (latest)
├── 📦 Python packages:
│   ├── opencensus-ext-azure
│   ├── python-dotenv
│   ├── flask
│   └── testing/linting tools
├── 🔧 VS Code Extensions:
│   ├── Python
│   ├── Terraform
│   ├── Azure Account
│   └── Azure Resource Groups
└── 📁 Volume mounts:
    └── ~/.azure (para persistir login)
```

### **🗂️ Estructura de archivos:**

```
.devcontainer/
├── devcontainer.json    # Configuración principal
└── Dockerfile          # Imagen personalizada
```

---

## 🚀 Proceso de Setup

### **1. Clonar el Repositorio**

```bash
git clone <repository-url>
cd azure-log-analytics-workshop
```

### **2. Abrir en VS Code**

```bash
code .
```

### **3. Abrir Dev Container**

VS Code detectará automáticamente la configuración del devcontainer y mostrará una notificación:

#### **📢 Opción A: Notificación Automática**
```
🔔 Folder contains a Dev Container configuration file.
[Reopen in Container] [Show All Files]
```
→ **Hacer clic en "Reopen in Container"**

#### **⌨️ Opción B: Comando Manual**
1. `Cmd/Ctrl + Shift + P`
2. Escribir: "Dev Containers: Reopen in Container"
3. Presionar Enter

### **4. Esperar la Construcción**

**Primera vez (5-10 minutos):**
- Descarga de imagen base (~2GB)
- Instalación de features (Azure CLI, Terraform)
- Instalación de Python packages
- Configuración de VS Code extensions

**🔄 Verás estos pasos en el terminal:**
```
[1/8] Building dev container...
[2/8] Installing features...
[3/8] Installing Azure CLI...
[4/8] Installing Terraform...
[5/8] Installing Python packages...
[6/8] Configuring VS Code...
[7/8] Setting up workspace...
[8/8] Starting container...
```

### **5. Verificar que Funciona**

#### **✅ Señales de éxito:**

1. **Prompt del terminal cambia:**
   ```bash
   # Antes (local)
   user@hostname:~/project$
   
   # Después (container)
   vscode@container-id:/workspace$
   ```

2. **Extensions cargadas:**
   - Python extension activa
   - Terraform syntax highlighting
   - Azure extensions disponibles

3. **Herramientas disponibles:**
   ```bash
   python --version     # Python 3.11.x
   az --version        # Azure CLI
   terraform --version # Terraform
   ```

---

## 🔧 Configuración Avanzada

### **📁 Volume Mounts Configurados**

El devcontainer monta automáticamente:

```json
{
  "mounts": [
    "source=${localEnv:HOME}/.azure,target=/home/vscode/.azure,type=bind"
  ]
}
```

**🎯 Beneficio:** Tu login de Azure se persiste entre sesiones.

### **🌐 Port Forwarding**

```json
{
  "forwardPorts": [8000]
}
```

**🎯 Beneficio:** Si ejecutamos una web app, será accesible desde tu browser local.

### **⚡ Post Create Command**

```json
{
  "postCreateCommand": "pip install -r src/requirements.txt"
}
```

**🎯 Beneficio:** Instala automáticamente las dependencias Python al crear el container.

---

## 🔍 Verificación Completa

### **🧪 Test de Funcionamiento**

Ejecuta estos comandos en el terminal del devcontainer:

```bash
# 1. Verificar Python y packages
python --version
python -c "import opencensus.ext.azure; print('✅ Azure packages OK')"

# 2. Verificar Azure CLI
az --version
az account list-locations --query "[0].name" -o tsv

# 3. Verificar Terraform
terraform --version

# 4. Verificar estructura del proyecto
ls -la
tree -L 2 .
```

#### **📊 Resultado esperado:**
```
✅ Python 3.11.x
✅ Azure packages OK
✅ Azure CLI 2.x.x
✅ eastus (o similar)
✅ Terraform v1.x.x
✅ Estructura del proyecto visible
```

---

## 🚨 Troubleshooting

### **❌ Error: "Failed to create dev container"**

#### **🔍 Diagnóstico:**
1. **Verificar configuración:**
   ```bash
   # En tu sistema local
   docker --version     # O podman --version
   code --version
   ```

2. **Verificar que el engine esté corriendo:**
   ```bash
   docker ps           # O podman ps
   ```

#### **🛠️ Soluciones:**

**Problema 1: `dev.containers.dockerPath` mal configurado**
```
Error: spawn docker ENOENT
```
→ **Solución:** Revisar configuración en VS Code Settings

**Problema 2: Container engine no está corriendo**
```
Error: Cannot connect to Docker daemon
```
→ **Solución:** Iniciar Docker/Podman Desktop

**Problema 3: Permisos insuficientes**
```
Error: permission denied
```
→ **Solución (Linux):** `sudo usermod -aG docker $USER`

### **❌ Error: "Extension failed to install"**

#### **🛠️ Soluciones:**
1. **Internet connection issues:**
   ```bash
   # Verificar conectividad
   ping marketplace.visualstudio.com
   ```

2. **Rebuild container:**
   - `Cmd/Ctrl + Shift + P`
   - "Dev Containers: Rebuild Container"

### **❌ Container se construye pero falla al iniciar**

#### **🔍 Ver logs detallados:**
1. `Cmd/Ctrl + Shift + P`
2. "Dev Containers: Show Container Log"

#### **🛠️ Soluciones comunes:**
- **Limpiar cache:** "Dev Containers: Clean Up Dev Containers"
- **Rebuild sin cache:** "Dev Containers: Rebuild Container (No Cache)"

---

## 🎛️ Comandos Útiles del Dev Container

### **🔄 Gestión del Container:**
```bash
# Rebuild container
Cmd/Ctrl + Shift + P → "Dev Containers: Rebuild Container"

# Clean up old containers
Cmd/Ctrl + Shift + P → "Dev Containers: Clean Up Dev Containers"

# Show container log
Cmd/Ctrl + Shift + P → "Dev Containers: Show Container Log"
```

### **📁 Gestión de archivos:**
```bash
# El workspace está en /workspace
pwd                    # /workspace
ls -la                # Ver archivos del proyecto

# Tu home es /home/vscode
cd ~                  # /home/vscode
ls -la .azure/        # Config de Azure persistida
```

---

## 🎯 Beneficios del Dev Container

### **✅ Consistencia:**
- Todos usan el mismo entorno
- Mismas versiones de herramientas
- Configuración idéntica

### **✅ Reproducibilidad:**
- Funciona igual en Windows, macOS, Linux
- No hay conflictos con instalaciones locales
- Environment aislado

### **✅ Productividad:**
- Setup automático
- Extensions pre-configuradas
- Todas las herramientas incluidas

---

## ➡️ Siguiente Paso

Una vez que tu devcontainer esté funcionando correctamente:

**👉 Continúa con: [02-infrastructure-deployment.md](02-infrastructure-deployment.md)**

---

## 🤝 ¿Problemas?

Si encuentras issues:

1. **Revisa troubleshooting** arriba
2. **Verifica que tu `dev.containers.dockerPath`** esté configurado
3. **Intenta rebuild** del container
4. **Pregunta al instructor** con el error específico

**¡Tu entorno está listo para el workshop!** 🎉