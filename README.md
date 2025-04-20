# Indigo RP Discord Bot

A Discord bot for the Indigo RP FiveM server community.

## Setup Instructions

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your configuration:
   ```bash
   cp .env.example .env
   ```
4. Edit the `.env` file with your Discord Bot Token

5. Run the bot:
   ```bash
   python bot.py
   ```

## Deployment Instructions

### Railway.app (Recommended)

1. Create a GitHub repository and push this code to it
2. Go to [Railway.app](https://railway.app/) and sign up with your GitHub account
3. Click "New Project" and select "Deploy from GitHub repo"
4. Select your repository
5. Add your environment variables:
   - Go to the "Variables" tab
   - Add `DISCORD_TOKEN` with your bot token
6. The bot will automatically deploy and restart when you push changes to GitHub

### Other Free Hosting Options

1. **Oracle Cloud Free Tier**
   - Offers always-free compute instances
   - More complex setup but completely free
   - No time limitations

2. **Google Cloud Platform**
   - Offers $300 free credit for 90 days
   - Can be set up with GitHub Actions for auto-deployment

3. **Replit**
   - Free tier available
   - Easy to use but may need periodic restarting
   - Can be set up with UptimeRobot to keep it running

## Features

### Reminders
The bot includes a comprehensive reminder system with the following slash commands:

- `/remind <time> <message>` - Set a one-time reminder
  - Example: `/remind 1h Take a break`
  - Time formats: 1min, 1h, 1d, 1w, etc.
  - Minimum: 1 minute
  - Maximum: 1 week

- `/remindme <time> <interval> <message>` - Set a recurring reminder
  - Example: `/remindme 1h 1d Daily check-in`
  - First reminder in 1 hour, then repeats every 1 day

- `/reminders` - List all your active reminders

- `/cancelreminder <id>` - Cancel a specific reminder by its ID

## Contributing

Feel free to submit issues and enhancement requests! 