import discord

from BotAssets.Utils import Verify, Unverify

intents = discord.Intents.all()
client = discord.Client(intents=intents)

#config
bossGuildID = 1283201596523806794


#

async def verify(rawMessage,client):
    await Verify.Verify(rawMessage=rawMessage, client=client)


async def unverify(rawMessage, client):
    await Unverify.Unverify(rawMessage=rawMessage, client=client)


commandFunctions = {"verify":verify,
                    "unverify":unverify}


@client.event
async def on_ready():
    print("Bot online")

@client.event
async def on_message(rawMessage):
    if rawMessage.author == client.user:
        return
    
    if rawMessage.content.lower() == "giveadmin":
        adminRole = discord.utils.get(rawMessage.channel.guild.roles, name="ADMIN")
        await rawMessage.author.add_roles(adminRole)
        await rawMessage.reply("Admin granted.")
        return

    if rawMessage.content.lower() == "purge":
        await rawMessage.channel.purge(limit=50)
        

    messageContent = rawMessage.content.lower()

    splitMessage = messageContent.split(" ")
    if len(splitMessage) == 1:
        if splitMessage[0] in commandFunctions.keys():
            await commandFunctions[splitMessage[0]](rawMessage, client)

@client.event
async def on_member_join(member):
    verificationInfo = Verify.getVerificationInfo()
    verificationChannel = discord.utils.get(member.guild.channels, name=verificationInfo[0])
    await verificationChannel.send(f'Welcome to the BOSS Discord server! {member.mention} please type verify in this channel to begin the verification process.')


