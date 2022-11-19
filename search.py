# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    # DFS use stack as the fringe
    fringe = util.Stack()
    visited = [] # visited nodes
    # push the start state to the fringe
    fringe.push((problem.getStartState(), [], 1))

    # loop until we remove all nodes from the fringe
    while not fringe.isEmpty():
        node = fringe.pop()
        state = node[0]
        action = node[1]

        if problem.isGoalState(state):
            return action
        if state not in visited:
            visited.append(state)
            successor = problem.getSuccessors(state)
            for sub in successor:
                subState = sub[0]
                subAction = sub[1]
                if subState not in visited:
                    subAction = action + [subAction]
                    fringe.push((subState, subAction, 1))
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    # BFS use queue as the fringe
    fringe = util.Queue()
    visited = []  # visited nodes
    # push the start state to the fringe
    fringe.push((problem.getStartState(), [], 1))

    # loop until we remove all nodes from the fringe
    while not fringe.isEmpty():
        node = fringe.pop()
        state = node[0]
        action = node[1]

        if problem.isGoalState(state):
            return action
        if state not in visited:
            visited.append(state)
            successor = problem.getSuccessors(state)
            for sub in successor:
                subState = sub[0]
                subAction = sub[1]
                if subState not in visited:
                    subAction = action + [subAction]
                    fringe.push((subState, subAction, 1))
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    # UCS use priority queue as the fringe
    fringe = util.PriorityQueue()
    # using dictionary for visited and cost
    visited = {} 
    cost = {}
    solution = [] # solution node hold list of visited node
    parents = {}

    fringe.push((problem.getStartState(), 'None', 0), 0)
    visited[problem.getStartState()] = 'None'
    cost[problem.getStartState()] = 0

    # handle case where the start stae is the goal state
    if problem.isGoalState(problem.getStartState()):
        return solution

    goal = False # keep track of whether reach goal state yet
    # loop until the fringe is empty or goal is reach
    while(not fringe.isEmpty() and not goal):
        node = fringe.pop()
        visited[node[0]] = node[1]
        if problem.isGoalState(node[0]):
            node_sol = node[0]
            goal = True
            break
        for e in problem.getSuccessors(node[0]):
            if e[0] not in visited.keys():
                priority = node[2] + e[2]
                if e[0] in cost.keys():
                    if cost[e[0]] <= priority:
                        continue
                fringe.push((e[0], e[1], priority), priority)
                cost[e[0]] = priority
                parents[e[0]] = node[0]

    while(node_sol in parents.keys()):
        node_sol_prev = parents[node_sol]
        solution.insert(0, visited[node_sol])
        node_sol = node_sol_prev

    return solution

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    # a* use priority queue as the fringe
    fringe = util.PriorityQueue()
    visited = [] # visited node
    # push the start state to the fringe
    fringe.push((problem.getStartState(), [], 0), heuristic(problem.getStartState(), problem))

    # loop until the fringe is empty
    while not fringe.isEmpty():
        node = fringe.pop()
        state = node[0]
        action = node[1]
        if problem.isGoalState(state):
            return action
        if state not in visited:
            visited.append(state)
            successors = problem.getSuccessors(state)
            for sub in successors:
                subState = sub[0]
                subAction = sub[1]
                if subState not in visited:
                    subAction = action + [subAction]
                    cost = problem.getCostOfActions(subAction)
                    fringe.push((subState, subAction, 0), cost + heuristic(subState, problem))
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch