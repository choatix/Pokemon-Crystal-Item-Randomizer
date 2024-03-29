from collections import defaultdict

import yaml

import LoadLocationData
import RunCLI
from ItemRandomiser import ItemRandomiser
from RandomizeItemsBadgesAssumedFill import GetDefinitiveRequirements
from RunCustomRandomizationAssumedFill import ProcessModifiers


def testDefinitiveRequirements():
    d = {
        'Surf': 'Lake of Rage Hidden Power TM', 'S S Ticket': 'Goldenrod Tunnel Ultra Ball', 'Squirtbottle': 'Dark Cave Violet Potion', 'Mystery Egg': 'Ruins of Alph Rope Chamber 2', 'Pass': 'Victory Road Full Heal', 'Fog Badge': 'Tin Tower Max Revive', 'Flash': 'Flower Shop', 'Escape Rope': 'Celadon Dept Store 2F2 Great Ball', 'Bicycle': 'Mt Mortar Hidden Max Repel', 'Zephyr Badge': 'Bugsy TM', 'X Accuracy': 'Ecruteak Mart Burn Heal', 'Glacier Badge': 'Route 46 X Speed', 'Blue Card': 'Route 27 Rare Candy', 'Machine Part': 'Tin Tower Full Restore', 'Thunder Badge': 'Bug Catching Contest Third Place', 'Pokedex': 'Route 32 Roar Dude', 'Earth Badge': 'Vermilion City Gym Badge', 'X Special': 'Blackthorn Mart Max Potion', 'Volcano Badge': 'Celadon Game Corner Psychic TM', 'Cut': 'Charcoal Kiln', 'Red Scale': 'Mystic Water Man', 'X Speed': 'Goldenrod Department Store 2F2 Escape Rope', 'Storm Badge': 'Union Cave Floor 1 X Attack', 'Whirlpool': 'Mt. Silver Max Revive', 'Rock Smash': 'Cerulean Mart X Defend', 'Itemfinder': 'Route 42 Fisherman Tully', 'Coin Case': 'Rock Smash Guy', 'Cascade Badge': 'Route 37 Red Apricorn', 'X Defend': 'Violet Mart X Defend', 'Basement Key': 'Route 42 Ylw Apricorn', 'Soul Badge': 'Slowpoke Well Floor 1 Super Potion', 'Waterfall': 'Ice Path Rest TM', 'Sweet Scent': 'Lavender Mart Parlyz Heal', 'Fly': 'Sweet Scent Girl', 'Hive Badge': 'Ice Path PP Up', 'Card Key': 'Route 30 Berry Man', 'Rainbow Wing': 'Lake of Rage Hidden Full Restore', 'Radio Card': 'Bills Grandpa Wants Staryu', 'Rising Badge': "Diglett's Cave Hidden Max Revive", 'Dire Hit': 'Violet Mart Repel', 'Water Stone': 'Viridian Mart Full Heal', 'Pokegear': 'Radio Tower Sunny Day TM', 'X Attack': 'Underground Herb Shop Energy Powder', 'Mineral Badge': 'National Park Hidden Full Heal', 'Expansion Card': 'Vermilion Mart Parlyz Heal', 'Marsh Badge': 'Falkner TM', 'Rainbow Badge': 'Violet City Rare Candy', 'Lost Item': 'Lighthouse Ether', 'Boulder Badge': 'Celadon City Gym Badge', 'Strength': 'Ice Path Max Potion', 'Clear Bell': 'Elm Aide Potion', 'Secret Potion': 'Route 2 Psn Cure Berry', 'Guard Spec': 'Goldenrod Department Store 5F Thunder Punch TM', 'Plain Badge': 'Route 29 Tuscany'
    }

    assignList = \
        [
             ("Red Scale Dropped", "Squirtbottle"),
             ("Route 46 Picknicker Erin Calcium", "Pass"),
            # ("National Park Parlyz Heal", "Pass"),
            # ("Lighthouse Ether", "Rainbow Badge"),
            # ("Underground Path Hidden X Special", "S S Ticket"),
            # ("Mahogany Town Gym Badge", "Waterfall"),
            # ("Mt Mortar Elixer", "Lost Item"),
            # ("Route 46 PRZcureBerry", "Mystery Egg")
        ]

    #for xd in d.keys():
    #    assignList.append((d[xd], xd))


    changeListDict = defaultdict(lambda: [])

    modList = []

    settingsFile = "Modes/Custom/AwulAW.yml"

    yamlfile = open(settingsFile, encoding='utf-8')
    yamltext = yamlfile.read()
    settings = yaml.load(yamltext, Loader=yaml.FullLoader)

    # yamlfile = open(settings['BasePatch'],encoding='utf-8')
    # yamltext = yamlfile.read()
    # patches = json.loads(yamltext)

    modFileList = settings['DefaultModifiers']

    #filesToLoad = ["More Checks/OpenMtSilver", "More Checks/CardRandomization", "More Checks/HiddenItems",
    #               "Convenience/Fly/ForceEarlyFlyTournament2023", "More Checks/EnableTinTower",
    #               "More Checks/TimeEvents"]

    for file in modFileList:
        fileToLoad = "{}".format(file)
        yamlfile = open(fileToLoad)
        yamltext = yamlfile.read()
        modList.append(yaml.load(yamltext, Loader=yaml.FullLoader))

    requiredItems = [
        'Surf', 'Squirtbottle', 'Flash', 'Mystery Egg', 'Cut', 'Strength', 'Secret Potion', 'Red Scale',
                     'Whirlpool',
                     'Card Key', 'Basement Key', 'Waterfall', 'S S Ticket', 'Machine Part', 'Lost Item',
                     'Pass', 'Fly', "Zephyr Badge", "Hive Badge", "Plain Badge", "Fog Badge", "Storm Badge",
                     "Mineral Badge", "Glacier Badge", "Rising Badge", "Boulder Badge", "Cascade Badge",
                     "Thunder Badge", "Rainbow Badge", "Soul Badge", "Volcano Badge", "Marsh Badge", "Earth Badge"
                     ]

    progressItems = []

    ProcessModifiers(modList, [], {}, changeListDict, requiredItems, progressItems, [],
                     [],
                     [], [], [], [], [])

    fullLocationData = LoadLocationData.LoadDataFromFolder(".", None, None, changeListDict, [])
    locList = LoadLocationData.FlattenLocationTree(fullLocationData[0])

    locList = sorted(LoadLocationData.FlattenLocationTree(fullLocationData[0]), key= lambda i: ''.join(i.Name).join(i.requirementsNeeded(defaultdict(lambda: False))))


    spoiler = {}
    cacher = {}



    #assignList = []

    fullCache = {}

    for a in assignList:
        print("Lookup:", a)
        giveItem = a[1]
        litems = [ l for l in locList if l.Name == a[0]]
        if len(litems) > 1:
            raise Exception()
        litem = litems[0]

        # Need to change to store cache when not storing unsolved options
        # Or mark with detail to add the detail at the end
        # e.g. Route 2 Nugget House / Silver Wing Old Man example
        # With Route 2 North

        reqs = GetDefinitiveRequirements(locList, litem, cache={}, spoiler=spoiler,
                                         items=requiredItems, banItem=giveItem)
        print("reqs=", a[0], reqs.alwaysRequired)

        if giveItem is not None:

            if giveItem in reqs.alwaysRequired:
                print("Invalid option")
                raise Exception()

            elif "Banned" in reqs.alwaysRequired:
                print("Banned option:", a)
                raise Exception()

            else:
                spoiler[giveItem] = reqs

    #print("spoiler=", spoiler)
    final = "Radio Tower Rockets Part 1"
    #banItem = "Radio Card"
    #final = "Route 2 Nugget House"
    location = [l for l in locList if l.Name == final][0]
    reqs = GetDefinitiveRequirements(locList, location, cache={}, spoiler=spoiler,
                                     items=requiredItems, banItem=None)

    print("Always=", reqs.alwaysRequired)
    #print(reqs.options)







testDefinitiveRequirements()