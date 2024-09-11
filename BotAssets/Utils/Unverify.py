import discord
from BotAssets.Utils import Verify

verificationCategoryName, verifiedRoleName, unitList, bossRepTypes = Verify.getVerificationInfo()

async def Unverify(rawMessage, client):
    verifiedRole = discord.utils.get(rawMessage.channel.guild.roles, name=verifiedRoleName)
    if verifiedRole:
        await rawMessage.author.remove_roles(verifiedRole)

    for repType in bossRepTypes:
        repTypeRole = discord.utils.get(rawMessage.channel.guild.roles, name=bossRepTypes[repType])
        if repTypeRole != None:
            if repTypeRole in rawMessage.author.roles:
                await rawMessage.author.remove_roles(repTypeRole)
    
    for brigadeName in unitList:
        unitRole = discord.utils.get(rawMessage.channel.guild.roles, name=unitList[brigadeName])
        if unitRole != None:
            if unitRole in rawMessage.author.roles:
                await rawMessage.author.remove_roles(unitRole)

    await rawMessage.reply("Successfully unverified.")
    