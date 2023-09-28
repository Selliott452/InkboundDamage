import tkinter as tk

root = tk.Tk()
root.title("Inkbound Damage")
root.attributes('-topmost', True)
canvas = tk.Canvas(root)
canvas.pack()

player_frames = {}
player_labels: dict[int, dict[str, any]] = {}


def reset():
    global player_labels
    player_labels = {}
    global player_frames
    player_frames = {}
    for child in canvas.winfo_children():
        child.destroy()


def render(game_log):
    for player in game_log.players.values():

        if player.id not in player_frames.keys():
            player_frames[player.id] = tk.Frame(canvas, border=10)

        player_frame = player_frames[player.id]

        if player.id not in player_labels.keys():
            player_labels[player.id] = {}

        if "player_name_label" not in player_labels[player.id].keys():
            player_name_label = tk.Label(player_frame,
                                         font=('Helvetica', 10, 'bold'),
                                         foreground="white",
                                         background=get_class_color(game_log.entity_to_class_id[player.id]),
                                         width=50)
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

            player_name_label.config(
                text=player.name + ' - ' + get_class_name(
                    game_log.entity_to_class_id[player.id]) + ' ' + game_log.get_percent_total_damage(
                    player))
            total_damage_amount.config(text=str(player.get_total_damage()))
            damage_received_amount.config(text=str(player.get_total_damage_received()))
            label.grid(row=i, column=0, sticky=tk.W)
            amount.grid(row=i, column=1, sticky=tk.E)
            amount.config(text=player.damage_dealt[ability])
            percent.grid(row=i, column=2, sticky=tk.E)
            percent.config(text=player.get_percent_total_damage(ability))

        player_frame.pack()


def get_class_name(class_id):
    if class_id == "C01":
        return "Magma Miner"
    elif class_id == "C02":
        return "Mosscloak"
    elif class_id == "C03":
        return "Clairvoyant"
    elif class_id == "C04":
        return "Weaver"
    elif class_id == "C05":
        return "Obelisk"
    elif class_id == "C06":
        return "Unknown"
    elif class_id == "C07":
        return "Star Captain"


def get_class_color(class_id):
    if class_id == "C01":
        return "#d91e18"
    elif class_id == "C02":
        return "#26c281"
    elif class_id == "C03":
        return "#01017a"
    elif class_id == "C04":
        return "#963694"
    elif class_id == "C05":
        return "#67809f"
    elif class_id == "C06":
        return "grey"
    elif class_id == "C07":
        return "#fef160"
