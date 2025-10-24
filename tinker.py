import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
import requests
from io import BytesIO

def listar_repos_publicos(username):
    url = f"https://api.github.com/users/{username}/repos"
    repositorios = []
    page = 1

    try:
        while True:
            response = requests.get(
                url,
                params={'per_page': 100, 'page': page},
                headers={'User-Agent': 'Mozilla/5.0'}
            )
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
        messagebox.showerror("Erro", f"Erro na requisição: {e}")
        return []

def buscar_usuario():
    usuario = entrada_usuario.get().strip()
    if not usuario:
        messagebox.showwarning("Atenção", "Digite um nome de usuário do GitHub.")
        return

    resultado_texto.delete(1.0, tk.END)
    carregar_foto(usuario)

    repos = listar_repos_publicos(usuario)
    if repos:
        resultado_texto.insert(tk.END, f"📦 {len(repos)} repositório(s) encontrados para @{usuario}:\n\n")
        for r in repos:
            resultado_texto.insert(tk.END, f"🔹 Nome: {r['name']}\n")
            resultado_texto.insert(tk.END, f"🔗 Link: {r['url']}\n\n")
    else:
        resultado_texto.insert(tk.END, "Nenhum repositório encontrado ou erro na requisição.\n")

def carregar_foto(username):
    try:
        url = f"https://api.github.com/users/{username}"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        dados = response.json()
        avatar_url = dados.get("avatar_url", None)

        if avatar_url:
            imagem_bytes = requests.get(avatar_url).content
            imagem = Image.open(BytesIO(imagem_bytes)).resize((100, 100))
            imagem_tk = ImageTk.PhotoImage(imagem)
            foto_label.config(image=imagem_tk)
            foto_label.image = imagem_tk  # manter referência
            nome_usuario_label.config(text=f"👤 {dados.get('login', 'Usuário')}")
        else:
            foto_label.config(image='')
            nome_usuario_label.config(text="Usuário não encontrado")
    except Exception as e:
        foto_label.config(image='')
        nome_usuario_label.config(text="Erro ao carregar imagem")

# === Interface ===

janela = tk.Tk()
janela.title("Repositórios Públicos do GitHub")
janela.geometry("650x600")

# Entrada
tk.Label(janela, text="Usuário do GitHub:", font=("Arial", 12)).pack(pady=(10, 0))
entrada_usuario = tk.Entry(janela, font=("Arial", 12), width=30)
entrada_usuario.pack(pady=5)

botao_buscar = tk.Button(janela, text="Buscar Repositórios", font=("Arial", 12), command=buscar_usuario)
botao_buscar.pack(pady=10)

# Foto e nome do usuário
foto_label = tk.Label(janela)
foto_label.pack()
nome_usuario_label = tk.Label(janela, font=("Arial", 12, "bold"))
nome_usuario_label.pack()

# Área de resultados
resultado_texto = scrolledtext.ScrolledText(janela, width=75, height=20, font=("Courier", 10))
resultado_texto.pack(pady=10)

# Inicia a janela
janela.mainloop()