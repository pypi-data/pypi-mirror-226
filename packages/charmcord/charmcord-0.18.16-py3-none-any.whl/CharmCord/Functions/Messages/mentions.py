from CharmCord.CharmErrorHandling import CharmCordErrors
async def mentions(IDs, Context):
    try:
        return Context.message.mentions[int(IDs)]
    except ValueError:
        CharmCordErrors("Invalid ID in $mentions | Command..")