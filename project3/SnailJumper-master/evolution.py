import copy
import random
from player import Player
import numpy as np

class Evolution:
    def __init__(self):
        self.game_mode = "Neuroevolution"

    def next_population_selection(self, players, num_players):
        """
        Gets list of previous and current players (μ + λ) and returns num_players number of players based on their
        fitness value.

        :param players: list of players in the previous generation
        :param num_players: number of players that we return
        :returns player who selected with SUS algorithm
        """
        # TODO (Implement top-k algorithm here)
        # TODO (Additional: Implement roulette wheel here)
        # TODO (Additional: Implement SUS here)
        # TODO (Additional :Implement Q tournament here)
        #first create coppy of player
        players_copy=[]
        for i in players:
            players_copy.append(i)
        new_players=[]

        #implement SUS
        players_fittnes=[]
        players_sorted=sorted(players_copy,key=lambda x:x.fitness)
        fitness_sum=0
        for player in players_sorted:
            fitness_sum+=player.fitness
        for player in players_sorted:
            players_fittnes.append(player.fitness/fitness_sum)
        random_num=random.uniform(0,1/num_players)
        sum=players_fittnes[0]
        count=0
        for counter in range(num_players):
            while((random_num>sum)):
                count+=1
                sum+=players_fittnes[count]
            new_players.append(players_sorted[count])
            random_num+=1/num_players

        # implement Q tournament
        # for i in range(num_players):
        #     temp_players=[]
        #     for j in range(3):
        #         x=random.randint(0,len(players_copy))
        #         temp_players.append(players_copy[x])
        #     best_fitness=temp_players[0]
        #     for player in temp_players:
        #         if(player.fitness>best_fitness.fitness):
        #             best_fitness=player
        #     new_players.append(best_fitness)
        #

        # TODO (Additional: Learning curve)
        return new_players

    def generate_new_population(self, num_players, prev_players=None):
        """
        Gets survivors and returns a list containing num_players number of children.

        :param num_players: Length of returning list
        :param prev_players: List of survivors
        :return: A list of children
        """
        first_generation = prev_players is None
        if first_generation:
            return [Player(self.game_mode) for _ in range(num_players)]
        else:
            new_parents=[]
            # TODO ( Parent selection and child generation )
            # TODO ( Select  parent with Q Tournament )
            for i in range(num_players):
                temp_players=[]
                for j in range(3):
                    x=random.randint(0,len(prev_players))
                    temp_players.append(prev_players[x])
                best_fitness=temp_players[0]
                for player in temp_players:
                    if(player.fitness>best_fitness.fitness):
                        best_fitness=player
                new_parents.append(best_fitness)
            children=[]
            for j in range(num_players/2):
                parent1=random.randint(0,len(new_parents))
                parent2=random.randint(0,len(new_parents))
                parent1=new_parents[parent1]
                parent2=new_parents[parent2]

                while(parent1==parent2):
                    parent2 = random.randint(0, len(new_parents))
                children1=self.clone_player(parent1)
                children2=self.clone_player(parent2)
                for i in range(25):
                    children1.nn.w[0][i]=parent2.nn.w[0][i]
                    children2.nn.w[0][i]=parent1.nn.w[0][i]
                for k in range(25,50):
                    for counter in range(5):
                        children1.nn.w[0][k][counter]=random.uniform(0,1)


            new_players = prev_players  # DELETE THIS AFTER YOUR IMPLEMENTATION
            return new_players

    def clone_player(self, player):
        """
        Gets a player as an input and produces a clone of that player.
        """
        new_player = Player(self.game_mode)
        new_player.nn = copy.deepcopy(player.nn)
        new_player.fitness = player.fitness
        return new_player
