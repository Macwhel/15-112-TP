import random

# all the functions relation to items

def initItems(difficulty: str, level: int) -> tuple:
    if difficulty == 'Easy':
        d = 1
    elif difficulty == "Medium":
        d = 2
    elif difficulty == "Hard":
        d = 3
    else:
        d = 4

    # calculate overall difficulty
    od = level * d**2

    # increase effects of items based on od

    # init items based on od: every 10 they change (0, 10, 20)
    
    # item: (cost, (effect))

    # Dmg items
    # effectDmg = (playerDmgFlat, playerCritDmg, playerCritRate, playerCurHealth, playerMaxHealth, playerDefense)

    easyOdItemsDmg = {
        'Basic Weapon Upgrade' : (500, (1, 0, 0, 0, 0, 0)),
        'Basic Crit Rate Upgrade' : (2000, (0, 0, 10, 0, 0, 0)),
        'Basic Crit Dmg Upgrade' : (2000, (0, 20, 0, 0, 0, 0))
    }
    medOdItemsDmg = {
        'Adv Weapon Upgrade' : (2000, (5, 0, 0, 0, 0, 0)),
        'Adv Crit Rate Upgrade' : (3500, (0, 0, 20, 0, 0, 0)),
        'Adv Crit Dmg Upgrade' : (3500, (0, 40, 0, 0, 0, 0))
    }
    hardOdItemsDmg = {
        'Risky Weapon Upgrade' : (1000, (5, 0, 0, -20, -20, -20)),
        'Risky Crit Rate Upgrade' : (1250, (0, 0, 20, -20, -20, -20)),
        'Risky Crit Dmg Upgrade' : (1250, (0, 40, 20, -20, -20, -20))
    }

    # Survivability items
    # effectSurv = (playerCurHealth, playerMaxHealth, playerDefense, playerSpeed, playerDmg) 

    easyOdItemsSurv = {
        'Basic Health Potion' : (500, (10, 0, 0, 0, 0)),
        'Basic Armor Increase' : (750, (0, 0, 10, 0, 0)),
        'Basic Health Increase' : (1000, (10, 10, 0, 0, 0))
    }
    medOdItemsSurv = {
        'Adv Health Potion' : (1000, (25, 0, 0, 0, 0)),
        'Adv Armor Increase' : (1500, (0, 0, 25, 0, 0)),
        'Adv Health Increase' : (2000, (25, 25, 0, 0, 0))
    }
    hardOdItemsSurv = {
        'Risky Health Potion' : (1000, (50, 0, -20, 0, 0)),
        'Risky Armor Increase' : (1500, (0, 0, 50, -1, -5)),
        'Risky Health Increase' : (2000, (50, 50, -20, 0, 0))
    }

    # Misc items
    # effectMisc = (playerSpeed, mobMoneyDropMult, itemSpawnChance, maxComboIncrease, numOfMobsIncrease, playerArmorIncrease)
    easyOdItemsMisc = {
        'Basic Speed Increase' : (500, (0.5, 0, 0, 0, 0, 0)),
        'Mobs drop 20% more gold' : (500, (0, 0.2, 0, 0, 0, 0)),
        'Items spawn more\n frequently' : (500, (0, 0, 1.2, 0, 0, 0))
    }
    medOdItemsMisc = {
        'Adv Speed Increase' : (1000, (1.5, 0, 0, 0, 0, 0)),
        'Items spawn much more\n frequently' : (1000, (0, 0, 1.5, 0, 0, 0)),
        'Max Combo Increase' : (1000, (0, 0, 0, 1, 0, 0))
    }
    hardOdItemsMisc = {
        'Risky Speed Increase' : (1000, (2, 0, 0, 0, 0, -20)),
        'More mobs spawn' : (500, (0, 0, 0, 0, 1, 0))
    }

    # easiest difficulty
    if od < 10:
        return (easyOdItemsDmg, easyOdItemsSurv, easyOdItemsMisc)
    elif od < 20:
        return (
            {**easyOdItemsDmg, **medOdItemsDmg}, 
            {**easyOdItemsSurv, **medOdItemsSurv},
            {**easyOdItemsMisc, **medOdItemsMisc}
            )
    else:
        return (
            {**easyOdItemsDmg, **medOdItemsDmg, **hardOdItemsDmg}, 
            {**easyOdItemsSurv, **medOdItemsSurv, **hardOdItemsSurv},
            {**easyOdItemsMisc, **medOdItemsMisc, **hardOdItemsMisc}
        )

def rerollItems(difficulty: str, level: int) -> tuple:

    items = initItems(difficulty, level)

    dmgItem, dmgEffect = random.choice(list(items[0].items()))
    survItems, survEffect = random.choice(list(items[1].items()))
    miscItems, miscEffect = random.choice(list(items[2].items()))

    shopItems = (
        (dmgItem, dmgEffect), 
        (survItems, survEffect), 
        (miscItems, miscEffect)
        )

    return shopItems



