
meta =
{
    -- ID of your mod; Make sure this is unique!
    -- Will be used for identifying the mod in dependency lists
    -- Will be changed to workshop ID (ensuring uniqueness) when you upload the mod to the workshop
    id = "1969102649",

    -- Name of your mod; You may want this to be unique, but it's not absolutely necessary.
    -- This is an additional helper attribute for you to easily identify your mod in the Mods() list
    name = "TradeExport",

    -- Title of your mod that will be displayed to players
    title = "TradeExport",

    -- Type of your mod, either "mod" or "factionpack"
    type = "mod",

    -- Description of your mod that will be displayed to players
    description = "Exports the trading goods data as .csv files, usable for data mining purposes ;).\n\nIt only exports the data you can see with the basic trading system. Export is triggered when one of your ships equiped with a trading system enters a sector. Data is only updated if a ship of yours visits a sector again.\n\nIt exports one .csv file per sector. The files are saved in `.avorion/moddata/` and are named `TradeExport-{galaxy_seed}-sector{x_coord}-{y_coord}.csv`. Rows have the following format:\n\n```\naction ('buy' or 'sell' to station); good; price; stock; max_stock; coord_x; coord_y; station; size (of good)\n```\n\nSectors without any trading goods generate empty files.\n\nThe datamining folder contains an python example for working with the exported data.\n\nNote: Mod is currently only tested running under linux. If you experience any problems don't hesitate to open an issue at https://github.com/cbasix/avorionTradeExport\n    ",

    -- Insert all authors into this list
    authors = {"masterix"},

    -- Version of your mod, should be in format 1.0.0 (major.minor.patch) or 1.0 (major.minor)
    -- This will be used to check for unmet dependencies or incompatibilities, and to check compatibility between clients and dedicated servers with mods.
    -- If a client with an unmatching major or minor mod version wants to log into a server, login is prohibited.
    -- Unmatching patch version still allows logging into a server. This works in both ways (server or client higher or lower version).
    version = "1.2.1",

    -- If your mod requires dependencies, enter them here. The game will check that all dependencies given here are met.
    -- Possible attributes:
    -- id: The ID of the other mod as stated in its modinfo.lua
    -- min, max, exact: version strings that will determine minimum, maximum or exact version required (exact is only syntactic sugar for min == max)
    -- optional: set to true if this mod is only an optional dependency (will only influence load order, not requirement checks)
    -- incompatible: set to true if your mod is incompatible with the other one
    -- Example:
    -- dependencies = {
    --      {id = "Avorion", min = "0.17", max = "0.21"}, -- we can only work with Avorion between versions 0.17 and 0.21
    --      {id = "SomeModLoader", min = "1.0", max = "2.0"}, -- we require SomeModLoader, and we need its version to be between 1.0 and 2.0
    --      {id = "AnotherMod", max = "2.0"}, -- we require AnotherMod, and we need its version to be 2.0 or lower
    --      {id = "IncompatibleMod", incompatible = true}, -- we're incompatible with IncompatibleMod, regardless of its version
    --      {id = "IncompatibleModB", exact = "2.0", incompatible = true}, -- we're incompatible with IncompatibleModB, but only exactly version 2.0
    --      {id = "OptionalMod", min = "0.2", optional = true}, -- we support OptionalMod optionally, starting at version 0.2
    -- },
    dependencies = {
        {id = "Avorion", min = "0.29", max = "1.40"}
    },

    -- Set to true if the mod only has to run on the server. Clients will get notified that the mod is running on the server, but they won't download it to themselves
    serverSideOnly = false,

    -- Set to true if the mod only has to run on the client, such as UI mods
    clientSideOnly = true,

    -- Set to true if the mod changes the savegame in a potentially breaking way, as in it adds scripts or mechanics that get saved into database and no longer work once the mod gets disabled
    -- logically, if a mod is client-side only, it can't alter savegames, but Avorion doesn't check for that at the moment
    saveGameAltering = false,

    -- Contact info for other users to reach you in case they have questions
    contact = "https://github.com/cbasix/avorionTradeExport",
}
