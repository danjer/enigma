# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.9.0"
    }
    databricks = {
      source  = "databricks/databricks"
      version = "1.6.2"
    }
  }

  required_version = ">= 1.1.0"
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = true
    }
  }
}

provider "databricks" {
  host                        = azurerm_databricks_workspace.this.workspace_url
  azure_workspace_resource_id = azurerm_databricks_workspace.this.id
}

data "azurerm_client_config" "current" {}


resource "azurerm_resource_group" "this" {
  name     = "enigma-project-resource-group"
  location = var.location
}


resource "azurerm_databricks_workspace" "this" {
  name                = "enigmaprojectworkspace"
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  sku                 = "trial"

}









