locals {
  config = yamldecode(file("../config.yaml"))
}

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=2.97.0"
    }
  }
}

provider "azurerm" {
  features {}
}

module "learner_subscriptions" {
  source               = "./modules/subscription"
  subscription_count   = local.config.subscription_pool.count
  subscription_prefix  = local.config.subscription_pool.subscription_prefix
  billing_account_name = var.billing_account_name
  billing_profile_name = var.billing_profile_name
  invoice_section_name = var.invoice_section_name
}

module "subscription_pool" {
  source        = "./modules/subscription_pool"
  display_name  = "Subscription Pool"
  subscriptions = module.learner_subscriptions.subscription_ids
}

module "cohorts" {
  source           = "./modules/cohorts"
  cohorts          = local.config.cohorts
  role_definitions = local.config.role_definitions
}
