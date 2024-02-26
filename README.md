# Sysbot-Status
A custom Python Discord Bot script that will detect when a sysbot is online/offline.  

# *****__Bot Online/Offline Tracker:__*****
----------------------------------------------

Are you tired of changing your Sysbot's channel status between ✅ and ❌? This is the bot for you!

**Step 1) Bot Requirements**

- You must have a tradebot and a log channel for that bot for Sysbot Status Patrol to function correctly. Contact your bot developer and ask for a log channel made for this purpose. 

Example:  
Sv-TradeBot (Channel 1 where trades go through)

Sv-TradeBot Logs (Channel 2 where the bot logs everything)

## --------------------------------

**Step 2) Linking your Channels**

Input the command !logchannel followed by the bot's log channel and then the trade request channel you want changed from ❌ to ✅. This will allow Sysbot Status Patrol to change the channel's icon. *****Make sure to give this bot perms to manage the channel you want changed or it won't work!*****

Example:  `!logchannel #Sv-TradeBot-Logs #Sv-TradeBot`

**Remove Channels**

If you need to remove a channel from the list, simply run the command below

`!rlc #Sv-TradeBot-Logs #Sv-TradeBot` and replace the channels with your own that you have added in the command.



# Needed Permissions

- Do not give the bot any Admin or Ordinary Priveledges.  
- Only add the bot to the TradeBot Channel and Logging Channel

For TradeBot Channel, it needs the following:

![image](https://github.com/bdawg1989/Sysbot-Status/assets/80122551/b9b3d439-d6c3-43d5-a0d2-620cea210db3)

![image](https://github.com/bdawg1989/Sysbot-Status/assets/80122551/44837dc2-3757-4cad-a892-86599abc2e33)

![image](https://github.com/bdawg1989/Sysbot-Status/assets/80122551/7c3c1923-ae36-4d55-a51b-e0cc3447b22e)

![image](https://github.com/bdawg1989/Sysbot-Status/assets/80122551/b1b1dff4-79ab-4639-b53d-689fc28ca663)

![image](https://github.com/bdawg1989/Sysbot-Status/assets/80122551/09f7d950-442a-4e4c-8d39-bff75e4a538d)

**Important** - This bot will set the @everyone permission to deny anyone texting in the channel when it's closed.  And it will set it to allow @everyone when opened.
If you do not want it to change those permissions, set Manage Permissions to OFF for this bot.

![image](https://github.com/bdawg1989/Sysbot-Status/assets/80122551/514817ad-8d3b-4e00-8235-90613757adc7)

Any custom role you have set up for that channel **can** override the @everyone permission.  So make sure your custom roles **Send Messages** is set to **nuetral** for them to not be able to write in the channel when it's closed.


For the Log Channel:

![image](https://github.com/bdawg1989/Sysbot-Status/assets/80122551/293dc694-c186-4405-b556-4e1d6bc7b35e)

![image](https://github.com/bdawg1989/Sysbot-Status/assets/80122551/537ea4b4-f6a8-4a2d-86de-27754e9eb2c3)








Example screenshots below:

![image](https://github.com/bdawg1989/Sysbot-Status/assets/80122551/7338dd72-ea4e-4d80-b08a-29e04f2b7d5a)

![image](https://github.com/bdawg1989/Sysbot-Status/assets/80122551/056d436a-c7a5-49be-b1a8-4dccd93527ba)

![image](https://github.com/bdawg1989/Sysbot-Status/assets/80122551/6706a4a2-5ba5-4267-81ef-dd7da0eea23b)


# Important Links
Looking for a place to host your Bot?
[PebbleHost - $3/month](https://billing.pebblehost.com/aff.php?aff=2873)

Want to use my bot?
[Invite Link](https://discord.com/api/oauth2/authorize?client_id=1145124832497905724&permissions=0&scope=bot)
