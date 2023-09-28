from dataclasses import dataclass


class GameLog:
    entity_to_class_id: dict[int, str] = {}

    def __init__(self):
        self.players: dict[int, Player] = {}

    def get_total_damage(self):
        game_total_damage = 0
        for player in self.players.values():
            for value in player.damage_dealt.values():
                game_total_damage += value
        return game_total_damage

    def get_percent_total_damage(self, entity):
        return '({:.1%})'.format(entity.get_total_damage() / self.get_total_damage())


@dataclass
class Player:
    id: int
    name: str
    damage_dealt: dict[str, int]
    damage_received: dict[str, int]
    status_effects_applied: dict[str, int]
    status_effects_received: dict[str, int]

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
        return '({:.1%})'.format(self.damage_dealt[damage_source] / self.get_total_damage())
