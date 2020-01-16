#Trade Export

*Mod for the space sandbox game [Avorion](http://www.avorion.net)*

Exports the trading goods data as .csv files usable for data mining purposes ;). 

It only exports the data you can see with the basic trading system. 
That means only the current sector. Export is only triggered when the trading data is 
viewed via the trading system. It is meant as an alternative to use screenshots or 
paper to save the seen good prices. Data is only updated if you visit a sector 
again and use the trading system. 

It exports one .csv file per sector. The files are saved in `.avorion/moddata/TradeExport/` and 
are named `sector{x-coord}-{y-coord}.csv`. Rows have the following format: 

```
action ('buy' or 'sell' to station); good; price; stock; max_stock; coord_x; coord_y; station; size (of good) 
```
Sectors without any trading goods generate empty files. 

The datamining folder contains an python example for working with the exported data.\n",
