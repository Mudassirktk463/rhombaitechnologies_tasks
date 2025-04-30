users = {
    "alice": "password123",
    "bob": "secure456"
}
def authenticate(username, password):
    return users.get(username) == password
