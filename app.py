import os

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
DEMO_USERNAME = "Breno"


def login(username, password):
    if password == ADMIN_PASSWORD:
        return f"Login realizado para {username}"

    return "Senha incorreta"


def main():
    login_password = os.getenv("LOGIN_PASSWORD", "")
    print(login(DEMO_USERNAME, login_password))


if __name__ == "__main__":
    main()