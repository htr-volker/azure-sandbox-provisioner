output "subscription_ids" {
    value = azurerm_subscription.subscriptions[*].subscription_id
}