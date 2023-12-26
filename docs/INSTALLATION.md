# Installation

# Requirements 

* Python
* Discord

# Python packages

* discord
* yfinance

# Installing Python Dependencies
```zsh
pip install yfinance
pip install discord
```

# Cloning This Repository
```zsh
git clone https://github.com/demeil1/discord_stocksim_bot
```
# Creating Discord Bot
1. Go to discord developer portal: https://discord.com/developers/docs/intro
2. Log in
3. Click on applications tab
4. Click "new application" in the top right corner
5. Give the bot a name and agree to discord's terms of service
6. Click on the "OAuth2" tab
7. Scroll down to the "Authorization Method" drop down menu and select "in-app authorization"
8. In the "scopes" check list, click on the "bot" button
9. Scroll down to "bot permissons"
10. Tick of every box except administrator, the "text permissions" session is absolutely necessary. Other aspects may be used in future updates. (save changes)
11. Click on the "url generator" tab
12. In the "scopes" section, select bot, and in the bot permissions section reselect the same permission as you did in step 10.
13. Copy the "generated url" at the bottom of the page and put it somewhere safe
14. Click on the bot tab
15. Find the "priviliged gateway intents" section and check each button (save changes)
16. At the top of the page click on "reset token"
17. Copy the token and store it with your url that was generated
18. Paste the url generated in the discord developer portal into your browser and invite it into a server

# Configuring discord_stocksim_bot Files
1. open the bot_config.py file in the discord_stocksim_bot/src directory
2. replace "TOKEN" with the token from the discord developer portal

# Getting Slash Commands Working
```zsh
# Run the discord_stocksim_bot making sure you are in the discord_stocksim_bot directory
# This will sync the commands with discord
python3 main.py
```  
1. Open discord and go into the sever the bot was invited token
2. In the top left with the server's name, click on the drop down menu
3. Click on server settings
4. In the "Apps" section, click on intergrations
5. Find your bot in the "bots and apps" section and click on "manage"
6. Scroll down to "commands" and give discord a list of channels you would like the bot to work in
7. Restart the bot

Congratulations! You just got the discord_stocksim_bot working in your server!

# Uninstalling

```zsh
# Run this command in the terminal
# in the directory where discord_stocksim_bot
# is stored
rm -rf discord_stocksim_bot
```  