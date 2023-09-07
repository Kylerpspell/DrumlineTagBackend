import discord
import random
import uuid
import requests
from datetime import datetime, timedelta
import json
import shutil
import asyncio
from discord.ext import commands, tasks
from apikeys import BOTTOKEN, BACKEND
#import Spot

client = commands.Bot(command_prefix = '!', intents = discord.Intents.all())

def add_drummer_to_db(drummer_name):
	# Check to see if the drummer is in the database
	r = requests.get(BACKEND + "drummers")
	drummers = r.json()
	drummer_id = None
	if drummers is not None:
		for drummer in drummers:
			if drummer["name"] == drummer_name:
				drummer_id = drummer["_id"]
				break
	
	# If the drummer is not in the database, add them
	if drummer_id is None:
		r = requests.post(BACKEND + "drummers/add", json={"name": drummer_name})
		return True
	else:
		return False
	
def add_tag_to_db(tagger, tagged, img_url):
	print("Adding tag")
	# Check to see if the tagger and tagged are in the database
	r = requests.get(BACKEND + "drummers")
	drummers = r.json()
	tagger_id = None
	tagged_id = None
	if drummers is not None:
		for drummer in drummers:
			if drummer["name"] == tagger:
				tagger_id = drummer["_id"]
			if drummer["name"] == tagged:
				tagged_id = drummer["_id"]
	
	# If the tagger is not in the database, return an error
	if tagger_id is None:
		print("Tagger not found")
		return False
	
	# If the tagged is not in the database, add them
	if tagged_id is None:
		r = requests.post(BACKEND + "drummers/add", json={"name": tagged})
	# Get the tagger and tagged ids
	r = requests.get(BACKEND + "drummers")
	drummers = r.json()
	for drummer in drummers:
		if drummer["name"] == tagger:
			tagger_id = drummer["_id"]
		if drummer["name"] == tagged:
			tagged_id = drummer["_id"]

	# Add the tag to the database
	print("tagger_id", tagger_id, "tagged_id", tagged_id)
	r = requests.post(BACKEND + "tags/add", json={"tagger": tagger_id, "tagged": tagged_id, "date": datetime.now().isoformat(), "img_url": img_url})
	print("Tag added")
	return True
	 

def add_section_to_db(user, section):
	# Find the user in the database
	r = requests.get(BACKEND + "drummers")
	drummers = r.json()
	user_id = None
	if drummers is not None:
		for drummer in drummers:
			print(drummer['name'])
			if drummer["name"] == user:
				user_id = drummer["_id"]
				break
	
	# If the user is not in the database, return an error
	if user_id is None:
		print("User not found")
		return
	
	print(user_id)
	# Add the section to the database
	r = requests.put(BACKEND + "drummers/" + user_id + "/updateSection", json={"section": section})


def add_year_to_db(user, year):
	# Find the user in the database
	r = requests.get(BACKEND + "drummers")
	drummers = r.json()
	user_id = None
	if drummers is not None:
		for drummer in drummers:
			if drummer["name"] == user:
				user_id = drummer["_id"]
				break
	
	# If the user is not in the database, return an error
	if user_id is None:
		print("User not found")
		return
	
	print(user_id)
	# Add the year to the database
	r = requests.put(BACKEND + "drummers/" + user_id + "/updateYear", json={"year": year})

def change_drummer_isMostWanted(drummer_id, isMostWanted):
	# Update the drummer in the database
	r = requests.put(BACKEND + "drummers/" + drummer_id + "/updateIsMostWanted", json={"isMostWanted": isMostWanted})
def update_mostWanted():
	# Get the drummers from the database
	r = requests.get(BACKEND + "drummers")
	drummers = r.json()
	
	# Set the most wanted drummer to false
	for drummer in drummers:
		change_drummer_isMostWanted(drummer["_id"], False)
	
	# Select a random drummer
	for i in range(10):
		mostWanted = random.choice(drummers)
		print(mostWanted["name"])
	print(mostWanted["name"])
	# Set the most wanted drummer to true
	change_drummer_isMostWanted(mostWanted["_id"], True)
	print(mostWanted["name"] + " is now the most wanted")
	Name = mostWanted["name"]
	return Name

def clear_mostWanted():
	# Get the drummers from the database
	r = requests.get(BACKEND + "drummers")
	drummers = r.json()
	
	# Set the most wanted drummer to false
	for drummer in drummers:
		change_drummer_isMostWanted(drummer["_id"], False)
	
	print("Most wanted cleared")

