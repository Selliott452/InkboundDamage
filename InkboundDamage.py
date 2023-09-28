from dataclasses import dataclass
import time
import re
import tkinter as tk
import os
from threading import Thread


def follow(the_file):
    while True:
        # read last line of file
        next_line = the_file.readline()
        # sleep if file hasn't been updated
        if not next_line:
            render()
            time.sleep(0.1)
            continue

        yield next_line


def handle_line(line, game):
    if "Party run start triggered" in line:
        reset_game()
    if "is playing ability" in line:
        register_new_player(line, game)
    if "broadcasting EventOnUnitDamaged" in line:
        register_ability_damage(line, game)
    # if "EventOnUnitStatusEffectStacks" in line:
    #     register_status_effect_stacks(line, game)


def reset_game():
    global game_log
    game_log = GameLog()
    global player_labels
    player_labels = {}
    global player_frames
    player_frames = {}
    for child in canvas.winfo_children():
        child.destroy()


def register_status_effect_stacks(line, game):
    # TODO:: clean this up
    type = re.search("(?<=EventOnUnitStatusEffectStacks)([a-zA-Z]*)", line).group()
    caster_unit_id = int(re.search("(?<=CasterUnitEntityHandle:\(EntityHandle:)([\-\d]*)", line).group())
    target_unit_id = int(re.search("(?<=TargetUnitEntityHandle:\(EntityHandle:)([\-\d]*)", line).group())
    effect = re.search("(?<=StatusEffectData:StatusEffectData-)([a-zA-Z-_]*)", line).group()

    stacks_added = re.search("(?<=StacksAdded:)(\d*)", line)
    if stacks_added is None:
        stacks_added = 0
    else:
        stacks_added = int(stacks_added.group())

    stacks_removed = re.search("(?<=StacksRemoved:)(\d*)", line)
    if stacks_removed is None:
        stacks_removed = 0
    else:
        stacks_removed = int(stacks_removed.group())

    if type == 'Added':
        # if the target is a player record status effects received
        if target_unit_id in game.players.keys():
            game.players[target_unit_id].status_effects_received[effect] = (
                    game.players[target_unit_id].status_effects_received.get(effect, 0) + stacks_added)

        # if the attacker is a player record status effects applied
        if caster_unit_id in game.players.keys():
            game.players[caster_unit_id].status_effects_applied[effect] = (
                    game.players[caster_unit_id].status_effects_applied.get(effect, 0) + stacks_added)


def register_new_player(line, game):
    player_id = int(re.search("(?<=\(EntityHandle:)(\d*)", line).group())
    player_name = re.search("(?<=I )([a-zA-Z-_]*)", line).group()

    if player_id not in game.players.keys():
        game.players[player_id] = Entity(player_id, player_name, {}, {}, {}, {})


def register_ability_damage(line, game):
    target_id = int(re.search("(?<=TargetUnitHandle:\(EntityHandle:)(\d*)", line).group())
    attacker_id = int(re.search("(?<=SourceEntityHandle:\(EntityHandle:)(\d*)", line).group())
    damage_amount = int(re.search("(?<=DamageAmount:)(\d*)", line).group())
    # Why is their naming scheme so jank??
    damage_type = re.search("(?<=ActionData:)([a-zA-Z-_]*)", line).group().removeprefix(
        "ActionData-").removesuffix("_Action").removesuffix("_ActionData").removesuffix("Damage").removesuffix("_")

    # if the target is a player record damage received
    if target_id in game.players.keys():
        game.players[target_id].damage_received[damage_type] = (
                game.players[target_id].damage_received.get(damage_type, 0) + damage_amount)

    # if the attacker is a player record damage dealt
    if attacker_id in game.players.keys():
        game.players[attacker_id].damage_dealt[damage_type] = (
                game.players[attacker_id].damage_dealt.get(damage_type, 0) + damage_amount)


