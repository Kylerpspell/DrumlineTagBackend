from apikeys import BOTTOKEN, BACKEND
import asyncio
from datetime import datetime, timedelta
import discord
from discord.ext import commands, tasks
import random
import requests

# import Spot
client: commands.Bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

def add_drummer_to_db(drummer_name: str) -> bool:
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


def add_tag_to_db(tagger: str, tagged: str, img_url: str) -> bool:
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
	r = requests.post(
		BACKEND + "tags/add",
		json={
			"tagger": tagger_id,
			"tagged": tagged_id,
			"date": datetime.now().isoformat(),
			"img_url": img_url,
		},
	)
	print("Tag added")
	return True


def add_section_to_db(user: str, section: str):
	# Find the user in the database
	r = requests.get(BACKEND + "drummers")
	drummers = r.json()
	user_id = None
	if drummers is not None:
		for drummer in drummers:
			print(drummer["name"])
			if drummer["name"] == user:
				user_id = drummer["_id"]
				break

	# If the user is not in the database, return an error
	if user_id is None:
		print("User not found")
		return

	print(user_id)
	# Add the section to the database
	r = requests.put(
		BACKEND + "drummers/" + user_id + "/updateSection", json={"section": section}
	)


def add_year_to_db(user: str, year: str):
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
	r = requests.put(
		BACKEND + "drummers/" + user_id + "/updateYear", json={"year": year}
	)


def change_drummer_isMostWanted(drummer_id, isMostWanted):
	# Update the drummer in the database
	r = requests.put(
		BACKEND + "drummers/" + drummer_id + "/updateIsMostWanted",
		json={"isMostWanted": isMostWanted},
	)


def update_mostWanted():
	# Get the drummers from the database
	r = requests.get(BACKEND + "drummers")
	drummers = r.json()

	# Set the most wanted drummer to false
	for drummer in drummers:
		change_drummer_isMostWanted(drummer["_id"], False)

	# Select a random drummer
	mostWanted = random.choice(drummers)

	# Set the most wanted drummer to true
	change_drummer_isMostWanted(mostWanted["_id"], True)
	print(mostWanted["name"] + " is now the most wanted")


def clear_mostWanted():
	# Get the drummers from the database
	r = requests.get(BACKEND + "drummers")
	drummers = r.json()

	# Set the most wanted drummer to false
	for drummer in drummers:
		change_drummer_isMostWanted(drummer["_id"], False)

	print("Most wanted cleared")


def delete_all_tags():
	r = requests.get(BACKEND + "tags")
	tags = r.json()

	for tag in tags:
		id = tag["_id"]
		r = requests.delete(f"{BACKEND}tags/{id}/remove")

def delete_all_drummers():
	# Get the drummers from the database
	r = requests.get(BACKEND + "drummers")
	drummers = r.json()

	# Set the most wanted drummer to false
	for drummer in drummers:
		id = drummer["_id"]
		r = requests.delete(f"{BACKEND}drummers/{id}/remove")


def random_tag_message() -> str:
	roll = int(random.randint(1, 6))
	messages = [
		"*Click* Caught in 4K",
		"You hate to see it...",
		"Lookin good!",
		"That's gonna look great on my wall!",
		"When I was young my dad use to hit me with a Polaroid. I still get instant flashbacks...",
		"They never saw it coming...",
	]
	return messages[roll]


@client.event
async def on_ready():
	print("The bot is now ready for use!")
	print("------------------------------")
	schedule_daily_message.start()


@client.command(pass_context=True)
async def play(ctx):
	playerName = ctx.message.author.display_name
	if add_drummer_to_db(playerName):
		await ctx.send("You have been added to the database!")
	else:
		await ctx.send("You are already in the database!")


