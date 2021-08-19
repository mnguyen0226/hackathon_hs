# Credit: RemptonGames

import asyncio
import time

from src.benchmark_agents.scripted_player import battle_utilities
from poke_env.player.random_player import RandomPlayer
from src.benchmark_agents.scripted_player.max_damage_player import MaxDamagePlayer
from poke_env.player.player import Player
from poke_env.player.baselines import SimpleHeuristicsPlayer


class SwitchMaxDamagePlayer(Player):
    prev_dam_percent = 100
    curr_dam_percent = 100
    used_move_prev = False
    curr_opponent = None
    prev_opponent = None

    def choose_move(self, battle):
        """Choose the best move to beat the opponent's current pokemon. The logic is simple:
        Since the 6 pokemons are randomply provided, we measure weather our current pokemon
        "match" the type of the opponent's (the higher the match, the more likely we will lose).
        If score exceed the set threshold, then swap the pokemon in the pocket with the lowest matchup score
        of the opponent's pokemon. Else, we pick the max damage action.

        Parameter
        ----------
        battle:
            Max damage player's turn in the battle

        Return
        ----------
        Ordered action of the current pokemon.
        """
        self.curr_opponent = battle.opponent_active_pokemon
        if self.curr_opponent != self.prev_opponent:
            self.curr_dam_percent = 100
            self.prev_dam_percent = 100
        else:
            self.curr_dam_percent = battle.opponent_active_pokemon.current_hp
        self.prev_dam_percent = self.curr_dam_percent
        self.used_move_prev = False
        self.prev_opponent = self.curr_opponent

        # If Pokemon is out of moves, switch to best option
        if not battle.available_moves:
            best_switch = self.choose_best_switch(battle)
            if best_switch is None:
                return self.choose_default_move(battle)
            return self.create_order(best_switch)

        # Use info such as type matchup and relative speed to determine who to switch to
        matchup_score = self.get_matchup_score(
            battle.active_pokemon, battle.opponent_active_pokemon
        )
        # If negative situation exceeds threshold, switch Pokemon
        if matchup_score >= 1:
            best_switch = self.choose_best_switch(battle)
            if best_switch is not None:
                return self.create_order(best_switch)

        # finds the best move among available ones
        self.used_move_prev = True
        best_move = max(
            battle.available_moves,
            key=lambda move: battle_utilities.calculate_damage(
                move, battle.active_pokemon, battle.opponent_active_pokemon, True, True
            ),
        )
        return self.create_order(best_move)

    def choose_best_switch(self, battle):
        """Helper function: choose the best pokemon index to switch according to the match up score

        Parameter
        ----------
        battle:
            Max damage player's turn in the battle

        Return
        ----------
        best_switch:
            best pokemon index to switch with your current pokemon
        """
        if not battle.available_switches:
            return None
        # Go through each Pokemon that can be switched to, and choose one with the best type matchup
        # (smaller multipliers are better)
        best_score = float("inf")
        best_switch = battle.available_switches[0]
        for switch in battle.available_switches:
            score = self.get_matchup_score(switch, battle.opponent_active_pokemon)
            if score < best_score:
                best_score = score
                best_switch = switch
        return best_switch

    def get_matchup_score(self, my_pokemon, opponent_pokemon):
        """Helper function: gets a float number determining how well your current pokemon matches up with the
        opponent's. The lower the score, the better. This score is arbitrary.

        Parameter
        ----------
        my_pokemon:
            Your current pokemon on the battle field
        opponent_pokemon:
            The opponent's current pokemon on the battle fields

        Return
        ----------
        score:
            floating point match up score
        """
        score = 0
        defensive_multiplier = battle_utilities.get_defensive_type_multiplier(
            my_pokemon, opponent_pokemon
        )
        # A multiplier greater than 1 means we are at a type disadvantage. If there is a better type match, switch
        if defensive_multiplier == 4:
            score += 1
        elif defensive_multiplier == 2:
            score += 0.5
        elif defensive_multiplier == 0.5:
            score -= 0.5
        elif defensive_multiplier == 0.25:
            score -= 1
        if battle_utilities.opponent_can_outspeed(my_pokemon, opponent_pokemon):
            score += 0.5
        return score


async def main():
    # We create two players
    random_player = RandomPlayer(battle_format="gen8randombattle")
    heuristic_player = SimpleHeuristicsPlayer(battle_format="gen8randombattle")
    switch_max_damage_player = SwitchMaxDamagePlayer(battle_format="gen8randombattle")
    max_damage_player = MaxDamagePlayer(battle_format="gen8randombattle")

    # Start the time tracker
    start = time.time()

    # Let the switch-max-damage player fight against the random player 500 battles
    await switch_max_damage_player.battle_against(random_player, n_battles=500)

    # Print the results
    print(
        f"Max damage player won {switch_max_damage_player.n_won_battles} / 500 battles against random player [this took {time.time() - start} seconds]"
    )

    # Start the time tracker
    start = time.time()

    # Let the switch-max-damage player fight against the random player 500 battles
    await switch_max_damage_player.battle_against(max_damage_player, n_battles=500)

    # Print the results
    print(
        f"Max damage player won {switch_max_damage_player.n_won_battles - 500} / 500 battles against max damage player [this took {time.time() - start} seconds]"
    )

    # Start the time tracker
    start = time.time()

    # Let the switch-max-damage player fight against the random player 500 battles
    await switch_max_damage_player.battle_against(heuristic_player, n_battles=500)

    # Print the results
    print(
        f"Max damage player won {switch_max_damage_player.n_won_battles - 1000} / 500 battles against heuristic player [this took {time.time() - start} seconds]"
    )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    # Max damage player won 475 / 500 battles against random player [this took 58.64057779312134 seconds]
    # Max damage player won 388 / 500 battles against max damage player [this took 43.91090226173401 seconds]
    # Max damage player won 23 / 500 battles against heuristic player [this took 47.222079277038574 seconds]
