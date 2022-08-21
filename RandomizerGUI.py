# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QTGUIDesign.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(802, 619)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Randomize = QtWidgets.QPushButton(self.centralwidget)
        self.Randomize.setGeometry(QtCore.QRect(570, 480, 211, 91))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Randomize.setFont(font)
        self.Randomize.setObjectName("Randomize")
        self.SelectRomFile = QtWidgets.QPushButton(self.centralwidget)
        self.SelectRomFile.setGeometry(QtCore.QRect(330, 510, 221, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.SelectRomFile.setFont(font)
        self.SelectRomFile.setObjectName("SelectRomFile")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 0, 781, 41))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 70, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(170, 110, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setText("")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.ChooseSettings = QtWidgets.QPushButton(self.centralwidget)
        self.ChooseSettings.setGeometry(QtCore.QRect(320, 80, 241, 91))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.ChooseSettings.setFont(font)
        self.ChooseSettings.setObjectName("ChooseSettings")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(600, 110, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(590, 180, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.CurentSettings = QtWidgets.QLabel(self.centralwidget)
        self.CurentSettings.setGeometry(QtCore.QRect(580, 139, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.CurentSettings.setFont(font)
        self.CurentSettings.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.CurentSettings.setWordWrap(True)
        self.CurentSettings.setObjectName("CurentSettings")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(150, 70, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.modifierList = QtWidgets.QListWidget(self.centralwidget)
        self.modifierList.setGeometry(QtCore.QRect(150, 100, 161, 381))
        self.modifierList.setObjectName("modifierList")
        item = QtWidgets.QListWidgetItem()
        self.modifierList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.modifierList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.modifierList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.modifierList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.modifierList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.modifierList.addItem(item)
        self.LoadModifier = QtWidgets.QPushButton(self.centralwidget)
        self.LoadModifier.setGeometry(QtCore.QRect(320, 180, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.LoadModifier.setFont(font)
        self.LoadModifier.setObjectName("LoadModifier")
        self.DeleteModifier = QtWidgets.QPushButton(self.centralwidget)
        self.DeleteModifier.setGeometry(QtCore.QRect(320, 230, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.DeleteModifier.setFont(font)
        self.DeleteModifier.setObjectName("DeleteModifier")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(620, 70, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_9.setObjectName("label_9")
        self.CurrentGoal = QtWidgets.QLabel(self.centralwidget)
        self.CurrentGoal.setGeometry(QtCore.QRect(560, 90, 231, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.CurrentGoal.setFont(font)
        self.CurrentGoal.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.CurrentGoal.setObjectName("CurrentGoal")
        self.OutputSpoiler = QtWidgets.QCheckBox(self.centralwidget)
        self.OutputSpoiler.setGeometry(QtCore.QRect(20, 120, 121, 17))
        self.OutputSpoiler.setChecked(True)
        self.OutputSpoiler.setObjectName("OutputSpoiler")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(320, 330, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.SaveSettings = QtWidgets.QPushButton(self.centralwidget)
        self.SaveSettings.setGeometry(QtCore.QRect(10, 510, 111, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.SaveSettings.setFont(font)
        self.SaveSettings.setObjectName("SaveSettings")
        self.SeedInput = QtWidgets.QLineEdit(self.centralwidget)
        self.SeedInput.setGeometry(QtCore.QRect(70, 100, 71, 20))
        self.SeedInput.setText("")
        self.SeedInput.setObjectName("SeedInput")
        self.SetSeedLabel = QtWidgets.QLabel(self.centralwidget)
        self.SetSeedLabel.setGeometry(QtCore.QRect(10, 100, 51, 16))
        self.SetSeedLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.SetSeedLabel.setObjectName("SetSeedLabel")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(130, 520, 181, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setWordWrap(True)
        self.label_6.setOpenExternalLinks(True)
        self.label_6.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.label_6.setObjectName("label_6")
        self.ModifierDescription = QtWidgets.QTextEdit(self.centralwidget)
        self.ModifierDescription.setGeometry(QtCore.QRect(320, 370, 241, 111))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.ModifierDescription.setPalette(palette)
        self.ModifierDescription.setAutoFillBackground(False)
        self.ModifierDescription.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ModifierDescription.setFrameShadow(QtWidgets.QFrame.Plain)
        self.ModifierDescription.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.ModifierDescription.setObjectName("ModifierDescription")
        self.SettingsDescription = QtWidgets.QTextEdit(self.centralwidget)
        self.SettingsDescription.setGeometry(QtCore.QRect(580, 210, 211, 251))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.SettingsDescription.setPalette(palette)
        self.SettingsDescription.setAutoFillBackground(False)
        self.SettingsDescription.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.SettingsDescription.setFrameShadow(QtWidgets.QFrame.Plain)
        self.SettingsDescription.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.SettingsDescription.setPlaceholderText("")
        self.SettingsDescription.setObjectName("SettingsDescription")
        self.PlandoLabel = QtWidgets.QLabel(self.centralwidget)
        self.PlandoLabel.setGeometry(QtCore.QRect(0, 139, 61, 31))
        self.PlandoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.PlandoLabel.setWordWrap(True)
        self.PlandoLabel.setObjectName("PlandoLabel")
        self.LoadPlandoFile = QtWidgets.QPushButton(self.centralwidget)
        self.LoadPlandoFile.setGeometry(QtCore.QRect(10, 180, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.LoadPlandoFile.setFont(font)
        self.LoadPlandoFile.setObjectName("LoadPlandoFile")
        self.TurnOffPlando = QtWidgets.QPushButton(self.centralwidget)
        self.TurnOffPlando.setEnabled(False)
        self.TurnOffPlando.setGeometry(QtCore.QRect(60, 140, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.TurnOffPlando.setFont(font)
        self.TurnOffPlando.setObjectName("TurnOffPlando")
        self.DefaultSettings = QtWidgets.QPushButton(self.centralwidget)
        self.DefaultSettings.setGeometry(QtCore.QRect(10, 220, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.DefaultSettings.setFont(font)
        self.DefaultSettings.setObjectName("DefaultSettings")
        self.AddItem = QtWidgets.QPushButton(self.centralwidget)
        self.AddItem.setGeometry(QtCore.QRect(10, 260, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.AddItem.setFont(font)
        self.AddItem.setObjectName("AddItem")
        self.View_Items = QtWidgets.QPushButton(self.centralwidget)
        self.View_Items.setGeometry(QtCore.QRect(10, 300, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.View_Items.setFont(font)
        self.View_Items.setObjectName("View_Items")
        self.BadgesNeeded = QtWidgets.QPushButton(self.centralwidget)
        self.BadgesNeeded.setGeometry(QtCore.QRect(10, 340, 131, 61))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.BadgesNeeded.setFont(font)
        self.BadgesNeeded.setObjectName("BadgesNeeded")
        self.HintButton = QtWidgets.QPushButton(self.centralwidget)
        self.HintButton.setGeometry(QtCore.QRect(10, 410, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.HintButton.setFont(font)
        self.HintButton.setObjectName("HintButton")
        self.version = QtWidgets.QLabel(self.centralwidget)
        self.version.setGeometry(QtCore.QRect(260, 40, 261, 41))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.version.setFont(font)
        self.version.setScaledContents(True)
        self.version.setAlignment(QtCore.Qt.AlignCenter)
        self.version.setObjectName("version")
        self.LoadPack = QtWidgets.QPushButton(self.centralwidget)
        self.LoadPack.setGeometry(QtCore.QRect(320, 280, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.LoadPack.setFont(font)
        self.LoadPack.setObjectName("LoadPack")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 802, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Randomize.setText(_translate("MainWindow", "Randomize\n"
" Rom"))
        self.SelectRomFile.setText(_translate("MainWindow", "Select Rom File"))
        self.label.setText(_translate("MainWindow", "Pokemon Crystal-Speedchoice Item Randomizer Tool"))
        self.label_2.setText(_translate("MainWindow", "Options"))
        self.ChooseSettings.setText(_translate("MainWindow", "Select Logic\n"
"Settings"))
        self.label_4.setText(_translate("MainWindow", "Curent Settings"))
        self.label_5.setText(_translate("MainWindow", "Settings Description"))
        self.CurentSettings.setText(_translate("MainWindow", "No settings selected!"))
        self.label_8.setText(_translate("MainWindow", "Modifiers"))
        __sortingEnabled = self.modifierList.isSortingEnabled()
        self.modifierList.setSortingEnabled(False)
        item = self.modifierList.item(0)
        item.setText(_translate("MainWindow", "No"))
        item = self.modifierList.item(1)
        item.setText(_translate("MainWindow", "settings"))
        item = self.modifierList.item(2)
        item.setText(_translate("MainWindow", "have"))
        item = self.modifierList.item(3)
        item.setText(_translate("MainWindow", "been"))
        item = self.modifierList.item(4)
        item.setText(_translate("MainWindow", "loaded!"))
        self.modifierList.setSortingEnabled(__sortingEnabled)
        self.LoadModifier.setText(_translate("MainWindow", "Load New Modifier"))
        self.DeleteModifier.setText(_translate("MainWindow", "Delete Selected Modifier"))
        self.label_9.setText(_translate("MainWindow", "Current Goal"))
        self.CurrentGoal.setText(_translate("MainWindow", "No goal set!"))
        self.OutputSpoiler.setText(_translate("MainWindow", "Output Logic Spoiler?"))
        self.label_12.setText(_translate("MainWindow", "Selected Modifier Description"))
        self.SaveSettings.setText(_translate("MainWindow", "Save\n"
" Settings"))
        self.SetSeedLabel.setText(_translate("MainWindow", "Set Seed:"))
        self.label_6.setText(_translate("MainWindow", "Read this to learn how to use this randomizer: https://tinyurl.com/y9nsknqv "))
        self.SettingsDescription.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.PlandoLabel.setText(_translate("MainWindow", "Plandomizer Mode"))
        self.LoadPlandoFile.setText(_translate("MainWindow", "Load Plando File"))
        self.TurnOffPlando.setText(_translate("MainWindow", "Clear Plando"))
        self.DefaultSettings.setText(_translate("MainWindow", "Select Default"))
        self.AddItem.setText(_translate("MainWindow", "Add An Item"))
        self.View_Items.setText(_translate("MainWindow", "View/Remove Items"))
        self.BadgesNeeded.setText(_translate("MainWindow", "Change # of badges\n"
" to unlock Mt. Silver?\n"
"(Currently 16)"))
        self.HintButton.setText(_translate("MainWindow", "Set Hints (off)"))
        self.version.setText(_translate("MainWindow", "Version 7.0.10"))
        self.LoadPack.setText(_translate("MainWindow", "Load New Pack"))
