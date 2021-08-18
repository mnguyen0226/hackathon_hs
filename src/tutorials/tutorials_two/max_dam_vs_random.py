"""
For Max Damage Pokemon
- If the active pokemon can attack, it will attack and use the move with the highest damage.
- Else, if will perform random action.
- Max Damage Pokemon will be evaluated with 100 battles against Random Action Pokemon.
- Since both are scripted agents, there are no need for training.
"""

import asyncio
import time

from poke_env.player.player import Player
from poke_env.player.random_player import RandomPlayer

class MaxDamagePlayer(Player):
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

        # If no attacks is available, a random switch will be made
        else:
            return self.choose_random_move(battle)

async def main():
    # Start the time tracker
    start = time.time()

    # We create two players
    random_player = RandomPlayer(battle_format="gen8randombattle")
    max_damage_player = MaxDamagePlayer(battle_format="gen8randombattle")

    # Let the max-damage player fight against the random player 100 battles
    await max_damage_player.battle_against(random_player, n_battles=100)

    # Print the results
    print(
        f"Max damage player won {max_damage_player.n_won_battles} / 100 battles [this took {time.time() - start} seconds]"
    )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
