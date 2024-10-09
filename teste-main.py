import tkinter as tk
import random
from PIL import Image, ImageTk

# Variáveis do jogo
boneca_olhos_abertos = False
movimento_detectado = False
distancia_inicial = None
faixa_de_erro = 2  # Faixa de erro aceitável para a movimentação

# Função para simular a captura da distância
def capturar_distancia():
    return random.randint(50, 100)

# Função para o jogo
def iniciar_jogo():
    global boneca_olhos_abertos, distancia_inicial, movimento_detectado
    movimento_detectado = False
    boneca_olhos_abertos = False
    distancia_inicial = None

    botao_iniciar.grid_forget()

    # Exibe "Prepare-se!" em vermelho
    label_contagem.config(text="Prepare-se!", fg="red", font=("Arial", 48))
    label_contagem.grid(row=1, column=0, pady=20)  # Centraliza o texto novamente
    janela.after(2000, iniciar_contagem)

def iniciar_contagem():
    label_contagem.config(text="1", fg="black", font=("Arial", 72))
    janela.after(1000, lambda: label_contagem.config(text="2"))
    janela.after(2000, lambda: label_contagem.config(text="3"))
    janela.after(3000, comecar_jogo)

def comecar_jogo():
    global boneca_olhos_abertos
    boneca_olhos_abertos = False
    label_contagem.config(text="", fg="black")

    atualizar_imagem_boneca(imagem_fechada_exibida)

    tempo_contagem = random.uniform(3, 5)
    janela.after(int(tempo_contagem * 1000), verificar_movimento)

def verificar_movimento():
    global boneca_olhos_abertos, distancia_inicial
    
    boneca_olhos_abertos = True
    label_contagem.config(text="Vigiando!", fg="red", font=("Arial", 48))
    atualizar_imagem_boneca(imagem_aberta_exibida)
    
    distancia_inicial = capturar_distancia()
    
    if distancia_inicial is not None:
        janela.after(5000, verificar_resultado)

def verificar_resultado():
    global boneca_olhos_abertos, distancia_inicial
    
    distancia_atual = capturar_distancia()

    if distancia_atual is not None:
        if abs(distancia_atual - distancia_inicial) > faixa_de_erro:
            label_contagem.config(text="Você perdeu!!", fg="red", font=("Arial", 72))
            mostrar_botao_reload()
        else:
            label_contagem.config(text="Você venceu essa rodada!", fg="green", font=("Arial", 72))
            janela.after(2000, comecar_jogo)

def mostrar_botao_reload():
    # Reposiciona o botão no canto inferior direito
    botao_reload.grid(row=2, column=1, sticky="se", padx=20, pady=20)

def reiniciar_jogo():
    botao_reload.grid_forget()
    iniciar_jogo()

def redimensionar_imagem(event):
    largura_disponivel = canvas.winfo_width()
    altura_disponivel = canvas.winfo_height()

    margem = 10
    largura_disponivel = max(largura_disponivel - margem * 2, 100)
    altura_disponivel = max(altura_disponivel - margem * 2, 100)

    proporcao_original = imagem_fechada.width / imagem_fechada.height

    nova_largura = largura_disponivel
    nova_altura = int(nova_largura / proporcao_original)

    if nova_altura > altura_disponivel:
        nova_altura = altura_disponivel
        nova_largura = int(nova_altura * proporcao_original)

    nova_imagem_fechada = imagem_fechada.resize((nova_largura, nova_altura), Image.LANCZOS)
    nova_imagem_aberta = imagem_aberta.resize((nova_largura, nova_altura), Image.LANCZOS)

    global imagem_fechada_exibida, imagem_aberta_exibida
    imagem_fechada_exibida = ImageTk.PhotoImage(nova_imagem_fechada)
    imagem_aberta_exibida = ImageTk.PhotoImage(nova_imagem_aberta)

    if boneca_olhos_abertos:
        atualizar_imagem_boneca(imagem_aberta_exibida)
    else:
        atualizar_imagem_boneca(imagem_fechada_exibida)

def atualizar_imagem_boneca(nova_imagem):
    canvas.delete("all")
    canvas.create_image(canvas.winfo_width()//2, canvas.winfo_height()//2, image=nova_imagem, anchor=tk.CENTER)
    canvas.image = nova_imagem

# Configuração da interface gráfica
janela = tk.Tk()
janela.title("Batatinha Frita 1, 2, 3")
janela.geometry("800x600")

imagem_fechada = Image.open("C:\\Users\\ferna\\OneDrive\\Documentos\\Teste-apEngenharia\\imagens\\boneca_fechada.png")
imagem_aberta = Image.open("C:\\Users\\ferna\\OneDrive\\Documentos\\Teste-apEngenharia\\imagens\\boneca_aberta.png")

imagem_fechada_exibida = ImageTk.PhotoImage(imagem_fechada)
imagem_aberta_exibida = ImageTk.PhotoImage(imagem_aberta)

canvas = tk.Canvas(janela)
canvas.grid(row=0, column=0, rowspan=1, sticky="nsew")

label_contagem = tk.Label(janela, text="Aguardando...", font=("Arial", 24))
label_contagem.grid(row=1, column=0, pady=10)  # Centraliza o texto

botao_iniciar = tk.Button(janela, text="Iniciar", font=("Arial", 48), command=iniciar_jogo)
botao_iniciar.grid(row=1, column=0, pady=20)  # Centraliza o botão de iniciar

botao_reload = tk.Button(janela, text="Reiniciar", font=("Arial", 24), command=reiniciar_jogo)

# Configuração da grid para centralizar todos os elementos, exceto o botão de reiniciar
janela.grid_rowconfigure(0, weight=10)  # Linha da imagem
janela.grid_rowconfigure(1, weight=1)  # Linha para o texto
janela.grid_rowconfigure(2, weight=1)  # Linha para manter a proporção correta
janela.grid_columnconfigure(0, weight=1)  # Centraliza as colunas

janela.bind("<Configure>", redimensionar_imagem)

janela.mainloop()
