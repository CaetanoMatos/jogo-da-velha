# Jogo da Velha - Inteligência Artificial (Minimax com Poda Alfa-Beta) 🎮🤖

Este projeto consiste na implementação clássica do **Jogo da Velha (Tic-Tac-Toe)**, desenvolvido em Python. O objetivo principal do projeto é a criação de uma Inteligência Artificial imbatível, utilizando o algoritmo **Minimax** otimizado com a **Poda Alfa-Beta**.

O sistema conta com uma interface gráfica amigável desenvolvida em **Tkinter** e permite que o usuário escolha entre diferentes modos de jogo.

## 🚀 Funcionalidades

- **Menu de Seleção:** Tela inicial para escolha do modo de jogo.
- **Modo Humano vs IA (Obrigatório):** Jogue contra uma Inteligência Artificial que toma decisões otimizadas e nunca perde (no máximo empata).
- **Modo Humano vs Humano (Opcional):** Dois jogadores podem se enfrentar alternando os turnos na mesma máquina.
- **Interface Gráfica (GUI):** Interface construída com a biblioteca nativa Tkinter, dispensando instalação de pacotes de terceiros.
- **Validação de Jogadas:** O sistema impede cliques em espaços já preenchidos e reconhece automaticamente vitórias, derrotas ou empates, exibindo alertas na tela.

## 🧠 Sobre o Algoritmo (IA)

A Inteligência Artificial deste projeto foi construída usando o algoritmo de busca **Minimax**, que simula todas as jogadas futuras possíveis para decidir o melhor movimento atual. 

Para melhorar a eficiência da busca (evitando que o algoritmo processe caminhos irrelevantes), foi implementada a **Poda Alfa-Beta**. Essa otimização corta os ramos da "árvore de decisões" que não precisam ser explorados, tornando a resposta da IA praticamente instantânea.

## 💻 Como executar o projeto

### Pré-requisitos
- Ter o **Python 3.x** instalado na sua máquina. (Não é necessário instalar bibliotecas extras, pois o `tkinter` e o `math` são nativos do Python).

### Passos
1. Faça o clone do repositório ou baixe os arquivos para o seu computador:
   ```bash
   git clone URL_DO_SEU_REPOSITORIO