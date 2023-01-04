resource "azurerm_management_group" "cohort" {
  display_name               = var.cohort.name
  parent_management_group_id = var.parent_management_group_id
}

resource "azurerm_management_group_policy_assignment" "vm_sizes" {
  count                = var.cohort.vm_sizes.limit ? 1 : 0
  name                 = "limitVMSizes"
  policy_definition_id = var.vm_size_policy_definition_id
  management_group_id  = resource.azurerm_management_group.cohort.id

  parameters = <<PARAMETERS
    ${jsonencode(
    {
      "listOfAllowedSKUs" : {
        "value" : [for size in var.cohort.vm_sizes.allowed : "${size}"]
      }
    }
  )}
  PARAMETERS

  non_compliance_message {
    content = "You may only provision a virtual machine with one of the following sizes: ${join(", ", var.cohort.vm_sizes.allowed)}."
  }

  depends_on = [
    resource.azurerm_management_group.cohort
  ]
}
