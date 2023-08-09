from apikeys import BOTTOKEN, BACKEND
from main import add_drummer_to_db, add_section_to_db, add_year_to_db, add_tag_to_db, change_drummer_isMostWanted, update_mostWanted, clear_mostWanted
import requests
import json
import random


def tests():
	clear_mostWanted()

	# Add drummers to database
	print("Adding Benny Boy to db", add_drummer_to_db("Benny Boy"))
	print("Adding DORITO to db", add_drummer_to_db("DORITO"))

	# Add tags/ drummers to database
	add_tag_to_db("Benny Boy", "DORITO", 'https://media.discordapp.net/attachments/1072933532189589506/1119434180435116093/download.jpg')
	add_tag_to_db("DORITO", "Benny Boy", 'https://media.discordapp.net/attachments/1072933532189589506/1119434180435116093/download.jpg')

	# choose a random drummer
	update_mostWanted()

	add_tag_to_db("DORITO", "Benny Boy", 'https://media.discordapp.net/attachments/1072933532189589506/1119434180435116093/download.jpg')
	add_tag_to_db("Benny Boy", "DORITO", 'https://media.discordapp.net/attachments/1072933532189589506/1119434180435116093/download.jpg')

tests()