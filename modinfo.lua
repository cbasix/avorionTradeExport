
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

    -- Description of your mod that will be displayed to players
    description = [[
Exports the trading goods data as .csv files, usable for data mining purposes ;).

It only exports the data you can see with the basic trading system.  That means only the current sector. Export is only triggered when the trading data is viewed via the trading system. It is meant as an alternative to use screenshots or paper to save the seen good prices. Data is only updated if you visit a sector again and use the trading system.

It exports one .csv file per sector. The files are saved in `.avorion/moddata/` and are named `TradeExport-{galaxy_seed}-sector{x_coord}-{y_coord}.csv`. Rows have the following format:

```
action ('buy' or 'sell' to station); good; price; stock; max_stock; coord_x; coord_y; station; size (of good)
```

Sectors without any trading goods generate empty files.

The datamining folder contains an python example for working with the exported data.

Note: Mod is currently only tested running under linux. If you experience any problems don't hesitate to open an issue at https://github.com/cbasix/avorionTradeExport
    ]],

    -- Insert all authors into this list
    authors = {"masterix"},

    -- Version of your mod, should be in format 1.0.0 (major.minor.patch) or 1.0 (major.minor)
    -- This will be used to check for unmet dependencies or incompatibilities
    version = "1.1",

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
        {id = "Avorion", min = "0.29", max = "0.30.1"}
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
