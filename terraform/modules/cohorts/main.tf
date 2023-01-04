resource "azurerm_management_group" "parent" {
  display_name = "Cohorts"
}

resource "azurerm_role_definition" "roles" {
  for_each    = { for role_definition in var.role_definitions : role_definition.name => role_definition }
  name        = each.value.name
  description = each.value.description

  permissions {
    actions     = each.value.actions
    not_actions = each.value.not_actions
  }

  scope             = resource.azurerm_management_group.parent.id
  assignable_scopes = [resource.azurerm_management_group.parent.id]
}

resource "azurerm_policy_definition" "vm_sizes" {
  name                = "limitVMSizes"
  display_name        = "Allowed virtual machine size SKUs"
  policy_type         = "Custom"
  mode                = "Indexed"
  management_group_id = resource.azurerm_management_group.parent.group_id

  metadata = <<METADATA
    {
      "version": "1.0.1",
      "category": "Compute"
    }
  METADATA

  policy_rule = <<POLICY
    {
      "if": {
        "allOf": [
          {
            "field": "type",
            "equals": "Microsoft.Compute/virtualMachines"
          },
          {
            "not": {
              "field": "Microsoft.Compute/virtualMachines/sku.name",
              "in": "[parameters('listOfAllowedSKUs')]"
            }
          }
        ]
      },
      "then": {
          "effect": "Deny"
      }
    }
  POLICY

  parameters = <<PARAMETERS
    {
      "listOfAllowedSKUs": {
        "type": "Array",
        "metadata": {
          "description": "The list of size SKUs that can be specified for virtual machines.",
          "displayName": "Allowed Size SKUs",
          "strongType": "VMSKUs"
        }
      }
    }
  PARAMETERS
}

module "cohorts" {
  source                       = "./cohort"
  for_each                     = { for cohort in var.cohorts : cohort.name => cohort }
  cohort                       = each.value
  parent_management_group_id   = resource.azurerm_management_group.parent.id
  vm_size_policy_definition_id = resource.azurerm_policy_definition.vm_sizes.id
}
