import asyncio
from poke_env.player_configuration import PlayerConfiguration
from poke_env.server_configuration import ShowdownServerConfiguration
from stable_baselines import DQN
import numpy as np
from poke_env.player.random_player import RandomPlayer
from gym.spaces import Box, Discrete
from poke_env.player.env_player import Gen8EnvSinglePlayer

trained_model = DQN.load(
    "/home/mnguyen/Documents/summer2021/pokemon/hackathon_hs/src/tutorials/tutorial_six/dqn_sb_agent"
)

class TrainedRLPlayer(Gen8EnvSinglePlayer):
    observation_space = Box(low=-10, high=10, shape=(10,))
    action_space = Discrete(22)

    def getThisPlayer(self):
        """Get the current RL agent"""
        return self

    def __init__(self, *args, **kwargs):
        """Initialize agent"""
        Gen8EnvSinglePlayer.__init__(self, *args, **kwargs)
        self.model = trained_model

    def embed_battle(self, battle):
        """Embed Player to battles and return info from the Pokemon Showdown environment
        Parameter
        ----------
        battle:
            Max damage player's turn in the battle
        Return
        ----------
        list of [4 moves, damaging values of each moves, number of pokemons of player, number of pokemons of opponent]
        """
        # -1 indicates that the move does not have a base power
        # or is not available
        moves_base_power = -np.ones(4)
        moves_dmg_multiplier = np.ones(4)
        for i, move in enumerate(battle.available_moves):
            moves_base_power[i] = (
                move.base_power / 100
            )  # Simple rescaling to facilitate learning
            if move.type:
                moves_dmg_multiplier[i] = move.type.damage_multiplier(
                    battle.opponent_active_pokemon.type_1,
                    battle.opponent_active_pokemon.type_2,
                )

        # We count how many pokemons have not fainted in each team
        remaining_mon_team = (
            len([mon for mon in battle.team.values() if mon.fainted]) / 6
        )
        remaining_mon_opponent = (
            len([mon for mon in battle.opponent_team.values() if mon.fainted]) / 6
        )

        # Final vector with 10 components
        return np.concatenate(
            [
                moves_base_power,
                moves_dmg_multiplier,
                [remaining_mon_team, remaining_mon_opponent],
            ]
        )

    def compute_reward(self, battle) -> float:
        """Compute rewards for each action taken of player in the battle
        Parameter
        ----------
        battle:
            Max damage player's turn in the battle
        Return
        ---------
        float value of the rewards return from the environment
        """
        return self.reward_computing_helper(
            battle, fainted_value=2, hp_value=1, victory_value=30
        )

    def _action_to_move(self, action, battle):

        """Converts actions to move orders.

        The conversion is done as follows:

        0 <= action < 4:
        The actionth available move in battle.available_moves is executed.
        4 <= action < 8:
        The action - 4th available move in battle.available_moves is executed, with
        z-move.
        8 <= action < 12:
        The action - 8th available move in battle.available_moves is executed, with
        mega-evolution.
        12 <= action < 18
        The action - 12th available switch in battle.available_switches is executed.

        If the proposed action is illegal, a random legal move is performed.

        :param action: The action to convert.
        :type action: int
        :param battle: The battle in which to act.
        :type battle: Battle
        :return: the order to send to the server.
        :rtype: str
        """
        if (
                action < 4
                and action < len(battle.available_moves)
                and not battle.force_switch
        ):
            return self.create_order(battle.available_moves[action])
        elif (
                not battle.force_switch
                and battle.can_z_move
                and 0 <= action - 4 < len(battle.active_pokemon.available_z_moves)
        ):
            return self.create_order(
                battle.active_pokemon.available_z_moves[action - 4], z_move=True
            )
        elif (
                battle.can_mega_evolve
                and 0 <= action - 8 < len(battle.available_moves)
                and not battle.force_switch
        ):
            return self.create_order(battle.available_moves[action - 8], mega=True)
        elif (
                battle.can_dynamax
                and 0 <= action - 12 < len(battle.available_moves)
                and not battle.force_switch
        ):
            return self.create_order(battle.available_moves[action - 12], dynamax=True)
        elif 0 <= action - 16 < len(battle.available_switches):
            return self.create_order(battle.available_switches[action - 16])
        else:
            return self.choose_random_move(battle)

    def choose_move(self, battle):
        """Choose move automatically

        Parameter
        ----------
        battle:
            Max damage player's turn in the battle

        Return
        ----------
        Either best action or random action
        """
        if (battle.available_moves):
            observations = self.embed_battle(battle)
            action = self.model.predict(observations)[0] 
            return self._action_to_move(action, battle)
        else: 
            print("Random Move")
            return self.choose_random_move(battle)


class MaxDamagePlayer(RandomPlayer):
    def choose_move(self, battle):
        """Choose the best move of the max damage player.
        If the agents can attack then it will choose the best move,
        else it will be a random move

        Parameter
        ----------
        battle:
            Max damage player's turn in the battle

        Return
        ----------
        Either max-damage-move or random move
        """
        # If the player can attack, it will
        if battle.available_moves:
            # Finds the best move among available ones
            print("Choose Move")
            best_move = max(battle.available_moves, key=lambda move: move.base_power)
            return self.create_order(best_move)

        # If no attack is available, a random switch will be made
        else:
            print("Random Move")
            return self.choose_random_move(battle)


async def main():
    # Create a TrainedRLPlayer
    simplerl_player = TrainedRLPlayer(
        player_configuration=PlayerConfiguration("minheapolis_bot", "Minh123456!"),
        server_configuration=ShowdownServerConfiguration,
    )

    # Sending challenges to "your_username"
    await simplerl_player.send_challenges("mnguyen_2", n_challenges=1)

    # Accepting one challenge from any user
    await simplerl_player.accept_challenges(None, 1)

    # Accepting three challenges from "your_username"
    await simplerl_player.accept_challenges("mnguyen_2", 2)

    # Playing 5 games on the ladder
    await simplerl_player.ladder(5)

    # Print the rating of the player and tis opponent after each battle
    for battle in simplerl_player.battles.values():
        print(battle.rating, battle.opponent_rating)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
