ADMIN_PASSWORD = "123456"  # Vulnerabilidade intencional 
DEMO_USERNAME = "Breno"


def login(username, password):
    if password == ADMIN_PASSWORD:
        return f"Login realizado para {username}"

    return "Senha incorreta"


def main():
    print(login(DEMO_USERNAME, ADMIN_PASSWORD))


if __name__ == "__main__":
    main()