class GameLog:
    def __init__(self):
        self.players: dict[int, Entity] = {}

    def get_total_damage(self):
        game_total_damage = 0
        for player in self.players.values():
            for value in player.damage_dealt.values():
                game_total_damage += value
        return game_total_damage

    def get_percent_total_damage(self, entity):
        return '({:.1%})'.format(entity.get_total_damage() / self.get_total_damage())


@dataclass
class Entity:
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


logfile = open(os.environ["USERPROFILE"] + "/AppData/LocalLow/Shiny Shoe/Inkbound/logfile.log", "r")
log_lines = follow(logfile)
game_log = GameLog()

root = tk.Tk()
root.title("Inkbound Damage")
root.attributes('-topmost', True)
canvas = tk.Canvas(root)
canvas.pack()

player_frames = {}
player_labels: dict[int, dict[str, any]] = {}


def render():
    for player in game_log.players.values():

        if player.id not in player_frames.keys():
            player_frames[player.id] = tk.Frame(canvas, border=10)

        player_frame = player_frames[player.id]

        if player.id not in player_labels.keys():
            player_labels[player.id] = {}

        if "player_name_label" not in player_labels[player.id].keys():
            player_name_label = tk.Label(player_frame, background="grey", width=50)
            player_name_label.grid(row=0, columnspan=3)
            player_labels[player.id]["player_name_label"] = player_name_label

        if "total_damage_label" not in player_labels[player.id].keys():
            total_damage_label = tk.Label(player_frame, text="Total Damage Dealt")
            total_damage_label.grid(row=1, column=0, sticky=tk.W)
            player_labels[player.id]["total_damage_label"] = total_damage_label

        if "total_damage_amount" not in player_labels[player.id].keys():
            total_damage_amount = tk.Label(player_frame)
            total_damage_amount.grid(row=1, column=1, sticky=tk.E)
            player_labels[player.id]["total_damage_amount"] = total_damage_amount

        if "damage_received_label" not in player_labels[player.id].keys():
            damage_received_label = tk.Label(player_frame, text="Total Damage Received (Including blocked)")
            damage_received_label.grid(row=2, column=0, sticky=tk.W)
            player_labels[player.id]["damage_received_label"] = damage_received_label

        if "damage_received_amount" not in player_labels[player.id].keys():
            damage_received_amount = tk.Label(player_frame)
            damage_received_amount.grid(row=2, column=1, sticky=tk.E)
            player_labels[player.id]["damage_received_amount"] = damage_received_amount

        abilities = sorted(player.damage_dealt.keys(), reverse=True, key=lambda x: player.damage_dealt[x])
        for i, ability in enumerate(abilities, start=3):

            if ability + "_label" not in player_labels[player.id].keys():
                label = tk.Label(player_frame, text=ability)
                player_labels[player.id][ability + "_label"] = label

            if ability + "_amount" not in player_labels[player.id].keys():
                amount = tk.Label(player_frame)
                player_labels[player.id][ability + "_amount"] = amount

            if ability + "_percent" not in player_labels[player.id].keys():
                percent = tk.Label(player_frame)
                player_labels[player.id][ability + "_percent"] = percent

            player_name_label = player_labels[player.id]["player_name_label"]
            total_damage_amount = player_labels[player.id]["total_damage_amount"]
            damage_received_amount = player_labels[player.id]["damage_received_amount"]
            label = player_labels[player.id][ability + "_label"]
            amount = player_labels[player.id][ability + "_amount"]
            percent = player_labels[player.id][ability + "_percent"]

            player_name_label.config(text=player.name + ' ' + game_log.get_percent_total_damage(player))
            total_damage_amount.config(text=str(player.get_total_damage()))
            damage_received_amount.config(text=str(player.get_total_damage_received()))
            label.grid(row=i, column=0, sticky=tk.W)
            amount.grid(row=i, column=1, sticky=tk.E)
            amount.config(text=player.damage_dealt[ability])
            percent.grid(row=i, column=2, sticky=tk.E)
            percent.config(text=player.get_percent_total_damage(ability))

        player_frame.pack()


def parse():
    for line in log_lines:
        handle_line(line, game_log)


if __name__ == '__main__':
    thread = Thread(target=parse).start()
    root.mainloop()
