import pandas as pd
import glob
import os
import sys

from pandasql import sqldf
sql = lambda q: sqldf(q, globals())

if __name__ == '__main__':
    if sys.platform.startswith('linux'):
        avorion_data_path = os.path.expanduser("~/.avorion/")

    elif sys.platform.startswith('win32'):
        avorion_data_path = os.path.expandvars("%AppData%/Avorion")

    else:
        raise Exception("Unsupported OS: " + sys.platform)

    # instruct pandas to show the full dataset without abbreviations
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)
    pd.options.display.float_format = '{:,.2f}'.format  # use , as thousand separator

    # must be changed
    all_files = glob.glob(os.path.join(avorion_data_path, "moddata/TradeExport/sector*.csv"))
    # print(all_files)

    # build data frame from all csv files
    li = []
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=None, sep=";", names=['action', 'good', 'price', 'stock', 'max_stock', 'x', 'y', 'station', 'size'])
        li.append(df)
    data = pd.concat(li, axis=0, ignore_index=True)

    # add margin to dataset
    data = sql("""
        select *, 
        CASE action
             WHEN 'buy' THEN stock
             WHEN 'sell' THEN (max_stock-stock)
             ELSE 0 
        END as margin
        FROM data
    """)

    # combine all factories per sector
    data_sector = sql("""
        select action,
                good, 
                x,
                y, 
                sum(margin) as margin, 
                size,
                sum(margin*price) / sum(margin) as price
           from data 
           GROUP BY action, good, x, y, size
    """)
    # print(data_sector)


    # split up buy from station and sell to station goods
    buy = sql("select * from data where action = 'buy'")
    buy_sector = sql("select * from data_sector where action = 'buy'")
    # print(buy_sector)

    sell = sql("select * from data where action = 'sell'")
    sell_sector = sql("select * from data_sector where action = 'sell'")
    # print(sell_sector)


    # find good trade routes for less than 15M initial buy
    sector_margins = sql("""
           select 
                buy.good, 
                buy.x as buyX, 
                buy.y AS buyY, 
                buy.price AS buy,
                sell.x AS sellX, 
                sell.y AS sellY, 
                MAX(ABS(sell.x - buy.x), ABS(sell.y - buy.y)) + 0.5 * MIN(ABS(sell.x - buy.x), ABS(sell.y - buy.y)) AS dist,
                sell.price AS sell,
                min(sell.margin, buy.margin)AS margin,
                sell.price*min(sell.margin, buy.margin) - buy.price*min(sell.margin, buy.margin) as win,
                buy.size*min(sell.margin, buy.margin) AS cargoSpace,
                buy.price*min(sell.margin, buy.margin) AS buyTotal,
                (sell.price*min(sell.margin, buy.margin) - buy.price*min(sell.margin, buy.margin)) / (buy.size*min(sell.margin, buy.margin)) AS winPerCargo,
                (sell.price*min(sell.margin, buy.margin) - buy.price*min(sell.margin, buy.margin)) / (MAX(ABS(sell.x - buy.x), ABS(sell.y - buy.y)) + 0.5 * MIN(ABS(sell.x - buy.x), ABS(sell.y - buy.y))) as winPerDist,
                (sell.price*min(sell.margin, buy.margin) - buy.price*min(sell.margin, buy.margin)) / (MAX(ABS(sell.x - buy.x), ABS(sell.y - buy.y)) + 0.5 * MIN(ABS(sell.x - buy.x), ABS(sell.y - buy.y))) / (buy.size*min(sell.margin, buy.margin)) as winPerDistPerCargo
           from buy_sector as buy
           JOIN sell_sector as sell on buy.good = sell.good 

           WHERE buy.price < sell.price
           --AND win > 800000
           --AND buyTotal < 15000000
           and dist < 100
           --ORDER BY winPerDistPerCargo DESC
           ORDER BY win DESC
           LIMIT 25 
           """)
    print(sector_margins)


def search_good(x, y, good):
    print(sql("""
          select 
          good,
          station,
          buy.x,
          buy.y,
          margin,
          MAX(ABS({x} - buy.x), ABS({y} - buy.y)) + 0.5 * MIN(ABS({x} - buy.x), ABS({y} - buy.y)) AS dist
          from buy
          where good = '{good}'
          order by dist asc
      """.format(x=x, y=y, good=good)))


def manual():
    # x = 271
    x = 298
    # y = -11
    y = 30
    # good = 'Laser Compressor'
    # good = 'Laser Modulator'
    # good = 'High Capacity Lens'
    # good = 'Conductor'
    good = 'Steel'
    search_good(good, x, y)
