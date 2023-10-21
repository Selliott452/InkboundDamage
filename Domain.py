from dataclasses import dataclass


@dataclass
class Player:
    id: int
    name: str
    class_id: str
    # [ damage source, total damage, run, combat, turn ]
    damage_dealt: dict[str, int, int, int, int]
    damage_received: dict[str, int, int, int, int]
    status_effects_applied: dict[str, int, int, int, int]
    status_effects_received: dict[str, int, int, int, int]

    def get_total_damage(self):
        player_total_damage = 0
        for value in self.damage_dealt.values():
            player_total_damage += value
        return player_total_damage

    def get_total_damage_received(self):
        player_damage_taken = 0
        for value in self.damage_received.values():
            player_damage_taken += value
        return player_damage_taken

    def get_percent_total_damage(self, damage_source):
        return "({:.1%})".format(
            self.damage_dealt[damage_source] / self.get_total_damage()
        )


# restructure to allow multiple dives
class DiveLog:
    entity_to_class_id: dict[int, str] = {}
    dives: list[dict[int, Player]] = [{}]
    dive_number: int

    def __init__(self, dive_number) -> None:
        self.dive_number = dive_number

    def sync_player_classes(self):
        for player in self.get_players().values():
            if player.id in self.entity_to_class_id.keys():
                player.class_id = self.entity_to_class_id[player.id]

    def get_players(self):
        return self.dives[-1]

    def get_total_damage(self):
        game_total_damage = 0
        for player in self.get_players().values():
            for value in player.damage_dealt.values():
                game_total_damage += value
        return game_total_damage

    def get_percent_total_damage(self, entity):
        return "({:.1%})".format(entity.get_total_damage() / self.get_total_damage())


# TODO: CombatLog
# TODO: TurnLog
