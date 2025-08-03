# Lukas Freudenberg
#
# Permission is hereby granted, free of charge, to any person 
# obtaining a copy of this software and associated documentation 
# files (the "Software"), to deal in the Software without 
# restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software 
# is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR 
# OTHER DEALINGS IN THE SOFTWARE.

# 2025-08-03, ver0.3.4
# 
# LSB includes and starts a GUI for dynamically playing audio.

# Import modules
import numpy as np
import threading
from tkinter import ttk
#import time
import os
import math
import time
import tkinter as tk
from LFLib import LFLib as L
import LFAudio

class LSB:
	# Constructor method
	def __init__(self):
		# Default styles for widgets
		# Background colour
		self.bgc = "#101010"
		# Text colour
		self.fgc = "#ffffff"
		# Background colour for highlighted labels
		self.hbgc = "#505050"
		# Text colour for highlighted labels
		self.hfgc = "#ffffff"
		# Stop button colour
		self.sbc = "#CD0000"
		# Stop button text colour
		self.sbtc = "#000000"
		# Play button colour
		self.pbc = "#008000"
		# Play button text colour
		self.pbtc = "#000000"
		# Pause/Unpause button colour
		self.pubc = "#408000"
		# Pause/Unpause button text colour
		self.pubtc = "#000000"
		# Skip button colour
		self.skbc = "#808000"
		# Skip button text colour
		self.skbtc = "#000000"
		# Trough colour for volume control
		self.tc = "#505050"
		# View/edit queue button colour
		self.qc = "#0000FF"
		# Text font
		self.font = "Arial"
		# Font size for media control buttons
		self.mcfsize = 44
		# Font size for player name
		self.pnsize = 14
		# Font size for volume
		self.vfsize = 14
		# Font size for editing a player's queue
		self.eqsize = 14
		# Font size for tracks in the queue list
		self.qlsize = 14
		# Font size for adding a track to the queue
		self.atsize = 14
		# Minimum amplification for volume control
		self.minDB = -60
		# Maximum amplification for volume control
		self.maxDB = 0
		# Path of the currently active settings file
		self.settings = "./default.sbs"
		# Initialize all components
		# Create control window
		self.window = tk.Tk()
		L.window = self.window
		self.window.title("PB")
		# ToDo: implement functionality to switch themes - but not using ttk widgets if possible
		self.window["bg"] = self.bgc
		self.window.rowconfigure(2, weight=1)
		self.window.columnconfigure(0, weight=1)
		# List with all UI elements
		self.uiElements = []
		# List with the grid parameters of all UI elements
		self.uiGridParams = []
		
		
		# Create label for version number
		self.vLabel = tk.Label(master=self.window, text="PB by Lukas Freudenberg v0.1", bg=self.bgc, fg=self.fgc)
		self.uiElements.append(self.vLabel)
		self.uiGridParams.append([0, 0, 1, 1, "NESW"])
		# Create frame for genaral controls
		self.controlFrame = tk.Frame(master=self.window, bg=self.bgc)
		self.uiElements.append(self.controlFrame)
		self.uiGridParams.append([1, 0, 1, 1, "NESW"])
		self.controlFrame.columnconfigure(2, weight=1)
		# Create button for loading settings
		self.loadButton = tk.Button(master=self.controlFrame, text=u"\U0001F4C2", font=(self.font, self.mcfsize))
		self.uiElements.append(self.loadButton)
		self.uiGridParams.append([0, 0, 1, 1, "NESW"])
		self.loadButton.bind("<Button-1>", lambda event: self.loadSettings(settings=None))
		# Create button for saving settings
		self.saveButton = tk.Button(master=self.controlFrame, text=u"\U0001F4BE", font=(self.font, self.mcfsize))
		self.uiElements.append(self.saveButton)
		self.uiGridParams.append([0, 1, 1, 1, "NESW"])
		self.saveButton.bind("<Button-1>", lambda event: self.saveSettings())
		# Create general stop button
		self.stopButton = tk.Button(master=self.controlFrame, text=u"\U000023F9", fg=self.sbtc, bg=self.sbc, font=(self.font, self.mcfsize))
		self.uiElements.append(self.stopButton)
		self.uiGridParams.append([0, 2, 1, 1, "NESW"])
		self.stopButton.bind("<Button-1>", self.stopAll)
		
		# Create tabsystem for the different scenes
		#self.scenes = ttk.Notebook(self.window, background=self.bgc)
		self.scenes = ttk.Notebook(self.window)
		self.uiElements.append(self.scenes)
		self.uiGridParams.append([2, 0, 1, 1, "NESW"])
		
		# List with all players grouped by scene
		self.players = [[]]
		
		# Create frame for the default scene
		#self.scene1 = tk.Frame(master=self.scenes, bg=self.bgc)
		#self.scenes.add(self.scene1, text='Scene 1')
		#self.scene1.columnconfigure(0, weight=1)
		
		#self.addScene()
		
		# Index of currently active scene
		#self.activeScene = 0
		
		# Create frame for the "add a player button"
		#self.scene1addPlayerFrame = tk.Frame(master=self.scene1, width=100, height=100, bg=self.bgc, grid_propagate=False)
		#self.scene1addPlayerFrame = tk.Frame(master=self.scene1, height=40, bg=self.bgc)
		#self.uiElements.append(self.scene1addPlayerFrame)
		#self.uiGridParams.append([0, 0, 1, 1, "NESW"])
		#self.scene1addPlayerFrame.columnconfigure(0, weight=1)
		#self.scene1addPlayerFrame.rowconfigure(0, weight=1)
		#self.scene1addPlayerFrame.grid_propagate(False)
		
		
		
		# Create frame for the adding a new scene
		self.newScene = tk.Frame(master=self.scenes, bg=self.bgc)
		self.scenes.add(self.newScene, text='+')
		self.newScene.rowconfigure(0, weight=1)
		self.newScene.columnconfigure(0, weight=1)
		self.scenes.bind("<<NotebookTabChanged>>", lambda event: self.addScene())
		
		# Load default settings
		self.loadSettings()
		
		# Create default scene (this will be replaced by loading the settings)
		#self.addScene()
		# This doesn't do what I want - clicking on the tab is what should trigger the event. Maybe I can do this by adding a callback to the frame being on screen or the tab being selected.
		
		# Display the widgets
		L.buildUI(self.uiElements, self.uiGridParams)
		# Maximize the window
		self.window.attributes("-zoomed", True)
		# Add event for closing the window
		self.window.protocol("WM_DELETE_WINDOW", self.quit)
		
		#L.pln(self.scene1.winfo_children())
		
		# Execute mainloop of the window
		self.window.mainloop()
	
	# Get a list of all players (should be deprecated)
	def allPlayers(self):
		players = []
		for scene in self.players:
			for player in scene:
				players.append(player)
		return self.players
	
	# Stop all players
	def stopAll(self, event=None):
		for scene in self.players:
			for player in scene:
				player.stop()
	
	# Callback for quitting the program
	def quit(self, event=None):
		for scene in self.players:
			for player in scene:
				player.terminate()
		time.sleep(0.5)
		L.pln(threading.enumerate())
		self.window.destroy()
	
	# Removes a player and all its widgets.
	# 
	# @param player The player to be removed.
	# @param frame The player's control frame.
	# @param scene The scene that the players control frame lives in.
	def removePlayer(self, player, frame, scene, event=None):
		# Get scene index
		sceneNum = self.scenes.index(scene)
		# Get the index of the player in the scene
		playerIndex = self.players[sceneNum].index(player)
		# Terminate and remove the player
		player.terminate()
		self.players[sceneNum].remove(player)
		# Remove the player's widgets
		L.removeUI(frame, [(self.uiElements, self.uiGridParams)])
		# Rearrange the widgets of subsequent players
		pass
	
	# Edits the displayed name of a player
	# 
	# @param label the player's label
	def editPlayerName(self, label, event=None):
		newName = tk.simpledialog.askstring("Rename player", "Enter new name for " + label.cget("text") + ":")
		label.config(text=newName)
	
	# Starts a player (from the beginning of the current track - or should it be queue?).
	# 
	# @param player The player to start.
	# @param pauseButton The players pause button.
	# @param stopButton The players stop button.
	def play(self, player, pauseButton, event=None):
		# Go back to the start of the player
		player.stop()
		# Start the player
		player.play()
		# Enable pause and stop button
		pauseButton.config(state="normal")
		# Configure callback to update the button when the queue finishes
		player.setCallbackQueue(self.stop, [player, pauseButton])
	
	# Pauses/unpauses a player.
	# 
	# @param player The player to pause.
	# @param button The players pause button.
	def playPause(self, player, button, event=None):
		# If the button is disabled, this callback shouldn't be executed.
		if button.cget("state") == "disabled":
			return
		player.playPause()
	
	# Skips to the next track of a player.
	# 
	# @param player The player to skip the current track for.
	def skip(self, player, event=None):
		player.nextTrack()
	
	# Starts/pauses a player.
	# Do I want this? Or should it be more like a Soundboard and there be a separate pause button?
	# 
	# @param player the player to start/pause
	# @param button the players play/pause button
	#def play(self, player, button, event=None):
	#	player.playPause()
	#	if player.playing:
	#		button.config(text=u"\U000023F8")
	#		# Configure callback to update the button when the queue finishes
	#		player.setCallbackQueue(self.stop, [player, button])
	#	else:
	#		button.config(text=u"\U000023F5")
	
	# Stops a player
	# 
	# @param player the player to stop
	# @param button the players play/pause button
	def stop(self, player, pauseButton, event=None):
		player.stop()
		pauseButton.config(state="disabled")
	
	# Updates the volume of a player
	# 
	# @param player the player to adjust the volume of
	def updateVolume(self, player, volumeControl, event=None):
		# Get aplification
		dB = volumeControl.get()
		# Check if the player should be muted
		if dB == self.minDB:
			player.setVolume(0)
		else:
			player.setVolumeDB(dB)
	
	# Queues a track
	# 
	# @param player The player to add the track to.
	# @param button The players button for adding a track (if applicable).
	def addTrack(self, player, button=None, event=None):
		# Get parent frame
		frame = button.master
		# Open file dialogue
		path = tk.filedialog.askopenfilename(master=frame)
		# Get the name of the track
		name = L.fileNameFromPath(path)
		# Add label for this track
		label = tk.Label(frame, bg=self.bgc, fg=self.fgc, text="loading track...", font=(self.font, self.qlsize), anchor="w")
		label.grid(row=len(player.sources), column=0, sticky="NESW")
		frame.update_idletasks()
		# Queue track
		success = player.queue(path)
		# Change label to reflect loading completion
		if success:
			label.config(text=name)
		else:
			label.destroy()
		# Move button for adding a  (if applicable)
		if not button == None:
			button.grid(row=len(player.sources), column=0, sticky="NESW")
		# Update the window to accomodate bigger size - this should happen automatically, unless the user has resized the window
		#window.update()
	
	# Edits the queue of a player.
	# 
	# @param player The player for which to edit the queue.
	# @param name The player's name as displayed on it's label
	# @param button the player's edit queue button
	def editQueue(self, player, name, button, event=None):
		# Disable calling button
		#button.config(state="disabled")
		#time.sleep(1)
		#self.window.update_idletasks()
		#time.sleep(1)
		# Create window for queue
		editWindow = tk.Toplevel(self.window)
		editWindow.title(name + " queue")
		# ToDo: implement functionality to switch themes - but not using ttk widgets if possible
		editWindow["bg"] = self.bgc
		editWindow.columnconfigure(0, weight=1)
		# Create scrollable canvas
		canvas = tk.Canvas(editWindow, bg=self.bgc)
		canvas.columnconfigure(0, weight=1)
		canvas.grid(row=0, column=0, sticky="NESW")
		# Create frame for displaying and adding tracks
		tracks = tk.Frame(canvas, bg=self.bgc)
		tracks.columnconfigure(0, weight=1)
		tracks.grid(row=0, column=0, sticky="NESW")
		# Create scrollbar
		scroller = tk.Scrollbar(canvas, width=50)
		scroller.grid(row=0, column=1, sticky="NESW")
		canvas.config(yscrollcommand=scroller.set)
		#HERE scrolling
		#canvas.configure(scrollregion=canvas.bbox('all'))
		
		# Wait for window to open, then grab set
		#time.sleep(1)
		#editWindow.grab_set()
		# Show current tracks
		for i in range(len(player.sources)):
			name = L.fileNameFromPath(player.sources[i])
			bgc = self.bgc
			fgc = self.fgc
			# Highlight the current track
			if i == player.queuePos:
				bgc = self.hbgc
				fgc = self.hfgc
			label = tk.Label(tracks, bg=bgc, fg=fgc, text=name, font=(self.font, self.qlsize), anchor="w")
			label.grid(row=i, column=0, sticky="NESW")
		# Create button to add a track
		addTrackButton = tk.Button(tracks, text="+", bg=self.pbc, fg=self.pbtc, font=(self.font, self.atsize))
		addTrackButton.bind("<Button-1>", lambda event: self.addTrack(player, addTrackButton))
		addTrackButton.grid(row=len(player.sources), column=0, sticky="NESW")
		# Resize window to be wider if no tracks are queued yet
		#editWindow.update()
		L.pln(editWindow.winfo_reqwidth())
		#editWindow.geometry("200x50")
		#self.window.wait_window(editWindow)
	
	# Creates a new player in a scene and all its controls.
	# 
	# @param scene The scene to add the player to.
	# @param addPlayerButton The scenes button to add a player.
	# @return The newly created player.
	def addPlayer(self, scene, name=None, event=None):
		# Get scene index
		sceneNum = self.scenes.index(scene)
		# Get the scrollable canvas
		canvas = None
		for child in scene.winfo_children():
			if isinstance(child, tk.Canvas):
				canvas = child
		# Get the scroll frame
		scrollFrame = canvas.winfo_children()[0]
		# Get the add player button
		addPlayerButton = None
		#for child in canvas.winfo_children():
		for child in scrollFrame.winfo_children():
			if isinstance(child, tk.Button) and child.cget("text") == "+":
				addPlayerButton = child
		# Create the player
		player = LFAudio.Player()
		# Get index of the new player in the scene
		playerIndex = len(self.players[sceneNum])
		# Add the player to the global player list
		self.players[sceneNum].append(player)
		# Create frame for the player
		#playerFrame = tk.Frame(master=scene, bg=self.bgc)
		#playerFrame = tk.Frame(master=canvas, bg=self.bgc)
		playerFrame = tk.Frame(master=scrollFrame, bg=self.bgc)
		# Maybe this is bad - there should be no need to rebuild the UI and this leads to difficulties when moving players around
		self.uiElements.append(playerFrame)
		self.uiGridParams.append([playerIndex, 0, 1, 1, "NESW"])
		playerFrame.grid(row=playerIndex, column=0, sticky="NESW")
		playerFrame.columnconfigure(3, weight=1)
		# Create button to remove the player
		removeButton = tk.Button(master=playerFrame, text=u"\U00002716", bg=self.sbc, fg=self.sbtc, font=(self.font, self.pnsize))
		self.uiElements.append(removeButton)
		self.uiGridParams.append([0, 0, 1, 1, "WE"])
		removeButton.bind("<Button-1>", lambda event: self.removePlayer(player, playerFrame, scene))
		removeButton.grid(row=0, column=0, sticky="NESW")
		# Create player label
		if name == None:
			name = "player " + str(playerIndex + 1)
		playerLabel = tk.Label(master=playerFrame, bg=self.bgc, fg=self.fgc, text=name, font=(self.font, self.pnsize), anchor="w")
		self.uiElements.append(playerLabel)
		self.uiGridParams.append([0, 1, 1, 3, "NESW"])
		playerLabel.bind("<Button-1>", lambda event: self.editPlayerName(playerLabel))
		playerLabel.grid(row=0, column=1, columnspan=3, sticky="NESW")
		# Create button to start the player (from the beginning)
		playButton = tk.Button(master=playerFrame, text=u"\U000023F5", fg=self.pbtc, bg=self.pbc, font=(self.font, self.mcfsize))
		self.uiElements.append(playButton)
		self.uiGridParams.append([1, 0, 1, 1, "NESW"])
		playButton.grid(row=1, column=0, sticky="NESW")
		# Create button to pause/unpause the player
		pauseButton = tk.Button(master=playerFrame, text=u"\U000023EF", fg=self.pubtc, bg=self.pubc, font=(self.font, self.mcfsize), state="disabled")
		self.uiElements.append(pauseButton)
		self.uiGridParams.append([1, 1, 1, 1, "NESW"])
		pauseButton.bind("<Button-1>", lambda event: self.playPause(player, pauseButton))
		pauseButton.grid(row=1, column=1, sticky="NESW")
		# Bind event for starting the player
		playButton.bind("<Button-1>", lambda event: self.play(player, pauseButton))
		# Create button to go to the next track
		skipButton = tk.Button(master=playerFrame, text=u"\U000023ED", fg=self.skbtc, bg=self.skbc, font=(self.font, self.mcfsize))
		self.uiElements.append(skipButton)
		self.uiGridParams.append([1, 2, 1, 1, "WE"])
		skipButton.bind("<Button-1>", lambda event: self.skip(player))
		skipButton.grid(row=1, column=2, sticky="NESW")
		# Create slider for volume control
		# Update window to get correct size for the scale
		self.window.update_idletasks()
		volumeControl = tk.Scale(master=playerFrame, from_=self.minDB, to=self.maxDB, orient="horizontal", resolution=0.1, width=playButton.winfo_height(), sliderlength=playButton.winfo_height()/2, bg=self.bgc, fg=self.fgc, troughcolor=self.tc, font=(self.font, self.vfsize), showvalue=False)#command=lambda event: self.updateVolume(player, volumeControl)
		volumeControl.set(0)
		self.uiElements.append(volumeControl)
		self.uiGridParams.append([1, 3, 1, 1, "NESW"])
		#volumeControl.bind("<ButtonRelease-1>", lambda event: self.updateVolume(player))
		volumeControl.bind("<B1-Motion>", lambda event: self.updateVolume(player, volumeControl))
		volumeControl.grid(row=1, column=3, sticky="NESW")
		# Create button to edit the player's queue
		editQueueButton = tk.Button(master=playerFrame, text="view/edit queue", fg=self.fgc, bg=self.qc, font=(self.font, self.eqsize))
		self.uiElements.append(editQueueButton)
		self.uiGridParams.append([2, 0, 1, 4, "NESW"])
		editQueueButton.bind("<Button-1>", lambda event: self.editQueue(player, playerLabel.cget("text"), editQueueButton))
		editQueueButton.grid(row=2, column=0, columnspan=4, sticky="NESW")
		# Create separator between this player and next element 
		sepLabel = tk.Label(master=playerFrame, bg=self.bgc)
		self.uiElements.append(sepLabel)
		self.uiGridParams.append([3, 0, 1, 4, "NESW"])
		sepLabel.grid(row=3, column=0, columnspan=4, sticky="NESW")
		# Move button to add a new player
		self.uiGridParams[self.uiElements.index(addPlayerButton)] = [playerIndex+1, 0, 1, 1, "NESW"]
		addPlayerButton.grid(row=playerIndex+1, column=0, sticky="NESW")
		# Return player object
		return player
	
	# Updates the scroll frame of a scene to match the size of the canvas.
	# 
	# @param canvas The canvas, that the frame lives in.
	# @param frameID ID of the frame window.
	def updateFrame(self, canvas, frameID, event=None):
		canvas.itemconfig(frameID, width=canvas.winfo_width())
	
	# Scrolls the scene with the mouse wheel.
	# 
	# @param canvas The canvas to scroll.
	def scrollMouse(self, canvas, event=None):
		canvas.yview_scroll(int(-1*(event.delta/120)), "units")
		L.pln(canvas.winfo_master())
	
	# Creates a new scene in place of the "add scene" tab.
	# 
	# @param name Scene title in the tabsystem. By default, it is "Scene X" with X denoting the number of the scene
	def addScene(self, name=None, event=None):
		# Get selected tab
		scene = self.scenes.nametowidget(self.scenes.select())
		# Check if selected tab is the one for adding a scene
		if not scene == self.newScene:
			return
		L.pln("adding scene")
		# Get scene number
		sceneNum = self.scenes.index(scene)
		# If no name is given, the new scene will be given an iterative name
		if name == None:
			name = "Scene " + str(sceneNum + 1)
		self.scenes.tab(scene, text=name)
		# Add scene to list of all players
		self.players.append([])
		# Create scrollable canvas
		canvas = tk.Canvas(scene, bg=self.bgc)
		canvas.grid(row=0, column=0, sticky="NESW")
		# Create scrollbar
		scroller = tk.Scrollbar(scene, width=50, command=canvas.yview)
		scroller.grid(row=0, column=1, sticky="NESW")
		canvas.config(yscrollcommand=scroller.set)
		# Create window to scroll inside the canvas
		scrollFrame = tk.Frame(canvas, bg=self.bgc)
		scrollFrame.columnconfigure(0, weight=1)
		scrollFrameID = canvas.create_window((0, 0), window=scrollFrame, anchor="nw")
		# Update scroll area automatically
		scrollFrame.bind("<Configure>", lambda event: canvas.config(scrollregion=canvas.bbox("all")))
		canvas.bind("<Configure>", lambda event: self.updateFrame(canvas, scrollFrameID))
		# Set up scrolling binds
		# Mouse wheel scrolling
		canvas.bind_all("<MouseWheel>", lambda event: self.scrollMouse(canvas))
		# Arrow key scrolling
		canvas.bind_all("<Up>", lambda event: canvas.yview_scroll(-1, 'units'))
		canvas.bind_all("<Down>", lambda event: canvas.yview_scroll(1, "units"))
		# Touchpad scrolling (only works on Linux)
		self.window.bind('<Button-4>', lambda event: canvas.yview_scroll(-1, 'units'))
		self.window.bind('<Button-5>', lambda event: canvas.yview_scroll(1, 'units'))
        
		# Create button to add a player
		addPlayerButton = tk.Button(master=scrollFrame, text=u"\U0000002B", bg=self.pbc, fg=self.pbtc, font=(self.font, self.mcfsize))
		self.uiElements.append(addPlayerButton)
		self.uiGridParams.append([0, 0, 1, 1, "NESW"])
		addPlayerButton.grid(row=0, column=0, sticky="NESW")
		addPlayerButton.bind("<Button-1>", lambda event: self.addPlayer(scene))
		# Create new "add scene" tab
		newScene = tk.Frame(master=self.scenes, bg=self.bgc)
		self.scenes.add(newScene, text="+")
		newScene.rowconfigure(0, weight=1)
		newScene.columnconfigure(0, weight=1)
		self.newScene = newScene
	
	# Saves the current settings.
	def saveSettings(self, event=None):
		# Choose file path to save settings with the current save file as the given name
		settings = tk.filedialog.asksaveasfile(
			initialfile=L.fileNameFromPath(self.settings),
			filetypes=[("Soundboard Settings files", "*.sbs")]
		)
		# Check whether a file was selected
		if settings == None:
			L.pln("No save path selected.")
			return
		# Update path for current settings file
		self.settings = settings.name
		# Save settings
		# Get active scene
		activeScene = self.scenes.index(self.scenes.select())
		# Write active scene
		settings.writelines(["activeScene=", str(activeScene), "\n"])
		# Get and write all scenes
		for scene in self.scenes.tabs():
			# Get scene index
			sceneNum = self.scenes.index(scene)
			# Get scene frame
			#scene = self.scenes.tab(scene)
			# Get scene name
			#name = scene["text"]
			name = self.scenes.tab(scene)["text"]
			# Skip the "scene" for adding new scenes
			if name == "+":
				continue
			# Write scene name
			settings.writelines(["scene=", name, "\n"])
			# Get the scrollable canvas
			canvas = None
			for child in self.scenes.nametowidget(scene).winfo_children():
				if isinstance(child, tk.Canvas):
					canvas = child
			# Get the scroll frame
			scrollFrame = canvas.winfo_children()[0]
			# Get all player frames - the first widget is the add player button
			frames = scrollFrame.winfo_children()[1:]
			#frames = self.scenes.nametowidget(scene).winfo_children()
			#L.pln("Frames: ", frames)
			# Get and write all player data
			for i in range(len(self.players[sceneNum])):
				# Get player
				player = self.players[sceneNum][i]
				# Get player label - should be the second widget here
				label = frames[i].winfo_children()[1]
				# Get player name
				name = label.cget("text")
				# Write player line
				settings.writelines(["\tplayer=", name, "\n"])
				# Get and write player details
				# Write player volume
				settings.writelines(["\t\tvolume=", str(20*math.log(player.volume, 10)), "\n"])
				# Write queue looping
				settings.writelines(["\t\tqueueLoops=", str(player.queueLoops), "\n"])
				# Write individual track data
				for i in range(len(player.sources)):
					# Write track source
					settings.writelines(["\t\tsource=", player.sources[i], "\n"])
					# Write track looping
					settings.writelines(["\t\tloops=", str(player.loops[i]), "\n"])
				
		settings.close()
	
	# Loads the settings and scenes from a file.
	# The user can select a file or the default settings will be used.
	# Example for a settings file:
	#	# This line is a comment and will be ignored when loading the file.
	#	
	#	scene=Scene title
	#		player=Player title
	#			# Player volume in dB
	#			volume=-10
	#			# Qeue looping behavior
	#			queueLoops=0
	#			# An audio source
	#			source=/home/username/Desktop/Music.mp3
	#			# Amount of loops for the previous audio source
	#			loops=2
	#			# Another audio source
	#			source=/home/username/Desktop/MoreMusic.mp3
	#	
	#	scene=Empty scene
	# This file would produce two scenes: One with the title "Scene title"
	# and a player titled "Player title", that has the files
	# "/home/username/Desktop/Music.mp3" and "/home/username/Desktop/MoreMusic.mp3"
	# in its queue (with the first one being played twice,
	# the whole queue looping infinitely and a volume of -10dB);
	# the other an empty scene with the title "Empty Scene".
	# 
	# 
	# @param settings The path to the settings file. By default, the file for the default settings will be used.
	def loadSettings(self, event=None, settings="./default.sbs"):
		# Check whether to load default settings
		if settings == "./default.sbs":
			# Check if default settings exist; if not, create it
			if not os.path.exists(settings):
				L.pln("Default settings don't exist.")
				default = open(settings, "w")
				default.writelines([
					"# This is a comment and will be ignored when loading the settings file.\n",
					"\n",
					"# Index of active scene after loading settings.\n",
					"activeScene=0\n",
					"\n",
					"# Default empty scene.\n",
					"scene=Scene 1\n"
				])
				default.close()
		# Check if a path was provided
		elif settings == None:
			settings = tk.filedialog.askopenfilename(filetypes=[("Soundboard Settings files", "*.sbs")])
			# If no settings file was selected, don't load any
			if settings == ():
				L.pln("No settings file selected.")
				return
		else:
			# Check for correct data format
			if not isinstance(settings, str):
				L.pln("Path for settings file must be a string.")
				return
			# Check if path exists
			if not os.path.exists(settings):
				L.pln("Settings file: \"", settings, "\" doesn't exist.")
				return
		# Set the path for the current settings file
		self.settings = settings
		# Open the settings file
		settings = open(settings, "r")
		# Load settings
		# Remove all current players and widgets (except the "new scene" tab)
		for scene in self.scenes.tabs():
			# Get Scene widget
			scene = self.scenes.nametowidget(scene)
			if scene == self.newScene:
				continue
			# Get scene index
			sceneNum = self.scenes.index(scene)
			# Get players
			players = self.players[sceneNum]
			# Remove all players
			for player in players:
				player.terminate()
				players.remove(player)
			self.players.pop(sceneNum)
			# Remove all widgets
			L.removeUI(scene, [(self.uiElements, self.uiGridParams)])
		# Current scene
		scene = None
		# Current player
		player = None
		# Current player's volume control slider
		volumeSlider = None
		# Index of active scene after loading
		activeScene = None
		for line in settings.readlines():
			# Ignore the line if it is a comment (first character being "#") or empty
			if line[0] == "#" or line[0] == "\n":
				continue
			# Check if line declares the active scene
			elif len(line) > 12 and line[:12] == "activeScene=":
				activeScene = line[12:-1]
				try:
					activeScene = int(activeScene)
					if activeScene < 0:
						activeScene = None
						L.pln("Value for activeScene must be a non-negative integer.")
				except ValueError:
					L.pln("Value for activeScene must be a non-negative integer.")
			# Check if line declares a scene
			elif len(line) > 6 and line[:6] == "scene=":
				self.scenes.select(len(self.scenes.winfo_children()) - 1)
				scene = self.scenes.nametowidget(self.scenes.select())
				self.addScene(name=line[6:-1])
			# Check if line declares a player
			elif len(line) > 8 and line[:8] == "\tplayer=":
				# Create the player
				player = self.addPlayer(scene, name=line[8:-1])
				# Update the player's volume slider
				# Get the scrollable canvas
				canvas = None
				for child in scene.winfo_children():
					if isinstance(child, tk.Canvas):
						canvas = child
				# Get the scroll frame
				scrollFrame = canvas.winfo_children()[0]
				# Get the player frame
				playerFrame = None
				#for child in canvas.winfo_children():
				for child in scrollFrame.winfo_children():
					if isinstance(child, tk.Frame):
						playerFrame = child
				# Get the volume slider
				for child in playerFrame.winfo_children():
					if isinstance(child, tk.Scale):
						volumeSlider = child
			# Check if line declares player volume
			elif len(line) > 9 and line[:9] == "\t\tvolume=":
				volume = line[9:-1]
				try:
					volume = float(volume)
					player.setVolumeDB(volume)
					# Set the player's volume slider to match the value
					volumeSlider.set(volume)
				except ValueError:
					L.pln("Value for volume must be a number.")
			# Check if line declares loops for the player's queue
			elif len(line) > 13 and line[:13] == "\t\tqueueLoops=":
				loops = line[13:-1]
				try:
					loops = int(loops)
					player.loopQueue(loops=loops)
				except ValueError:
					L.pln("Value for loops must be an integer.")
			# Check if line declares an audio source
			elif len(line) > 9 and line[:9] == "\t\tsource=":
				player.queue(line[9:-1])
			# Check if line declares loops for a track
			elif len(line) > 8 and line[:8] == "\t\tloops=":
				loops = line[8:-1]
				try:
					loops = int(loops)
					player.loopTrack(track=len(player.sources)-1, loops=loops)
				except ValueError:
					L.pln("Value for loops must be an integer.")
		# Change to active scene
		if not activeScene == None and not activeScene >= len(self.scenes.winfo_children()):
			self.scenes.select(activeScene)
		# Close settings file
		settings.close()

# Initialize the gui
gui = LSB()
