# How to Contribute

Realistically in order to contribute you must be a part of the Nexus Aurora Discord server. To join you should follow the instructions [here](https://nexusaurora.com/pages/discord). From there you can ask for help or an assignment in [#programming-lounge](https://discord.com/channels/702336499307511898/717673469709516801) or [#web-nexus-bot](https://discord.com/channels/702336499307511898/717309475618553927).

## Coding Conventions

We use the [PEP 8](https://www.python.org/dev/peps/pep-0008/) standard for python code. All code should be linted with [autopep8](https://pypi.org/project/autopep8/) before commiting.

## Feature Branches

To contribute to the project, you should fork the repository and make a new branch off of develop. You can then make all your changes and open a pull request when you're finished.

## Developing Extensions

The project is based around discord.py and its [extension architecture](https://discordpy.readthedocs.io/en/latest/ext/commands/extensions.html) which allows changes to be made to the bot without ever restarting. This means that [its documentation](https://discordpy.readthedocs.io/en/latest/index.html) and especially that on [the commands extension](https://discordpy.readthedocs.io/en/latest/ext/commands/index.html) is your best friend. A simple extension would look something like this:

``` python
from discord.ext import commands

class PingPong(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def Ping(self, ctx):
        """Ping the bot"""
        return await ctx.send('Pong!')

    @commands.command()
    async def Pong(self, ctx):
        """Pong the bot"""
        return await ctx.send('Ping!')

def setup(bot):
    bot.add_cog(PingPong(bot))
```

First we define a Cog with a couple commands and then we attach it to the bot in `setup()` . The `setup()` function is a special function that runs when the extension is loaded. There is also `teardown()` which runs when the extension is unloaded. When loading an extension, the name is dot-qualified, so our extension `extensions/pingpong.py` would be loaded as `extensions.pingpong` .

---
Bot Reference: In the following passages, the variable `bot` is referring to the instance of `discordbot.Bot` we that is created and passed to each extension in `setup()` . In most cases you can get a reference to it using `ctx.bot` or `self.bot` .

### Naming

Extensions are all lowercase and no distinction is given between words, so "wanderingllama" would be a correct name, but "wandering_llama, " "wanderingLlama, " "WanderingLlama, " and "wandering-llama" would not. Cog and command names should be CamelCase starting with a capital letter, so "StartWandering" would be a correct name for a command. If an extension has only one cog or command, it is usually named similarly to the extension, but it doesn't have to be.

### Docstrings

Every command should have a docstring so the help command can have a helpful and intelligent output for users who can't be bothered to try and figure out what the command does themselves. Here's an example:

``` python
@commands.command()
    async def Ping(self, ctx):
        """Ping the bot""" # <-- This is the docstring. It'll be included in the help command output.
        return await ctx.send('Pong!')
```

or if you have arguments,

``` python
@commands.command()
    async def TableTennis(self, ctx, count: int, delay: int):
        """Set roles which can run a command

        Args:
            count: Number of volleys.
            delay: Time in seconds between volleys.
        """
        tasks.Loop(self.volley, seconds=delay, count=count)
```

### Configuration

Configuration for the bot is stored in [config.json](./config.json.template). Key names should be snake-case with hyphens. You should store any configuration your bot needs there like this:

``` json
{
    "token": "your bot token",
    "bot-prefix": "bot command prefix",
    "guild-id": your guild id,
    "extensions": ["your list of extensions"],
    "extension-data": {
        "rolemgr": {"role-setup-channel-id": 0},
        "extension name": {"whatever": "arbitrary json"}
    }
}
```

You can access all config data as a `dict` in `bot.config` . For example if your extension's name was "mememaker" you could access your own data at `bot.config['extension-data']['mememaker']` .

### Databases

We are currently using [TinyDB](https://tinydb.readthedocs.io/en/latest/) for extensions which need a database. **This is subject to change** so it is advisable not to use obscure features of TinyDB. The database is stored in `bot.db` . **Do not use the default table**, instead create your own table using `bot.db.table('<your extension name>-<table name>')` . For instance, if I was creating an extension to kick users who've been active for a week I would store their activity data in a table named `kickinactive-users` or similar. I could get a reference to this table using `bot.db.table('kickinactive-users')`.
