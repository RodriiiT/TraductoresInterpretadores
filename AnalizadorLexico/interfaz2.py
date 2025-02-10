# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interfaz2.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from analizador import analizar_lexicamente, obtener_errores


class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
                MainWindow.setObjectName("MainWindow")
                MainWindow.resize(800, 600)
                MainWindow.setStyleSheet("background-color:rgb(0, 49, 53)")
                self.centralwidget = QtWidgets.QWidget(MainWindow)
                self.centralwidget.setObjectName("centralwidget")
                
                #Parte resultados
                self.resultadosButton = QtWidgets.QPushButton(self.centralwidget)
                self.resultadosButton.setGeometry(QtCore.QRect(170, 430, 75, 24))
                self.resultadosButton.setStyleSheet("""
    QPushButton {
        color: rgb(0, 0, 0);
        background-color: rgb(217, 217, 217);
        border-radius: 10px;
    }
    QPushButton:hover {
        background-color: rgb(180, 180, 180);
    }
""")
                self.resultadosButton.setObjectName("resultadosButton")
                self.resultadosButton.clicked.connect(self.mostrar_resultados)
                
                
                #Parte errores
                self.erroresButton_2 = QtWidgets.QPushButton(self.centralwidget)
                self.erroresButton_2.setGeometry(QtCore.QRect(560, 430, 75, 24))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.erroresButton_2.setFont(font)
                self.erroresButton_2.setStyleSheet("""
    QPushButton {
        color: rgb(0, 0, 0);
        background-color: rgb(217, 217, 217);
        border-radius: 10px;
    }
    QPushButton:hover {
        background-color: rgb(180, 180, 180); /* Color más oscuro al pasar el mouse */
    }
""")
                self.erroresButton_2.setObjectName("erroresButton_2")
                self.erroresButton_2.clicked.connect(self.mostrar_errores)
                
                
                
                # Campo de texto para ingresar código Java
                self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
                self.textEdit.setGeometry(QtCore.QRect(50, 50, 701, 121))
                self.textEdit.setStyleSheet("background-color: rgb(217, 217, 217); color: black;")
                self.textEdit.setObjectName("textEdit")

                self.label = QtWidgets.QLabel("")
                self.label.setWordWrap(True)  # Permite que el texto haga saltos de línea
                #self.scrollLayout.addWidget(self.label)
                #self.scrollArea.setWidget(self.scrollContent)
                
                """
                self.salidaResultados = QtWidgets.QFrame(self.centralwidget)
                self.salidaResultados.setGeometry(QtCore.QRect(50, 220, 311, 191))
                self.salidaResultados.setStyleSheet("background-color: rgb(217, 217, 217);")
                self.salidaResultados.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.salidaResultados.setFrameShadow(QtWidgets.QFrame.Raised)
                self.salidaResultados.setObjectName("salidaResultados")
                """
                
                # Campo de texto para mostrar los resultados del análisis
                self.salidaResultados = QtWidgets.QTextEdit(self.centralwidget)
                self.salidaResultados.setGeometry(QtCore.QRect(50, 220, 311, 191))
                self.salidaResultados.setStyleSheet("background-color: rgb(255, 255, 255); color: black;")
                self.salidaResultados.setObjectName("salidaResultados")
                self.salidaResultados.setReadOnly(True)  # Para que solo se muestren los resultados

                 # Campo de texto para mostrar los errores
                self.salidaErrores = QtWidgets.QTextEdit(self.centralwidget)
                self.salidaErrores.setGeometry(QtCore.QRect(430, 220, 311, 191))
                self.salidaErrores.setStyleSheet("background-color: rgb(255, 255, 255); color: black;")
                self.salidaErrores.setObjectName("salidaErrores")
                self.salidaErrores.setReadOnly(True)  # Solo lectura

                
                self.textCodigo = QtWidgets.QLabel(self.centralwidget)
                self.textCodigo.setGeometry(QtCore.QRect(50, 20, 131, 20))
                self.textCodigo.setStyleSheet("color:rgb(255, 255, 255)")
                self.textCodigo.setObjectName("textCodigo")
                self.textResultados = QtWidgets.QLabel(self.centralwidget)
                self.textResultados.setGeometry(QtCore.QRect(50, 190, 131, 20))
                self.textResultados.setStyleSheet("color: rgb(255, 255, 255)")
                self.textResultados.setObjectName("textResultados")
                self.textErrores = QtWidgets.QLabel(self.centralwidget)
                self.textErrores.setGeometry(QtCore.QRect(430, 190, 131, 20))
                self.textErrores.setStyleSheet("color:rgb(255, 255, 255)")
                self.textErrores.setObjectName("textErrores")
                self.titulo = QtWidgets.QLabel(self.centralwidget)
                self.titulo.setGeometry(QtCore.QRect(230, 0, 431, 41))
                font = QtGui.QFont()
                font.setFamily("Arial Rounded MT")
                font.setPointSize(24)
                font.setBold(True)
                self.titulo.setFont(font)
                self.titulo.setStyleSheet("color: rgb(255, 255, 255);")
                self.titulo.setObjectName("titulo")
                self.titulo_2 = QtWidgets.QLabel(self.centralwidget)
                self.titulo_2.setGeometry(QtCore.QRect(650, 520, 141, 41))
                font = QtGui.QFont()
                font.setFamily("Arial Rounded MT")
                font.setPointSize(12)
                font.setBold(True)
                self.titulo_2.setFont(font)
                self.titulo_2.setStyleSheet("color: rgb(255, 255, 255);")
                self.titulo_2.setObjectName("titulo_2")
                MainWindow.setCentralWidget(self.centralwidget)
                self.menubar = QtWidgets.QMenuBar(MainWindow)
                self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
                self.menubar.setObjectName("menubar")
                self.menuQue_es_esto = QtWidgets.QMenu(self.menubar)
                self.menuQue_es_esto.setObjectName("menuQue_es_esto")
                MainWindow.setMenuBar(self.menubar)
                self.statusbar = QtWidgets.QStatusBar(MainWindow)
                self.statusbar.setObjectName("statusbar")
                MainWindow.setStatusBar(self.statusbar)
                self.menubar.addAction(self.menuQue_es_esto.menuAction())

                self.retranslateUi(MainWindow)
                QtCore.QMetaObject.connectSlotsByName(MainWindow)
                
        def retranslateUi(self, MainWindow):
                _translate = QtCore.QCoreApplication.translate
                MainWindow.setWindowTitle(_translate("MainWindow", "Analizador Léxico"))
                self.resultadosButton.setText(_translate("MainWindow", "Resultados"))
                self.erroresButton_2.setText(_translate("MainWindow", "Errores"))
                self.textCodigo.setText(_translate("MainWindow", "Introduzca su código"))
                self.textResultados.setText(_translate("MainWindow", "Resultados"))
                self.textErrores.setText(_translate("MainWindow", "Errores"))
                self.titulo.setText(_translate("MainWindow", "Fase #1 Análisis Léxico"))
                self.titulo_2.setText(_translate("MainWindow", "Rodrigo Torres\n"
        "Jesús Araujo"))
                self.menuQue_es_esto.setTitle(_translate("MainWindow", "AnalisisLexico"))
                
        def mostrar_resultados(self):
                codigo_java = self.textEdit.toPlainText()  # Obtener el código ingresado
                tokens = analizar_lexicamente(codigo_java)  # Llamar al analizador
                
                # Convertir los tokens en una cadena de texto para mostrar en la interfaz
                resultado_texto = "\n".join([f"{token[0]} → {token[1]}, {token[2]}" for token in tokens])
                
                self.salidaResultados.setPlainText(resultado_texto)  # Mostrar resultados en la GUI
                
                #Imprimir en la consola
                for palabra, linea, categoria in tokens:
                        print(f"{palabra} -> Línea {linea}, {categoria}")
                
                        
        def mostrar_errores(self):
                codigo_java = self.textEdit.toPlainText()  # Obtener el código ingresado
                errores = obtener_errores(codigo_java)  # Llamar a la función que obtiene los errores
                
                # Mostrar los errores en la interfaz
                if errores:
                        errores_texto = "\n".join(errores)
                else:
                        errores_texto = "No se detectaron errores."
                        
                self.salidaErrores.setPlainText(errores_texto)
                print("Presionando botón error")



if __name__ == "__main__":
        import sys
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
