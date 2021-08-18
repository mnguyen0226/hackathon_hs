import asyncio
from poke_env.player.random_player import RandomPlayer
from poke_env.player_configuration import PlayerConfiguration
from poke_env.server_configuration import ShowdownServerConfiguration

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


async def main():
    # Create a max damage player with an account
    pokebot = MaxDamagePlayer(
        player_configuration=PlayerConfiguration("minheapolis_bot", "heron_is_a_bird"),
        server_configuration=ShowdownServerConfiguration,
    )

    # Sending challenges to "your_username"
    await pokebot.send_challenges("mnguyen", n_challenges=1)

    # Accepting one challenge from any user
    await pokebot.accept_challenges(None, 1)

    # Accepting three challenges from "your_username"
    await pokebot.accept_challenges("mnguyen", 2)

    # Playing 5 games on the ladder
    await pokebot.ladder(5)

    # Print the rating of the player and tis opponent after each battle
    for battle in pokebot.battles.values():
        print(battle.rating, battle.opponent_rating)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
