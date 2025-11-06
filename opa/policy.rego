package authz

default allow = false

# Any authenticated user can GET /users
allow {
    input.path == "/users"
    input.method == "GET"
}

# Only admins can POST /users
allow {
    input.path == "/users"
    input.method == "POST"
    input.user.role == "admin"
}
