data "databricks_spark_version" "this" {
  long_term_support = true
  depends_on = [
    azurerm_databricks_workspace.this
  ]
}

data "databricks_current_user" "me" {
  depends_on = [
    azurerm_databricks_workspace.this
  ]
}

resource "databricks_cluster" "single_node" {
  cluster_name            = "Single Node"
  spark_version           = data.databricks_spark_version.this.id
  node_type_id            = "Standard_DS3_v2"
  autotermination_minutes = 20

  spark_conf = {
    "spark.databricks.cluster.profile" : "singleNode"
    "spark.master" : "local[*]"
  }
  custom_tags = {
    "ResourceClass" = "SingleNode"
  }
  library {
    whl = databricks_dbfs_file.enigma_emulator.dbfs_path
  }
}

resource "databricks_notebook" "cracking_engima" {
  source = "../notebooks/cracking_enigma.dbc"
  path   = "/Shared/cracking_enigma"
}

resource "databricks_dbfs_file" "enigma_emulator" {
  source = "../dist/enigma-1.0.0-py3-none-any.whl"
  path   = "/FileStore/enigma-1.0.0-py3-none-any.whl"
}





