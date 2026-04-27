# Jogo da Velha - Inteligência Artificial (Minimax com Poda Alfa-Beta) 

Este projeto consiste na implementação clássica do **Jogo da Velha (Tic-Tac-Toe)**, desenvolvido em Python. O objetivo principal do projeto é a criação de uma Inteligência Artificial imbatível, utilizando o algoritmo **Minimax** otimizado com a **Poda Alfa-Beta**, além de permitir a análise de desempenho em tempo real.

O sistema conta com uma interface gráfica amigável desenvolvida em **Tkinter** e permite que o usuário escolha entre diferentes modos de jogo e teste a eficiência dos algoritmos.

## Funcionalidades

- **Menu de Seleção:** Tela inicial para escolha do modo de jogo e tipo de algoritmo.
- **Análise de Desempenho:** O sistema imprime no terminal o tempo de execução (em milissegundos) e a quantidade de nós avaliados (estados do tabuleiro) a cada jogada da IA.
- **1 Jogador (IA com Poda):** Jogue contra a IA otimizada. É possível notar a resposta instantânea e a baixa quantidade de nós processados no terminal.
- **1 Jogador (IA sem Poda / Minimax Puro):** Jogue contra a IA sem otimização. Ideal para testes acadêmicos, permitindo comparar como a ausência da poda eleva o número de cálculos para centenas de milhares.
- **2 Jogadores (Humano vs Humano):** Dois jogadores podem se enfrentar alternando os turnos na mesma máquina.
- **Interface Gráfica (GUI):** Interface construída com a biblioteca nativa Tkinter, dispensando instalação de pacotes de terceiros.
- **Validação de Jogadas:** O sistema impede cliques em espaços já preenchidos e reconhece automaticamente vitórias, derrotas ou empates.

## Sobre o Algoritmo (IA)

A Inteligência Artificial deste projeto foi construída usando o algoritmo de busca **Minimax**, que simula todas as jogadas futuras possíveis para decidir o melhor movimento atual. Como consequência, a IA nunca perde (no máximo, o jogo termina em empate).

Para demonstrar a melhoria na eficiência da busca, implementamos a **Poda Alfa-Beta**. Essa otimização corta os ramos da "árvore de decisões" que não precisam ser explorados. Ao comparar os modos de jogo no terminal, fica evidente que o Minimax puro avalia mais de 300.000 possibilidades na primeira jogada, enquanto a Poda Alfa-Beta reduz esse número drasticamente (geralmente para menos de 30.000 nós), poupando processamento e memória sem alterar a precisão da jogada.

## Como executar o projeto

### Pré-requisitos
- Ter o **Python 3.x** instalado na sua máquina (recomendado Python 3.12+).
- Não é necessário instalar bibliotecas externas, pois o `tkinter`, `time` e o `math` são nativos da linguagem.
"""


### Passos para execução:
1. Faça o clone do repositório para o seu computador digitando no terminal:
   git clone https://github.com/CaetanoMatos/jogo-da-velha.git

2. Acesse a pasta do projeto recém-baixada:
   cd jogo-da-velha

3. Execute o script principal do jogo:
   python main.py
"""