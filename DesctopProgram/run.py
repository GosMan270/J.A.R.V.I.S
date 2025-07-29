# -*- coding: utf-8 -*-

import sys
import threading
import asyncio
import aiohttp

from PyQt5 import QtCore, QtGui, QtWidgets


class JarvisWebSocketClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.ws_url = f"ws://127.0.0.1:8000/ws/ai/{self.api_key}"
        self.session = None
        self.ws = None

    async def connect(self):
        self.session = aiohttp.ClientSession()
        self.ws = await self.session.ws_connect(self.ws_url)
        print('WS connected!')

    async def send_message(self, text):
        print(f"Try send: {text}")
        await self.ws.send_json({"text": text})
        print("Sent!")

    async def receive_message(self):
        msg = await self.ws.receive_json()
        print(f"Got: {msg}")
        return msg

    async def close(self):
        if self.ws:
            await self.ws.close()
        if self.session:
            await self.session.close()



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setMinimumSize(QtCore.QSize(350, 450))
        MainWindow.setMaximumSize(QtCore.QSize(350, 450))
        MainWindow.setBaseSize(QtCore.QSize(150, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.UpSHAP = QtWidgets.QFrame(self.centralwidget)
        self.UpSHAP.setGeometry(QtCore.QRect(0, 0, 351, 61))
        self.UpSHAP.setStyleSheet("background-color: rgb(34, 34, 34);")
        self.UpSHAP.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.UpSHAP.setFrameShadow(QtWidgets.QFrame.Raised)
        self.UpSHAP.setObjectName("UpSHAP")
        self.JARVIStext = QtWidgets.QLabel(self.UpSHAP)
        self.JARVIStext.setGeometry(QtCore.QRect(20, 20, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        font.setPointSize(11)
        self.JARVIStext.setFont(font)
        self.JARVIStext.setStyleSheet("color: rgb(255, 255, 255);")
        self.JARVIStext.setObjectName("JARVIStext")
        self.SettingsBTN = QtWidgets.QPushButton(self.UpSHAP)
        self.SettingsBTN.setGeometry(QtCore.QRect(180, 20, 71, 23))
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        self.SettingsBTN.setFont(font)
        self.SettingsBTN.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.SettingsBTN.setObjectName("SettingsBTN")
        self.CommandsBTN = QtWidgets.QPushButton(self.UpSHAP)
        self.CommandsBTN.setGeometry(QtCore.QRect(260, 20, 71, 23))
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        self.CommandsBTN.setFont(font)
        self.CommandsBTN.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.CommandsBTN.setObjectName("CommandsBTN")
        self.DownSHAP = QtWidgets.QFrame(self.centralwidget)
        self.DownSHAP.setGeometry(QtCore.QRect(0, 370, 351, 81))
        self.DownSHAP.setStyleSheet("background-color: rgb(34, 34, 34);")
        self.DownSHAP.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.DownSHAP.setFrameShadow(QtWidgets.QFrame.Raised)
        self.DownSHAP.setObjectName("DownSHAP")
        self.Version = QtWidgets.QLabel(self.DownSHAP)
        self.Version.setGeometry(QtCore.QRect(310, 60, 47, 13))
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        self.Version.setFont(font)
        self.Version.setStyleSheet("color: rgb(255, 255, 255);")
        self.Version.setObjectName("Version")
        self.GitHubURL = QtWidgets.QLabel(self.DownSHAP)
        self.GitHubURL.setGeometry(QtCore.QRect(10, 10, 41, 21))
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB Demi")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.GitHubURL.setFont(font)
        self.GitHubURL.setStyleSheet("color: rgb(97, 253, 255);")
        self.GitHubURL.setObjectName("GitHubURL")
        self.TelegramURL = QtWidgets.QLabel(self.DownSHAP)
        self.TelegramURL.setGeometry(QtCore.QRect(10, 30, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        font.setPointSize(9)
        self.TelegramURL.setFont(font)
        self.TelegramURL.setStyleSheet("color: rgb(129, 255, 90);")
        self.TelegramURL.setObjectName("TelegramURL")
        self.YouTubeURL = QtWidgets.QLabel(self.DownSHAP)
        self.YouTubeURL.setGeometry(QtCore.QRect(10, 50, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        font.setPointSize(9)
        self.YouTubeURL.setFont(font)
        self.YouTubeURL.setStyleSheet("color: rgb(255, 0, 0);")
        self.YouTubeURL.setObjectName("YouTubeURL")
        self.MicLED = QtWidgets.QLabel(self.centralwidget)
        self.MicLED.setGeometry(QtCore.QRect(10, 90, 16, 16))
        self.MicLED.setMinimumSize(QtCore.QSize(16, 16))
        self.MicLED.setStyleSheet("background-color: rgb(18, 255, 1);")
        self.MicLED.setText("")
        self.MicLED.setObjectName("MicLED")
        self.ConnectLED = QtWidgets.QLabel(self.centralwidget)
        self.ConnectLED.setGeometry(QtCore.QRect(10, 150, 16, 16))
        self.ConnectLED.setMinimumSize(QtCore.QSize(16, 16))
        self.ConnectLED.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.ConnectLED.setText("")
        self.ConnectLED.setObjectName("ConnectLED")
        self.WifiLED = QtWidgets.QLabel(self.centralwidget)
        self.WifiLED.setGeometry(QtCore.QRect(10, 180, 16, 16))
        self.WifiLED.setMinimumSize(QtCore.QSize(16, 16))
        self.WifiLED.setStyleSheet("background-color: rgb(255, 249, 52);")
        self.WifiLED.setText("")
        self.WifiLED.setObjectName("WifiLED")
        self.mic = QtWidgets.QLabel(self.centralwidget)
        self.mic.setGeometry(QtCore.QRect(30, 90, 71, 16))
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        font.setPointSize(10)
        self.mic.setFont(font)
        self.mic.setStyleSheet("color: rgb(82, 255, 19);")
        self.mic.setObjectName("mic")
        self.Connect = QtWidgets.QLabel(self.centralwidget)
        self.Connect.setGeometry(QtCore.QRect(30, 150, 71, 16))
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        font.setPointSize(10)
        self.Connect.setFont(font)
        self.Connect.setStyleSheet("color: rgb(255, 0, 0);")
        self.Connect.setObjectName("Connect")
        self.Wifi = QtWidgets.QLabel(self.centralwidget)
        self.Wifi.setGeometry(QtCore.QRect(30, 180, 31, 16))
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        font.setPointSize(10)
        self.Wifi.setFont(font)
        self.Wifi.setStyleSheet("color: rgb(252, 255, 48);")
        self.Wifi.setObjectName("Wifi")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(30, 330, 321, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.RESPONCE = QtWidgets.QLabel(self.centralwidget)
        self.RESPONCE.setGeometry(QtCore.QRect(140, 300, 81, 20))
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        font.setPointSize(12)
        self.RESPONCE.setFont(font)
        self.RESPONCE.setStyleSheet("color: rgb(255, 255, 255);")
        self.RESPONCE.setObjectName("RESPONCE")
        self.SoundLED = QtWidgets.QLabel(self.centralwidget)
        self.SoundLED.setGeometry(QtCore.QRect(10, 120, 16, 16))
        self.SoundLED.setMinimumSize(QtCore.QSize(16, 16))
        self.SoundLED.setStyleSheet("background-color: rgb(9, 255, 5);")
        self.SoundLED.setText("")
        self.SoundLED.setObjectName("SoundLED")
        self.Sound = QtWidgets.QLabel(self.centralwidget)
        self.Sound.setGeometry(QtCore.QRect(30, 120, 41, 16))
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        font.setPointSize(10)
        self.Sound.setFont(font)
        self.Sound.setStyleSheet("color: rgb(42, 255, 10);")
        self.Sound.setObjectName("Sound")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(130, 90, 211, 151))
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        font.setPointSize(11)
        self.textEdit.setFont(font)
        self.textEdit.setStyleSheet(
            "color: rgb(255, 255, 255);\n"
            "background-color: rgb(44, 44, 44);"
        )
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(200, 250, 75, 23))
        font = QtGui.QFont()
        font.setFamily("Bauhaus 93")
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet(
            "background-color: rgb(57, 57, 57);\n"
            "color: rgb(255, 255, 255);"
        )
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # ---- WebSocket инициализация ----
        self.api_key = "secretkey123"  # <-- свой реальный API-KEY!
        self.ws_client = JarvisWebSocketClient(self.api_key)
        self.ws_loop = asyncio.new_event_loop()
        self.ws_connected = threading.Event()
        threading.Thread(target=self.start_ws, daemon=True).start()
        self.pushButton.clicked.connect(self.handle_send)

    def start_ws(self):
        asyncio.set_event_loop(self.ws_loop)
        self.ws_loop.run_until_complete(self.ws_client.connect())
        self.ws_connected.set()
        self.ws_loop.run_forever()

    def handle_send(self):
        user_text = self.textEdit.toPlainText().strip()
        if not user_text:
            self.RESPONCE.setText("Поле ввода пустое!")
            return
        self.RESPONCE.setText("Загрузка...")
        if not self.ws_connected.is_set():
            self.RESPONCE.setText("Подключение к серверу...")
            self.ws_connected.wait()
        future = asyncio.run_coroutine_threadsafe(self.send_and_receive(user_text), self.ws_loop)

        def done_callback(fut):
            if exc := fut.exception():
                print("WS-ошибка:", exc)

        future.add_done_callback(done_callback)

    async def send_and_receive(self, user_text):
        try:
            await self.ws_client.send_message(user_text)
            job_msg = await self.ws_client.receive_message()
            job_id = job_msg.get('job_id')
            result_msg = await self.ws_client.receive_message()
            print(result_msg)
            print(result_msg)
            print(result_msg)
            print(result_msg)
            print(result_msg)

            self.RESPONCE.setText("Выполненно!")
            self.textEdit.setText(result_msg['ai_final_answer'])
            text = result_msg.get('result', 'Нет ответа от сервера!')
        except Exception as e:
            text = f"[WS-клиент ошибка] {e}"
        QtCore.QMetaObject.invokeMethod(
            self.RESPONCE,
            "setText",
            QtCore.Qt.QueuedConnection,
            QtCore.Q_ARG(str, text)
        )


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "J.A.R.V.I.S"))
        self.JARVIStext.setText(_translate("MainWindow", "J.A.R.V.I.S"))
        self.SettingsBTN.setText(_translate("MainWindow", "SETTINGS"))
        self.CommandsBTN.setText(_translate("MainWindow", "COMMANDS"))
        self.Version.setText(_translate("MainWindow", "v 0.0.1"))
        self.GitHubURL.setText(_translate("MainWindow", "GitHub"))
        self.TelegramURL.setText(_translate("MainWindow", "Telegram"))
        self.YouTubeURL.setText(_translate("MainWindow", "YouTube"))
        self.mic.setText(_translate("MainWindow", "Microphone"))
        self.Connect.setText(_translate("MainWindow", "Connect"))
        self.Wifi.setText(_translate("MainWindow", "Wifi"))
        self.RESPONCE.setText(_translate("MainWindow", "RESPONCE"))
        self.Sound.setText(_translate("MainWindow", "Sound"))
        self.textEdit.setHtml(_translate("MainWindow",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" />"
                                         "<style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head>"
                                         "<body style=\" font-family:'Bauhaus 93'; font-size:11pt; font-weight:400; font-style:normal;\">"
                                         "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; "
                                         "-qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-weight:600; "
                                         "color:#ffffff;\">Yor responce:</span></p></body></html>"
                                         ))
        self.pushButton.setText(_translate("MainWindow", "RESPONCE"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())