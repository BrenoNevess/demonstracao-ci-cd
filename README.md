# Demo DevSecOps com Bandit

Demonstração acadêmica de SAST integrado ao GitHub Actions. O programa começa com uma senha fixa de propósito para o Bandit encontrar a regra B105. Depois, você troca essa senha por uma variável de ambiente e envia a correção.

> A senha `123456` é fictícia e existe somente para a demonstração. Nunca use credenciais reais neste código.

## Como executar no Windows

Abra o terminal PowerShell do VS Code e entre na pasta do projeto:

```powershell
Set-Location "D:\FACULDADE\4Semestre\Int. DevOps"
```

Execute a aplicação:

```powershell
python app.py
```

Se o comando `python` não for reconhecido, tente `py -3 app.py`. A saída esperada é `Login realizado para Breno`.

O código de `app.py` está organizado em três partes: `ADMIN_PASSWORD` contém a senha fixa, `login` compara a senha e monta a resposta, e `main` inicia a demonstração. A senha fixa é intencionalmente insegura nesta primeira etapa.

## Análise local com Bandit

Instale a ferramenta uma vez:

```powershell
python -m pip install bandit
```

Se `python` não for reconhecido, use `py -3 -m pip install bandit`. Depois execute a análise:

```powershell
python -m bandit -r .
```

O resultado esperado contém `B105:hardcoded_password_string` e um código de saída 1. Isso não é um erro de instalação: significa que a ferramenta encontrou o problema. O mesmo código de saída faz o job do GitHub Actions falhar.

## Publicar a primeira etapa no GitHub

Crie um repositório vazio no GitHub, sem adicionar README, licença ou `.gitignore` pelo site. Então, no terminal, rode os comandos abaixo nesta pasta, substituindo a URL pelo endereço do repositório que você criou:

```powershell
git init
git branch -M main
git add .
git commit -m "feat: adiciona demo DevSecOps"
git remote add origin https://github.com/SEU-USUARIO/devsecops-demo.git
git push -u origin main
```

O primeiro push dispara o workflow. No GitHub, abra **Actions**, selecione **DevSecOps Pipeline** e veja que a etapa do Bandit falhou por causa da senha fixa.

## Corrigir e publicar a segunda etapa

Agora substitua o conteúdo de `app.py` pelo código abaixo:

```python
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
```

Teste a correção no PowerShell:

```powershell
$env:ADMIN_PASSWORD = "123456"
$env:LOGIN_PASSWORD = "123456"
python app.py
python -m bandit -r .
```

A aplicação deve imprimir `Login realizado para Breno`; o Bandit deve terminar sem B105. No PowerShell, essas variáveis valem somente para a janela atual do terminal.

Envie a correção:

```powershell
git add app.py
git commit -m "fix: remove senha hardcoded"
git push
```

Volte à aba **Actions**. A nova execução deve passar. Não faça esse segundo commit antes de mostrar a primeira execução com falha.

## Limites da demonstração

O workflow em `.github/workflows/security.yml` faz checkout do código, configura Python e roda SAST. Ele não implementa build, testes automatizados ou deploy. Em produção, segredos devem ser guardados em um gerenciador de segredos, não em código ou variáveis versionadas. O Bandit identifica classes específicas de problemas e não substitui uma revisão de segurança completa.