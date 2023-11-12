import hashlib
import json
import os
import string
import sys
import traceback
import zlib
from collections import OrderedDict
import time
import random
from shutil import copyfile

import GenerateWarpData
import Items
import RandomizeItemsBadgesAssumedFill
import RunCustomRandomizationAssumedFill as RunCustomRandomization

import yaml
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog

import FileOperations
import LoadLocationData
import RandomizeFunctions
import Version




class ItemRandomiser():
    def DisplayMessage(self, message, messageName, type="INFO", GUI=None):
        if GUI is not None:
            if type == "INFO":
                QtWidgets.QMessageBox.about(GUI, messageName, message)
            elif type == "ERROR":
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.showMessage(message)
                error_dialog.exec_()
        else:
            file = sys.stdout
            if type == "ERROR":
                file = sys.stderr

            print(message, file=file)

    def __init__(self, GUI):
        self.GUI = GUI
        self.modeVariables = {}
        self.modList = []
        self.settings = {}

        self.result = None
        self.seed = None

        return

    def ResetPlando(self):
        self.PlandoData = {}
        self.PlandoMode = False

    def makeFileNameSafe(self, mod):
        runningDirectory = os.getcwd().replace("\\", "/") + "/"

        sp = runningDirectory.split("/")
        root = sp[0]
        isAbsolute = False
        if root == "":
            if mod.startswith("/"):
                isAbsolute = True
        elif mod.startswith(root):
            isAbsolute = True

        if runningDirectory in mod:
            safeFile = mod.replace(runningDirectory, "")
            return safeFile
        elif isAbsolute:
            return None

        return mod

    def loadSettings(self, settingsFile):
        _translate = QtCore.QCoreApplication.translate

        self.SettingsFilename = self.makeFileNameSafe(settingsFile)
        if self.SettingsFilename is None:
            raise Exception("Must load correctly.")

        if not os.path.isfile(settingsFile):
            raise Exception("Mode file not found:", settingsFile)

        yamlfile = open(settingsFile, encoding='utf-8')
        yamltext = yamlfile.read()
        settings = yaml.load(yamltext, Loader=yaml.FullLoader)
        self.settings = settings

        # yamlfile = open(settings['BasePatch'],encoding='utf-8')
        # yamltext = yamlfile.read()
        # patches = json.loads(yamltext)

        modFileList = settings['DefaultModifiers']
        self.loadModifiers(modFileList)

        if "ModeVariables" in self.settings:
            for variable in self.settings["ModeVariables"].keys():
                self.modeVariables[variable] = self.settings["ModeVariables"][variable]

        if "Plando" in self.settings:
            newSpoiler = OrderedDict()
            for key in self.settings["Plando"]:
                newSpoiler[key] = self.settings["Plando"][key]
            self.PlandoData = newSpoiler
            del self.settings['Plando']
            self.PlandoMode = True
        else:
            self.ResetPlando()

    def loadModifiers(self, modifiersList, reset=True):
        if reset:
            self.modList = []

        current = [x["fileName"] for x in self.modList]

        for i in modifiersList:
            fileToLoad = i
            if not os.path.isfile(i):
                filepart = i.split("/")[-1]
                fileToLoad = FileOperations.FindModifier(filepart)

            if fileToLoad is not None:
                if fileToLoad in current:
                    continue
                yamlfile = open(fileToLoad)
                yamltext = yamlfile.read()
                self.modList.append(yaml.load(yamltext, Loader=yaml.FullLoader))
                self.modList[-1]['fileName'] = self.makeFileNameSafe(fileToLoad)
            else:
                message = 'Modifier not found:' + "\n" + i
                self.DisplayMessage(message, None, "ERROR", self.GUI)

    def checkForConflictingMods(self):
        conflicts = []
        seenMods = []
        repeatedMods = []
        modNames = [mod['Name'] for mod in self.modList]

        for mod in self.modList:
            if mod in seenMods:
                repeatedMods.append(mod)
            else:
                seenMods.append(mod)

            if 'IncompatibleWith' in mod:
                for item in mod['IncompatibleWith']:
                    if item in modNames:
                        conflicts.append(mod['Name'] + item)

            withoutRequired = False
            potentialConflicts = []
            if 'IncompatibleWithout' in mod:
                for item in mod['IncompatibleWithout']:
                    if item not in modNames:
                        potentialConflicts.append(mod['Name'] + item)
                    else:
                        withoutRequired = True

                if not withoutRequired:
                    conflicts.extend(potentialConflicts)

        if len(conflicts) > 0:
            message = "Mod config error with: " + ','.join(conflicts)
            self.DisplayMessage(message, None, "ERROR", self.GUI)
            return True

        if len(repeatedMods) > 0:
            message = "Mod repeated error with: " + ','.join([x["Name"] for x in repeatedMods])
            self.DisplayMessage(message, None, "ERROR", self.GUI)
            return True

        return False

    def desireKey(self, key):
        if key == "Description":
            return False

        return True

    def AmendHash(self, value, h):
        if type(value) == str:
            h.append(value)
        elif type(value) == int:
            h.append(str(value))
        elif type(value) == list:
            for v in value:
                self.AmendHash(v, h)
        elif value is None:
            h.append("0")
        elif type(value) == bool:
            h.append(str(value))
        elif type(value) == float:
            h.append(str(value))
        elif type(value) == dict:
            for key in value.keys():
                if not self.desireKey(key):
                    continue
                keyvalue = value[key]
                self.AmendHash(key, h)
                self.AmendHash(keyvalue, h)
        else:
            print("Unhandled type:", type(value))

    def GetModeHash(self):
        value_to_hash = []
        self.AmendHash(Version.GetItemRandoVersion(), value_to_hash)
        self.AmendHash(Version.GetSupportedSpeedchoiceVersion(), value_to_hash)
        self.AmendHash(self.settings, value_to_hash)
        self.AmendHash(self.modList, value_to_hash)
        if self.PlandoMode:
            for value in self.PlandoData:
                self.AmendHash(value, value_to_hash)
        new_hash = str.join(";", value_to_hash)

        return hashlib.md5(new_hash.encode()).hexdigest()

    def yamlSortFunction(self, y):
        return y["Name"]

    def GetSettingsMD5(self):
        mods = self.modList.copy()
        mods.sort(key=self.yamlSortFunction)
        full_string = ";"
        for mod in mods:
            full_string += mod["Name"] + ";"

        return hashlib.md5(full_string.encode()).hexdigest()

    def GetActiveModifiers(self, filenames=False):
        mods = self.modList.copy()
        mods.sort(key=self.yamlSortFunction)
        full_string = ";"
        for mod in mods:
            if filenames:
                fName = mod["fileName"]
            else:
                fName = mod["Name"]

            full_string += fName + ";"

        return full_string

    def LoadRaceModeSettings(self, raceString=None):
        inputString = raceString
        hex_bytes = bytes.fromhex(inputString)
        decompressed = zlib.decompress(hex_bytes)
        d_string = decompressed.decode("utf8")

        data = d_string.split("#")
        if len(data) != 4:
            raise Exception("Invalid race mode string")

        mode = data[0]
        mode_hash = data[1]
        # seed = data[2]
        # md5 = data[3]

        # race_string = seed["Mode"] + "#" + seed["ModeHash"] + "#" + seed["Seed"]

        self.loadSettings(mode)
        my_mode_hash = self.GetModeHash()

        if my_mode_hash != mode_hash:
            print("Mode hash does not match!")
            raise Exception("Mode doesn't match: ", mode)

        return data

    def GetRaceModeValue(self, seed):
        # Contains Mode, RNG Seed and ModeHash
        race_string = "#".join([seed["Mode"], seed["ModeHash"], seed["Seed"], seed["RomMD5"]])
        hexstring = zlib.compress(bytes(race_string, "utf8")).hex()
        # print(hexstring)
        return hexstring

    def runRandomizer(self, seed=None, out_dir=None, in_file=None, out_file=None, requiredMD5=None, run_flags=None,
                      attempts=0):

        if 'Name' not in self.settings:
            self.DisplayMessage("No mode has been loaded", "No Mode", type="ERROR", GUI=self.GUI)
            return

        dataHash = LoadLocationData.GetDataHash()

        if run_flags is None:
            run_flags = {}

        if dataHash != Version.GetExpectedDataHash():
            print("dataHash = ", dataHash)
            message = "Map Data invalid. Try reinstalling. Continue at your own risk."
            self.DisplayMessage(message, None, "ERROR", self.GUI)

        conflict = self.checkForConflictingMods()
        if conflict:
            return

        hasWarpsMod = len([mod for mod in self.modList if mod["Name"] == "Warps"])>0
        if not hasWarpsMod:
            # Check a series of warps to see if warp rando seems to be enabled
            is_vanilla = GenerateWarpData.checkForVanilla(in_file)
            if not is_vanilla:
                message = "Warps are not vanilla. Please enable the Warps Pack or check your rom."
                self.DisplayMessage(message, None, "ERROR", self.GUI)
                return

        os.environ['PYTHONHASHSEED'] = '0'  # this needs to be reproducible! so this can't be random!
        if seed is None:
            rngSeed = str(time.time())
            random.seed(rngSeed)
            rngSeed = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        else:
            rngSeed = seed

        if type(rngSeed) is str:
            rngSeedBytes = rngSeed.encode('utf-8')
            rSeed = int(hashlib.md5(rngSeedBytes).hexdigest(), 16)
        else:
            rSeed = rngSeed
            rngSeed = "N"+str(rSeed)

        print('numeric seed is: ' + str(rSeed))
        random.seed(rSeed)
        _translate = QtCore.QCoreApplication.translate
        yamlfile = open(self.settings['BasePatch'])
        yamltext = yamlfile.read()
        patches = json.loads(yamltext)
        modFileList = self.settings['DefaultModifiers']
        try:
            tlv = 0
            wlv = 0
            QtGui.QGuiApplication.processEvents()
            validFileName = False

            if out_file is not None:
                validFileName = True
                file = out_file

            base_dir = out_dir

            if base_dir is None:
                base_dir = ""

            if base_dir == "." or base_dir == "":
                for i in range(0, len(in_file.split("/")) - 1):
                    if base_dir != "":
                        base_dir += "/"
                    base_dir += in_file.split("/")[i]

            exits = 0
            stop_after = 1
            while not validFileName:
                file = QFileDialog.getSaveFileName(directory=base_dir)[0]
                if file != '':
                    validFileName = True
                else:
                    self.DisplayMessage('Please name and save the generated rom...', "File",
                                   "INFO", self.GUI)
                    exits += 1
                    if exits > stop_after:
                        break
            randomizedFileName = file

            if not validFileName:
                self.DisplayMessage('3 Failed filenames, cancelling', "Error",
                               "INFO", self.GUI)
                return

            if not randomizedFileName.endswith(".gbc"):
                randomizedFileName += ".gbc"




            if 'HintLevel' in self.settings:
                HINT_LEVEL = self.settings['HintLevel']
                MAX_HINTS = self.settings['nHints']
            else:
                HINT_LEVEL = 0
                MAX_HINTS = 0
            HintOptions = RandomizeFunctions.ConvertHintLevelToFlags(HINT_LEVEL, MaxHints=MAX_HINTS)

            settings_md5 = self.GetSettingsMD5()
            # print(settings_md5)

            f = open(in_file, 'rb')
            romMD5 = str(hashlib.md5(f.read()).hexdigest())
            f.close()

            # print("reqMD5", requiredMD5)
            if requiredMD5 is not None:
                if romMD5 != requiredMD5:
                    raise Exception("Invalid rom MD5")

            copyfile(in_file, randomizedFileName)
            with open('SAVEDSEEDLOG.log', 'a+') as f:
                f.write(rngSeed + "\n")

            # Fix issue with flags NOT resetting on running a second rom!
            # This will be appended to by modifiers, so ensure a copy is made, not the original!
            flagSettings = self.settings["FlagsSet"].copy()

            if "BannedLocations" in self.settings:
                bannedLocations = self.settings["BannedLocations"]
                if bannedLocations is not None:
                    bannedLocations = bannedLocations.copy()

            if "AllowedLocations" in self.settings:
                allowedLocations = self.settings["AllowedLocations"]
                if allowedLocations is not None:
                    allowedLocations = allowedLocations.copy()

            preventAdd = None
            if "PreventAddItems" in self.settings:
                preventAdd = self.settings["PreventAddItems"]
                if preventAdd is not None:
                    preventAdd = preventAdd.copy()

            progressItems = self.settings["ProgressItems"].copy() if "ProgressItems" in self.settings else None

            coreProgress = self.settings["CoreProgress"].copy() if "CoreProgress" in self.settings else None
            bonusTrash = self.settings["BonusItems"].copy() if "BonusItems" in self.settings else None

            resultDict = RunCustomRandomization. \
                randomizeRom(randomizedFileName, self.settings['Goal'], rSeed, flagSettings, patches,
                             banList=bannedLocations, allowList=allowedLocations,
                             modifiers=self.modList, adjustTrainerLevels=False, adjustRegularWildLevels=False,
                             adjustSpecialWildLevels=False,
                             trainerLVBoost=tlv, wildLVBoost=wlv, requiredItems=progressItems,
                             coreProgress=coreProgress,
                             otherSettings=self.settings, plandoPlacements=self.PlandoData, hintConfig=HintOptions,
                             preventAddingItems=preventAdd, bonusTrash=bonusTrash, modeVariables=self.modeVariables)

            if "AllowedLocations" in self.settings and self.settings["AllowedLocations"] is not None:
                for item in self.settings["AllowedLocations"]:
                    if item not in resultDict["Reachable"]:
                        print("Unreachable allowed:", item)

            if resultDict is None:
                self.DisplayMessage("Incorrect rom version provided!", None, "ERROR", self.GUI)
                raise Exception("Invalid ROM")

            self.result = resultDict
            self.seed = rSeed

            hasWarning = False
            if "Warnings" in resultDict:
                warnings = resultDict["Warnings"]
                if "HasSilverLeaf" in warnings:
                    HasSilverLeaf = warnings["HasSilverLeaf"]
                    if HasSilverLeaf:
                        hasWarning = True

                if "HasGoldLeaf" in warnings:
                    HasGoldLeaf = warnings["HasGoldLeaf"]
                    if HasGoldLeaf:
                        hasWarning = True

                if "HasLeftoverTrash" in warnings:
                    HasLeftoverTrash = warnings["HasLeftoverTrash"]
                    if HasLeftoverTrash:
                        hasWarning = True

                if "CantReachE4" in warnings:
                    CantReachE4 = warnings["CantReachE4"]
                    if CantReachE4:
                        hasWarning = True

                if "NotAllPlaced" in warnings:
                    NotAllPlaced = warnings["NotAllPlaced"]
                    if NotAllPlaced:
                        hasWarning = True

            raceModeString = None

            isRaceMode = run_flags["RaceMode"] if "RaceMode" in run_flags else False
            isSpoilerOutput = run_flags["Spoiler"] if "Spoiler" in run_flags else False

            if isRaceMode or isSpoilerOutput:
                raceMode = {}
                raceMode['Seed'] = rngSeed
                raceMode["Mode"] = self.SettingsFilename
                raceMode["ModeHash"] = self.GetModeHash()
                raceMode["RomMD5"] = romMD5

                raceModeString = self.GetRaceModeValue(raceMode)

                if isRaceMode:
                    self.LoadRaceModeSettings(raceString=raceModeString)

                    # cb = QApplication.clipboard()
                    # cb.setText(raceModeString, mode=cb.Clipboard)

                    # DisplayMessage('Copied race output to clipboard', "Race Output",
                    #			   "INFO", self.GUI)

                    with open(randomizedFileName + '_SPOILER.txt', 'w') as f:
                        f.write(raceModeString)

            if isSpoilerOutput:
                outputSpoiler = {}
                outputSpoiler['RNG Seed'] = rngSeed
                outputSpoiler['Solution'] = resultDict["Spoiler"]
                outputSpoiler['Useless Stuff'] = resultDict["Trash"]
                if "RandomizedExtra" in resultDict:
                    outputSpoiler["Xtra Stuff"] = resultDict["RandomizedExtra"]

                if "UpgradedItems" in resultDict:
                    outputSpoiler["Xtra Upgrades"] = resultDict["UpgradedItems"]

                outputSpoiler["CIR Version"] = Version.GetItemRandoVersion()
                outputSpoiler["Mode"] = self.settings['Name']
                outputSpoiler["ModifierHash"] = self.GetSettingsMD5()
                outputSpoiler["Modifiers"] = self.GetActiveModifiers()
                if hasWarning:
                    outputSpoiler["Warnings"] = resultDict["Warnings"]

                if raceModeString is not None:
                    outputSpoiler["Race"] = raceModeString

                with open(randomizedFileName + '_SPOILER.txt', 'w') as f:
                    yaml.dump(outputSpoiler, f, default_flow_style=False)

            successMessage = "Successfully randomized rom"
            successBoxName = "Success"

            # TODO
            # Change warning handling and result to dictionary for easier readability and extension
            # Handle E4 not possible in the same way

            if hasWarning:
                successMessage = "Sucessfully generated rom with warnings"
                successBoxName = "Success..."

            self.DisplayMessage(successMessage, successBoxName,
                           "INFO", self.GUI)

            _translate = QtCore.QCoreApplication.translate
        except:
            message = ''.join(traceback.format_exc())
            #DisplayMessage(message, messageName, type="INFO", GUI=None):
            self.DisplayMessage(message, None, "ERROR", self.GUI)


    def GetAllAccessible(self):
        if self.result is None:
            return None

        spoiler = self.result["Spoiler"]
        fullTree = self.result["FullTree"]
        inputFlags = self.result["InputFlags"]
        goal = self.result["Goal"]
        locations = self.result["Locations"]
        badgeDict = self.result["BadgeDict"]

        beatability = RandomizeItemsBadgesAssumedFill.checkBeatability(spoiler, fullTree, inputFlags,
                                                         None, None, None, locations,
                                                         badgeDict, None, assign_trash=False,
                                                         forbidden=[], recommended=False)

        return beatability


    def performChecks(self, checksList):

        if self.result is None:
            return None

        spoiler = self.result["Spoiler"]
        fullTree = self.result["FullTree"]
        inputFlags = self.result["InputFlags"]
        goal = self.result["Goal"]
        locations = self.result["Locations"]
        badgeDict = self.result["BadgeDict"]

        sanityCheckFailure = \
            RandomizeFunctions.IsVariableRequired(None, spoiler, locations, inputFlags, fullTree, badgeDict, goal)

        if sanityCheckFailure:
            raise Exception("Invalid created base conditions")

        KIMap = Items.GetKeyItemMap()
        InverseKIMap = Items.GetKeyItemMap()

        variable_checks = {}

        for check in checksList:
            isItem = False
            isFlag = False
            if check in KIMap.keys():
                v = KIMap[check]
                if v.startswith("ENGINE"):
                    isFlag = True
                else:
                    isItem = True

            checkBase = check
            input_vars = []
            if "/" in check:
                checkList = check.split("/")
                checkUse = None
                input_vars = checkList
            else:
                checkUse = checkBase

            required = RandomizeFunctions.IsVariableRequired(checkUse, spoiler, locations, inputFlags,
                                                             fullTree, badgeDict, goal, input_variables=input_vars)

            variable_checks[checkBase] = required

        return variable_checks

