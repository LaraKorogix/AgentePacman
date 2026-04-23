# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState
from multiAgents import MultiAgentSearchAgent


class MinimaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState: GameState):
        """Seu código vem aqui
        Adicione o código para minimax
        """
        def minimax(agentIndex=0, depth=0, state=gameState):
            # verifica se jogo acabou, se sim retorna self.evaluationFunction(state) ou betterEvaluationFunction do estado
            # isWin() e isLose() indicam fim de jogo; depth == self.depth indica que atingimos o limite de busca
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            # calcula próximo agente
            # os agentes são indexados: 0 = Pac-Man, 1..N-1 = fantasmas
            # quando chegamos no último fantasma, o próximo agente volta a ser o Pac-Man (índice 0)
            numAgents = state.getNumAgents()
            nextAgent = 0 if agentIndex == numAgents - 1 else agentIndex + 1

            # calcula próxima profundidade (apenas e agentIndex == self.index a profundidade aumenta)
            # uma "rodada" completa acontece quando todos os agentes jogaram uma vez
            # então só incrementamos a profundidade quando o último fantasma terminar sua jogada
            nextDepth = depth + 1 if agentIndex == numAgents - 1 else depth

            if agentIndex == 0:
                # turno do Pac-Man: nó MAX — queremos o maior score possível
                bestScore = -float('inf')  # inicia com o pior valor possível para maximização
                bestAction = None          # vai armazenar a ação que leva ao melhor score

                # para cada ação possível em state.getLegalActions(agentIndex)
                # getLegalActions retorna todas as direções válidas que o agente pode seguir
                for action in state.getLegalActions(agentIndex):
                    # calcula o próximo estado com state.generateSuccessor(agentIndex, action)
                    # generateSuccessor simula o que acontece no jogo após o agente executar a ação
                    successor = state.generateSuccessor(agentIndex, action)

                    # calcula o score chamando minimax recursivamente
                    # chamamos minimax para o próximo agente e próxima profundidade nesse estado sucessor
                    score = minimax(nextAgent, nextDepth, successor)

                    # se for um passo de maximização e o score for maior que o anterior, selecione ele
                    # atualizamos o melhor score e guardamos a ação correspondente
                    if score > bestScore:
                        bestScore = score
                        bestAction = action

                # retorne a melhor ação
                # na chamada raiz (depth == 0) retornamos a ação para o jogo executar
                # nas chamadas recursivas internas retornamos apenas o score numérico
                return bestAction if depth == 0 else bestScore

            else:
                # turno dos fantasmas: nó MIN — querem o menor score possível para o Pac-Man
                bestScore = float('inf')  # inicia com o pior valor possível para minimização

                # para cada ação possível em state.getLegalActions(agentIndex)
                # getLegalActions retorna todas as direções válidas que o fantasma pode seguir
                for action in state.getLegalActions(agentIndex):
                    # calcula o próximo estado com state.generateSuccessor(agentIndex, action)
                    # generateSuccessor simula o que acontece no jogo após o fantasma executar a ação
                    successor = state.generateSuccessor(agentIndex, action)

                    # calcula o score chamando minimax recursivamente
                    # chamamos minimax para o próximo agente e próxima profundidade nesse estado sucessor
                    score = minimax(nextAgent, nextDepth, successor)

                    # se for um passo de minimização e o score for menor que o anterior, selecione ele
                    # o fantasma quer piorar ao máximo a situação do Pac-Man
                    if score < bestScore:
                        bestScore = score

                # retorne a melhor ação
                # fantasmas não precisam retornar a ação, apenas o score mínimo encontrado
                return bestScore

        return minimax()


def betterEvaluationFunction(currentGameState: GameState):
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()

    # Calcula a distância de Manhattan para a comida mais próxima
    foodDistances = [manhattanDistance(pos, f) for f in food]
    if len(foodDistances) > 0:
        minFoodDistance = min(foodDistances)
    else:
        minFoodDistance = 0

    # Distância para o fantasma mais próximo
    ghostDistances = [manhattanDistance(pos, ghost.getPosition()) for ghost in ghostStates]
    minGhostDistance = min(ghostDistances)

    # Aumenta a pontuação se o fantasma estiver assustado, mas penaliza se estiver muito perto
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    if min(scaredTimes) > 0:
        minGhostDistance = 0  # Ignora fantasmas assustados

    return currentGameState.getScore() - (1.5 / (minFoodDistance + 1)) + (2 / (minGhostDistance + 1))

# Abbreviation
better = betterEvaluationFunction
