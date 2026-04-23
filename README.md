#  Pac-Man com Minimax

**Disciplina:** Inteligência Artificial  
**Curso:** Ciência da Computação  
**Professor:** Nikson Bernardes Fernandes Ferreira  

---

##  Integrantes

- Lara Alves Korogi - 22400272  
- Guilherme Costa Rodrigues - 22401952
- Davi Ribeiro Nobre - 22401443
- Brenno Miranda Viana - 22402170 

---

##  Descrição

Este projeto implementa o algoritmo **Minimax** para controlar o Pac-Man, permitindo que ele tome decisões estratégicas com base nas ações dos fantasmas.

---

##  Objetivo

-  Maximizar a pontuação do Pac-Man  
-  Minimizar os riscos causados pelos fantasmas  
-  Aplicar jogos de soma zero  
-  Desenvolver tomada de decisão baseada em busca  

---

##  Funcionamento do Minimax

- **MAX (Pac-Man):** escolhe a melhor jogada  
- **MIN (Fantasmas):** tentam prejudicar o Pac-Man  

O algoritmo explora uma árvore de decisões até uma profundidade definida.

---

##  Como Executar

No terminal:

```bash
python pacman.py -p MinimaxAgent
```

Para definir a profundidade:

```bash
python pacman.py -p MinimaxAgent -a depth=2
```

---

##  Sobre a Profundidade

O parâmetro `depth` controla quantos níveis da árvore serão explorados:

- `depth=1` → execução rápida ⚡  
- `depth=2` → equilíbrio 👍  
- `depth=3+` → mais inteligente, porém mais lento 🐢  

Recomenda-se iniciar com valores baixos.

---

##  Melhorias Implementadas

-  Remoção da ação `STOP`  
-  Desempate aleatório  
-  Penalização por ficar parado  
-  Função de avaliação aprimorada considerando:
  - Distância até comida  
  - Quantidade de comida  
  - Distância dos fantasmas  
  - Estado dos fantasmas  

---

##  Resultado

O Pac-Man agora:

-  Busca comida de forma eficiente  
-  Evita fantasmas perigosos  
-  Persegue fantasmas assustados  

---

##  Estrutura do Projeto

```bash
pacman-minimax/
│── README.md
│── seuPacManAgents.py
```

---

##  Arquivo Principal

- `seuPacManAgents.py` → Minimax + função de avaliação  

