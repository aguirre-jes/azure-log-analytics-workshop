variable "subscription_id" {
  description = "Azure Subscription ID"
  type        = string
  # No default - must be provided
}

variable "resource_group_name" {
  description = "Name of the Azure Resource Group"
  type        = string
  default     = "rg-log-analytics-workshop"
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "East US"
}

variable "log_analytics_workspace_name" {
  description = "Name of the Log Analytics Workspace"
  type        = string
  default     = "law-workshop"
}

variable "application_insights_name" {
  description = "Name of the Application Insights instance"
  type        = string
  default     = "ai-workshop"
}

variable "action_group_name" {
  description = "Name of the Monitor Action Group"
  type        = string
  default     = "ag-workshop"
}

variable "admin_email" {
  description = "Email address for alert notifications"
  type        = string
  # No default - must be provided
}

variable "prefix" {
  description = "Prefix for resource names to ensure uniqueness"
  type        = string
  default     = ""
}