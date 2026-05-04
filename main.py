import tkinter as tk
from tkinter import messagebox, ttk
import math
import time
import sys
import json
import os
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

HUMANO = 'X'
IA = 'O'
VAZIO = ' '

nos_avaliados = 0

ARQUIVO_HISTORICO = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'historico.json')

# --- lógica do jogo e ia (minimax + alfa-beta) ---

def verificar_vencedor(tabuleiro, jogador):
    vitorias = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combinacao in vitorias:
        if tabuleiro[combinacao[0]] == tabuleiro[combinacao[1]] == tabuleiro[combinacao[2]] == jogador:
            return True
    return False

def verificar_empate(tabuleiro):
    return VAZIO not in tabuleiro

def avaliar(tabuleiro):
    if verificar_vencedor(tabuleiro, IA):
        return 10
    elif verificar_vencedor(tabuleiro, HUMANO):
        return -10
    else:
        return 0

def minimax(tabuleiro, profundidade, alpha, beta, maximizando, usar_poda):
    global nos_avaliados
    nos_avaliados += 1

    pontuacao = avaliar(tabuleiro)

    if pontuacao == 10 or pontuacao == -10:
        return pontuacao
    if verificar_empate(tabuleiro):
        return 0

    if maximizando:
        melhor_pontuacao = -math.inf
        for i in range(9):
            if tabuleiro[i] == VAZIO:
                tabuleiro[i] = IA
                pontuacao_atual = minimax(tabuleiro, profundidade + 1, alpha, beta, False, usar_poda)
                tabuleiro[i] = VAZIO
                melhor_pontuacao = max(melhor_pontuacao, pontuacao_atual)
                alpha = max(alpha, melhor_pontuacao)
                if usar_poda and (beta <= alpha):
                    break
        return melhor_pontuacao
    else:
        pior_pontuacao = math.inf
        for i in range(9):
            if tabuleiro[i] == VAZIO:
                tabuleiro[i] = HUMANO
                pontuacao_atual = minimax(tabuleiro, profundidade + 1, alpha, beta, True, usar_poda)
                tabuleiro[i] = VAZIO
                pior_pontuacao = min(pior_pontuacao, pontuacao_atual)
                beta = min(beta, pior_pontuacao)
                if usar_poda and (beta <= alpha):
                    break
        return pior_pontuacao

def melhor_jogada_ia(tabuleiro, usar_poda):
    """retorna (jogada, nos_avaliados, tempo_ms)."""
    global nos_avaliados
    nos_avaliados = 0

    inicio_tempo = time.perf_counter()

    melhor_pontuacao = -math.inf
    jogada = -1

    for i in range(9):
        if tabuleiro[i] == VAZIO:
            tabuleiro[i] = IA
            pontuacao_atual = minimax(tabuleiro, 0, -math.inf, math.inf, False, usar_poda)
            tabuleiro[i] = VAZIO

            if pontuacao_atual > melhor_pontuacao:
                melhor_pontuacao = pontuacao_atual
                jogada = i

    fim_tempo = time.perf_counter()
    tempo_ms = (fim_tempo - inicio_tempo) * 1000

    modo_str = "COM PODA ALFA-BETA" if usar_poda else "MINIMAX PURO (SEM PODA)"
    print(f"--- DESEMPENHO DA IA: {modo_str} ---")
    print(f"Jogada escolhida: posição {jogada}")
    print(f"Nós avaliados: {nos_avaliados}")
    print(f"Tempo de processamento: {tempo_ms:.2f} ms\n")

    return jogada, nos_avaliados, tempo_ms


# --- interface gráfica (tkinter) com menu ---

class JogoDaVelhaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("jogo da velha")
        self.tabuleiro = [VAZIO] * 9
        self.botoes = []

        self.modo_jogo = None
        self.jogador_atual = HUMANO
        self.label_desempenho = None

        self.historico = []
        self.carregar_historico()

        self.frame_menu = tk.Frame(self.root)
        self.frame_jogo = tk.Frame(self.root)

        self.criar_menu()

    def carregar_historico(self):
        if os.path.exists(ARQUIVO_HISTORICO):
            try:
                with open(ARQUIVO_HISTORICO, 'r', encoding='utf-8') as f:
                    self.historico = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.historico = []

    def salvar_historico(self):
        try:
            with open(ARQUIVO_HISTORICO, 'w', encoding='utf-8') as f:
                json.dump(self.historico, f, ensure_ascii=False, indent=2)
        except IOError:
            pass

    def registrar_partida(self, resultado):
        modos = {
            'IA_PODA': 'IA com Poda',
            'IA_PURO': 'IA sem Poda',
            'HUMANO': '2 Jogadores'
        }
        self.historico.append({
            'data_hora': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'modo': modos.get(self.modo_jogo, self.modo_jogo),
            'resultado': resultado
        })
        self.salvar_historico()

    def criar_menu(self):
        self.frame_jogo.pack_forget()
        self.frame_menu.pack(padx=40, pady=40)

        for widget in self.frame_menu.winfo_children():
            widget.destroy()

        titulo = tk.Label(self.frame_menu, text="escolha o modo de jogo", font=('Arial', 16, 'bold'))
        titulo.pack(pady=15)

        btn_ia_poda = tk.Button(self.frame_menu, text="1 jogador (IA COM Poda)", font=('Arial', 12), width=25, height=2,
                                bg="#d4edda", command=lambda: self.iniciar_jogo('IA_PODA'))
        btn_ia_poda.pack(pady=5)

        btn_ia_puro = tk.Button(self.frame_menu, text="1 jogador (IA SEM Poda)", font=('Arial', 12), width=25, height=2,
                                bg="#f8d7da", command=lambda: self.iniciar_jogo('IA_PURO'))
        btn_ia_puro.pack(pady=5)

        btn_humano = tk.Button(self.frame_menu, text="2 jogadores (vs humano)", font=('Arial', 12), width=25, height=2,
                               command=lambda: self.iniciar_jogo('HUMANO'))
        btn_humano.pack(pady=5)

        btn_historico = tk.Button(self.frame_menu, text="ver histórico de partidas", font=('Arial', 11), width=25,
                                  bg="#cce5ff", command=self.ver_historico)
        btn_historico.pack(pady=(15, 5))

    def iniciar_jogo(self, modo):
        self.modo_jogo = modo
        self.jogador_atual = HUMANO
        self.tabuleiro = [VAZIO] * 9

        self.frame_menu.pack_forget()
        self.frame_jogo.pack(padx=10, pady=10)

        self.criar_interface_jogo()

    def criar_interface_jogo(self):
        for widget in self.frame_jogo.winfo_children():
            widget.destroy()

        self.botoes = []

        for i in range(9):
            btn = tk.Button(self.frame_jogo, text=VAZIO, font='normal 30 bold', width=5, height=2,
                            bg='white', command=lambda i=i: self.realizar_jogada(i))
            linha = i // 3
            coluna = i % 3
            btn.grid(row=linha, column=coluna, padx=5, pady=5)
            self.botoes.append(btn)

        btn_voltar = tk.Button(self.frame_jogo, text="voltar ao menu", font=('Arial', 10),
                               command=self.criar_menu)
        btn_voltar.grid(row=3, column=0, columnspan=3, pady=10, sticky='we')

        if self.modo_jogo in ['IA_PODA', 'IA_PURO']:
            self.label_desempenho = tk.Label(
                self.frame_jogo,
                text="aguardando jogada da IA...",
                font=('Courier', 9),
                fg='gray',
                justify=tk.LEFT,
                anchor='w',
                relief=tk.GROOVE,
                padx=8,
                pady=4
            )
            self.label_desempenho.grid(row=4, column=0, columnspan=3, pady=(0, 5), sticky='we')
        else:
            self.label_desempenho = None

    def atualizar_label_desempenho(self, nos, tempo_ms):
        if self.label_desempenho is None:
            return
        modo_str = "com poda alfa-beta" if self.modo_jogo == 'IA_PODA' else "minimax puro (sem poda)"
        texto = (
            f"modo: {modo_str}\n"
            f"nós avaliados: {nos}    tempo: {tempo_ms:.2f} ms"
        )
        self.label_desempenho.config(text=texto, fg='#333333')

    def realizar_jogada(self, idx):
        if self.tabuleiro[idx] != VAZIO:
            return

        if self.modo_jogo in ['IA_PODA', 'IA_PURO']:
            self.tabuleiro[idx] = HUMANO
            self.botoes[idx].config(text=HUMANO, fg='blue')

            if self.checar_fim_de_jogo(HUMANO):
                return

            self.root.update()

            usar_poda = self.modo_jogo == 'IA_PODA'
            movimento_ia, nos, tempo_ms = melhor_jogada_ia(self.tabuleiro, usar_poda)

            self.atualizar_label_desempenho(nos, tempo_ms)

            if movimento_ia != -1:
                self.tabuleiro[movimento_ia] = IA
                self.botoes[movimento_ia].config(text=IA, fg='red')
                self.checar_fim_de_jogo(IA)

        elif self.modo_jogo == 'HUMANO':
            self.tabuleiro[idx] = self.jogador_atual
            cor = 'blue' if self.jogador_atual == HUMANO else 'red'
            self.botoes[idx].config(text=self.jogador_atual, fg=cor)

            if self.checar_fim_de_jogo(self.jogador_atual):
                return

            self.jogador_atual = IA if self.jogador_atual == HUMANO else HUMANO

    def checar_fim_de_jogo(self, jogador):
        if verificar_vencedor(self.tabuleiro, jogador):
            if self.modo_jogo in ['IA_PODA', 'IA_PURO']:
                if jogador == HUMANO:
                    mensagem = "parabéns! você venceu a IA!"
                    resultado = "Vitória do Humano"
                else:
                    mensagem = "a IA venceu! mais sorte na próxima."
                    resultado = "Vitória da IA"
            else:
                if jogador == HUMANO:
                    mensagem = "parabéns! o jogador 'X' venceu!"
                    resultado = "Vitória do Jogador X"
                else:
                    mensagem = "vitória do jogador 'O'!"
                    resultado = "Vitória do Jogador O"

            messagebox.showinfo("fim de jogo", mensagem)
            self.registrar_partida(resultado)
            self.reiniciar_jogo()
            return True

        elif verificar_empate(self.tabuleiro):
            messagebox.showinfo("fim de jogo", "deu velha! empate.")
            self.registrar_partida("Empate")
            self.reiniciar_jogo()
            return True

        return False

    def reiniciar_jogo(self):
        self.tabuleiro = [VAZIO] * 9
        self.jogador_atual = HUMANO
        for btn in self.botoes:
            btn.config(text=VAZIO)
        if self.label_desempenho:
            self.label_desempenho.config(text="aguardando jogada da IA...", fg='gray')

    def ver_historico(self):
        janela = tk.Toplevel(self.root)
        janela.title("Histórico de Partidas")
        janela.resizable(False, False)

        frame = tk.Frame(janela, padx=15, pady=15)
        frame.pack(fill=tk.BOTH, expand=True)

        total = len(self.historico)
        tk.Label(frame, text=f"total de partidas registradas: {total}",
                 font=('Arial', 10, 'bold')).pack(pady=(0, 8))

        if total == 0:
            tk.Label(frame, text="nenhuma partida registrada ainda.",
                     font=('Arial', 11), fg='gray', pady=20).pack()
            return

        colunas = ('#', 'Data/Hora', 'Modo', 'Resultado')
        tree = ttk.Treeview(frame, columns=colunas, show='headings', height=15)

        tree.heading('#', text='#')
        tree.heading('Data/Hora', text='Data/Hora')
        tree.heading('Modo', text='Modo')
        tree.heading('Resultado', text='Resultado')

        tree.column('#', width=40, anchor='center')
        tree.column('Data/Hora', width=135, anchor='center')
        tree.column('Modo', width=130, anchor='center')
        tree.column('Resultado', width=165, anchor='center')

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        for i, partida in enumerate(reversed(self.historico), 1):
            tree.insert('', tk.END, values=(i, partida['data_hora'], partida['modo'], partida['resultado']))

        def limpar():
            if messagebox.askyesno("confirmar", "limpar todo o histórico?", parent=janela):
                self.historico.clear()
                self.salvar_historico()
                janela.destroy()

        tk.Button(janela, text="limpar histórico", font=('Arial', 10), fg='red',
                  command=limpar).pack(pady=10)


if __name__ == "__main__":
    janela_principal = tk.Tk()
    janela_principal.resizable(False, False)
    app = JogoDaVelhaGUI(janela_principal)
    janela_principal.mainloop()
