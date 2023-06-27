import discord
import random
import uuid
import requests
from datetime import datetime
import json
import shutil
from discord.ext import commands
from apikeys import BOTTOKEN, BACKEND
#import Spot

client = commands.Bot(command_prefix = '!', intents = discord.Intents.all())


def tests():
	# Add section to database
	add_section_to_db("Test1", "bass")
	add_section_to_db("Test2", "cymbals")
	add_section_to_db("Test3", "tenor")
	add_section_to_db("Test4", "flub")
	add_section_to_db("Test5", "snare")

	# Add year to database
	add_year_to_db("Test1", 2021)
	add_year_to_db("Test2", 2020)
	add_year_to_db("Test3", 2019)
	add_year_to_db("Test4", 2018)
	add_year_to_db("Test5", 2017)


def add_tag_to_db(tagger, tagged):
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
	r = requests.post(BACKEND + "tags/add", json={"tagger": tagger_id, "tagged": tagged_id, "date": datetime.now().isoformat()})
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



@client.event
async def on_ready():
	print("The bot is now ready for use!")
	print("------------------------------")


@client.command(pass_context = True)
async def play(ctx):
	playerName = ctx.message.author.display_name
	requests.post(BACKEND + "drummers/add", json={"name": playerName})
	await ctx.send("You have been added to the database!")


@client.command(pass_context = True)
async def tag(ctx):
		roll = int(random.randint(1,6))
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
				if url[0:26] == "https://cdn.discordapp.com":
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
				await ctx.send("Sorry {}".format(tagged))

				add_tag_to_db(ctx.message.author.display_name, tagged)
		

@client.command(pass_context = True)
async def hello(ctx):
	await ctx.send("Hello {}!".format(ctx.message.author.mention))

@client.command(pass_context = True)
async def section(ctx, arg = None):
	arg = arg.lower()
	if(arg == 'snare' or arg == 'bass' or arg == 'tenor' or arg == 'cymbal' or arg == 'flub'):
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
	if(arg == 'senior' or arg == 'junior' or arg == 'sophomore' or arg == 'freshman'):
		await ctx.send("Got it, you are a " + arg + "\nWe can't wait for you to do big things this semester!")
		add_year_to_db(ctx.message.author.display_name, arg)
		print("Year is " + arg + ".")
	else:
		await ctx.send("That is not a valid year...")
		print("Invalid year.")
	if(arg == None):
		await ctx.send("Be sure to enter what class year you are after typing in !year (Senior, Junior, Sophomore, or Freshman)")
		print("Did not enter a year")


@client.command(pass_context = True)
async def assist(ctx):
	await ctx.send("Hey! My names Spot, The Drumline Tag Bot!  \nThis year I will be helping to keep track of the Drumline Tag score to make your life easier." 
				   "\nHere is how to use me and my rules \nCommand One: !tag @<name> + <attached image> \nThis command will save the name of the photographer and their victim. "
				   "When a tag is completed, the photographer gains 3 points and the victim loses 1.  Scores CAN be negative!"
				   "\nCommand Two: !challenge @<name> This command will be given if a picture seems unfair or is taken to close to practice time. "
				   "If you fail three challenges you will lose 10 points. If you fail 5, your score will not be accounted for in the final tally."
				   "\nNow onto my rules \nRule One: One Photo, One @Person.  My brain is very small and I cannot handle a large flux of inputs at once :("
				   "\nRule Two:  Have Fun, we will determine prizes as the semester goes on so always be on the look out for others."
				   "\nHappy tagging and Go Cocks!\n"
				   "\nLeaderboard: https://drumlinetag.surge.sh/leaderboard")

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
