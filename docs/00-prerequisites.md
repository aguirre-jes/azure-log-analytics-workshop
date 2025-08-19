# 📋 Prerrequisitos del Workshop

Este documento detalla todos los requisitos necesarios antes de comenzar el workshop de Azure Log Analytics.

## 🎯 Objetivo

Asegurar que tengas todas las herramientas y accesos necesarios para completar exitosamente el workshop.

---

## 🔧 Herramientas Requeridas

### 1. **Cuenta de Microsoft Azure**

#### ✅ **Requisitos:**
- Cuenta activa de Azure (puede ser gratuita)
- Permisos para crear recursos en una suscripción
- Créditos suficientes para crear recursos (el costo del workshop es < $5 USD)

#### 🔗 **Cómo obtenerla:**
- **Cuenta gratuita:** [azure.microsoft.com/free](https://azure.microsoft.com/free)
- **Cuenta de estudiante:** [azure.microsoft.com/students](https://azure.microsoft.com/students)
- **Cuenta corporativa:** Contacta a tu administrador de Azure

#### ✨ **Verificación:**
```bash
# Instala Azure CLI (o usa el del devcontainer)
az --version
az login
az account show
```

### 2. **Container Runtime**

Necesitas **UNO** de los siguientes:

#### **Opción A: Docker Desktop** (Recomendado)
- **Descargar:** [docker.com/products/docker-desktop](https://docker.com/products/docker-desktop)
- **Sistemas:** Windows, macOS, Linux
- **Requisitos:** 4GB RAM mínimo, 8GB recomendado

**Verificación:**
```bash
docker --version
docker run hello-world
```

#### **Opción B: Podman Desktop**
- **Descargar:** [podman-desktop.io](https://podman-desktop.io)
- **Sistemas:** Windows, macOS, Linux
- **Ventaja:** No requiere privilegios de administrador

**Verificación:**
```bash
podman --version
podman run hello-world
```

### 3. **Visual Studio Code**

#### ✅ **Requisitos:**
- **Versión:** 1.74.0 o superior
- **Extensiones obligatorias:**
  - `ms-vscode-remote.remote-containers` (Dev Containers)

#### 🔗 **Instalación:**
1. Descargar: [code.visualstudio.com](https://code.visualstudio.com)
2. Instalar extensión Dev Containers:
   - `Cmd/Ctrl + Shift + X`
   - Buscar: "Dev Containers"
   - Instalar la de Microsoft

#### ✨ **Verificación:**
```bash
code --version
code --list-extensions | grep remote-containers
```

---

## 🌍 Conocimientos Recomendados

### **Nivel Básico (Suficiente para el workshop):**
- ✅ Uso básico de terminal/command line
- ✅ Conceptos básicos de contenedores
- ✅ Navegación en Azure Portal

### **Nivel Intermedio (Ayuda mucho):**
- 🟡 Experiencia con Python básico
- 🟡 Conocimientos de Infrastructure as Code
- 🟡 Conceptos de observabilidad y logging

### **Nivel Avanzado (Opcional):**
- 🔵 KQL (Kusto Query Language)
- 🔵 Terraform
- 🔵 DevOps practices

---

## 💰 Costos Estimados

### **Recursos Azure creados:**
- **Log Analytics Workspace:** ~$2.00/día
- **Application Insights:** ~$1.00/día
- **Storage Account:** ~$0.50/día

### **Total estimado:** $3.50 USD/día

> 💡 **Tip:** El workshop toma 2-3 horas. Si eliminas los recursos inmediatamente después, el costo será < $1 USD.

---

## 🚀 Verificación Final

Antes de continuar, asegúrate de que **TODOS** estos comandos funcionen:

### **✅ Checklist:**

```bash
# 1. Azure CLI (si está instalado localmente)
az --version
az login

# 2. Container Runtime
docker --version     # O podman --version
docker ps           # O podman ps

# 3. VS Code
code --version

# 4. Extensión Dev Containers
code --list-extensions | grep remote-containers
```

### **📊 Resultado esperado:**
- ✅ Todos los comandos ejecutan sin errores
- ✅ Puedes hacer login a Azure
- ✅ Docker/Podman muestra contenedores (aunque esté vacío)
- ✅ VS Code abre correctamente

---

## 🆘 Troubleshooting Común

### ❌ **"az: command not found"**
**Solución:** Azure CLI no está instalado o no está en PATH
- **macOS/Linux:** `curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash`
- **Windows:** Descargar desde [aka.ms/installazurecliwindows](https://aka.ms/installazurecliwindows)

### ❌ **"docker: command not found"**
**Solución:** Docker Desktop no está instalado o no está corriendo
1. Verificar que Docker Desktop esté ejecutándose
2. Reiniciar Docker Desktop
3. En Windows: verificar que esté en modo Linux containers

### ❌ **"Cannot connect to the Docker daemon"**
**Solución:** Problema de permisos o daemon
- **Linux:** `sudo usermod -aG docker $USER` (luego logout/login)
- **macOS/Windows:** Reiniciar Docker Desktop

### ❌ **VS Code no encuentra la extensión**
**Solución:** Marketplace connection issues
1. Verificar conexión a internet
2. `Cmd/Ctrl + Shift + P` → "Extensions: Check for Updates"
3. Instalar manualmente desde VSIX si es necesario

---

## 📚 Recursos Adicionales

### **Documentación Oficial:**
- [Azure CLI Documentation](https://docs.microsoft.com/cli/azure/)
- [Docker Desktop Documentation](https://docs.docker.com/desktop/)
- [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)

### **Videos Útiles:**
- Azure Portal Overview: 10 minutos
- Docker Desktop Setup: 5 minutos
- VS Code Dev Containers: 15 minutos

---

## ➡️ Siguiente Paso

Una vez que hayas completado todos los prerrequisitos:

**👉 Continúa con: [01-devcontainer-setup.md](01-devcontainer-setup.md)**

---

## 🤝 ¿Necesitas Ayuda?

Si tienes problemas con algún prerrequisito:

1. **Revisa la sección de troubleshooting** arriba
2. **Consulta la documentación oficial** de cada herramienta
3. **Busca en Stack Overflow** el error específico
4. **Pregunta al instructor** durante el workshop

**¡Estás listo para comenzar el workshop!** 🎉