@client.command(pass_context=True)
async def tag(ctx):
	try:
		tagged = ctx.message.mentions[0].display_name
		tagger = ctx.message.author.display_name
	except IndexError:
		print("No one was tagged")
		await ctx.send(
			"Beep Beep Boop.  \nERROR  \nNo dice, @ someone in the server after you !tag"
		)
	else:
		try:
			# Determine if the message has an attachment
			attachment: discord.Attachment = ctx.message.attachments[0]
		except IndexError:
			print("Error: No attachments")
			await ctx.send(
				"Boop Boop Beep.  \nERROR  \nThere is no picture here! \nBe sure to attach an image!"
			)
		else:
			
			await ctx.send(tagger + " tagged " + tagged)
			await ctx.send(random_tag_message())
			await ctx.send("Sorry {}".format(tagged))
			
			image_content: discord.File = attachment.to_file()
			
			# Post the image to AWS S3 Bucket
			add_tag_to_db(ctx.message.author.display_name, tagged, None)


@client.command(pass_context=True)
async def hello(ctx):
	await ctx.send("Hello {}!".format(ctx.message.author.mention))


@client.command(pass_context=True)
async def section(ctx, arg=None):
	arg = arg.lower()
	if (
		arg == "snare"
		or arg == "bass"
		or arg == "tenor"
		or arg == "cymbal"
		or arg == "multi"
	):
		await ctx.send(
			"Got it, you are a " + arg + " player!" "\nGood luck " + arg + " line!"
		)
		add_section_to_db(ctx.message.author.display_name, arg)
		print("Section is " + arg + ".")
	else:
		await ctx.send("That is not a section...")
		print("Invalid section.")
	if arg == None:
		await ctx.send(
			"Be sure to enter what section you are in after typing in !section"
		)
		print("Did not enter a section.")


@client.command(pass_context=True)
async def year(ctx, arg=None):
	arg = arg.lower()
	if arg == "senior" or arg == "junior" or arg == "sophomore" or arg == "freshman":
		await ctx.send(
			"Got it, you are a "
			+ arg
			+ "\nWe can't wait for you to do big things this semester!"
		)
		add_year_to_db(ctx.message.author.display_name, arg)
		print("Year is " + arg + ".")
	else:
		await ctx.send("That is not a valid year...")
		print("Invalid year.")
	if arg == None:
		await ctx.send(
			"Be sure to enter what class year you are after typing in !year (Senior, Junior, Sophomore, or Freshman)"
		)
		print("Did not enter a year")


@client.command(pass_context=True)
async def assist(ctx):
	user = ctx.message.author
	await user.send(
		"Hey! My names Spot, The Drumline Tag Bot!  \nThis year I will be helping to keep track of the Drumline Tag"
		"score to make your life easier."
		"\nHere is how to use me and my rules"
		"\n"
		"\nCommand One: !play"
		"\nIf you wish to participate in drumline tag, throw your hat in the ring by typing !play."
		"\n"
		"\nCommand Two: !section <your section>"
		"\n(Snare, Bass, Tenor, Cymbol, Multi)"
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
		"\nNow onto my rules \nRule One: One Photo, One @Person.  My brain is very small and I cannot handle a large"
		"flux of inputs at once :("
		"\nRule Two: If I break yell at Ben."
		"\nRule Three:  Have Fun, we will determine prizes (if any) as the semester goes on so always be on the look out"
		"for other members."
		"\nHappy tagging and Go Cocks!\n"
		"\nWebsite: https://drumlinetag.surge.sh/leaderboard"
		"\nNote: The website tends to load slow, if you do not see any information when first opening it, that is normal."
		"Give it a bit of time."
	)


def seconds_until_midnight():
	now = datetime.now()
	target = (now + timedelta(days=0)).replace(
		hour=8, minute=0, second=0, microsecond=0
	)
	diff = (target - now).total_seconds()
	if diff < 0:
		target = (now + timedelta(days=1)).replace(
			hour=8, minute=0, second=0, microsecond=0
		)
		diff = (target - now).total_seconds()
	print(f"{target} - {now} = {diff}")
	return diff


@tasks.loop(seconds=1)
async def schedule_daily_message():
	await asyncio.sleep(seconds_until_midnight())
	channel = client.get_channel(1072933532189589506) #TODO: This should also probably be in APIKEYS
	print(f"Got channel {channel}")
	update_mostWanted()
	await channel.send("I work!")


@schedule_daily_message.before_loop
async def before():
	await client.wait_until_ready()
	print("Finished waiting")

if __name__ == "__main__":
	# tests()
	client.run(BOTTOKEN)
