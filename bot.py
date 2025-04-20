import discord
from discord.ext import commands
import config
import logging
import sys
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('IndigoBot')

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=config.BOT_PREFIX, intents=intents)

@bot.event
async def on_ready():
    logger.info(f'Bot is ready! Logged in as {bot.user.name} ({bot.user.id})')
    await bot.change_presence(activity=discord.Game(name="Reminders | Indigo RP"))
    
    # Load the reminders cog
    try:
        await bot.load_extension('cogs.reminders')
        logger.info('Loaded reminders cog')
        
        # Sync slash commands
        synced = await bot.tree.sync()
        logger.info(f'Synced {len(synced)} slash commands')
    except Exception as e:
        logger.error(f'Failed to load reminders cog: {e}')

@bot.event
async def on_member_join(member):
    if config.WELCOME_CHANNEL_ID:
        channel = bot.get_channel(config.WELCOME_CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                title="Welcome to Indigo RP!",
                description=f"Welcome {member.mention} to the Indigo RP community!",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await channel.send(embed=embed)

@bot.command(name='ping')
async def ping(ctx):
    """Check the bot's latency"""
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! Latency: {latency}ms')

@bot.command(name='serverinfo')
async def serverinfo(ctx):
    """Display server information"""
    guild = ctx.guild
    embed = discord.Embed(
        title=f"{guild.name} Server Information",
        color=discord.Color.blue()
    )
    embed.add_field(name="Server ID", value=guild.id, inline=True)
    embed.add_field(name="Created On", value=guild.created_at.strftime("%B %d, %Y"), inline=True)
    embed.add_field(name="Member Count", value=guild.member_count, inline=True)
    embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    await ctx.send(embed=embed)

@bot.command(name='userinfo')
async def userinfo(ctx, member: discord.Member = None):
    """Display user information"""
    member = member or ctx.author
    embed = discord.Embed(
        title=f"User Information - {member.name}",
        color=member.color
    )
    embed.add_field(name="User ID", value=member.id, inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%B %d, %Y"), inline=True)
    embed.add_field(name="Account Created", value=member.created_at.strftime("%B %d, %Y"), inline=True)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await ctx.send(embed=embed)

def run_bot():
    """Run the bot"""
    try:
        bot.run(config.BOT_TOKEN)
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_bot() 