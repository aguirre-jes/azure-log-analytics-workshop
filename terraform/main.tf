# Configure the Azure Provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
  subscription_id                 = var.subscription_id
}

# Create a resource group
resource "azurerm_resource_group" "workshop" {
  name     = var.resource_group_name
  location = var.location

  tags = {
    Environment = "Workshop"
    Purpose     = "Azure Log Analytics Demo"
    Workshop    = "azure-log-analytics"
  }
}

# Create Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "workshop" {
  name                = var.log_analytics_workspace_name
  location            = azurerm_resource_group.workshop.location
  resource_group_name = azurerm_resource_group.workshop.name
  sku                 = "PerGB2018"
  retention_in_days   = 30

  tags = {
    Environment = "Workshop"
    Purpose     = "Log Analytics"
  }
}

# Create Application Insights
resource "azurerm_application_insights" "workshop" {
  name                = var.application_insights_name
  location            = azurerm_resource_group.workshop.location
  resource_group_name = azurerm_resource_group.workshop.name
  workspace_id        = azurerm_log_analytics_workspace.workshop.id
  application_type    = "web"

  tags = {
    Environment = "Workshop"
    Purpose     = "Application Insights"
  }
}

# Create Action Group for Alerts
resource "azurerm_monitor_action_group" "workshop" {
  name                = var.action_group_name
  resource_group_name = azurerm_resource_group.workshop.name
  short_name          = "workshop"

  email_receiver {
    name          = "admin"
    email_address = var.admin_email
  }

  tags = {
    Environment = "Workshop"
    Purpose     = "Alert Action Group"
  }
}

# Create Log Query Alert Rule
resource "azurerm_monitor_scheduled_query_rules_alert" "error_alert" {
  name                = "high-error-rate-alert"
  location            = azurerm_resource_group.workshop.location
  resource_group_name = azurerm_resource_group.workshop.name

  action {
    action_group = [azurerm_monitor_action_group.workshop.id]
  }

  data_source_id = azurerm_application_insights.workshop.id
  description    = "Alert when error rate is high"
  enabled        = true

  query       = <<-QUERY
    traces
    | where timestamp > ago(5m)
    | where severityLevel >= 3
    | summarize count()
  QUERY

  severity    = 2
  frequency   = 5
  time_window = 5

  trigger {
    operator  = "GreaterThan"
    threshold = 5
  }

  tags = {
    Environment = "Workshop"
    Purpose     = "Error Rate Alert"
  }
}