@client.event
async def on_ready():
	print("The bot is now ready for use!")
	print("------------------------------")
	schedule_daily_message.start()


@client.command(pass_context = True)
async def play(ctx):
	playerName = ctx.message.author.display_name
	if(add_drummer_to_db(playerName)):
		await ctx.send("You have been added to the database!")
	else:
		await ctx.send("You are already in the database!")

@client.command(pass_context = True)
async def tag(ctx):
		roll = int(random.randint(1,19))
		try:
			tagged = ctx.message.mentions[0].display_name
			tagger = ctx.message.author.display_name
		except IndexError:
			print("No one was tagged")
			await ctx.send("Beep Beep Boop.  \nERROR  \nNo dice, @ someone in the server after you !tag")
		else:
			try:
				url = ctx.message.attachments[0].url
			except IndexError:
				print("Error: No attachments")
				await ctx.send("Boop Boop Beep.  \nERROR  \nThere is no picture here! \nBe sure to attach an image!")
			else:
				if tagged != "Spot":
					if url[0:26] == "https://cdn.discordapp.com" and tagged != "Spot":
						r = requests.get(url, stream=True)
						imageName = str(uuid.uuid4()) + '.jpg'
						with open(imageName, 'wb') as out_file:
							print('Saving image: ' + imageName)
							shutil.copyfileobj(r.raw, out_file)
					await ctx.send(tagger + " tagged " + tagged)
					if roll == 1:
							await ctx.send("*Click* Caught in 4K")
					if roll == 2:
						await ctx.send("You hate to see it...")
					if roll == 3:
						await ctx.send("Lookin good!")
					if roll == 4:
						await ctx.send("That's gonna look great on my wall!")
					if roll == 5:
						await ctx.send("When I was young my dad use to hit me with a Polaroid. I still get instant flashbacks...")
					if roll == 6:
						await ctx.send("They never saw it coming...")
					if roll == 7:
						await ctx.send("Behind you!")
					if roll == 8:
						await ctx.send("I had to give up my career as a professional photographer... \nI kept losing focus...")
					if roll == 9:
						await ctx.send("Photography is a developing hobby")
					if roll == 10:
						await ctx.send("Say click! Take a pic \nCan you find the drummer/crasher in this photo?")
					if roll == 11:
						await ctx.send("Tagged, just like a trending meme! \nAdding this one to the folder")
					if roll == 12:
						await ctx.send("Caught in the act, tag-style! \nThey are going to be so pissed...")
					if roll == 13:
						await ctx.send("You've been caught, but not for ransom!")
					if roll == 14:
						await ctx.send("Tagged and bagged \nIn a friendly way!")
					if roll == 15:
						await ctx.send("Tagged... \nJust a reminder you are never alone")
					if roll == 16:
						await ctx.send("Tagged! \nJust like a ghost in the night")
					if roll == 17:
						await ctx.send("Bang the drums! \nTag the players!")
					if roll == 18:
						await ctx.send("Syncopated tagging! \nYou're it!")
					if roll == 19:
						await ctx.send("Cymbal crash and tag dash! \nDon't drop the camera!")
					await ctx.send("Sorry {}".format(tagged))

					add_tag_to_db(ctx.message.author.display_name, tagged, url)

				if tagged == "Spot":
					await ctx.send("Trying to get free points?  \nNice try, but I'm not a Drumline member :)")
		

@client.command(pass_context = True)
async def hello(ctx):
	await ctx.send("Hello {}!".format(ctx.message.author.mention))

@client.command(pass_context = True)
async def section(ctx, arg = None):
	arg = arg.lower()
	if(arg == 'snare' or arg == 'bass' or arg == 'tenor' or arg == 'cymbal' or arg == 'multi'):
		await ctx.send("Got it, you are a " + arg + " player!" "\nGood luck " + arg + " line!")
		add_section_to_db(ctx.message.author.display_name, arg)
		print("Section is " + arg + ".")
	else:
		await ctx.send("That is not a section...")
		print("Invalid section.")
	if(arg == None):
		await ctx.send("Be sure to enter what section you are in after typing in !section")
		print("Did not enter a section.")

  
