# content of test_sysexit.py
import re


def test_handle_line_Client_unit_state_damaging_unit():
    line = "0T14:32:34 68 I Client unit state damaging unit (EntityHandle:51). Attacker-(EntityHandle:15) : Damage Amount-234 : AbilityAbilityData-Smash_Ability (Smash xaQq5YBR) New hp: 0"

    ### Sample Input
    ### 0T14:32:34 68 I Client unit state damaging unit (EntityHandle:51). Attacker-(EntityHandle:15) : Damage Amount-234 : AbilityAbilityData-Smash_Ability (Smash xaQq5YBR) New hp: 0

    if "Client unit state damaging unit" in line:
        print(line)
        damagedUnit = int(re.search("(EntityHandle:\\d*)", line).group(0).split(":")[1])
        attackingUnit = int(
            re.search("(Attacker-\\(EntityHandle:\\d*)", line).group(0).split(":")[1]
        )
        damageAmount = int(
            re.search("(Damage Amount-\\d*)", line).group(0).split("-")[1]
        )
        abilityData = str(re.search("(AbilityAbilityData-(.*)_)", line).group(2))
        newHP = int(re.search("(New hp: (.*))", line).group(2))

    assert damagedUnit is 51
    assert attackingUnit is 15
    assert damageAmount is 234
    assert abilityData == "Smash"
    assert newHP is 0


def test_damage_type_parser():
    input = "0T17:21:51 48 I [EventSystem] broadcasting EventOnUnitDamaged-WorldStateChangeDamageUnit-TargetUnitHandle:(EntityHandle:549)-SourceEntityHandle:(EntityHandle:7)-TargetUnitTeam:Enemy-IsInActiveCombat:True-DamageAmount:192-IsCriticalHit:False-WasDodged:False-ActionData:ActionData-ConstrictUpgrade_Legendary_Entwine_Damage_Action (89rCWNKl)-AbilityData:AbilityData-ConstrictUpgrade_Legendary_Entwine2_Ability (Entwine cndP79gn)-StatusEffectData:(none)-LootableData:(none)"

    damage_type = re.search("(?<=ActionData:)([a-zA-Z-_]*)", input).group()

    damage_type = (
        damage_type.removeprefix("ActionData-")
        .removesuffix("_Action")
        .removesuffix("_ActionData")
        .removesuffix("Damage")
        .removesuffix("_")
    )

    if "Upgrade_Legendary_" in damage_type:
        damage_type = damage_type.replace("Upgrade_Legendary_", " -> ")

    assert damage_type == "Constrict -> Entwine"
