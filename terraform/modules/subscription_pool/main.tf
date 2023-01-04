resource "azurerm_management_group" "main" {
  display_name               = var.display_name
  subscription_ids           = [for subscription in var.subscriptions : subscription.subscription_id]
  parent_management_group_id = var.parent_management_group_id
}
