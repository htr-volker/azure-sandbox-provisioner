resource "azurerm_role_definition" "role" {
  name        = var.name
  scope       = var.scope
  description = var.description

  permissions {
    actions     = var.actions
    not_actions = var.not_actions
  }

  assignable_scopes = var.assignable_scopes
}