@client.command(pass_context = True)
async def year(ctx, arg = None):
	arg = arg.lower()
	if(arg == 'super-senior' or arg == 'senior' or arg == 'junior' or arg == 'sophomore' or arg == 'freshman'):
		await ctx.send("Got it, you are a " + arg + "\nWe can't wait for you to do big things this semester!")
		add_year_to_db(ctx.message.author.display_name, arg)
		print("Year is " + arg + ".")
	else:
		await ctx.send("That is not a valid year...")
		print("Invalid year.")
	if(arg == None):
		await ctx.send("Be sure to enter what class year you are after typing in !year (Super-Senior, Senior, Junior, Sophomore, or Freshman)")
		print("Did not enter a year")


@client.command(pass_context = True)
async def assist(ctx):
	user = ctx.message.author
	await user.send("Hey! My name is Spot, The Drumline Tag Bot!  \nThis year I will be helping to keep track of the Drumline Tag "
		 		    "score to make your life easier."
					"\n" 
				   	"\nHere is how I work and my rules:"
				   	"\n"
				   	"\nCommand One: !play"
				   	"\nIf you wish to participate in Drumline Tag, throw your hat in the ring by typing !play."
				   	"\n"
				   	"\nCommand Two: !section <your section>"
				   	"\n(Snare, Bass, Tenor, Cymbal, Multi)"
				   	"\n"
				   	"\nCommand Three: !year <your year>"
				   	"\n(Freshman, Sophomore, Junior, Senior)"
				   	"\n"
				   	"\nCommand Four: !tag @<name> + <attached image>" 
				   	"\nThis command will save the name of the photographer and their victim. "
				   	"When a tag is completed, the photographer gains 3 points and the victim loses 1 point."  
				   	"\nScores CAN be negative!"
				   	"\n"
				   	"\nExample of a proper tag:"
				   	"\nhttps://drive.google.com/file/d/10TcV6A_6CeSYaMS7rETLn0eYdNJZtMMn/view?usp=sharing"
				   	"\n"
				   	"\nNow onto my rules: "
				   	"\n"
					"\nRule One: You only recive points if the person you are trying to tag does not see you before you post the tag."
				   	"\nRule Two: One photo, One @person.  My brain is very small and I cannot handle a large " 
				   	"number of inputs at once :(" 
				   	"\nRule Three: If I break, talk to Ben."
				   	"\nRule Four: Every day at 8 am I will randomly select a \"Most Wanted\" player. They will be displayed on the website and " 
				   	"you will score 5 points instead of 3 for tagging them!"
				   	"\n(They will still only lose one point)"
				   	"\nRule Five:  Have fun! \nWe will determine prizes (if any) as the semester goes on so always be on the look out "
				   	"for other members."
				   	"\nRule Six: NO FOUL IMAGES"
				   	"\nIf you break this rule you will be given one warning. If you continue to post vulgar images, your score will be scrapped, "
				   	"and you will be removed from the game. \n(Depending on the context of the image, a warning may not be issued and you will be removed immediately)"
				   	"\n"
				   	"\nHappy tagging and Go Cocks!\n"
				   	"\nWebsite: https://drumlinetag.surge.sh/leaderboard"
				   	"\nNote: The website tends to load slow, if you do not see any information when first opening it, that is normal. " 
				   	"Give it a bit of time.")

def seconds_until_midnight():
	now = datetime.now()
	target = (now + timedelta(days=0)).replace(hour=8, minute=0, second=0, microsecond=0)
	diff = (target - now).total_seconds()
	if (diff < 0):
		target = (now + timedelta(days=1)).replace(hour=8, minute=0, second=0, microsecond=0)
		diff = (target - now).total_seconds()
	print(f"{target} - {now} = {diff}")
	return diff
	

@tasks.loop(seconds =1)
async def schedule_daily_message():
	await asyncio.sleep(seconds_until_midnight())
	channel = client.get_channel(1144783433827106907)
	print(f"Got channel {channel}")
	await channel.send(update_mostWanted() + " is now wanted!")

@schedule_daily_message.before_loop
async def before():
	await client.wait_until_ready()
	print("Finished waiting")

'''
@client.command()
async def save(ctx):
	try:
		url = ctx.message.attachments[0].url
	except IndexError:
		print("Error: No attachments")
		await ctx.send("No attachments detected!")
	else:
		if url[0:26] == "https://cdn.discordapp.com":
			r = requests.get(url, stream=True)
			imageName = str(uuid.uuid4()) + '.jpg'
			with open(imageName, 'wb') as out_file:
				print('Saving image: ' + imageName)
				shutil.copyfileobj(r.raw, out_file)
'''     

if __name__ == "__main__":
	#tests()
	client.run(BOTTOKEN)
