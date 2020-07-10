from sklearn.cluster import AffinityPropagation

from random import randint

import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import os
import json

import discord
import logging
from discord.ext import commands

# Logger setup
logging.basicConfig(level=logging.INFO)

# Folders
FOLDER = "./data/"
if not os.path.isdir(FOLDER):
    os.mkdir(FOLDER)

# Token
FILE_TOKEN = FOLDER+'/token.json'
if os.path.isfile(FILE_TOKEN):
    file = open(file=FILE_TOKEN,mode="r",encoding="utf-8")
    dati_token = json.loads(file.read(),encoding="utf-8")
    file.close()
else:
    sys.exit("No tokenfile, aborting")

TOKEN = dati_token["discord_bot"]

# Command prefix structure
class CMD_Prefix:
    def __call__(self, bot, message):
        return "!"

# Get the bot
bot = commands.Bot(command_prefix="!")

# Handle ready event
@bot.event
async def on_ready():
    print(str(bot.user)+" has connected to Discord!")

    print("Listing managed guilds:")
    for guild in bot.guilds:
        print("- "+str(guild.name)+" ("+str(guild.id)+")")
        print("\n List of roles in the guild:")
        for role in guild.roles:
            print("  - "+str(role.name)+" ("+str(role.id)+")")
        print("")


# Handle joining a server
@bot.event
async def on_guild_join(guild):
    print("Joined guild "+str(guild.name)+" ("+str(guild.id)+")")


# Handle player join
@bot.event
async def on_member_join(member):
    # Log to terminal
    print(str(member.name)+" ("+str(member.id)+") has joined the guild '" +
          str(member.guild.name)+"' ("+str(member.guild.id)+")")
    
    # Greet the member
    #await member.create_dm()
    #await member.dm_channel.send(
    #   f'Salve {member.name}, benvenuto nel canale!\n'
    #)


# Handle messages
@bot.event
async def on_message(message):
    if message.author == bot.user:
        # Ignore bot message
        return

    if message.channel.type == discord.ChannelType.private:
        print(str(message.author.name) + " ("+str(message.author.id)+") sent <"+str(message.content)+"> on private channel ("+str(message.channel.id)+")")
    else:
        print(str(message.author.name) + " ("+str(message.author.id)+") sent <"+str(message.content)+"> on channel '"+str(message.channel.name) +
            "' ("+str(message.channel.id)+") of guild '"+str(message.channel.guild.name)+"' ("+str(message.channel.guild.id)+")")

    # Process commands overriden
    await bot.process_commands(message)


@bot.command(name="server_list",help="List monitored servers")
async def list_servers(ctx):
    print("servers command")

    # Prepare output
    text_output = ""

    # Read data
    f = open(file=FOLDER+"/gpsdata.json",mode="r")
    serverdata = json.loads(f.read(),encoding="utf-8")
    f.close()

    for server in serverdata["servers"]:
        text_output = text_output + server["name"] + "\n"

    await ctx.send("Listing all monitored servers:\n"+text_output)


@bot.command(name="gps_list",help="List all GPS coordinates of a server. Example <!gps_list server_name>")
async def gps_list(ctx, arg):
    print("add command")
    
    # Check command syntax
    if (arg == None) or (arg == ""):
        await ctx.send("Wrong format for !gps_list, please use:\n"+
                 "!gps_list server_name")

    # Read data
    f = open(file=FOLDER+"/gpsdata.json",mode="r")
    serverdata = json.loads(f.read(),encoding="utf-8")
    f.close()

    targetserver = None
    for server in serverdata["servers"]:
        if server["name"].strip().lower() == arg.strip().lower():
            targetserver = server
            break

    if targetserver == None:
        await ctx.send("Server '"+arg+"' not found!")
        return

    text_output = ""
    for gps in targetserver["gps"]:
        text_output = text_output + "GPS:" + gps["name"] + ":" + str(gps["x"]) + ":" + str(gps["y"]) + ":" + str(gps["z"]) + ":\n"

    await ctx.send("Listing all GPS for server "+targetserver["name"]+"\n"+text_output)


@bot.command(name="gps_add",help="Add a GPS coordinate to the system. Example <!gps_add server_name GPS_pasted_from_clipboard>")
async def add_gps(ctx, arg1, arg2):
    print("add command")
    
    # Check command syntax
    if (arg1 == None) or (arg1 == "") or (arg2 == None) or (arg2 == ""):
        await ctx.send("Wrong format for !gps_add, please use:\n"+
                 "!add server_name GPS_pasted_from_clipboard")

    gpsparse = arg2.split(":")
    if len(gpsparse) != 6:
        await ctx.send("Wrong format for gps data, please paste coordinates from clipboard")
        return

    gpsdict = dict()
    gpsdict["name"] = gpsparse[1]
    gpsdict["x"] = float(gpsparse[2])
    gpsdict["y"] = float(gpsparse[3])
    gpsdict["z"] = float(gpsparse[4])

    # Read data
    f = open(file=FOLDER+"/gpsdata.json",mode="r")
    serverdata = json.loads(f.read(),encoding="utf-8")
    f.close()

    targetserver = None
    for server in serverdata["servers"]:
        if server["name"].strip().lower() == arg1.strip().lower():
            targetserver = server
            break

    if targetserver == None:
        await ctx.send("Server '"+arg1+"' not found!")
        return

    targetserver["gps"].append(gpsdict)

    f = open(file=FOLDER+"/gpsdata.json",mode="w")
    f.write(json.dumps(serverdata,sort_keys=True,indent=4))
    f.close()

    print("Added coordinates ",arg2," to server ",arg1)
    await ctx.send("Coordinates "+arg2+" added to server "+arg1)


