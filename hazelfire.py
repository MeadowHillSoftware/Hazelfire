#!/usr/bin/env python3

# Hazelfire 0.1.1
# Copyright 2013 Meadow Hill Software
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Hazelfire is based on the yags rule system by Samuel Penn (http://yags.glendale.org.uk/).

# damage roll = (strength x 4) + weapon damage bonus + d20
# soak roll = soak + armor bonus + d20

# zombie strength = 3, player strength = irrelevant (3)
# zombie soak = 12, player soak = 12
# zombie body levels = 10, player body levels = 5
# human bite damage bonus = 0, Glock 17 damage bonus = 23
# zombie armor bonus = 0, player armor bonus = 0

# alive: 0 = dead, 1 = alive
# closed: 0 = open (call close method), 1 = closed (call close method), 2 = can't be opened (print generic string), "" = can't be opened (print this string)
# examine: 0 = call examine method, "" = print this string
# name: 0 = generic name, 1 = Proper Name, 2 = Nickname, "" = name in this area
# use: 0 = does nothing (print generic string), 1 = does something (call use method), "" = does nothing (print this string)
# locked: 0 = unlocked, 1 = locked, 2 = unlockable
# coordinates: {latitude: {longitude: ID}}

import random
import time

class Object:
	def __init__(self):
		self.closed = 2
		self.examine = ""
		self.location = []
		self.locked = 2
		self.name = {}
		self.use = 0

class Area(Object):
	def __init__(self):
		Object.__init__(self)
		self.coordinates = {}
		self.items = []

class Book(Object):
	def __init__(self):
		Object.__init__(self)
		self.cover = ""
		self.text = ""

	def utilize(self):
		if self.closed == 1:
			print("\nThe book is closed.")
		else:
			print("\nYou have nothing to write with.")

	def view(self):
		if self.closed == 0:
			print(self.text)
		else:
			print(self.cover)

class Clock(Object):
	def __init__(self):
		Object.__init__(self)
		self.time = "00:00"

	def utilize(self):
		time = input("Type a four digit number and press enter: ")
		if len(time) != 4 or time[0] > 2 or time[2] > 5:
			print("\nInvalid input.")
		else:
			time = time[0] + time[1] + ":" + time[2] + time[3]
			self.time = time
			correct = 0
			for location in locations:
				if objects[location].name[1] == "north room":
					for item in objects[location].items:
						if objects[item].name[0] == "clock":
							if objects[item].time == "00:00":
								correct += 1
				elif objects[location].name[1] == "east room":
					for item in objects[location].items:
						if objects[item].name[0] == "clock":
							if objects[item].time == "07:00":
								correct += 1
				elif objects[location].name[1] == "south room":
					for item in objects[location].items:
						if objects[item].name[0] == "clock":
							if objects[item].time == "12:00":
								correct += 1
				elif objects[location].name[1] == "west room":
					for item in objects[location].items:
						if objects[item].name[0] == "clock":
							if objects[item].time == "17:00":
								correct += 1
			if correct == 4:
				for location in locations:
					if objects[location].name[1] == "laboratory":
						for item in objects[location].items:
							if objects[item].name[0] == "ladder":
								objects[item].extended = 1
								print("\nYou hear a rattling sound in the lab.")

	def view(self):
		print("\nYou are looking at a digital clock with a keypad afixed to the wall. The clock is set to {0}.".format(self.time))

class Clothing(Object):
	def __init__(self):
		Object.__init__(self)
		self.slot = ""

class Ladder(Object):
	def __init__(self):
		Object.__init__(self)
		self.extended = 0

	def utilize(self):
		global youWin
		if self.extended == 0:
			print("\nThe ladder is retracted and is too high to reach.")
		else:
			print("\nYou climb to the roof of the laboratory where the chopper waits.")
			print("\nThe chopper takes you back to the safety of your base.")
			print("\n\n\n\nG A M E   O V E R")
			youWin = 1

	def view(self):
		if self.extended == 0:
			print("\nYou are looking at a large telescoping ladder attached to the wall near")
			print("the ceiling. The ladder is retracted and is too high too reach.")
		else:
			print("The ladder is extended, allowing access to the roof.")

class Lifeform(Object):
	def __init__(self):
		Object.__init__(self)
		self.alive = 1
		self.attackStrength = 0
		self.bodyLevels = 0
		self.items = {}
		self.naturalWeapon = {}
		self.soak = 7
		self.strength = 0
		self.wounds = 0

class Weapon(Object):
	def __init__(self):
		Object.__init__(self)
		self.damage = 0
		self.strength = 1
		self.strengthApplies = 1

	def utilize(self):
		print("\nWhy are you using the {0}? There's nothing to attack here.\nAre you attacking the darkness?".format(self.name[0]))

def attackRoll(weapons):
	attackDic = {}
	for weapon in weapons:
		attackNum = 1
		attackDic[weapon] = attackNum
	return attackDic

def characterCreation():
	global objects
	global party
	global activeCharacter
	item = "human"
	location = ""
	ID = createObject(item, location)
	strength = 3
	objects[ID].attackStrength = strength
	objects[ID].strength = strength
	bodyLevels = 5
	objects[ID].bodyLevels = bodyLevels
	objects[ID].examine = "\nYou are unremarkable."
	objects[ID].name[1] = "self"
	objects[ID].naturalWeapon["damage"] = 0
	soak = 12
	objects[ID].soak = soak
	objects[ID].use = "\nThat felt good."
	wounds = 0
	objects[ID].wounds = wounds
	item = "glock 17"
	key = createObject(item, ID)
	slot = "right hand"
	objects[ID].items[slot] = key
	party.append(ID)
	AC = ID
	activeCharacter = AC

def checkForEnemies(location):
	global enemies
	for ID in objects[location].items:
		if objects[ID].name[0] in lifeforms:
			if ID not in party:
				if objects[ID].alive == 1:
					enemies.append(ID)
	if enemies != []:
		print("\nYou are attacked.")
		combat()

def combat():
	target = ""
	initiative = initiativeRoll()
	order = sorted(initiative)
	global youLose
	global enemies
	global objects
	while True:
		dead = 0
		for member in party:
			if objects[member].alive == 0:
				dead += 1
		if dead == len(party):
			youLose = 1
			break
		if enemies == []:
			break
		for number in order:
			killed = []
			for attacker in initiative[number]:
				if attacker in party:
					attackerName = "You"
				else:
					attackerName = "The " + objects[attacker].name[0]
				#add target selection function later when there are > 2 combatants
				if attackerName == "You":
					defender = enemies[0]
				else:
					defender = party[0]
				if attacker in party:
					target = enemies[0]
				else:
					target = party[0]
				if defender in party:
					defenderName = "You"
				else:
					defenderName = "The " + objects[defender].name[0]
				weapons = getWeapons(attacker)
				attackDic = attackRoll(weapons)
				damageDic = damageRoll(attackDic, attacker)
				for weapon in damageDic.keys():
					strength = damageDic[weapon]["strength"]
					damage = damageDic[weapon]["damage"]
					for attack in damageDic[weapon]["rolls"].keys():
						roll = damageDic[weapon]["rolls"][attack]
						total = (strength * 4) + damage + roll
						if attacker in party:
							input("\nPress Enter to make your damage roll.")
							IA = indefiniteArticle(roll)
							print("\n{0} rolled {1} {2} for a total of {3} (({4} x 4) + {5} + {2} = {3})".format(attackerName, IA, roll, total, strength, damage))
						else:
							print("\n{0}'s damage roll is {1}.".format(attackerName, total))
						soak = soakRoll(target)
						net = total - soak
						wounds = determineWounds(net)
						objects[target].wounds += wounds
						plural = pluralizer(wounds)
						if target in party:
							verb = verbForm(defenderName)
							print("\n{0} {1} received {2} wound{3} from {4}.".format(defenderName, verb, wounds, plural, attackerName.lower()))
						else:
							verb = verbForm(attackerName)
							print("\n{0} {1} delivered {2} wound{3} to {4}.".format(attackerName, verb, wounds, plural, defenderName.lower()))
						if wounds > 0:
							description = woundLevel(target)
							if defenderName == "You":
								verb = "are"
							else:
								verb = "is"
							print("\n{0} {1} {2}.".format(defenderName, verb, description))
						if objects[target].wounds >= objects[target].bodyLevels:
							objects[target].alive = 0
							killed.append(target)
							if target in enemies:
								enemies.remove(target)
							verb = verbForm(attackerName)
							print("\n{0} {1} killed {2}.".format(attackerName, verb, defenderName.lower()))
			alive = []
			for number in order:
				for attacker in initiative[number]:
					if attacker not in killed:
						alive.append(attacker)
				initiative[number] = alive

def createObject(item, location):
	global objectCount
	global objects
	global locations
	if item in objectCount.keys():
		objectCount[item] += 1
	else:
		objectCount[item] = 1
	ID = item + " (" + str(objectCount[item]) + ")"
	if item == "book":
		objects[ID] = Book()
		objects[ID].examine = 0
	elif item == "clock":
		objects[ID] = Clock()
		objects[ID].examine = 0
	elif item == "door":
		objects[ID] = Area()
		objects[ID].closed = 1
	elif item == "ladder":
		objects[ID] = Ladder()
		objects[ID].examine = 0
		objects[ID].use = 1
	elif item in lifeforms:
		objects[ID] = Lifeform()
		objects[ID].use = 0
		if item == "zombie":
			objects[ID].attackStrength = 3
			objects[ID].bodyLevels = 10
			objects[ID].examine = "You are looking at a putrid rotting corpse."
			objects[ID].naturalWeapon["damage"] = 0
			objects[ID].strength = 3
			objects[ID].use = "That relieved some tension. The body was cold but, fortunately, stiff in the right places."
	elif item == "room":
		objects[ID] = Area()
		locations.append(ID)
	elif item in weapons:
		objects[ID] = Weapon()
		objects[ID].use = 1
		if item == "battle axe":
			objects[ID].damage = 10
			objects[ID].examine = "\nYou are looking at a battle axe."
			objects[ID].strength = 3
			objects[ID].strengthApplies = 1
		elif item == "broad sword":
			objects[ID].damage = 12
			objects[ID].examine = "\nYou are looking at a broad sword."
			objects[ID].strength = 3
			objects[ID].strengthApplies = 1
		elif item == "buckler":
			objects[ID].damage = 0
			objects[ID].examine = "\nYou are looking at a buckler."
			objects[ID].strength = 1
			objects[ID].strengthApplies = 1
		elif item == "club":
			objects[ID].damage = 5
			objects[ID].examine = "\nYou are looking at a club."
			objects[ID].strength = 2
			objects[ID].strengthApplies = 1
		elif item == "composite bow":
			objects[ID].damage = 11
			objects[ID].examine = "\nYou are looking at a composite bow."
			objects[ID].strength = 3
			objects[ID].strengthApplies = 1
		elif item == "dagger":
			objects[ID].damage = 4
			objects[ID].examine = "\nYou are looking at a dagger."
			objects[ID].strength = 1
			objects[ID].strengthApplies = 1
		elif item == "glock 17":
			objects[ID].damage = 23
			objects[ID].examine = "\nYou are looking at a semi-automatic pistol partially made of synthetic materials."
			objects[ID].strength = 2
			objects[ID].strengthApplies = 0
		elif item == "hand axe":
			objects[ID].damage = 5
			objects[ID].examine = "\nYou are looking at a hand axe."
			objects[ID].strength = 1
			objects[ID].strengthApplies = 1
		elif item == "hunting spear":
			objects[ID].damage = 7
			objects[ID].examine = "\nYou are looking at a hunting spear."
			objects[ID].strength = 2
			objects[ID].strengthApplies = 1
		elif item == "javelin":
			objects[ID].damage = 5
			objects[ID].examine = "\nYou are looking at a javelin."
			objects[ID].strength = 2
			objects[ID].strengthApplies = 1
		elif item == "knife":
			objects[ID].damage = 2
			objects[ID].examine = "\nYou are looking at a knife."
			objects[ID].strength = 1
			objects[ID].strengthApplies = 1
		elif item == "long bow":
			objects[ID].damage = 12
			objects[ID].examine = "\nYou are looking at a long bow."
			objects[ID].strength = 3
			objects[ID].strengthApplies = 1
		elif item == "long spear":
			objects[ID].damage = 11
			objects[ID].examine = "\nYou are looking at a long spear."
			objects[ID].strength = 5
			objects[ID].strengthApplies = 1
		elif item == "quarterstaff":
			objects[ID].damage = 8
			objects[ID].examine = "\nYou are looking at a quarterstaff."
			objects[ID].strength = 4
			objects[ID].strengthApplies = 1
		elif item == "round shield":
			objects[ID].damage = 0
			objects[ID].examine = "\nYou are looking at a round shield."
			objects[ID].strength = 2
			objects[ID].strengthApplies = 1
		elif item == "scramasax":
			objects[ID].damage = 7
			objects[ID].examine = "\nYou are looking at a scramasax."
			objects[ID].strength = 2
			objects[ID].strengthApplies = 1
		elif item == "short bow":
			objects[ID].damage = 5
			objects[ID].examine = "\nYou are looking at a short bow."
			objects[ID].strength = 3
			objects[ID].strengthApplies = 1
		elif item == "short sword":
			objects[ID].damage = 9
			objects[ID].examine = "\nYou are looking at a short sword."
			objects[ID].strength = 2
			objects[ID].strengthApplies = 1
		elif item == "sling":
			objects[ID].damage = 7
			objects[ID].examine = "\nYou are looking at a sling."
			objects[ID].strength = 2
			objects[ID].strengthApplies = 1
		elif item == "small shield":
			objects[ID].damage = 0
			objects[ID].examine = "\nYou are looking at a small shield."
			objects[ID].strength = 2
			objects[ID].strengthApplies = 1
		elif item == "throwing axe":
			objects[ID].damage = 4
			objects[ID].examine = "\nYou are looking at a throwing axe."
			objects[ID].strength = 2
			objects[ID].strengthApplies = 1
		elif item == "throwing knife":
			objects[ID].damage = 2
			objects[ID].examine = "\nYou are looking at a throwing knife."
			objects[ID].strength = 1
			objects[ID].strengthApplies = 1
		elif item == "war spear":
			objects[ID].damage = 11
			objects[ID].examine = "\nYou are looking at a war spear."
			objects[ID].strength = 3
			objects[ID].strengthApplies = 1
	else:
		objects[ID] = Object()
	objects[ID].name[0] = item
	objects[ID].name[1] = item
	objects[ID].name[2] = item
	if item != "room":
		objects[ID].location = [location]
	if location in locations:
		objects[location].items.append(ID)
	return ID

def damageRoll(attackDic, attacker):
	damageDic = {}
	for weapon in attackDic.keys():
		attack = 0
		while attack < attackDic[weapon]:
			if weapon == 0:
				strength = objects[attacker].attackStrength
				damage = objects[attacker].naturalWeapon["damage"]
			else:
				strengthApplies = objects[weapon].strengthApplies
				if strengthApplies == 1:
					strength = objects[attacker].attackStrength
				else:
					strength = 0
				damage = objects[weapon].damage
			roll = random.randint(1, 20)
			total = ((strength * 4) + damage + roll)
			damageDic[weapon] = {}
			damageDic[weapon]["strength"] = strength
			damageDic[weapon]["damage"] = damage
			damageDic[weapon]["rolls"] = {}
			damageDic[weapon]["rolls"][attack] = roll
			attack += 1
		return damageDic

def definiteArticle(ID, name):
	if objects[ID].name[0] == name:
		DA = "The "
	elif "door" in objects[ID].name[0]:
		DA = "The "
	else:
		DA = ""
	return DA

def determineWounds(net):
	if net > 0:
		wounds = 1
		net -= 1
		while net > 4:
			wounds += 1
			net -= 5
	else:
		wounds = 0
	return wounds

def getID(phrase):
	num = 2
	name = phrase[1]
	while num < len(phrase):
		name = name + " " + phrase[num]
		num += 1
	names = listObjects()
	print(name)
	print(names)
	if name not in names:
		print("\nThere is no such object.")
		ID = 0
		name = 0
	else:
		ID = ""
		IDs = listIDs()
		if name in IDs:
			ID = name
		else:
			for item in IDs:
				if objects[item].name[1] == name:
					ID = item
				elif "door" in objects[item].name[0]:
					location = objects[activeCharacter].location[0]
					if objects[item].name[location] == name:
						ID = item
	return name, ID

def getWeapons(attacker):
	holders = ["claw", "hand", "tentacle"]
	slots = objects[attacker].items.keys()
	wielded = []
	for holder in holders:
		for slot in slots:
			# determine if it's a weapon-wielding slot (e.g. "hand" is in the slot string)
			if holder in slot:
				# get generic name of item in attacker's slot and determine if it's a weapon
				item = objects[attacker].items[slot]
				if objects[item].name[0] in weapons:
					# add object's ID to wielded list
					wielded.append(item)
	if wielded == []:
		# if wielding no weapons add 0, signifying use of natural weapons
		wielded = [0]
	return wielded

def indefiniteArticle(roll):
	if roll in [8, 18]:
		IA = "an"
	else:
		IA = "a"
	return IA

def initiativeRoll():
	initiative = {}
	for member in party:
		total = 0
		if total in initiative.keys():
			initiative[total].append(member)
		else:
			initiative[total] = [member]
	for enemy in enemies:
		total = 0
		if total in initiative.keys():
			initiative[total].append(enemy)
		else:
			initiative[total] = [enemy]
	return initiative

def listIDs():
	items = []
	location = objects[activeCharacter].location[0]
	items.append(location)
	for ID in objects[location].items:
		items.append(ID)
	for key in objects[activeCharacter].items.keys():
		ID = objects[activeCharacter].items[key]
		items.append(ID)
	return items

def listObjects():
	items = listIDs()
	names = []
	for ID in items:
		if "door" in objects[ID].name[0]:
			location = objects[activeCharacter].location[0]
			names.append(objects[ID].name[location])
		else:
			names.append(objects[ID].name[1])
	names2 = []
	duplicates = []
	for name in names:
		if name not in names2:
			names2.append(name)
		else:
			duplicates.append(name)
	names = []
	for ID in items:
		if "door" in objects[ID].name[0]:
			location = objects[activeCharacter].location[0]
			names.append(objects[ID].name[location])
		else:
			names.append(objects[ID].name[1])
	return names

def parseAction(phrase = "0"):
	global objects
	if phrase == "0":
		while phrase[0] not in actions:
			phrase = input("\nType in your action and press Enter: ")
			if phrase == "":
				phrase = "0"
			phrase = phrase.lower().split()
	else:
		phrase = phrase.lower().split()
	if len(phrase) == 1:
		if phrase[0] == "actions":
			printActions()
		elif phrase[0] == "cheat":
			option = input("")
			if option in ["attribute", "location", "possession"]:
				subject = input("")
			if option == "attribute" and subject in lifeforms:
				attribute = input("")
				if attribute in ["strength"]:
					number = input("")
					number = int(number)
					if objects[subject].name[0] == "human":
						if number > 0 and number < 11:
							objects[subject].strength = number
					else:
						if number > -1 and number < 21:
							objects[subject].strength = number
			elif option == "enemy":
				location = input("")
				if location == "" or location in locations:
					newEnemy = input("")
					oldEnemy = input("")
					if location == "":
						areas = locations
					else:
						areas = [location]
					finished = 0
					for area in areas:
						if finished == 1:
							break
						for item in objects[area].items:
							if oldEnemy == "":
								if objects[item].name[0] in lifeforms:
									if item not in party:
										ID = replaceObject(area, item, newEnemy)
										objects[area].items.append(ID)
							elif item == oldEnemy:
								ID = replaceObject(area, item, newEnemy)
								objects[area].items.append(ID)
								finished = 1
								break
							elif objects[item].name[0] == oldEnemy:
								ID = replaceObject(area, item, newEnemy)
								objects[area].items.append(ID)
			elif option == "location":
				location = input("")
				if location in locations:
					if subject in party:
						for member in party:
							objects[member].location[0] = location
							objects[location].items.append(member)
					else:
						objects[subject].location[0] = location
						objects[location].items.append(subject)
			elif option == "possession":
				possession = input("")
				slot = input("")
				ID = createObject(possession, subject)
				if possession in weapons:
					if objects[subject].strength >= objects[ID].strength:
						objects[subject].items[slot] = ID
					else:
						del objects[ID]
				elif possession in clothing:
					if slot == objects[ID].slot:
						objects[subject].items[slot] = ID
					else:
						del objects[ID]
				else:
					objects[subject].items[slot] = ID
		elif phrase[0] in ["east", "west"]:
			location = objects[activeCharacter].location[0]
			latitude = objects[location].coordinates["x"]
			longitude = objects[location].coordinates["y"]
			if phrase[0] == "east":
				longitude += 1
			else:
				longitude -= 1
			newArea = coordinates[latitude][longitude]
			if "door" in objects[newArea].name[0]:
				if objects[newArea].closed == 1:
					print("\nA closed door is blocking your path.")
					if phrase[0] == "east":
						longitude -= 1
					else:
						longitude += 1
				else:
					if phrase[0] == "east":
						longitude += 1
					else:
						longitude -= 1
			newArea = coordinates[latitude][longitude]
			if newArea != location:
				for member in party:
					objects[location].items.remove(member)
					objects[member].location[0] = newArea
					objects[newArea].items.append(member)
				checkForEnemies(newArea)
				phrase = "examine " + newArea
				parseAction(phrase)
		elif phrase[0] in ["north", "south"]:
			location = objects[activeCharacter].location[0]
			latitude = objects[location].coordinates["x"]
			longitude = objects[location].coordinates["y"]
			if phrase[0] == "north":
				latitude += 1
			else:
				latitude -= 1
			newArea = coordinates[latitude][longitude]
			if "door" in objects[newArea].name[0]:
				if objects[newArea].closed == 1:
					print("\nA closed door is blocking your path.")
					if phrase[0] == "north":
						latitude -= 1
					else:
						latitude += 1
				else:
					if phrase[0] == "north":
						latitude += 1
					else:
						latitude -= 1
			newArea = coordinates[latitude][longitude]
			if newArea != location:
				for member in party:
					objects[location].items.remove(member)
					objects[member].location[0] = newArea
					objects[newArea].items.append(member)
				checkForEnemies(newArea)
				phrase = "examine " + newArea
				parseAction(phrase)
		elif phrase[0] == "objects":
			names = listObjects()
			names.sort()
			print("\n~Objects~")
			for name in names:
				print(name)
		elif phrase[0] == "stats":
			print("\n~Stats~")
			print("Body Levels: " + str(objects[activeCharacter].bodyLevels))
			print("Soak: " + str(objects[activeCharacter].soak))
			print("Strength: {0} ({1})".format(str(objects[activeCharacter].strength), str(objects[activeCharacter].attackStrength)))
			print("Wounds: " + str(objects[activeCharacter].wounds))
	if len(phrase) > 1:
		name, ID = getID(phrase)
		if ID != 0:
			DA = definiteArticle(ID, name)
			if phrase[0] == "close":
				if objects[ID].locked in [0, 2]:
					actor = "You"
					verb = " have "
					if objects[ID].closed == 0:
						objects[ID].closed = 1
						print("\n" + actor + verb + "closed " + DA.lower() + name + ".")
					elif objects[ID].closed == 1:
						print("\n" + DA + name + " is already closed.")
					elif objects[ID].closed == 2:
						print("\nYou cannot close " + DA.lower() + name + ".")
					else:
						print(objects[ID].closed)
				else:
					print("\n" + DA + name + " is locked.")
			elif phrase[0] == "examine":
				if objects[ID].examine == 0:
					objects[ID].view()
				else:
					print(objects[ID].examine)
			elif phrase[0] == "open":
				if objects[ID].locked in [0, 2]:
					actor = "You"
					verb = " have "
					if objects[ID].closed == 1:
						objects[ID].closed = 0
						print("\n" + actor + verb + "opened " + DA.lower() + name + ".")
						for location in objects[ID].location:
							if location != objects[activeCharacter].location[0]:
								checkForEnemies(location)
					elif objects[ID].closed == 0:
						print("\n" + DA + name + "is already open.")
					elif objects[ID].closed == 2:
						print("\nYou cannot open " + DA.lower() + name + ".")
					else:
						print(objects[ID].closed)
				else:
					print("\n" + DA + name + " is locked.")
			elif phrase[0] == "use":
				if objects[ID].use == 0:
					print("\nYou cannot use {0}{1}.".format(DA.lower(), name))
				elif objects[ID].use == 1:
					objects[ID].utilize()
				else:
					print(objects[ID].use)

def pluralizer(number):
	if number == 1:
		plural = ""
	else:
		plural = "s"
	return plural

def printActions():
	print("\n~List of Commands~")
	for action in actions:
		if action != "cheat":
			print(action)

def printIntro():
	print(("\n" * 10) + (" " * 26) + "--- Hazelfire ---")
	time.sleep(2)
	print("\n" + (" " * 34) + "by")
	time.sleep(2)
	print("\n" + (" " * 25) + "Meadow Hill Software")
	time.sleep(2)
	print("\n")

def replaceObject(area, item, newObject):
	global objects
	objects[location].items.remove(item)
	del objects[item]
	ID = createObject(newObject, location)
	return ID

def soakRoll(defender):
	soak = objects[defender].soak
	slots = ["head", "legs", "torso"]
	armor = []
	armorBonus = 0
	for slot in slots:
		if slot in objects[defender].items.keys():
			piece = objects[defender].items[slot]
			if objects[piece].name[0] in armor:
				bonus += objects[piece].soak
	roll = random.randint(1, 20)
	total = soak + armorBonus + roll
	if defender in party:
		defenderName = "You"
	else:
		defenderName = "The " + objects[defender].name[0]
	if defender in party:
		IA = indefiniteArticle(roll)
		input("\nPress Enter to make your soak roll.")
		print("\n{0} rolled {1} {2} for a total of {3} ({4} + {5} + {2} = {3}).".format(defenderName, IA, roll, total, soak, armorBonus))
	if defender in enemies:
		print("\n{0}'s soak roll is {1}.".format(defenderName, total))
	return total

def verbForm(name):
	if name == "You":
		verb = "have"
	else:
		verb = "has"
	return verb

def worldCreation():
	global objects
	global coordinates
	lab = createObject("room", "")
	objects[lab].examine = '''\nYou are in a laboratory. Before you lies a desk and a chair. Upon the
desk sits a book. Twenty feet above you is a trap door leading to the
roof. There is a telescoping ladder leading up to the trap door. The
room also contains doors to the north, east, south, and west of you.'''
	objects[lab].coordinates = {"x": 0, "y": 0}
	coordinates[0] = {0: lab}
	for member in party:
		objects[lab].items.append(member)
		objects[member].location.remove("")
		objects[member].location.append(lab)
	objects[lab].name[1] = "laboratory"
	objects[lab].name[2] = "lab"
	diary = createObject("book", lab)
	objects[diary].closed = 1
	objects[diary].cover = "\nYou are looking at a black leather-bound diary."
	objects[diary].text = '''\nMidnight and just now getting to sleep. Wife is asleep, of course. Too
tired for soulless mechanical sex anyway.  Just want to sleep so that I
can look forward to the nightmares my job gives me.  Still better than 
work though but then what isn't?

7:00 AM, up with the sun, and ready for another shitty day at the lab. 
Going to pour myself some cheerios with SOY MILK. Oh, boy! No, honey, it
tastes GREAT. Really. How the fuck do you milk a soybean anyway?

It's noon... no wait, it's twelve hundred hours. I keep forgetting how 
everything in the lab needs to be in fucking military time. Yesterday I 
lost my twelve hundred hours break due to a fire drill... no wait, 
emergency preparedness operation. If there was ever a fire I'd burn 
alive before I could get out because they can't bother to put things in 
regular time like normal human beings.  Anyway I'm way behind on work 
today. Going to have to eat at my desk and lose my twelve hunded hours 
break AGAIN. Well you know what they say: Work is good for the soul! Too
bad I don't have one because this job just sucked it out of me.

It's now 5:00 PM. The sun is setting and I'm still at work. Too tired to
even complain...'''
	objects[diary].use = 1
	chair = createObject("chair", lab)
	objects[chair].examine = "\nYou are looking at a black ergonomic chair."
	objects[chair].use = "\nYou are seated in an uncomfortable chair."
	desk = createObject("desk", lab)
	objects[desk].examine = '''\nYou are looking at a white desk made of metal  There is a book sitting
atop it.'''
	objects[desk].use = "\nYou are standing on the desk. The ladder is still too high to reach."
	ladder = createObject("ladder", lab)
	northRoom = createObject("room", "")
	objects[northRoom].examine = "\nYou are in a small room containing a clock and a dead body."
	objects[northRoom].coordinates = {"x": 2, "y": 0}
	coordinates[2] = {0: northRoom}
	objects[northRoom].name[1] = "north room"
	ID = createObject("door", lab)
	objects[northRoom].items.append(ID)
	objects[ID].coordinates = {"x": 1, "y": 0}
	coordinates[1] = {0: ID}
	objects[ID].examine = "\nYou are looking at an unremarkable metal door."
	objects[ID].location.append(northRoom)
	objects[ID].name[lab] = "north door"
	objects[ID].name[northRoom] = "south door"
	southRoom = createObject("room", "")
	objects[southRoom].examine = "\nYou are in a small room containing a clock and a dead body."
	objects[southRoom].coordinates = {"x": -2, "y": 0}
	coordinates[-2] = {0: southRoom}
	objects[southRoom].name[1] = "south room"
	ID = createObject("door", lab)
	objects[southRoom].items.append(ID)
	objects[ID].coordinates = {"x": -1, "y": 0}
	coordinates[-1] = {0: ID}
	objects[ID].examine = "\nYou are looking at an unremarkable metal door."
	objects[ID].location.append(southRoom)
	objects[ID].name[lab] = "south door"
	objects[ID].name[southRoom] = "north door"
	eastRoom = createObject("room", "")
	objects[eastRoom].examine = "\nYou are in a small room containing a clock and a dead body."
	objects[eastRoom].coordinates = {"x": 0, "y": 2}
	coordinates[0][2] = southRoom
	objects[eastRoom].name[1] = "east room"
	ID = createObject("door", lab)
	objects[eastRoom].items.append(ID)
	objects[ID].coordinates = {"x": 0, "y": 1}
	coordinates[0][1] = ID
	objects[ID].examine = "\nYou are looking at an unremarkable metal door."
	objects[ID].location.append(eastRoom)
	objects[ID].name[lab] = "east door"
	objects[ID].name[eastRoom] = "west door"
	westRoom = createObject("room", "")
	objects[westRoom].examine = "\nYou are in a small room containing a clock and a dead body."
	objects[westRoom].coordinates = {"x": 0, "y": -2}
	coordinates[0][-2] = westRoom
	objects[westRoom].name[1] = "west room"
	ID = createObject("door", lab)
	objects[westRoom].items.append(ID)
	objects[ID].coordinates = {"x": 0, "y": -1}
	coordinates[0][-1] = ID
	objects[ID].examine = "\nYou are looking at an unremarkable metal door."
	objects[ID].location.append(eastRoom)
	objects[ID].name[lab] = "west door"
	objects[ID].name[westRoom] = "east door"
	ID = createObject("zombie", northRoom)
	ID = createObject("zombie", southRoom)
	ID = createObject("zombie", eastRoom)
	ID = createObject("zombie", westRoom)
	ID = createObject("clock", northRoom)
	ID = createObject("clock", southRoom)
	ID = createObject("clock", eastRoom)
	ID = createObject("clock", westRoom)

def woundLevel(defender):
	if objects[defender].bodyLevels == 5:
		if objects[defender].wounds == 0:
			description = "not wounded"
		elif objects[defender].wounds == 1:
			description = "barely wounded"
		elif objects[defender].wounds == 2:
			description = "lightly wounded"
		elif objects[defender].wounds == 3:
			description = "moderately wounded"
		elif objects[defender].wounds == 4:
			description = "heavily wounded"
		elif objects[defender].wounds == 5:
			description = "critically wounded"
		else:
			description = "fatally wounded"
	elif objects[defender].bodyLevels == 10:
		if objects[defender].wounds == 0:
			description = "not wounded"
		elif objects[defender].wounds in [1, 2]:
			description = "barely wounded"
		elif objects[defender].wounds in [3, 4]:
			description = "lightly wounded"
		elif objects[defender].wounds in [5, 6]:
			description = "moderately wounded"
		elif objects[defender].wounds in [7, 8]:
			description = "heavily wounded"
		elif objects[defender].wounds in [9, 10]:
			description = "critically wounded"
		else:
			description = "fatally wounded"
	return description

#printIntro()
clothing = []
weapons = ["battle axe", "broad sword", "buckler", "club", "composite bow", "dagger", "glock 17", "hand axe", "hunting spear", "javelin", "knife", "long bow", "long spear", "quarterstaff", "round shield", "scramasax", "short bow", "short sword", "sling", "small shield", "throwing axe", "throwing knife", "war spear"]
lifeforms = ["human", "zombie"]
locations = []
coordinates = {}
actions = ["actions", "cheat", "close", "east", "examine", "north", "objects", "open", "rules", "south", "stats", "use", "west"]
replay = "y"

while replay.lower() in ["yes", "y"]:
	objects = {}
	objectCount = {}
	party = []
	activeCharacter = ""
	characterCreation()
	worldCreation()
	enemies = []
	youLose = 0
	youWin = 0
	print('''You are in a mad scientist's lab somewhere in North America. Before you
lies a desk and a chair. Upon the desk sits a book. Twenty feet above 
you is a trap door leading to the roof. You know that on that roof lies 
a helipad where a chopper waits to extract you. The ladder used to climb 
to the roof, however, is retracted and is too high to reach. The room 
also contains doors to the north, east, south, and west of you. You are 
carrying a loaded Glock 17 pistol.''')
	printActions()
	while youLose == 0 and youWin == 0:
		parseAction()
	print(("\n" * 3) + (" " * 26) + "--- GAME OVER ---")
	replay = input("\n\n\nReplay? (yes or no): ")
