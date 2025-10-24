import requests

def listar_repos_publicos(username):
    url = f"https://api.github.com/users/{username}/repos"
    repositorios = []
    page = 1

    try:
        while True:
            response = requests.get(url, params={'per_page': 100, 'page': page}, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            repos = response.json()
            if not repos:
                break
            for repo in repos:
                repositorios.append({
                    "name": repo['name'],
                    "full_name": repo['full_name'],
                    "url": repo['html_url']
                })
            page += 1
        return repositorios

    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")
        return []

#  Aqui você chama a função com o nome de usuário desejado
usuario = input("Digite o nome de usuário do GitHub: ")
repos = listar_repos_publicos(usuario)

#  Exibe os resultados
if repos:
    for r in repos:
        print(f"Nome: {r['name']}")
        print(f"Nome completo: {r['full_name']}")
        print(f"URL: {r['url']}\n")
else:
    print("Nenhum repositório encontrado ou erro na requisição.")
