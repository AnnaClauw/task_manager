from user_interface import authenticate_user, register_user
from user_interface import start_application

if __name__ == "__main__":
    while True:
        print("Welcome to Task Manager")
        print("1. Log in")
        print("2. Register")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = authenticate_user()
            if username:
                print("Authentication successful!")
                break
            else:
                print("Authentication failed. Please try again.")
        elif choice == "2":
            register_user()
        elif choice == "3":
            print("Exiting the application. Goodbye!")
            exit()
        else:
            print("Invalid choice. Please try again.")

    print(f"Welcome, {username}!")
    start_application()
