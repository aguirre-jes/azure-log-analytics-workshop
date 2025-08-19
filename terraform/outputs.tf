output "resource_group_name" {
  description = "Name of the created resource group"
  value       = azurerm_resource_group.workshop.name
}

output "log_analytics_workspace_id" {
  description = "ID of the Log Analytics Workspace"
  value       = azurerm_log_analytics_workspace.workshop.id
}

output "log_analytics_workspace_name" {
  description = "Name of the Log Analytics Workspace"
  value       = azurerm_log_analytics_workspace.workshop.name
}

output "application_insights_connection_string" {
  description = "Application Insights Connection String"
  value       = azurerm_application_insights.workshop.connection_string
  sensitive   = true
}

output "application_insights_instrumentation_key" {
  description = "Application Insights Instrumentation Key"
  value       = azurerm_application_insights.workshop.instrumentation_key
  sensitive   = true
}

output "log_analytics_workspace_primary_key" {
  description = "Primary key for Log Analytics Workspace"
  value       = azurerm_log_analytics_workspace.workshop.primary_shared_key
  sensitive   = true
}