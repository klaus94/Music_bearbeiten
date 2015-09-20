#!/ usr/binenv python
# -*- coding: iso-8859-1 -*-

from Tkinter import *
import tkMessageBox
import sys
import os
from mutagen.id3 import ID3, TRCK, TIT2, TPE1, TALB, TDRC, TCON, COMM, APIC

#########################################
############### FUNCTIONS ###############


def extractTitleAndArtist(fileName):
	try:
		name = fileName.replace("_"," ")			
		content = name.split(" - ")			
		artist = content[0]					
		artist.replace(" _ ", "")		
		title = content[1][0:(len(content[1]) - 4)]		#.mp3 abhaengen
		title.replace(" _ ","")
	except:
		name = fileName.replace("_"," ")
		title = name.strip(".mp3")
		artist = ""

	return [artist, title]


def makeScreenshot():
	#mp4 loeschen
	os.system('find . -name "*.mp4" -exec rm -rf {} \;')


	fn = list1.get(ACTIVE)
	if (len(sys.argv) > 1):
		fpath = sys.argv[1]
	else:
		fpath = os.path.abspath(os.path.dirname(sys.argv[0]))

	fname = os.path.join(fpath, fn)
	
	title = entry_title.get()
	artist = entry_artist.get()
	os.system("gnome-screenshot --file=screenshot.png -a")
	os.system("sleep 1")

	audio = ID3(fname)
	audio.add(TIT2(encoding=3, text=title))			# title
	audio.add(TPE1(encoding=3, text=artist))		# artist
	# test
	audio.add(TCON(encoding=3, text=chosenGenre.get() ))			# genre
	audio.add(TDRC(encoding=3, text=chosenYear.get() ))				# year
		
	audio.add(
		APIC(										# cover
			encoding=3, # 3 is for utf-8
			mime='image/png', # image/jpeg or image/png
			type=3, # 3 is for the cover image
			desc=u'Cover (front)',
			data=open('screenshot.png').read()
		)
	)
	audio.save()
	
	sendTitle = fn.replace(" ", "\ ").replace("(", "\(").replace(")", "\)")#.replace("&", "\&")
	fname = os.path.join(fpath, sendTitle)
	#test
	fname.replace(" ", "\ ").replace("(", "\(").replace(")", "\)").replace("_","\ ")
	#tkMessageBox.showinfo("Info", "fname: %s"%(fname))
	os.system("mv " + fname + " /home/dominik/Musik")

	
	
	if (artist != ""):
		newTitle = artist + " - " + title + ".mp3"
	else:
		newTitle = title + ".mp3"
	newTitle = newTitle.replace(" ", "\ ").replace("(", "\(").replace(")", "\)").replace("_","\ ")

	if sendTitle != newTitle:
		os.system("mv /home/dominik/Musik/" + sendTitle + " /home/dominik/Musik/" + newTitle)

	

	
	#screenshot loeschen
	os.system("rm screenshot.png")
	list1.delete(list1.index(ACTIVE))

	if (list1.size() == 0):
		root.destroy()


def setEntry(event):
	artist, title = extractTitleAndArtist(list1.get(ACTIVE))
	entry_title.delete(0, END)
	entry_artist.delete(0, END)
	entry_title.insert(0, title)
	entry_artist.insert(0, artist)

def presetEntry():
	artist, title = extractTitleAndArtist(list1.get(ACTIVE))
	entry_title.insert(0, title)
	entry_artist.insert(0, artist)
	


####################################
####################################
################ INIT ##############
####################################

musicList = {}

if (len(sys.argv) > 1):
	fpath = sys.argv[1]
else:
	fpath = os.path.abspath(os.path.dirname(sys.argv[0]))	#print os.listdir(fpath)

index = 0
for fn in os.listdir(fpath):				# z.B.: fn: Darude - Sandstorm.mp3
	fname = os.path.join(fpath, fn)			# z.B.: fname: /home/dominik/Dokumente/Programmieren/Python/Anwendungen/Music_bearbeiten/Darude - Sandstorm.mp3 
	if fname.lower().endswith('.mp3'):
		musicList[index] = fn
		index += 1

######################################
########### GUI ######################


if (len(musicList) == 0):
	tkMessageBox.showinfo("Info", "Im Ordner: %s ist keine mp3-Datei"%(fpath))
else:
	HEIGHT = 400
	WIDTH = 320

	root = Tk()
	root.geometry(str(WIDTH) + "x" + str(HEIGHT) + "+1050+200")
	root.title("Bilder-Macher")

	label_info = Label(root, text="Achtung! Titel zum Auswaehlen doppelt klicken").pack()

	frame1 = Frame(root, width = WIDTH, height = HEIGHT / 2)

	# Vorbereitung Komponenten:
	chosenGenre = StringVar(root)
	chosenGenre.set("Drum & Bass")			# default value
	chosenYear = StringVar(root)
	chosenYear.set("2015")

	# Komponenten:
	list1 = Listbox(frame1, selectmode = SINGLE, width=WIDTH / 10)
	label_title = Label(frame1, text="title: ")
	label_artist = Label(frame1, text="artist: ")
	entry_artist = Entry(frame1)
	entry_title = Entry(frame1)
	combobox_genre = OptionMenu(frame1, chosenGenre, "Drum & Bass", "Tech House", "Deep House")
	combobox_year = OptionMenu(frame1, chosenYear, "2015", "2014", "2013", "2012", "2011", "2010", "2009")


	# Bearbeitung der Komponenten:
	for item in musicList:
		list1.insert(END, musicList[item])

	list1.selection_set(0)				# erstes element wird aktiv gesetzt
	presetEntry()						# titel und autor des ersten titels ausgeben
	list1.bind("<Double-Button-1>", setEntry)

	#combobox_genre['values'] = ('Drum & Bass', 'Tech House', 'Deep House', 'Techno')

	# Komponenten in Grid packen:
	list1.grid(row = 0, column = 0, columnspan = 2, pady = 10)
	label_title.grid(row = 2, column = 0, padx = 10, pady = 10)
	label_artist.grid(row = 1, column = 0, padx = 10, pady = 10)
	entry_title.grid(row = 2, column = 1, padx = 5, pady = 10)
	entry_artist.grid(row = 1, column = 1, padx = 5, pady = 10)
	combobox_genre.grid(row = 3, column = 0, padx = 10, pady = 10)
	combobox_year.grid(row = 3, column = 1, padx = 10, pady = 10)


	frame1.pack()

	frame2 = Frame(root, width=WIDTH, height = HEIGHT / 2)
	makePhotoButton = Button(frame2, text="make photo!", command=makeScreenshot).grid(row=0, column=0, padx = 10, pady = 30)	
	#useUKF_Button = Button(frame2, text="use UKF-photo").grid(row=0, column=1, padx = 10, pady = 30)	#, command=...
	frame2.pack()

	root.mainloop()