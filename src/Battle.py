from Othello import OthelloBoard
from AlphaBetaAgent import AlphaBetaAgent
from MCTSAgent import MonteCarloTreeSearchAgent
from OtherAgents import RandomAgent, MaxStonesAgent, MinStonesAgent

# Plays a game between the agent for black and the agent for white
def play_game(agentBlack, agentWhite):
    board = OthelloBoard()
    while not board.game_over:
        if board.current_player == 1:
            board = agentBlack.make_move(board)
        else:
            board = agentWhite.make_move(board)
        if board is None:
            print(agentBlack.name)
            print(agentWhite.name)
            
    return board.get_result()

# Plays a match between two agents with "games" pairs of games
def play_match(agent1, agent2, games):
    wins = 0
    losses = 0
    draws = 0
    for i in range(games):
        res = play_game(agent1, agent2)
        if res == 1:
            wins += 1
        elif res == -1:
            losses += 1
        else:
            draws += 1
        res = play_game(agent2, agent1)
        if res == 1:
            losses += 1
        elif res == -1:
            wins += 1
        else:
            draws += 1
    return (wins, losses, draws)

# Plays a round-robin
def play_round(agents, ratings):
    results = [[0 for _ in range(len(agents))] for _ in range(len(agents))]
    expected_results = [[0 for _ in range(len(agents))] for _ in range(len(agents))]
    for i in range(len(agents)):
        for j in range(i+1, len(agents)):
            match_result = play_match(agents[i], agents[j], 1)
            results[i][j] = match_result[0] + match_result[2]/2
            results[j][i] = match_result[1] + match_result[2]/2
            expected_results[i][j] = 2/(1+10**((ratings[j]-ratings[i])/400))
            expected_results[j][i] = 2/(1+10**((ratings[i]-ratings[j])/400))
    actual = [sum(results[i]) for i in range(len(agents))]
    expected = [sum(expected_results[i]) for i in range(len(agents))]
    print(actual)
    print(expected)
    next_ratings = [ratings[i] + 100*(actual[i]-expected[i]) for i in range(len(agents))]
    return results, next_ratings

# Plays a tournament between an array of agents
def play_tournament(agents, pairs):
    ratings = [1000 for _ in range(len(agents))]
    overall_results = [[0 for _ in range(len(agents))] for _ in range(len(agents))]
    for i in range(pairs):
        results, ratings = play_round(agents, ratings)
        for i in range(len(agents)):
            for j in range(len(agents)):
                overall_results[i][j] += results[i][j]
        print(f'Round {i}')
        print_results(results, list(map(lambda agent:agent.name, agents)))
        print(ratings)
    print_results(overall_results, list(map(lambda agent:agent.name, agents)))
    
# Print results for the tournament
def print_results(results, team_names):
    # Printing the header row
    print("{:<20}".format(""), end="")
    for team_name in team_names:
        print("{:<20}".format(team_name), end="")
    print()

    # Printing the rows with results
    for i, row in enumerate(results):
        print("{:<20}".format(team_names[i]), end="")
        for result in row:
            print("{:<20}".format(result), end="")
        print()
    
# Main method to run tournaments.
def main():
    agents = [AlphaBetaAgent(0.02), AlphaBetaAgent(0.1), AlphaBetaAgent(0.5), MonteCarloTreeSearchAgent(0.02), MonteCarloTreeSearchAgent(0.1), MonteCarloTreeSearchAgent(0.5), MaxStonesAgent, MinStonesAgent, RandomAgent]
    #agents = [AlphaBetaAgent(0.02), MonteCarloTreeSearchAgent(0.02), MaxStonesAgent, MinStonesAgent, RandomAgent]
    play_tournament(agents, 10)

if __name__ == "__main__":
    main()