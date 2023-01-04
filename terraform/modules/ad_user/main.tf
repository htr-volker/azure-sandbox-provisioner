resource "random_password" "password" {
    count = length(var.names)
  length           = 12
  min_upper        = 1
  min_numeric      = 1
  min_special      = 1
  special          = true
  override_special = "_%@!"
}

resource "azuread_user" "users" {
  count = length(var.names)
  user_principal_name   = "${replace(lower(var.names[count.index]), " ", "")}@${var.domain}"
  display_name          = var.names[count.index]
  password              = random_password.password[count.index].result
  force_password_change = true
}
