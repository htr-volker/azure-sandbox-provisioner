variable "name" {}
variable "scope" {}
variable "assignable_scopes" {}
variable "description" {}
variable "actions" {
  type = list(string)
}
variable "not_actions" {
  type = list(string)
}
