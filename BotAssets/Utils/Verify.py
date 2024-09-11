import discord


#configs
verificationChannelName = "verification"
verificationRoleName = "BossVerified"
bossRepIdentifierRoleName = "Boss Rep"

#unitlist for reaction role when verifying
unitList = {
    "8️⃣" : "READY CO",
    "7️⃣" : "4CAB",
    "6️⃣" : "4DA",
    "5️⃣" : "4DSB",
    "4️⃣" : "3ABCT",
    "3️⃣" : "2ABCT",
    "2️⃣" : "1ABCT",
    "1️⃣" : "HHBN",
    "0️⃣" : "Unspecified Brigade"
}

repTypes = {
    "3️⃣" : "Company Rep",
    "2️⃣" : "Battalion Rep",
    "1️⃣" : "Brigade Rep",
}

def getVerificationInfo():
    return verificationChannelName, verificationRoleName, unitList, repTypes
#

async def Verify(client, rawMessage):
    
    if rawMessage.channel.name == verificationChannelName:
        verifiedRole = discord.utils.get(rawMessage.channel.guild.roles, name=verificationRoleName)

        if verifiedRole in rawMessage.author.roles:
            await rawMessage.reply("You're already verified.")
            return
        
        #gathering name------
        await rawMessage.reply("Please send your first name.")
        firstNameMsg = await client.wait_for("message", check=(lambda m: m.author == rawMessage.author))

        await rawMessage.reply("Please send your last name.")
        lastNameMsg = await client.wait_for("message", check=(lambda m: m.author == rawMessage.author))
        #------------------------

        #gathering rank---------------------------------------------

        await rawMessage.reply("Please send your rank in an abbreviated format.")
        rankMsg = await client.wait_for("message", check=(lambda m: m.author == rawMessage.author))

        if len(rankMsg.content)>3:
            await rawMessage.reply("Incorrect rank abbreviation. Try the verify command again.")
            return

        #-----------------------------------------


        #gathering unit----------------------
        unitEmbed = discord.Embed(title="Unit List", description="Choose your unit associated with the number")
        unitMsg = await rankMsg.reply(content = "", embed=unitEmbed)

        for unitEmoji in unitList.keys():
            unitRole = discord.utils.get(rawMessage.channel.guild.roles, name=unitList[unitEmoji])
            if unitRole:
                unitEmbed.add_field(name="", value=f'{unitEmoji} = {unitRole.mention}', inline=False)

        await unitMsg.edit(embed=unitEmbed)

        for unitEmoji in unitList.keys():
            unitRole = discord.utils.get(rawMessage.channel.guild.roles, name=unitList[unitEmoji])
            if unitRole:
                await unitMsg.add_reaction(unitEmoji)




        global validUnitCheck
        global givenUnit
        validUnitCheck = False
        
        def check(reaction, user):
            global givenUnit
            global validUnitCheck

            givenUnit = str(reaction.emoji)
            if str(reaction.emoji) in unitList:
                validUnitCheck = True
            return user == rawMessage.author
        

        await client.wait_for("reaction_add", check=check, timeout=120)
        if validUnitCheck == True:
            if givenUnit in unitList.keys():
                userSpecifiedUnitRole = discord.utils.get(rawMessage.channel.guild.roles, name=unitList[givenUnit])
                await rawMessage.author.add_roles(userSpecifiedUnitRole)
        else:
            await rawMessage.reply("Invalid response, the verify command to start over.")

        #-------------------------------------------------------------------------------


        #asking if boss rep, and what type
        reactionConfirmation = await rankMsg.reply(f'Are you a boss rep?')
        await reactionConfirmation.add_reaction("👍")
        await reactionConfirmation.add_reaction("👎")
        
        global bossRep
        bossRep = False
        
        def check(reaction, user):
            global bossRep
            if str(reaction.emoji) == "👍":
                bossRep = True
                return user == rawMessage.author
            return user == rawMessage.author
        

        await client.wait_for("reaction_add", check=check, timeout=120)
        if bossRep == True:
            repTypeEmbed = discord.Embed(title="Boss rep types", description="Choose the number associated with what type of boss rep you are")
            repTypeMsg = await rankMsg.reply(content = "", embed=repTypeEmbed)

            for repTypeEmoji in repTypes.keys():
                repTypeRole = discord.utils.get(rawMessage.channel.guild.roles, name=repTypes[repTypeEmoji])
                if repTypeRole:
                    repTypeEmbed.add_field(name="", value=f'{repTypeEmoji} = {repTypeRole.mention}', inline=False)

            await repTypeMsg.edit(embed=repTypeEmbed)

            for repTypeEmoji in repTypes.keys():
                repTypeRole = discord.utils.get(rawMessage.channel.guild.roles, name=repTypes[repTypeEmoji])
                if repTypeRole:
                    await repTypeMsg.add_reaction(repTypeEmoji)



            global validRepTypeCheck
            global givenRepType
            validRepTypeCheck = False
            
            def check(reaction, user):
                global givenRepType
                global validRepTypeCheck

                givenRepType = str(reaction.emoji)
                if str(reaction.emoji) in repTypes:
                    validRepTypeCheck = True
                return user == rawMessage.author
            

            await client.wait_for("reaction_add", check=check, timeout=120)
            # if validRepTypeCheck == True:
            #     if givenRepType in repTypes.keys():
            #         userSpecifiedRepTypeRole = discord.utils.get(rawMessage.channel.guild.roles, name=repTypes[givenRepType])
            #         await rawMessage.author.add_roles(userSpecifiedRepTypeRole)

        #------------------------------


        formattedNickname = f'[{rankMsg.content.upper()}]{lastNameMsg.content.lower().title()}, {firstNameMsg.content.lower().title()}'


        reactionConfirmation = await rankMsg.reply(f'``Is this information correct?: {formattedNickname}``')
        await reactionConfirmation.add_reaction("👍")
        await reactionConfirmation.add_reaction("👎")
        
        global agreed
        agreed = False
        
        def check(reaction, user):
            global agreed
            if str(reaction.emoji) == "👍":
                agreed = True
            return user == rawMessage.author
        

        await client.wait_for("reaction_add", check=check, timeout=120)
        if agreed == True:
            await rawMessage.author.add_roles(verifiedRole)
            if bossRep == True and validRepTypeCheck == True:
                if givenRepType in repTypes.keys():
                    userSpecifiedRepTypeRole = discord.utils.get(rawMessage.channel.guild.roles, name=repTypes[givenRepType])
                    await rawMessage.author.add_roles(userSpecifiedRepTypeRole)

            try:
                await rawMessage.author.edit(nick=formattedNickname)
            except:
                await rawMessage.reply("Missing nickname permissions.")
            
            await rawMessage.reply(f'Successfully verified. Welcome, {formattedNickname}')
        else:
            await rawMessage.reply("Reuse the m?verify command to start over.")

