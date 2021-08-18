import asyncio
from poke_env.player.random_player import RandomPlayer
from poke_env.player_configuration import PlayerConfiguration
from poke_env.server_configuration import ShowdownServerConfiguration


async def main():
    # Create a max damage player with an account
    random_pokebot = RandomPlayer(
        player_configuration=PlayerConfiguration("mnguyen", "heron_is_a_bird"),
        server_configuration=ShowdownServerConfiguration,
    )

    # Sending challenges to "your_username"
    await random_pokebot.send_challenges("minheapolis_bot", n_challenges=1)

    # Accepting one challenge from any user
    await random_pokebot.accept_challenges(None, 1)

    # Accepting three challenges from "your_username"
    await random_pokebot.accept_challenges("minheapolis_bot", 2)

    # Playing 5 games on the ladder
    await random_pokebot.ladder(5)

    # Print the rating of the player and tis opponent after each battle
    for battle in random_pokebot.battles.values():
        print(battle.rating, battle.opponent_rating)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
