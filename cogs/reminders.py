import discord
from discord.ext import commands, tasks
from discord import app_commands
import humanfriendly
import asyncio
from datetime import datetime, timedelta
import pytz
import json
import os

class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders_file = 'data/reminders.json'
        self.reminders = {}
        self.load_reminders()
        self.check_reminders.start()

    def load_reminders(self):
        """Load reminders from file"""
        os.makedirs('data', exist_ok=True)
        if os.path.exists(self.reminders_file):
            with open(self.reminders_file, 'r') as f:
                self.reminders = json.load(f)
        else:
            self.save_reminders()

    def save_reminders(self):
        """Save reminders to file"""
        with open(self.reminders_file, 'w') as f:
            json.dump(self.reminders, f, indent=4)

    @tasks.loop(seconds=30)
    async def check_reminders(self):
        """Check for due reminders"""
        current_time = datetime.now(pytz.UTC)
        to_remove = []

        for reminder_id, reminder in self.reminders.items():
            reminder_time = datetime.fromisoformat(reminder['time'])
            if current_time >= reminder_time:
                channel = self.bot.get_channel(reminder['channel_id'])
                if channel:
                    user = self.bot.get_user(reminder['user_id'])
                    if user:
                        embed = discord.Embed(
                            title="⏰ Reminder!",
                            description=reminder['message'],
                            color=discord.Color.blue()
                        )
                        embed.set_footer(text=f"Set by {user.name}")
                        await channel.send(content=user.mention, embed=embed)
                
                if reminder.get('recurring'):
                    # Calculate next reminder time
                    interval = humanfriendly.parse_timespan(reminder['interval'])
                    next_time = reminder_time + timedelta(seconds=interval)
                    reminder['time'] = next_time.isoformat()
                else:
                    to_remove.append(reminder_id)

        # Remove non-recurring reminders that have been triggered
        for reminder_id in to_remove:
            del self.reminders[reminder_id]
        
        if to_remove:
            self.save_reminders()

    @check_reminders.before_loop
    async def before_check_reminders(self):
        await self.bot.wait_until_ready()

    @app_commands.command(name='remind', description='Set a one-time reminder')
    @app_commands.describe(
        time='When to remind you (e.g., 1min, 1h, 1d, 1w)',
        message='What to remind you about'
    )
    async def remind(self, interaction: discord.Interaction, time: str, message: str):
        """Set a one-time reminder"""
        try:
            # Parse the time interval
            seconds = humanfriendly.parse_timespan(time)
            if seconds < 60:  # Minimum 1 minute
                await interaction.response.send_message("Please set a reminder for at least 1 minute.", ephemeral=True)
                return
            if seconds > 604800:  # Maximum 1 week
                await interaction.response.send_message("Please set a reminder for no more than 1 week.", ephemeral=True)
                return

            reminder_time = datetime.now(pytz.UTC) + timedelta(seconds=seconds)
            reminder_id = str(len(self.reminders) + 1)

            self.reminders[reminder_id] = {
                'user_id': interaction.user.id,
                'channel_id': interaction.channel_id,
                'message': message,
                'time': reminder_time.isoformat(),
                'recurring': False
            }
            self.save_reminders()

            embed = discord.Embed(
                title="✅ Reminder Set",
                description=f"I'll remind you about: {message}",
                color=discord.Color.green()
            )
            embed.add_field(name="Time", value=time)
            await interaction.response.send_message(embed=embed)

        except humanfriendly.InvalidTimespan:
            await interaction.response.send_message(
                "Invalid time format. Please use formats like: 1min, 1h, 1d, 1w",
                ephemeral=True
            )

    @app_commands.command(name='remindme', description='Set a recurring reminder')
    @app_commands.describe(
        time='When to start the reminder (e.g., 1min, 1h, 1d, 1w)',
        interval='How often to repeat (e.g., 1min, 1h, 1d, 1w)',
        message='What to remind you about'
    )
    async def remindme(self, interaction: discord.Interaction, time: str, interval: str, message: str):
        """Set a recurring reminder"""
        try:
            # Parse the time interval
            seconds = humanfriendly.parse_timespan(time)
            if seconds < 60:  # Minimum 1 minute
                await interaction.response.send_message("Please set a reminder for at least 1 minute.", ephemeral=True)
                return
            if seconds > 604800:  # Maximum 1 week
                await interaction.response.send_message("Please set a reminder for no more than 1 week.", ephemeral=True)
                return

            reminder_time = datetime.now(pytz.UTC) + timedelta(seconds=seconds)
            reminder_id = str(len(self.reminders) + 1)

            self.reminders[reminder_id] = {
                'user_id': interaction.user.id,
                'channel_id': interaction.channel_id,
                'message': message,
                'time': reminder_time.isoformat(),
                'recurring': True,
                'interval': interval
            }
            self.save_reminders()

            embed = discord.Embed(
                title="✅ Recurring Reminder Set",
                description=f"I'll remind you about: {message}",
                color=discord.Color.green()
            )
            embed.add_field(name="Initial Time", value=time)
            embed.add_field(name="Repeat Every", value=interval)
            await interaction.response.send_message(embed=embed)

        except humanfriendly.InvalidTimespan:
            await interaction.response.send_message(
                "Invalid time format. Please use formats like: 1min, 1h, 1d, 1w",
                ephemeral=True
            )

    @app_commands.command(name='reminders', description='List all your active reminders')
    async def list_reminders(self, interaction: discord.Interaction):
        """List all your active reminders"""
        user_reminders = {
            k: v for k, v in self.reminders.items()
            if v['user_id'] == interaction.user.id
        }

        if not user_reminders:
            await interaction.response.send_message("You have no active reminders.", ephemeral=True)
            return

        embed = discord.Embed(
            title="Your Active Reminders",
            color=discord.Color.blue()
        )

        for reminder_id, reminder in user_reminders.items():
            time = datetime.fromisoformat(reminder['time'])
            time_str = time.strftime("%Y-%m-%d %H:%M:%S UTC")
            status = "Recurring" if reminder.get('recurring') else "One-time"
            embed.add_field(
                name=f"Reminder #{reminder_id} ({status})",
                value=f"Message: {reminder['message']}\nTime: {time_str}",
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name='cancelreminder', description='Cancel a specific reminder')
    @app_commands.describe(reminder_id='The ID of the reminder to cancel')
    async def cancel_reminder(self, interaction: discord.Interaction, reminder_id: str):
        """Cancel a reminder by its ID"""
        if reminder_id in self.reminders:
            if self.reminders[reminder_id]['user_id'] == interaction.user.id:
                del self.reminders[reminder_id]
                self.save_reminders()
                await interaction.response.send_message(
                    f"✅ Reminder #{reminder_id} has been cancelled.",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "You can only cancel your own reminders.",
                    ephemeral=True
                )
        else:
            await interaction.response.send_message(
                "Reminder not found. Use /reminders to see your active reminders.",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Reminders(bot)) 