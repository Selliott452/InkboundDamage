import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Inkbound Damage")
root.attributes("-topmost", True)
canvas = tk.Canvas(root)
# root.attributes('-alpha', 0.8)
canvas.pack()
player_frames = {}
player_labels: dict[int, dict[str, any]] = {}


DIVE_TABS = {}


def reset():
    global player_labels
    player_labels = {}
    global player_frames
    player_frames = {}
    for child in canvas.winfo_children():
        child.destroy()


def render(dive_logs):
    global DIVE_TABS

    if len(dive_logs) != 0:
        for dive_log in dive_logs:
            # if DIVE_TABS is empty like at the start of the program
            if len(DIVE_TABS) == 0:
                # create tab controller
                tabControl = ttk.Notebook(canvas)
                # create a frame for current dive
                dive_tab = ttk.Frame(tabControl, width=600, height=200)
                dive_tab.pack(fill="both", expand=True)

                # add tab to all tabs
                DIVE_TABS[dive_log.dive_number] = dive_tab
                # print("adding dive_tab #" + str(dive_log.dive_number))

                tabControl.add(dive_tab, text="Dive #" + str(dive_log.dive_number))
                tabControl.pack(expand=1, fill="both")
            else:
                # get dive dab for current dive_number
                if dive_log.dive_number in DIVE_TABS:
                    dive_tab = DIVE_TABS[dive_log.dive_number]
                    # print("getting dive_tab #" + str(dive_log.dive_number))
                else:
                    # if it doesnt exist then create a new dive tab
                    # create a frame for current dive
                    dive_tab = ttk.Frame(tabControl, width=600, height=200)
                    dive_tab.pack(fill="both", expand=True)

                    # add tab to all tabs
                    DIVE_TABS[dive_log.dive_number] = dive_tab

                    # add to tabController
                    tabControl.add(dive_tab, text="Dive #" + str(dive_log.dive_number))
                    tabControl.pack(expand=1, fill="both")

            players = dive_log.get_players()

            for player in players.values():
                player_class_id = "Unknown"
                if player.class_id:
                    player_class_id = player.class_id
                elif player.id in dive_log.entity_to_class_id.keys():
                    player_class_id = dive_log.entity_to_class_id[player.id]

                if player.id not in player_frames.keys():
                    player_frames[player.id] = tk.Frame(dive_tab, border=10)

                player_frame = player_frames[player.id]

                if player.id not in player_labels.keys():
                    player_labels[player.id] = {}

                if "player_name_label" not in player_labels[player.id].keys():
                    player_name_label = tk.Label(
                        player_frame,
                        font=("Helvetica", 10, "bold"),
                        foreground="white",
                        background=get_class_color(player_class_id),
                        width=50,
                    )
                    player_name_label.grid(row=0, columnspan=3)
                    player_labels[player.id]["player_name_label"] = player_name_label

                if "total_damage_label" not in player_labels[player.id].keys():
                    player_labels[player.id]["total_damage_label"] = label_and_grid(
                        player_frame, "Total Damage Dealt", 1, 0, tk.W
                    )

                if "total_damage_amount" not in player_labels[player.id].keys():
                    player_labels[player.id]["total_damage_amount"] = label_and_grid(
                        player_frame, None, 1, 1, tk.E
                    )

                if "damage_received_label" not in player_labels[player.id].keys():
                    player_labels[player.id]["damage_received_label"] = label_and_grid(
                        player_frame,
                        "Total Damage Received (Including blocked)",
                        2,
                        0,
                        tk.W,
                    )

                if "damage_received_amount" not in player_labels[player.id].keys():
                    player_labels[player.id]["damage_received_amount"] = label_and_grid(
                        player_frame, None, 2, 1, tk.E
                    )

                abilities = sorted(
                    player.damage_dealt.keys(),
                    reverse=True,
                    key=lambda x: player.damage_dealt[x],
                )
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
                    total_damage_amount = player_labels[player.id][
                        "total_damage_amount"
                    ]
                    damage_received_amount = player_labels[player.id][
                        "damage_received_amount"
                    ]
                    label = player_labels[player.id][ability + "_label"]
                    amount = player_labels[player.id][ability + "_amount"]
                    percent = player_labels[player.id][ability + "_percent"]

                    player_name_label.config(
                        text=player.name
                        + " - "
                        + get_class_name(player_class_id)
                        + " "
                        + dive_log.get_percent_total_damage(player)
                    )
                    total_damage_amount.config(text=str(player.get_total_damage()))
                    damage_received_amount.config(
                        text=str(player.get_total_damage_received())
                    )
                    label.grid(row=i, column=0, sticky=tk.W)
                    amount.grid(row=i, column=1, sticky=tk.E)
                    amount.config(text=player.damage_dealt[ability])
                    percent.grid(row=i, column=2, sticky=tk.E)
                    percent.config(text=player.get_percent_total_damage(ability))

                player_frame.pack()


def label_and_grid(player_frame, label_text, row, column, sticky) -> tk.Label:
    label = tk.Label(player_frame, text=label_text)
    label.grid(row=row, column=column, sticky=sticky)

    return label


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
    else:
        return class_id


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
        return "#F4C430"
    else:
        return "grey"
