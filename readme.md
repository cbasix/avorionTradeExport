#Trade Export

*Mod for the space sandbox game [Avorion](http://www.avorion.net)*

Exports the trading goods data as .csv files, usable for data mining purposes ;). 

It only exports the data you can see with the basic trading system. 
Export is triggered when one of your ships equiped with a trading system enters a sector. 
Data is only updated if a ship of yours visits a sector again.

It exports one .csv file per sector. The files are saved in `.avorion/moddata/` and 
are named `TradeExport-{galaxy_seed}-sector{x_coord}-{y_coord}.csv`. Rows have the following format: 

```
action ('buy' or 'sell' to station); good; price; stock; max_stock; coord_x; coord_y; station; size (of good) 
```
Sectors without any trading goods generate empty files. 

The datamining folder contains an python example for working with the exported data.
Usage of the datamining example:

```bash
user@pc$ cd <path_to_steam_folder>/steamapps/workshop/content/445220/1969102649/datamining
user@pc$ pip3 install -r requirements.txt
user@pc$ python3 main.py <your_current_x_coordinate> <y_coordinate> find Acid

   good       station    x    y  margin   dist
0  Acid  Trading Post -366  232  2096   710.50

user@pc$ python3 main.py -366 235 routes

     good  buyX  buyY   buy  sellX  sellY  dist   sell  margin       win  cargoSpace   buyTotal  winPerCargo  winPerDist  winPerDistPerCargo  buyDist
0  Oxygen -366   232  97.00 -367    230   2.50  111.00  2676   37,464.00 2,676.00    259,572.00 14.00        14,985.60   5.60                3.00

user@pc$ python3 main.py -h
usage: main.py [-h] [--folder FOLDER] [--seed SEED] [--orderBy ORDERBY]
               [--limit LIMIT]
               x y {routes,route,find,findGood} ...

positional arguments:
  x                     Current position x-coordinate, from which distances
                        are measured.
  y                     Current position y-coordinate, from which distances
                        are measured.

optional arguments:
  -h, --help            show this help message and exit
  --folder FOLDER, -f FOLDER
                        The folder containing the .csv files to load
  --seed SEED           The seed of the galaxy to load the files for
  --orderBy ORDERBY, -o ORDERBY
                        Order in which entrys are displayed. Example 'win
                        DESC' for descending, 'dist ASC' for ascending
  --limit LIMIT, -l LIMIT
                        Number of routes to show

Sub-commands:
  {routes,route,find,findGood}
    routes (route)      Displays good trade routes according to the specified
                        criteria
    find (findGood)     Find a station selling the selected good

```

If you use this mod in multiple galaxies you must specify the `--seed <seed_of_your_galaxy>` parameter to load 
only the files of the specified galaxy. If more than one of your galaxies use the same seed, you are out of luck.
This mod can't handle that case. Your only possibility is to move the .csv files to subfolders and restore them 
on each switch between the galaxies.
