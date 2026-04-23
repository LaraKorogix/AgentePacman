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

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState
from multiAgents import MultiAgentSearchAgent


class MinimaxAgent(MultiAgentSearchAgent):

    def getAction(self, gameState: GameState):
        """
        Implementação do algoritmo Minimax.
        O Pac-Man busca maximizar a pontuação enquanto os fantasmas tentam minimizá-la.
        """

        def minimax(agentIndex=0, depth=0, state=gameState):

            # Para quando o jogo acaba ou atinge a profundidade máxima
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            numAgents = state.getNumAgents()

            # Define próximo agente
            nextAgent = 0 if agentIndex == numAgents - 1 else agentIndex + 1

            # Aumenta profundidade apenas quando todos jogaram
            nextDepth = depth + 1 if agentIndex == numAgents - 1 else depth

            # Turno do Pac-Man (MAX)
            if agentIndex == 0:
                bestScore = -float('inf')
                bestAction = None

                for action in state.getLegalActions(agentIndex):

                    # Remove ação STOP para evitar ficar parado
                    if action == Directions.STOP:
                        continue

                    successor = state.generateSuccessor(agentIndex, action)
                    score = minimax(nextAgent, nextDepth, successor)

                    # Escolhe melhor ação
                    if score > bestScore:
                        bestScore = score
                        bestAction = action

                    # Desempate aleatório
                    elif score == bestScore:
                        bestAction = random.choice([bestAction, action])

                return bestAction if depth == 0 else bestScore

            # Turno dos fantasmas (MIN)
            else:
                bestScore = float('inf')

                for action in state.getLegalActions(agentIndex):

                    # Também removo STOP dos fantasmas
                    if action == Directions.STOP:
                        continue

                    successor = state.generateSuccessor(agentIndex, action)
                    score = minimax(nextAgent, nextDepth, successor)

                    if score < bestScore:
                        bestScore = score

                return bestScore

        return minimax()


def betterEvaluationFunction(currentGameState: GameState):
    """
    Função heurística que avalia o estado do jogo.
    Considera comida, fantasmas e movimentação do Pac-Man.
    """

    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()

    score = currentGameState.getScore()

    # Penaliza ficar parado
    if currentGameState.getPacmanState().getDirection() == Directions.STOP:
        score -= 5

    # Distância até comida
    foodDistances = [manhattanDistance(pos, f) for f in food]
    if foodDistances:
        minFoodDistance = min(foodDistances)
        score -= 1.5 / (minFoodDistance + 1)

    # Menos comida é melhor
    score -= 4 * len(food)

    # Análise dos fantasmas
    for ghost in ghostStates:
        ghostDistance = manhattanDistance(pos, ghost.getPosition())

        if ghost.scaredTimer > 0:
            score += 2 / (ghostDistance + 1)
        else:
            score -= 3 / (ghostDistance + 1)

            if ghostDistance < 2:
                score -= 10

    return score


better = betterEvaluationFunction