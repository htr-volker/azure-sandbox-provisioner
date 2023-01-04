data "azurerm_billing_mca_account_scope" "main" {
  billing_account_name = var.billing_account_name
  billing_profile_name = var.billing_profile_name
  invoice_section_name = var.invoice_section_name
}

resource "azurerm_subscription" "subscriptions" {
    count = var.subscription_count
    subscription_name = "${format("${var.subscription_prefix}%04s", count.index + 1)}"
    alias = "${format("${var.subscription_prefix}%04s", count.index + 1)}"
    billing_scope_id  = data.azurerm_billing_mca_account_scope.main.id
}
