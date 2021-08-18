import numpy as np
from gym.spaces import Box, Discrete
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN
from poke_env.player.env_player import Gen8EnvSinglePlayer
from poke_env.player.random_player import RandomPlayer


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
            best_move = max(battle.available_moves, key=lambda move: move.base_power)
            return self.create_order(best_move)

        # If no attack is available, a random switch will be made
        else:
            return self.choose_random_move(battle)


# Class create a simple RL player DQN
class SimpleRLPlayer(Gen8EnvSinglePlayer):

    observation_space = Box(low=-10, high=10, shape=(10,))
    action_space = Discrete(22)

    def getThisPlayer(self):
        """Get the current RL agent"""
        return self

    def __init__(self, *args, **kwargs):
        """Initialize agent"""
        Gen8EnvSinglePlayer.__init__(self)

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


# Create 3 players compatible with the pokemon environment
envPlayer = SimpleRLPlayer(battle_format="gen8randombattle")
opponent_random = RandomPlayer(battle_format="gen8randombattle")
opponent_max_dam = MaxDamagePlayer(battle_format="gen8randombattle")

# Create a DQN model
model = DQN(MlpPolicy, envPlayer, gamma=0.5, verbose=1)

# Training script
def training(player):
    """Training script for DQN Player

    Parameter
    ----------
    player:
        current envPlayer
    """
    print("Training...")
    model.learn(total_timesteps=1000)
    print("Training complete.")


# Evaluating scripts
def evaluating(player):
    """Evaluating script for the DQN Player

    Parameter
    ----------
    player:
        current envPlayer
    """
    player.reset_battles()
    for _ in range(100):
        done = False
        obs = player.reset()
        while not done:
            action = model.predict(obs)[0]
            obs, _, done, _ = player.step(action)
            # print ("done:" + str(done))
    player.complete_current_battle()

    print(
        "DQN Evaluation: %d victories out of %d episodes" % (player.n_won_battles, 100)
    )


def main():
    # Training against random player
    envPlayer.play_against(
        env_algorithm=training,
        opponent=opponent_random,
    )

    # Training against max damage player
    envPlayer.play_against(
        env_algorithm=training,
        opponent=opponent_max_dam,
    )

    print("Evaluating against random player")
    envPlayer.play_against(
        env_algorithm=evaluating,
        opponent=opponent_random,
    )

    print("Evaluating against max damage player")
    envPlayer.play_against(
        env_algorithm=evaluating,
        opponent=opponent_max_dam,
    )

    print("Saving Model...")
    model.save("/path_to_this/hackathon_hs/src/tutorials/tutorial_five/dqn_sb_agent")
    print("Model Save")


if __name__ == "__main__":
    main()
