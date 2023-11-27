### Game Roulette Main Class
## Contains:
# Main Menu, GUI code
# Daniel O'Brien : Project Start : 21/11/23

import tkinter as tk
import tkinter.ttk as ttk
import threading
import time
import pygame
import sv_ttk
import webbrowser
from tkinter import *
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QVBoxLayout, QWidget, QDialog, QLabel, QPushButton
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QFont,QTransform, QPainter
from PyQt6.QtCore import QSize, Qt, QUrl, QTimer, Qt
from PyQt6.QtMultimedia import QMediaPlayer
from gameDatabaseAPICalls import gameNameCall
import urllib.parse

from PyQt6 import *

# Global Variables
muted = False
shouldRun = True
gr = None

class CustomMainWindow(QMainWindow):
    def closeEvent(self, event):
        global shouldRun
        shouldRun = False 
        QApplication.quit()
          
# This Uses Tkinter
class main():
    def MainAppRoulette(self):
        global gr,shouldRun
        def on_closing():
            global shouldRun
            shouldRun = False 
            gr.destroy()
        gr = tk.Tk()
        gr.protocol("WM_DELETE_WINDOW", on_closing)
        # Title Screen Music
        def PlayMainMenuMusic(music):
            pygame.mixer.init()
            pygame.mixer.music.load(music)
            pygame.mixer.music.play(-1)
            while shouldRun:
                pygame.time.wait(100)  # Check the flag at regular intervals
            pygame.mixer.music.stop()
        
        def fadeOutMusic(duration_ms):
            clock = pygame.time.Clock()
            initial_volume = pygame.mixer.music.get_volume()
            fade_steps = 100  # Number of steps for the fade-out effect
            fade_duration = duration_ms / fade_steps  # Time for each step
            volume_step = initial_volume / fade_steps

            for _ in range(fade_steps):
                initial_volume -= volume_step
                pygame.mixer.music.set_volume(initial_volume)
                pygame.time.delay(int(fade_duration))
                clock.tick(60)
            pygame.mixer.music.stop()
            
        # Toggle Mute and Unmute
        def ToggleMute():
            global muted
            if muted:
                pygame.mixer.music.unpause()
                muted = False
                muteButton.config(text="Mute")
            else:
                pygame.mixer.music.pause()
                muted = True
                muteButton.config(text="Unmute")
        # Setting Up Window

        sv_ttk.set_theme("dark")
        gr.title("Game Roulette!")
        gr.geometry('700x500')
        gr.eval('tk::PlaceWindow . center')
        gr.resizable(False,False)
        gr.tk.call("set_theme", "dark")
        # Setting Up
        br = PhotoImage(file = "Images\gameroulettelogo.png")
        brImageLabel = Label(gr,image = br)
        brImageLabel.place(x=0,y=0)
        musicThread = threading.Thread(target=PlayMainMenuMusic, args=("Music\Prelude-in-e-minor.mp3",),daemon=True)
        musicThread.start()
        # Mute Button
        style = ttk.Style()
        style.configure("TButton", font=("Playfair Display",15), padding=(5, 5), background="black", foreground="red")
        style.configure("TButton.Muted", font=("Helvetica", 12), padding=(5, 5), relief=tk.RAISED, background="red", borderwidth=3, focusthickness=3)
        muteButton = ttk.Button(gr, text="Mute", command=ToggleMute, style="TButton")
        muteButton.pack(side=tk.LEFT, padx=10, pady=10, anchor="sw")
        # LinkedIn Link
        def linkToLinkedIn():
            webbrowser.open_new("https://www.linkedin.com/in/danielo-brien/") # Shameless self promotion
        style = ttk.Style()
        style.configure("TButton", font=("Playfair Display",15), padding=(5,5), foreground="red",relief=tk.RAISED,focusthickness=4)
        linkedInButton = ttk.Button(gr,text = "LinkedIn",command=linkToLinkedIn)
        linkedInButton.pack(side=tk.RIGHT,padx=10,pady=10,anchor="se")
        # Enter App Button
        appMain = applicationMain()
        style=ttk.Style()
        style.configure("TButton", font=("Playfair Display",15), padding=(5,5), foreground="red",relief=tk.RAISED,focusthickness=4)
        beginButton = ttk.Button(gr, text='Enter The Roulette', command=lambda: [fadeOutMusic(2000), gr.destroy(), appMain.SecondaryMenu()])
        beginButton.place(relx=0.5,rely=0.5,anchor=CENTER,width=250,height=50)
        tk.mainloop()

