import copy
import sys
import time
from collections import defaultdict

import yaml

import LoadLocationData
import RunCLI
from ItemRandomiser import ItemRandomiser
from RandomizeItemsBadgesAssumedFill import GetDefinitiveRequirements, UpdateCacheOfSpoilerLocations, \
    CheckSpecialValidity
from RunCustomRandomizationAssumedFill import ProcessModifiers


def GetBadges(requiredItems):
    return [ item for item in requiredItems if "Badge" in item and "Badges" not in item ]

def testDefinitiveRequirements():
    d = {
        'Surf': 'Route 2 Carbos',
 #'S S Ticket': 'Ecruteak City Hidden Hyper Potion',
 'Squirtbottle': 'Route 2 Hidden Full Heal',
 'Pass': 'Victory Road Max Revive'
         }

    assignList = \
        [
            #("Mr. Pokemon's Egg", "Surf"),
            # ("Pewter City Gym Badge", "Cut"),
             #("Silver Wing Old Man", "Cascade Badge"),

            # ("Violet City Gym Badge", "Cascade Badge"),
            # ("Falkner TM", "Boulder Badge"),
            # ("Underground Path Hidden X Special", "S S Ticket"),
            # ("Mahogany Town Gym Badge", "Waterfall"),
            # ("Mt Mortar Elixer", "Lost Item"),
            # ("Route 46 PRZcureBerry", "Mystery Egg")
        ]

    for xd in d.keys():
        assignList.append((d[xd], xd))


    changeListDict = defaultdict(lambda: [])

    modList = []

    settingsFile = "Modes/Custom/CrazyA.yml"

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

    # useCache = cacher

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

        useCache = copy.copy(cacher)

        reqs = GetDefinitiveRequirements(locList, litem, cache=useCache, spoiler=spoiler,
                                         items=requiredItems)
        #, banItem=giveItem)

        cacher[litem] = reqs
        UpdateCacheOfSpoilerLocations(spoiler, cacher, locList, requiredItems)

        # keysToRemove = []
        # for optionItem in cacher.items():
        #     optionKey = optionItem[0]
        #     if not optionItem[1].permanent:
        #         keysToRemove.append(optionKey)

        # for key in keysToRemove:
        #     print("Not perm:", key.Name, cacher[key].alwaysRequired, cacher[key].options)
        #     reqs = GetDefinitiveRequirements(locList, key, cache=cacher,
        #                                      spoiler=spoiler, items=requiredItems)
        #
        #     reqs.permanent = True
        #
        #     cacher[key] = reqs


        print("reqs=", a[0], reqs.alwaysRequired, reqs.options)

        # keysToRemove = []
        # for optionItem in fullCache.items():
        #     optionKey = optionItem[0]
        #     if not optionItem[1].permanent:
        #         keysToRemove.append(optionKey)
        #
        # for key in keysToRemove:
        #     del fullCache[key]

        # print([ (f[0].Name, f[1].options) for f in fullCache.items()])

        if giveItem is not None:

            if giveItem in reqs.alwaysRequired:
                print("Invalid option")
                raise Exception()

            elif "Banned" in reqs.alwaysRequired:
                print("Banned option:", a)
                raise Exception()

            elif not CheckSpecialValidity(reqs, GetBadges(requiredItems), [], spoiler, giveItem):
                print("Special Prevented option:", a)
                raise Exception()
            else:
                spoiler[giveItem] = reqs
                #time.sleep(5)

    #print("spoiler=", spoiler)
    sys.exit(0)
    print("hello")
    #final = "Board SS Aqua"
    #final = "Vermilion City Fan Club President"
    #banItem = "Radio Card"
    #final = "Route 2 Nugget House"
    location = [l for l in locList if l.Name == final][0]

    useCache = copy.copy(cacher)

    reqs = GetDefinitiveRequirements(locList, location, cache=useCache, spoiler=spoiler,
                                     items=requiredItems, banItem=None)

    print("Always=", reqs.alwaysRequired)
    print(reqs.options)







testDefinitiveRequirements()