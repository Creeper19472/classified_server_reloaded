# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wizard1.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Wizard(object):
    def setupUi(self, Wizard):
        Wizard.setObjectName("Wizard")
        Wizard.resize(517, 360)
        Wizard.setMinimumSize(QtCore.QSize(517, 360))
        Wizard.setMaximumSize(QtCore.QSize(517, 360))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI Light")
        Wizard.setFont(font)
        self.wizardPage1 = QtWidgets.QWizardPage()
        self.wizardPage1.setObjectName("wizardPage1")
        self.label = QtWidgets.QLabel(self.wizardPage1)
        self.label.setGeometry(QtCore.QRect(10, 10, 261, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI Light")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.wizardPage1)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 491, 21))
        self.label_2.setObjectName("label_2")
        Wizard.addPage(self.wizardPage1)
        self.wizardPage2 = QtWidgets.QWizardPage()
        self.wizardPage2.setObjectName("wizardPage2")
        self.label_4 = QtWidgets.QLabel(self.wizardPage2)
        self.label_4.setGeometry(QtCore.QRect(9, 9, 64, 21))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI Light")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.textBrowser = QtWidgets.QTextBrowser(self.wizardPage2)
        self.textBrowser.setGeometry(QtCore.QRect(9, 58, 481, 231))
        self.textBrowser.setObjectName("textBrowser")
        self.label_3 = QtWidgets.QLabel(self.wizardPage2)
        self.label_3.setGeometry(QtCore.QRect(9, 36, 192, 16))
        self.label_3.setObjectName("label_3")
        Wizard.addPage(self.wizardPage2)
        self.wizardPage = QtWidgets.QWizardPage()
        self.wizardPage.setObjectName("wizardPage")
        self.label_5 = QtWidgets.QLabel(self.wizardPage)
        self.label_5.setGeometry(QtCore.QRect(10, 10, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI Light")
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.wizardPage)
        self.label_6.setGeometry(QtCore.QRect(10, 40, 171, 16))
        self.label_6.setObjectName("label_6")
        self.progressBar = QtWidgets.QProgressBar(self.wizardPage)
        self.progressBar.setGeometry(QtCore.QRect(20, 260, 471, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        Wizard.addPage(self.wizardPage)

        self.retranslateUi(Wizard)
        QtCore.QMetaObject.connectSlotsByName(Wizard)

    def retranslateUi(self, Wizard):
        _translate = QtCore.QCoreApplication.translate
        Wizard.setWindowTitle(_translate("Wizard", "向导"))
        self.label.setText(_translate("Wizard", "欢迎使用"))
        self.label_2.setText(
            _translate("Wizard", "欢迎使用Classified File Management Service！请按下“下一步”准备安装。")
        )
        self.label_4.setText(_translate("Wizard", "使用协议"))
        self.textBrowser.setHtml(
            _translate(
                "Wizard",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'Microsoft YaHei UI Light'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt; font-weight:600;">Classified Services License</span></p>\n'
                '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:9pt;"><br /></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt; font-weight:600;">Copyright (c) 2020 Creeper Team</span></p>\n'
                '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:9pt;"><br /></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">The Classified file management system is an open source, free, and everyone can</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">contribute project. Before using the Classified file management system (Hereinafter</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">referred to as &quot;this system&quot;), the following regulations should be followed:</span></p>\n'
                '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:9pt;"><br /></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">1. Before using this system, regardless of personal or commercial behavior, you</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">   must apply to the developer in advance. Unauthorized use behavior we have the</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">   right to pursue legal responsibility and not responsible for any losses caused</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">   thereby.</span></p>\n'
                '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:9pt;"><br /></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">2. Modification and redistribution of this system are allowed, but you must include</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">   the original copyright information of this system when redistributing. We have the</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">   right to request the infringer to compensate any loss caused by this system.</span></p>\n'
                '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:9pt;"><br /></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">3. All modules, libraries, sample resources, etc. referenced by the system follow</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">   their original distribution license.</span></p>\n'
                '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:9pt;"><br /></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">4. We have the right to deprive a user of the right to use the system at any time</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">   without any explanation.</span></p>\n'
                '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:9pt;"><br /></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">5. If users use the cloud service provided by us, please pay attention to regularly</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">   backup your data to the local and regularly check whether your service is normal.</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">   WE ARE NOT RESPONESIBLE FOR ANY LOSSES CAUSED BY SUCH NEGLIGENCE. At any time, we</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">   recommend that users use their own servers for hosting.</span></p>\n'
                '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:9pt;"><br /></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">6. If the user\'s right to use the system is cancelled, the data hosted on our cloud</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">   service will be deleted synchronously. We have the right not to provide backup of</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">   data.</span></p>\n'
                '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:9pt;"><br /></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">7. If the user has donated before the right to use is cancelled, the decision to </span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">   cancel the right to use will still be executed, but we will provide a copy (if any)</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">   of the latest data of the cloud service. It may not be the latest, and we are not </span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">   responsible for data loss caused by its old version.</span></p>\n'
                '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:9pt;"><br /></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">When using the Classified file management system, you have accepted all the terms of</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:9pt;">this agreement. WE RESERVE THE RIGHT TO CHANGE THE LICENSE AT ANY TIME WITHOUT NOTICE.</span></p>\n'
                '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:9pt;"><br /></p></body></html>',
            )
        )
        self.label_3.setText(_translate("Wizard", "您必须同意下列协议才能继续安装。"))
        self.label_5.setText(_translate("Wizard", "正在安装"))
        self.label_6.setText(_translate("Wizard", "请您等待。"))
