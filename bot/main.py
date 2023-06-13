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

@client.event
async def on_ready():
	print("The bot is now ready for use!")
	print("------------------------------")

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
				stringTag = ctx.message.author.display_name
				stringTagged = tagged
				await ctx.send("Sorry {}".format(tagged))

				# Check to see if the tagger is already in the database
				r = requests.get(BACKEND + "drummers/")
				if r.status_code == 200:
					drummers = r.json()
					if stringTag not in drummers:
						# Add the drummer to the database
						r = requests.post(BACKEND + "drummers/add", json={"name": stringTag})
						if r.status_code == 200:
							print("Tagger added successfully")
					
					if stringTagged not in drummers:
						# Add the drummer to the database
						r = requests.post(BACKEND + "drummers/add", json={"name": stringTagged})
						if r.status_code == 200:
							print("Tagged added successfully")
				else:
					print("Error getting drummers")
					print(r.text)
					await ctx.send("Error getting drummers. Please try again later.")
				
				# find the drummer's id's
				r = requests.get(BACKEND + "drummers/")
				if r.status_code == 200:
					drummers = r.json()
					print(drummers)
					taggerId = ""
					taggedId = ""
					for drummer in drummers:
						if drummer["name"] == stringTag:
							taggerId = drummer["_id"]
						if drummer["name"] == stringTagged:
							taggedId = drummer["_id"]
					
					if taggerId == "":
						print("Error: taggerId not found")
						await ctx.send("Error: taggerId not found")
						return
					if taggedId == "":
						print("Error: taggedId not found")
						await ctx.send("Error: taggedId not found")
						return

				else:
					print("Error getting drummers")
					print(r.text)
					await ctx.send("Error getting drummers. Please try again later.")

				# Send the tag to the backend
				body = {
					"tagger": taggerId,
					"tagged": taggedId,
					"date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
				}
				r = requests.post(BACKEND + "tags/add", json=body)
				print("Sent tag to backend")
				if r.status_code == 200:
					print("Tag saved successfully")
				else:
					print("Error saving tag")
					print(r.text)
					await ctx.send("Error saving tag. Please try again later.")

@client.command(pass_context = True)
async def hello(ctx):
	await ctx.send("Hello {}!".format(ctx.message.author.mention))

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


client.run(BOTTOKEN)