output "object_ids" {
    value = azuread_user.users[*].object_id
}

output "user_details" {
    value = [
        for user in azuread_user.users[*] : 
        zipmap(["user_principal_name", "initial_password"], [user.user_principal_name, nonsensitive(user.password)])
    ]
}
