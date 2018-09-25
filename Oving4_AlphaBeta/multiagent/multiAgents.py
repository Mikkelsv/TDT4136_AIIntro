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
import operator

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    def is_terminal(self,state):
        return (state.isWin() or state.isLose())

    def minmax_value(self,state,c):
        if state.isWin() or state.isLose() or c==self.depth*self.agents:
            return self.evaluationFunction(state)
        a = c%self.agents #current agent
        
        if a: v = float('inf') #if ghosts
        else: v = -float('inf') #if pacmnan
        for action in state.getLegalActions(a): #Actions for agent
            s_state = state.generateSuccessor(a,action)
            if a: v = min(v,self.minmax_value(s_state,c+1)) #min value for ghosts
            else: v = max(v,self.minmax_value(s_state,c+1))  #max for pac
        return v
          
    def getAction(self, gameState):
        self.agents = gameState.getNumAgents();

        actions = gameState.getLegalActions(0)
        choises = {}
        for action in actions:
            choises[action] =  self.minmax_value(gameState.generateSuccessor(0,action),1)
        return max(choises.iteritems(), key=operator.itemgetter(1))[0]

class AlphaBetaAgent(MultiAgentSearchAgent):
    def minmax_value(self, state, c, a, b):
        if state.isWin() or state.isLose() or c == self.depth * self.agents:
            return self.evaluationFunction(state), None #if final state return values
        g = c%self.agents
        if g: v = float('inf'),None #if ghosts
        else: v = -float('inf'), None #else pacman
        actions = state.getLegalActions(g)
        if not actions:
            return self.evaluationFunction(state), None
        for action in actions:
            s_state = state.generateSuccessor(g, action)
            s = self.minmax_value(s_state, c+1, a, b)
            if g: #min value for ghosts
              if s[0] < v[0]: v = s[0], action
              if v[0] < a: return v
              b = min(b, v[0])
            else: #max value for pac
              if s[0] > v[0]: v = s[0], action
              if v[0] > b: return v
              a = max(a, v[0])
        return v

    def getAction(self, gameState):
        self.agents = gameState.getNumAgents()
        return self.minmax_value(gameState, 0, -float('inf'), float('inf'))[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

