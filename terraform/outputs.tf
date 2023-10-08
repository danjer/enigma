output "databricks_url" {
  value = "https://${azurerm_databricks_workspace.this.workspace_url}/"
}
output "databricks_notebook_url" {
  value = "https://${databricks_notebook.cracking_engima.url}/"
}