# This Uses PyQt
class applicationMain():
    def SecondaryMenu(self):
         
        def openDiscordWindow():
            dialog = QDialog()
            dialog.setWindowTitle("Discord Bot Link")
            dialog.setFixedSize(400, 400)
            label = QLabel("Thank You.\n Redirecting To Web To add Bot To Server", dialog)
            dialogLayout = QVBoxLayout()
            dialogLayout.addWidget(label)
            webbrowser.open("https://discord.com/api/oauth2/authorize?client_id=839982509559513099&permissions=517544061952&scope=bot") #Will need to upload bot to server before this is ready
            dialog.close()
            
        def openGameDatabaseWindow():
            
            global displayRandomGame
            global displayRandomGameStoreSearch
            global displaySeparator
            displayRandomGame = None
            displayRandomGameStoreSearch = None
            displaySeparator = None
            
            def exitButtonClicked(gameDatabaseLayout):
                gameDatabaseDialog.close()
                
            def randomGameButtonClicked(gameDatabaseLayout):
                global displayRandomGame
                global displayRandomGameStoreSearch
                global displaySeparator
                
                if displayRandomGame is not None: # this removes already generated random games from the display window
                    gameDatabaseLayout.removeWidget(displayRandomGame)
                    displayRandomGame.deleteLater()
                if displayRandomGameStoreSearch is not None:
                    gameDatabaseLayout.removeWidget(displayRandomGameStoreSearch)
                    displayRandomGameStoreSearch.deleteLater()
                if displaySeparator is not None:
                    gameDatabaseLayout.removeWidget(displaySeparator)

                    
                randomGameCall = gameNameCall()
                randomGame = randomGameCall.apiCallGame()
                randomGameStr = ",".join(str(element) for element in randomGame)
                displayRandomGame = QLabel("The Game Picked is:" + " " + randomGameStr)
                encodedGameName = urllib.parse.quote(randomGameStr)
                displaySeparator = QLabel("=========================================================")
                displayRandomGameStoreSearch = QLabel(f'<a href="https://store.steampowered.com/search/?term={encodedGameName}">Store Search: {randomGameStr}</a>')
                rouletteLayout.addWidget(displayRandomGame)
                displayRandomGameStoreSearch.setOpenExternalLinks(True)
                displayRandomGameStoreSearch.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
                rouletteLayout.addWidget(displayRandomGameStoreSearch)
                rouletteLayout.addWidget(displaySeparator)

            gameDatabaseDialog = QDialog()
            gameDatabaseDialog.setWindowTitle("Game Roulette Database")
            gameDatabaseDialog.setFixedSize(700,400)
            
            randomGameButton = QPushButton(gameDatabaseDialog)
            exitWindowButton = QPushButton(gameDatabaseDialog)
            
            disclaimerLabel = QLabel("Note: Some games may not have completeable Single-Player Stories/Campaigns, just reroll if this happens")
            disclaimerLabel.setStyleSheet("font-weight: lighter;")
            
            randomGameButton.setText("ROULETTE!")
            randomGameButton.setFixedSize(400,200)
            
            exitWindowButton.setText("Exit")
            
            gameDatabaseLayout = QVBoxLayout()
            gameDatabaseLayout.addWidget(disclaimerLabel)
            gameDatabaseLayout.addStretch(1)
            rouletteLayout = QVBoxLayout()
            rouletteLayout.addWidget(randomGameButton)
            rouletteOutputPlaceholder = QWidget()
            rouletteLayout.addWidget(rouletteOutputPlaceholder)
            gameDatabaseLayout.addLayout(rouletteLayout)
            gameDatabaseLayout.addStretch(1)
            
            randomGameButton.clicked.connect(lambda: randomGameButtonClicked(gameDatabaseLayout))
            
            gameDatabaseLayout.addWidget(exitWindowButton)
            exitWindowButton.clicked.connect(lambda: exitButtonClicked(gameDatabaseLayout))
            
            gameDatabaseDialog.setLayout(gameDatabaseLayout)
            gameDatabaseDialog.exec()
            
        
        def handleItemClick(item):
            if item.text().endswith("Exit"):
                menuApp.exit()
            elif item.text().endswith("Discord Bot"):
                openDiscordWindow()
            elif item.text().endswith("Games Database Picker"):
                openGameDatabaseWindow()
                
        menuApp = QApplication([]) 
        window = CustomMainWindow()
        window.setWindowTitle("Game Roulette!")
        window.setFixedSize(800, 600)
        backgroundImagePath = 'Images\mainApplicationBackground.png'
        pixmap = QPixmap(backgroundImagePath)
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        window.setPalette(palette)
        
        centralWidget = QWidget()
        layout = QVBoxLayout()
        centralWidget.setLayout(layout)
        window.setCentralWidget(centralWidget)
        listWidget = QListWidget()
        font = QFont()
        font.setPointSize(25)
        listWidget.setFont(font)

        listItems = ["Discord Bot", "Games Database Picker", "Exit"]
        for itemText in listItems:
            item = QListWidgetItem(f". {itemText}")
            item.setSizeHint(QSize(-1, 60))
            listWidget.addItem(item)

        listWidget.itemClicked.connect(handleItemClick)
        listWidget.setStyleSheet("""
        QListWidget {
        border: 2px solid black; /* Black border */
        background: transparent; /* No background */
        color: #38023B;  /* Text color */
        font-weight: bold;
}
    QListWidget::item:selected {
        background-color: lightblue;
}
    """)
        layout.addWidget(listWidget)
        window.show()
        menuApp.exec()
        sys.exit(0)
        
mainCall = main()
mainCall.MainAppRoulette()