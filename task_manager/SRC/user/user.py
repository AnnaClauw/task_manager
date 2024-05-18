existing_users = []


class User():
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"User(name='{self.name}')"

    @classmethod
    def create_user(cls, name):
        return cls(name)


def register_user():
    while True:
        username = input("Enter a username to register: ")
        if any(user.name == username for user in existing_users):
            print("Username already exists. Choose a different username.")
        else:
            new_user = User.create_user(username)
            existing_users.append(new_user)
            print("User registration successful!")
        return username
