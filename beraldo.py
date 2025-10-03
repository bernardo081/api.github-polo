import requests

def listar_repos_publicos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    
    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            print(repo['name'])
            print(repo['full_name'])
            print(repo['url'])
            print("\n")
    else:
        print(f"Erro {response.status_code} ao acessar a API.")

# Exemplo de uso
listar_repos_publicos("bernardo081")
