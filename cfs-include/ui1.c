/********************************************************************************
** Form generated from reading UI file 'wizard1.ui'
**
** Created by: Qt User Interface Compiler version 5.15.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI1_H
#define UI1_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QLabel>
#include <QtWidgets/QProgressBar>
#include <QtWidgets/QTextBrowser>
#include <QtWidgets/QWizard>
#include <QtWidgets/QWizardPage>

QT_BEGIN_NAMESPACE

class Ui_Wizard
{
public:
    QWizardPage *wizardPage1;
    QLabel *label;
    QLabel *label_2;
    QWizardPage *wizardPage2;
    QLabel *label_4;
    QTextBrowser *textBrowser;
    QLabel *label_3;
    QWizardPage *wizardPage;
    QLabel *label_5;
    QLabel *label_6;
    QProgressBar *progressBar;

    void setupUi(QWizard *Wizard)
    {
        if (Wizard->objectName().isEmpty())
            Wizard->setObjectName(QString::fromUtf8("Wizard"));
        Wizard->resize(517, 360);
        Wizard->setMinimumSize(QSize(517, 360));
        Wizard->setMaximumSize(QSize(517, 360));
        QFont font;
        font.setFamily(QString::fromUtf8("Microsoft YaHei UI Light"));
        Wizard->setFont(font);
        wizardPage1 = new QWizardPage();
        wizardPage1->setObjectName(QString::fromUtf8("wizardPage1"));
        label = new QLabel(wizardPage1);
        label->setObjectName(QString::fromUtf8("label"));
        label->setGeometry(QRect(10, 10, 261, 31));
        QFont font1;
        font1.setFamily(QString::fromUtf8("Microsoft YaHei UI Light"));
        font1.setPointSize(12);
        label->setFont(font1);
        label_2 = new QLabel(wizardPage1);
        label_2->setObjectName(QString::fromUtf8("label_2"));
        label_2->setGeometry(QRect(10, 50, 491, 21));
        Wizard->addPage(wizardPage1);
        wizardPage2 = new QWizardPage();
        wizardPage2->setObjectName(QString::fromUtf8("wizardPage2"));
        label_4 = new QLabel(wizardPage2);
        label_4->setObjectName(QString::fromUtf8("label_4"));
        label_4->setGeometry(QRect(9, 9, 64, 21));
        label_4->setFont(font1);
        textBrowser = new QTextBrowser(wizardPage2);
        textBrowser->setObjectName(QString::fromUtf8("textBrowser"));
        textBrowser->setGeometry(QRect(9, 58, 464, 177));
        label_3 = new QLabel(wizardPage2);
        label_3->setObjectName(QString::fromUtf8("label_3"));
        label_3->setGeometry(QRect(9, 36, 192, 16));
        Wizard->addPage(wizardPage2);
        wizardPage = new QWizardPage();
        wizardPage->setObjectName(QString::fromUtf8("wizardPage"));
        label_5 = new QLabel(wizardPage);
        label_5->setObjectName(QString::fromUtf8("label_5"));
        label_5->setGeometry(QRect(10, 10, 101, 21));
        label_5->setFont(font1);
        label_6 = new QLabel(wizardPage);
        label_6->setObjectName(QString::fromUtf8("label_6"));
        label_6->setGeometry(QRect(10, 40, 171, 16));
        progressBar = new QProgressBar(wizardPage);
        progressBar->setObjectName(QString::fromUtf8("progressBar"));
        progressBar->setGeometry(QRect(10, 190, 471, 23));
        progressBar->setValue(0);
        Wizard->addPage(wizardPage);

        retranslateUi(Wizard);

        QMetaObject::connectSlotsByName(Wizard);
    } // setupUi

    void retranslateUi(QWizard *Wizard)
    {
        Wizard->setWindowTitle(QCoreApplication::translate("Wizard", "\345\220\221\345\257\274", nullptr));
        label->setText(QCoreApplication::translate("Wizard", "\346\254\242\350\277\216\344\275\277\347\224\250", nullptr));
        label_2->setText(QCoreApplication::translate("Wizard", "\346\254\242\350\277\216\344\275\277\347\224\250Classified File Management Service\357\274\201\350\257\267\346\214\211\344\270\213\342\200\234\344\270\213\344\270\200\346\255\245\342\200\235\345\207\206\345\244\207\345\256\211\350\243\205\343\200\202", nullptr));
        label_4->setText(QCoreApplication::translate("Wizard", "\344\275\277\347\224\250\345\215\217\350\256\256", nullptr));
        textBrowser->setHtml(QCoreApplication::translate("Wizard", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI Light'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Classified Services License</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Copyright (c) 2020 Creeper Team</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-bl"
                        "ock-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The Classified file management system is an open source, free, and everyone can</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">contribute project. Before using the Classified file management system (Hereinafter</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">referred to as &quot;this system&quot;), the following regulations should be followed:</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1. Before using this system, regardless of personal or co"
                        "mmercial behavior, you</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">   must apply to the developer in advance. Unauthorized use behavior we have the</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">   right to pursue legal responsibility and not responsible for any losses caused</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">   thereby.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2. Modification and redistribution of this system are allowed, but you must include</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left"
                        ":0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">   the original copyright information of this system when redistributing. We have the</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">   right to request the infringer to compensate any loss caused by this system.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3. All modules, libraries, sample resources, etc. referenced by the system follow</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">   their original distribution license.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-i"
                        "ndent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">4. We have the right to deprive a user of the right to use the system at any time</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">   without any explanation.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">5. If users use the cloud service provided by us, please pay attention to regularly</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">   backup your data to the local and regularly check whether your service is normal.</p>\n"
"<p style=\" margin-top:0px"
                        "; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">   WE ARE NOT RESPONESIBLE FOR ANY LOSSES CAUSED BY SUCH NEGLIGENCE. At any time, we</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">   recommend that users use their own servers for hosting.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">6. If the user's right to use the system is cancelled, the data hosted on our cloud</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">   service will be deleted synchronously. We have the right not to provide backup of</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0p"
                        "x; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">   data.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">7. If the user has donated before the right to use is cancelled, the decision to </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">   cancel the right to use will still be executed, but we will provide a copy (if any)</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">   of the latest data of the cloud service. It may not be the latest, and we are not </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">   responsible for data "
                        "loss caused by its old version.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">When using the Classified file management system, you have accepted all the terms of</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">this agreement. WE RESERVE THE RIGHT TO CHANGE THE LICENSE AT ANY TIME WITHOUT NOTICE.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", nullptr));
        label_3->setText(QCoreApplication::translate("Wizard", "\346\202\250\345\277\205\351\241\273\345\220\214\346\204\217\344\270\213\345\210\227\345\215\217\350\256\256\346\211\215\350\203\275\347\273\247\347\273\255\345\256\211\350\243\205\343\200\202", nullptr));
        label_5->setText(QCoreApplication::translate("Wizard", "\346\255\243\345\234\250\345\256\211\350\243\205", nullptr));
        label_6->setText(QCoreApplication::translate("Wizard", "\350\257\267\346\202\250\347\255\211\345\276\205\343\200\202", nullptr));
    } // retranslateUi

};

namespace Ui {
    class Wizard: public Ui_Wizard {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI1_H
