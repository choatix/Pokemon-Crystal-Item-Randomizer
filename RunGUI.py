import shutil
import sys

import FileOperations
import RandomizerGUI
import yaml
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QInputDialog

import RunCLI
from collections import OrderedDict
import csv
import os
import Version
from ItemRandomiser import ItemRandomiser


class RunWindow(QtWidgets.QMainWindow, RandomizerGUI.Ui_MainWindow):

	def updateGUIFromSettings(self, settings):
		_translate = QtCore.QCoreApplication.translate

		self.updateModListView()

		if 'Name' in settings:
			self.CurentSettings.setText(_translate("MainWindow", settings['Name']))

		if 'Description' in settings:
			self.SettingsDescription.setText(_translate("MainWindow", settings['Description']))

		if 'Goal' not in settings:
			settings["Goal"] = "Red"

		self.CurrentGoal.setText(_translate("MainWindow", settings['Goal']))


		if "SilverBadgeUnlockCount" in self.item_rando.settings:
			_translate = QtCore.QCoreApplication.translate
			self.BadgesNeeded.setText(_translate("MainWindow",
												 "Change # of badges\n to unlock Mt. Silver? \n(Currently " + str(
													 self.item_rando.settings["SilverBadgeUnlockCount"]) + ")"))
			QtGui.QGuiApplication.processEvents()
		else:
			self.BadgesNeeded.setText(_translate("MainWindow",
												 "Change # of badges\n to unlock Mt. Silver? \n(Currently " + str(
													 16) + ")"))

		if 'HintLevel' in self.item_rando.settings:
			self.HintButton.setText(_translate("MainWindow",
											   "Set Hints (LV: " + str(self.item_rando.settings['HintLevel']) + " N" + str(
												   self.item_rando.settings['nHints']) + ")"))
			QtGui.QGuiApplication.processEvents()
		else:
			self.HintButton.setText(_translate("MainWindow", "Set Hints (off)"))
			QtGui.QGuiApplication.processEvents()

		if "Plando" in self.item_rando.settings:
			self.TurnOffPlando.setEnabled(True)
		else:
			self.DeactivatePlando()

	def __init__(self, parent=None):
		super(RunWindow, self).__init__(parent)
		self.setupUi(self)
		self.item_rando = ItemRandomiser(GUI=self)

		_translate = QtCore.QCoreApplication.translate
		yamlfile = open('RandomizerConfig.yml',encoding='utf-8')
		yamltext = yaml.load(yamlfile,Loader=yaml.FullLoader)

		try:
			self.item_rando.loadSettings(yamltext['DefaultSettings'])
		except Exception as e:
			pass

		self.updateGUIFromSettings(self.item_rando.settings)

		self.modifierList.itemSelectionChanged.connect(self.updateModifierDescription)
		self.ChooseSettings.clicked.connect(self.selectLogicSettings)
		self.LoadModifier.clicked.connect(self.loadModifier)
		self.LoadPack.clicked.connect(self.loadPack)
		self.DeleteModifier.clicked.connect(self.deleteModifier)
		self.romPath = ''
		self.defaultRomDirectory = "."
		if 'BaseRomInputDirectory' in yamltext:
			self.defaultRomDirectory = yamltext['BaseRomInputDirectory']
		self.defaultRomOutDirectory = "."
		self.defaultRom = None
		if 'BaseRomOutputDirectory' in yamltext:
			self.defaultRomOutDirectory = yamltext['BaseRomOutputDirectory']
		if 'BaseRom' in yamltext:
			self.defaultRom = yamltext['BaseRom']
		self.SelectRomFile.clicked.connect(self.selectRom)
		self.Randomize.setEnabled(False)
		self.Randomize.setText(_translate("MainWindow", "No Rom Loaded!"))
		self.Randomize.clicked.connect(self.pressRunRandomiser)
		self.SaveSettings.clicked.connect(self.saveSettings)

		#self.PlandoMode = False
		#self.PlandoData = {}

		self.LoadPlandoFile.clicked.connect(self.SetUpPlando)
		self.TurnOffPlando.clicked.connect(self.DeactivatePlando)
		self.DefaultSettings.clicked.connect(self.SelectDefaultSettings)
		self.LoadRaceMode.clicked.connect(self.LoadRaceModeSettingsUI)
		self.AddItem.clicked.connect(self.AddBonusItem)
		self.View_Items.clicked.connect(self.RemoveBonusItem)
		self.BadgesNeeded.clicked.connect(self.SetBadgeForSilver)
		self.HintButton.clicked.connect(self.ProcessHintSettings)
		self.modeVariables = {}
		self.setCurrentVariables.clicked.connect(self.SetCurrentVariables)
		self.version.setText(_translate("MainWindow", "Version "+Version.GetItemRandoVersion()))

		self.itemsList = []
		with open('AddItemValues.csv', newline='',encoding='utf-8-sig') as csvfile:
			reader = csv.reader(csvfile)
			for i in reader:
				if(len(i)>0):
					self.itemsList.append(i[0])
					#self.ItemList.addItem(i[0])

		if 'FirstRun' in yamltext:
			firstRunCheck = yamltext['FirstRun']
			if firstRunCheck:
				ItemRandomiser.DisplayMessage(None,'Please select previous install directory to import custom settings', "First Run", "INFO", self)
				previous_dir = QFileDialog.getExistingDirectory()
				if previous_dir != "":
					self.importSettings(previous_dir)


				self.WriteRandomizerConfig(firstRun=False)

		if self.defaultRom is not None:
			isFullPath = os.path.isfile(self.defaultRom)
			if isFullPath:
				self.romPath = self.defaultRom
				self.Randomize.setEnabled(True)
				self.Randomize.setText(_translate("MainWindow", "Randomize Rom"))
			elif self.defaultRomDirectory is not None:
				romPath = self.defaultRomDirectory + "/" +self.defaultRom
				isEndPath = self.defaultRomDirectory is not None and \
							os.path.isfile(romPath)
				if isEndPath:
					self.romPath = romPath
					self.Randomize.setEnabled(True)
					self.Randomize.setText(_translate("MainWindow", "Randomize Rom"))

	def importSettings(self, oldDirectory):
		oldSettings = oldDirectory + "/RandomizerConfig.yml"
		config_exists = os.path.isfile(oldSettings)
		if config_exists:
			yamlfile = open(oldSettings, encoding='utf-8')
			yamltext = yaml.load(yamlfile, Loader=yaml.FullLoader)

			if "DefaultSettings" in yamltext["DefaultSettings"]:
				self.WriteRandomizerConfig(defaultFile=yamltext["DefaultSettings"])

		modeDirectory = oldDirectory + "/" + "Modes"
		if os.path.isdir(modeDirectory):
			oldModes = []
			newModes = []
			files = os.listdir(modeDirectory)
			for mode in files:
				if os.path.isfile(modeDirectory + "/" + mode):
					oldModes.append(mode)

			if os.path.isdir(modeDirectory + "/" + "Custom"):
				files = os.listdir(modeDirectory + "/Custom" )
				for mode in files:
					if os.path.isfile(modeDirectory + "/Custom/" + mode):
						oldModes.append("Custom/"+mode)

			release_modes = os.listdir("Modes")
			for mode in release_modes:
				if os.path.isfile("Modes" + "/" + mode):
					newModes.append(mode)

			if os.path.isdir("Modes" + "/" + "Custom"):
				files = os.listdir("Modes" + "/" + "Custom")
				for mode in files:
					if os.path.isfile("Modes" + "/Custom/" + mode):
						newModes.append("Custom/"+mode)

			additionalModes = [ mode for mode in
								[ old.replace("Custom/", "") for old in oldModes ]
								if mode not in
								[ new.replace("Custom/", "") for new in newModes ]]
			custom_modes = os.path.isdir("Modes/Custom")
			if not custom_modes:
				os.mkdir("Modes/Custom")

			for additionalMode in additionalModes:
				isCustom = os.path.isfile(modeDirectory + "/Custom/" + additionalMode)
				if isCustom:
					shutil.copy(modeDirectory + "/Custom/" + additionalMode, "Modes/Custom")
				else:
					shutil.copy(modeDirectory + "/" + additionalMode, "Modes/Custom")


	def runGUIRandomiser(self, requiredMD5=None):
		_translate = QtCore.QCoreApplication.translate

		self.Randomize.setEnabled(False)
		self.Randomize.setText(_translate("MainWindow", "Randomizing"))

		gui_flags = {
			"RaceMode":self.RaceModeRadioButton.isChecked(),
			"Spoiler":self.SpoilerOutputRadioButton.isChecked()
					 }

		gui_seed = self.SeedInput.text()
		if gui_seed == "":
			gui_seed = None

		result = self.item_rando.runRandomizer(seed=gui_seed, in_file=self.romPath, run_flags=gui_flags, requiredMD5=None)

		self.Randomize.setEnabled(True)
		self.Randomize.setText(_translate("MainWindow", "Randomize Rom"))

	def pressRunRandomiser(self):
		self.runGUIRandomiser()

	def SetBadgeForSilver(self):
		(nBadge, ok2) = QInputDialog.getInt(self,"How many badges will Mt. Silver unlock with?","How many badges will Mt. Silver unlock with?")
		if nBadge <= 16 and ok2:
			if nBadge <= 0:
				message = "You must choose a number of badges greater than 1! Setting badge requirement to 1."
				ItemRandomiser.DisplayMessage(None,message, None, "ERROR", self)
			self.item_rando.settings["SilverBadgeUnlockCount"] = nBadge
			_translate = QtCore.QCoreApplication.translate
			self.BadgesNeeded.setText(_translate("MainWindow", "Change # of badges\n to unlock Mt. Silver? \n(Currently "+str(nBadge)+")"))
			QtGui.QGuiApplication.processEvents()
		elif ok2:
			message = "There are only 16 badges in Pokemon Crystal! You can't require more, or your game will not be completable!"
			ItemRandomiser.DisplayMessage(None,message, None, "ERROR", self)

	def AddBonusItem(self):
		(addedItem, ok1) = QInputDialog.getItem(self, "Select item you wish to add to the pool", "Select item you wish to add to the pool", self.itemsList, 0, False)
		if ok1:
			(nAdded, ok2) = QInputDialog.getInt(self,"Add how many?","Add how many?")
		if not ('BonusItems' in self.item_rando.settings):
			self.item_rando.settings['BonusItems'] = []
		if ok1 and ok2:
			for i in range(0,nAdded):
				self.item_rando.settings['BonusItems'].append(addedItem)

	def RemoveBonusItem(self):
		if 'BonusItems' in self.item_rando.settings and len(self.item_rando.settings['BonusItems']) > 0:
			self.item_rando.settings['BonusItems'] = []
			if ('BonusItems' in self.item_rando.settings):
				(addedItem, ok1) = QInputDialog.getItem(self, r"View/Remove Items in pool", "Select any item you wish to remove, or cancel to remove nothing",
														self.item_rando.settings['BonusItems'], 0, False)
			if ok1:
				(nAdded, ok2) = QInputDialog.getInt(self,"Remove how many?","Remove how many?")
			if not ('BonusItems' in self.item_rando.settings):
				self.item_rando.settings['BonusItems'] = []
			if ok1 and ok2:
				for i in range(0,nAdded):
					if addedItem in self.item_rando.settings['BonusItems']:
						self.item_rando.settings['BonusItems'].remove(addedItem)

	def selectRom(self):
		_translate = QtCore.QCoreApplication.translate
		romDirectory = self.defaultRomDirectory
		file = QFileDialog.getOpenFileName(directory = romDirectory)[0]
		self.romPath = file
		if file != '':
			self.Randomize.setEnabled(True)
			self.Randomize.setText(_translate("MainWindow", "Randomize Rom"))
		else:
			self.Randomize.setEnabled(False)
			self.Randomize.setText(_translate("MainWindow", "No Rom Loaded!"))


	def selectLogicSettings(self):
		file = QFileDialog.getOpenFileName(directory = 'Modes')[0]
		if file != '':
			self.item_rando.loadSettings(file)
			self.updateGUIFromSettings(self.item_rando.settings)

	def loadPack(self):
		packfiles = QFileDialog.getOpenFileNames(directory = 'Packs')[0]
		if len(packfiles) > 0:
			currentModifierFiles = [obj["fileName"] for obj in self.item_rando.modList]
			modifiersToLoad = []
			for packfile in packfiles:
				yamlfile = open(packfile)
				yamltext = yamlfile.read()

				loadedYaml = yaml.load(yamltext, Loader=yaml.FullLoader)

				if 'Modifiers' in loadedYaml:
					self.item_rando.loadModifiers(loadedYaml['Modifiers'], reset=False)

			for mod in modifiersToLoad:
				if os.path.isfile(mod):
					yamlfile = open(mod)
					yamltext = yamlfile.read()
					loadedYaml = yaml.load(yamltext, Loader=yaml.FullLoader)
					self.item_rando.modList.append(loadedYaml)
					self.item_rando.modList[-1]['fileName'] = self.item_rando.makeFileNameSafe(mod)
				else:
					message = 'Pack Modifier not found:' + "\n" + mod
					ItemRandomiser.DisplayMessage(None,message, None, "ERROR", self)



			self.updateModListView()

	def loadModifier(self):
		modfiles = QFileDialog.getOpenFileNames(directory = FileOperations.DEFAULT_MODIFIERS_DIRECTORY)[0]
		if len(modfiles) > 0:

			variablesToSet = []

			potentiallyMiss = {}

			for modfile in modfiles:
				yamlfile = open(modfile)
				yamltext = yamlfile.read()

				loadedYaml = yaml.load(yamltext, Loader=yaml.FullLoader)
				currentModifierNames = [obj["Name"] for obj in self.item_rando.modList]

				if loadedYaml["Name"] in currentModifierNames:
					if len(modfiles) == 1:
						message = loadedYaml["Name"] + " is already loaded!"
						ItemRandomiser.DisplayMessage(None,message, None, "ERROR", self)
					continue

				is_incompatible = False
				if "IncompatibleWith" in loadedYaml:
					for incomp in loadedYaml["IncompatibleWith"]:
						if incomp in currentModifierNames:
							is_incompatible = True
							message = loadedYaml["Name"] + "/" + incomp
							ItemRandomiser.DisplayMessage(None, message, None, "ERROR", GUI=self)

				if "IncompatibleWithout" in loadedYaml:
					options = loadedYaml["IncompatibleWithout"]
					optionFound = False
					for option in options:
						if option in currentModifierNames:
							optionFound = True
					if not optionFound:
						#TODO If loading multiple only show this message at the endpoint
						potentiallyMiss[modfile] = loadedYaml
						is_incompatible = True

				if not is_incompatible:
					self.item_rando.modList.append(loadedYaml)
					self.item_rando.modList[-1]['fileName'] = self.item_rando.makeFileNameSafe(modfile)

					if "VariablesSet" in loadedYaml:
						for variable in loadedYaml["VariablesSet"]:
							variablesToSet.append(variable)


			if len(potentiallyMiss) > 0:
				currentModifierNames = [obj["Name"] for obj in self.item_rando.modList]
				for miss in potentiallyMiss.keys():
					missYaml = potentiallyMiss[miss]
					is_incompatible = True

					options = missYaml["IncompatibleWithout"]
					found = False
					for option in options:
						if option in currentModifierNames:
							found = True

					if found:
						is_incompatible = False

					if not is_incompatible:
						self.item_rando.modList.append(missYaml)
						self.item_rando.modList[-1]['fileName'] = self.item_rando.makeFileNameSafe(miss)
					else:
						message = missYaml["Name"] + ":" + '/'.join(options)
						ItemRandomiser.DisplayMessage(None,message, None, "ERROR", self)

			if self.setNewVariables.isChecked():
				for variable in variablesToSet:
					self.PromptForVariable(variable)

			self.updateModListView()

	def PromptForVariable(self, variable):
		variableName = list(variable.keys())[0]
		variableDefault = variable[variableName]

		success = QInputDialog.getText(self, "Set variable", variableName + " (default is " + str(variableDefault) + ")")
		if success[1]:
			variableValue = success[0]
			if len(variableValue) != 0:
				self.modeVariables[variableName] = variableValue

		else:
			return



	def deleteModifier(self):
		row = self.modifierList.currentRow()
		if(row != -1):
			self.modifierList.setCurrentRow(-1)
			self.item_rando.modList.pop(row)
			self.updateModListView()

	def findFileWithinDirectory(self, name, directory):
		files = os.listdir(directory)
		for file in files:
			path_full = directory + "/" + file
			if os.path.isdir(path_full):
				found = self.findFileWithinDirectory(name, path_full)
				if found is not None:
					return found
			elif os.path.isfile(path_full):
				if name == file:
					return path_full

		return None

	def saveSettings(self):
		fName = QFileDialog.getSaveFileName(directory = 'Modes/Custom')[0]
		fName = self.item_rando.makeFileNameSafe(fName)
		if(fName != ''):
			filename = fName if fName.endswith(".yml") else fName + ".yml"
			self.item_rando.settings['DefaultModifiers'] = []
			for i in self.item_rando.modList:
				self.item_rando.settings['DefaultModifiers'].append(i['fileName'])

			if self.item_rando.PlandoMode:
				self.item_rando.settings["Plando"] = {}
				for key in self.item_rando.PlandoData.keys():
					self.item_rando.settings["Plando"][key] = self.item_rando.PlandoData[key]

			if "ModeVariables" not in self.item_rando.settings:
				self.item_rando.settings["ModeVariables"] = {}
			for variable_name in self.modeVariables:
				self.item_rando.settings["ModeVariables"][variable_name] = self.modeVariables[variable_name]


			with open(filename, 'w',encoding='utf-8') as f:
				yaml.dump(self.item_rando.settings, f, default_flow_style=False)

			self.item_rando.loadSettings(filename)
			self.updateGUIFromSettings(self.item_rando.settings)
				
	def SetUpPlando(self):
		ItemRandomiser.DisplayMessage(None,'Select a log file (which need not specify every item allocation) to use as basis for plandomizer.\n'
					   ' NOTE: We are not reponsible for any lost friendships due to use of plandomizer mode',
					   'Plandomizer Mode',"INFO", self)
		file = QFileDialog.getOpenFileName(directory = '.')[0]
		if file != '':
			yamlfile = open(file)
			yamltext = yamlfile.read()
			spoiler = yaml.load(yamltext, Loader=yaml.FullLoader)
			newSpoiler = OrderedDict()

			if 'Solution' in spoiler:
				for i in sorted(spoiler['Solution'],reverse=True):
					print("Plando:",i)
					print(spoiler['Solution'][i])
					newSpoiler[spoiler['Solution'][i]] = i
				print(newSpoiler)
			if 'Useless Stuff' in spoiler:
				for i in spoiler['Useless Stuff']:
					iValue = spoiler['Useless Stuff'][i]
					itemSplit = iValue.split("->")
					if len(itemSplit) > 1:
						itemUse = itemSplit[0]
					else:
						itemUse = itemSplit[0]
					print("Plando-load", i, itemUse)
					newSpoiler[i] = itemUse
			self.item_rando.PlandoData = newSpoiler
			self.item_rando.PlandoMode = True
			self.TurnOffPlando.setEnabled(True)
			
	def DeactivatePlando(self):
		self.item_rando.ResetPlando()
		self.TurnOffPlando.setEnabled(False)

	def updateModListView(self):
		self.modifierList.clear()
		for i in self.item_rando.modList:
			self.modifierList.addItem(i['Name'])

	def updateModifierDescription(self):
		_translate = QtCore.QCoreApplication.translate
		row = self.modifierList.currentRow()
		if(row != -1 and row < len(self.item_rando.modList)):
			self.ModifierDescription.setText(_translate("MainWindow", self.item_rando.modList[row]['Description']))
		else:
			self.ModifierDescription.setText(_translate("MainWindow", "No modifier selected!"))

	def WriteRandomizerConfig(self, defaultFile=None, firstRun=None):
		yamlfile = open('RandomizerConfig.yml')
		yamltext = yaml.load(yamlfile, Loader=yaml.FullLoader)

		if defaultFile is not None:
			yamltext['DefaultSettings'] = defaultFile

		if firstRun is not None:
			yamltext["FirstRun"] = firstRun

		with open('RandomizerConfig.yml', 'w', encoding='utf-8') as f:
			yaml.dump(yamltext, f, default_flow_style=False)
			
	def SelectDefaultSettings(self):
		ItemRandomiser.DisplayMessage(None,
			'Select the mode which should be loaded by default when you open up the randomizer',
			'Choose default settings', "INFO", self)
		defaultFile = QFileDialog.getOpenFileName(directory = 'Modes')[0]
		if(defaultFile != ''):
			self.WriteRandomizerConfig(defaultFile)
		else:
			ItemRandomiser.DisplayMessage(None,"A file was not selected", None, "ERROR", self)

	def LoadRaceModeSettingsUI(self):
		success = QInputDialog.getText(self, "Race Mode", "Input Race Mode Here")
		if success[1]:
			inputString = success[0]
		else:
			return

		raceModeSettings = self.item_rando.LoadRaceModeSettings(raceString=inputString)

		seed = raceModeSettings[2]
		md5 = raceModeSettings[3]

		self.SpoilerOutputRadioButton.setChecked(False)
		self.RaceModeRadioButton.setChecked(False)
		self.NoOutputRadioButton.setChecked(True)

		self.SeedInput.setText(seed)
		if self.romPath is None or len(self.romPath) == 0:
			self.selectRom()
		self.runGUIRandomiser(requiredMD5=md5)
			
	def ProcessHintSettings(self):
		_translate = QtCore.QCoreApplication.translate
		(option, ok1) = QInputDialog.getItem(self,"What hint level should be used?","What hint level should be used?",['0. No Hints', '1. Gym Signs', '2. Max one per location', '3. More hints types', '4. Hint useless items','5. Many hints everywhere', '6. Hints might be more useless than on 4'])
		if ok1:
			(nHints, ok2) = QInputDialog.getInt(self,"How many different hints?","How many different hints?")
			if ok2 and int(option[0]) > 0:
				self.item_rando.settings['HintLevel'] = int(option[0])
				self.item_rando.settings['nHints'] = nHints
				self.HintButton.setText(_translate("MainWindow", "Set Hints (LV: "+str(self.item_rando.settings['HintLevel'])+" N"+str(self.item_rando.settings['nHints'])+")"))
				QtGui.QGuiApplication.processEvents()
		else:
			self.item_rando.settings['HintLevel'] = 0
			self.item_rando.settings['nHints'] = 0
			
			self.HintButton.setText(_translate("MainWindow", "Set Hints (off)"))
			QtGui.QGuiApplication.processEvents()

	def SetCurrentVariables(self):
		variablesToSet = []
		loadedVariableNames = []

		for variable in self.modeVariables.keys():
			variablesToSet.append({variable:self.modeVariables[variable]})
			loadedVariableNames.append(variable)


		for mod in self.item_rando.modList:
			if "VariablesSet" in mod:
				for variable in mod["VariablesSet"]:
					variableName = list(variable.keys())[0]
					if variableName not in loadedVariableNames:
						variablesToSet.append(variable)

		if len(variablesToSet) == 0:
			ItemRandomiser.DisplayMessage(None,
				'No variables to set.',
				'Variables', "INFO", self)
		else:
			for variable in variablesToSet:
				self.PromptForVariable(variable)

		return


def main():

	try:
		CLIArgs = RunCLI.ArgumentParser()
		if CLIArgs.cli:
			CLIArgs.main()
			return
	except SystemExit:
		pass

	os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
	app = QApplication(sys.argv)
	form = RunWindow()
	form.show()
	app.exec_()

if __name__ == '__main__':
	main()