@bot.command(name="gps_remove",help="Remove a GPS coordinate to the system. Example <!gps_remove server_name GPS_pasted_from_clipboard>")
async def remove_gps(ctx, arg1, arg2):
    print("remove command")
    
    # Check command syntax
    if (arg1 == None) or (arg1 == "") or (arg2 == None) or (arg2 == ""):
        await ctx.send("Wrong format for !gps_remove, please use:\n"+
                 "!gps_remove server_name GPS_pasted_from_clipboard")

    gpsparse = arg2.split(":")
    if len(gpsparse) != 6:
        await ctx.send("Wrong format for gps data, please paste coordinates from clipboard")
        return

    gpsdict = dict()
    gpsdict["name"] = gpsparse[1]
    gpsdict["x"] = float(gpsparse[2])
    gpsdict["y"] = float(gpsparse[3])
    gpsdict["z"] = float(gpsparse[4])

    # Read data
    f = open(file=FOLDER+"/gpsdata.json",mode="r")
    serverdata = json.loads(f.read(),encoding="utf-8")
    f.close()

    targetserver = None
    for server in serverdata["servers"]:
        if server["name"].strip().lower() == arg1.strip().lower():
            targetserver = server
            break

    if targetserver == None:
        await ctx.send("Server '"+arg1+"' not found!")
        return

    targetgps = None
    for gps in targetserver["gps"]:
        if (gps["name"] == gpsdict["name"]) and (gps["x"] == gpsdict["x"]) and (gps["y"] == gpsdict["y"]) and (gps["z"] == gpsdict["z"]):
            targetgps = gps

    if targetgps == None:
        await ctx.send("GPS '"+arg2+"' not found!")
        return

    targetserver["gps"].remove(targetgps)

    f = open(file=FOLDER+"/gpsdata.json",mode="w")
    f.write(json.dumps(serverdata,sort_keys=True,indent=4))
    f.close()

    print("Removed coordinates ",arg2," to server ",arg1)
    await ctx.send("Coordinates "+arg2+" removed from server "+arg1)


@bot.command(name="draw",help="Compute and draw the centroids on screen. Example <!draw server_name>")
async def draw(ctx, arg):
    print("draw command")

    # Check command syntax
    if (arg == None) or (arg == ""):
        await ctx.send("Wrong format for !draw, please use:\n"+
                 "!draw server_name")

    # Read data
    f = open(file=FOLDER+"/gpsdata.json",mode="r")
    serverdata = json.loads(f.read(),encoding="utf-8")
    f.close()

    targetserver = None
    for server in serverdata["servers"]:
        if server["name"].strip().lower() == arg.strip().lower():
            targetserver = server
            break

    if targetserver == None:
        await ctx.send("Server '"+arg+"' not found!")
        return

    # Init text output
    text_output = ""
    
    # Init plot
    fig = plt.figure()
    ax = plt.axes(projection="3d")

    x = list()
    y = list()
    z = list()
    datamatrix = list()

    for gps in targetserver["gps"]:
        datamatrix.append([gps["x"],gps["y"],gps["z"]])

    # Run clustering algorithm
    af = AffinityPropagation().fit(datamatrix)

    cluster_centers_indices = af.cluster_centers_indices_
    labels = af.labels_
    n_clusters_ = len(cluster_centers_indices)

    print('Estimated number of clusters: %d' % n_clusters_)
    print("Estimated GPS coordinates of centroids:")

    text_output = text_output + 'Estimated number of clusters: '+str(n_clusters_)+"\n"
    text_output = text_output + "Estimated GPS coordinates of centroids:\n"
    
    counter = 0
    for center in af.cluster_centers_:
        print("GPS:Cluster "+str(counter)+":"+str(center[0])+":"+str(center[1])+":"+str(center[2])+":")
        text_output = text_output + "GPS:Cluster "+str(counter)+":"+str(center[0])+":"+str(center[1])+":"+str(center[2])+":\n"
        counter = counter+1

    clusterlist = list()
    for i in range(n_clusters_):
        clusterlist.append([list(),list(),list()])
    clustercolors = cm.rainbow(np.linspace(0, 1, n_clusters_))

    counter = 0
    for item in labels:
        clusterlist[item][0].append(datamatrix[counter][0])
        clusterlist[item][1].append(datamatrix[counter][1])
        clusterlist[item][2].append(datamatrix[counter][2])
        counter = counter + 1
        
    # Draw plot
    for cluster in range(n_clusters_):
        ax.scatter(clusterlist[cluster][0],clusterlist[cluster][1],clusterlist[cluster][2],
                   color=clustercolors[cluster],marker='.',alpha=0.3,label=str(cluster))

    counter = 0
    for center in af.cluster_centers_:
        ax.scatter(center[0],center[1],center[2],
                   color=clustercolors[counter],marker='v',alpha=1)
        counter = counter+1

    ax.legend()
    plt.title('Estimated number of clusters: %d' % n_clusters_)

    print("Draw command saving")
    plt.savefig("plot.png")
    #plt.show()

    await ctx.send(content="Displaying clusters for server "+targetserver["name"]+"\n"+text_output,file=discord.File("plot.png"))

# Finally run the bot
bot.run(TOKEN)
