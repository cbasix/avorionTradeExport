import pandas as pd
import glob
import os
import sys
from pandasql import sqldf


def main(args):
    # instruct pandas to show the full dataset without abbreviations
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)
    pd.options.display.float_format = '{:,.2f}'.format  # use , as thousand separator

    # load data and prepare some intermediate tables
    data = load_csv_files(args.folder, args.seed)
    data = add_margin_column(data)
    data_sector = group_by_sector(data)

    if args.cmd == 'routes':
        print(find_trade_routes(data_sector, args.x, args.y,
                                order_by=args.orderBy if args.orderBy is not None else 'win DESC',
                                limit=args.limit,
                                min_win=args.minWin,
                                max_budget=args.maxBudget,
                                max_dist=args.maxDist,
                                max_start_dist=args.maxStartDist))

    elif args.cmd == 'find':
        print(find_good(data, args.x, args.y, args.good,
                        order_by=args.orderBy if args.orderBy is not None else 'dist ASC',
                        limit=args.limit))

    else:
        print('No sub-command specified')
        args.print()


def add_margin_column(data):
    # add margin to dataset, for 'buy from station' -> stock; for 'sell to station' -> max_stock - stock
    return sqldf("""
        select *, 
        CASE action
             WHEN 'buy' THEN stock
             WHEN 'sell' THEN (max_stock-stock)
             ELSE 0 
        END as margin
        FROM data
    """, locals())


def group_by_sector(data):
    # combine all factories per sector
    return sqldf("""
        select action,
                good, 
                x,
                y, 
                sum(margin) as margin, 
                size,
                sum(margin*price) / sum(margin) as price
           from data 
           GROUP BY action, good, x, y, size
    """, locals())


def find_trade_routes(data_sector, x, y, max_dist, max_start_dist, max_budget,
                      min_win, order_by, limit):

    buy_sector = sqldf("select * from data_sector where action = 'buy'", locals())  # buy from stations, grouped by sector
    sell_sector = sqldf("select * from data_sector where action = 'sell'", locals())  # sell to stations, grouped by sector

    # find good trade routes for less than 15M initial buy
    return sqldf("""
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
                (sell.price*min(sell.margin, buy.margin) - buy.price*min(sell.margin, buy.margin)) / (MAX(ABS(sell.x - buy.x), ABS(sell.y - buy.y)) + 0.5 * MIN(ABS(sell.x - buy.x), ABS(sell.y - buy.y))) / (buy.size*min(sell.margin, buy.margin)) as winPerDistPerCargo,
                MAX(ABS({x} - buy.x), ABS({y} - buy.y)) + 0.5 * MIN(ABS({x} - buy.x), ABS({y} - buy.y)) AS buyDist
           from buy_sector as buy
           JOIN sell_sector as sell on buy.good = sell.good 

           WHERE buy.price < sell.price
           AND win > {min_win}
           AND buyTotal < {max_budget}
           and dist < {max_dist}
           and buyDist < {max_start_dist}
           ORDER BY {orderBy} 
           LIMIT {limit} 
           """.format(x=x, y=y, min_win=min_win, max_budget=max_budget, max_dist=max_dist,
                      max_start_dist=max_start_dist, orderBy=order_by, limit=limit), locals())


def find_good(data, x, y, good, limit=15, order_by='dist DESC'):
    buy = sqldf("select * from data where action = 'buy'")
    return sqldf("""
          select 
          good,
          station,
          buy.x,
          buy.y,
          margin,
          MAX(ABS({x} - buy.x), ABS({y} - buy.y)) + 0.5 * MIN(ABS({x} - buy.x), ABS({y} - buy.y)) AS dist
          from buy
          where good = '{good}'
          order by {order_by}
          LIMIT {limit}
      """.format(x=x, y=y, good=good, limit=limit, order_by=order_by), locals())


def load_csv_files(folder, seed):
    file_list = glob.glob(os.path.join(folder, "TradeExport-{seed}-sector*.csv".format(seed=seed)))

    # build pandas data frame from all csv files
    li = []
    for filename in file_list:
        df = pd.read_csv(filename, index_col=None, header=None, sep=";",
                         names=['action', 'good', 'price', 'stock', 'max_stock', 'x', 'y', 'station', 'size'])
        li.append(df)
    return pd.concat(li, axis=0, ignore_index=True)


if __name__ == '__main__':
    import argparse

    if sys.platform.startswith('linux'):
        folder = os.path.expanduser("~/.avorion/moddata/")

    elif sys.platform.startswith('win32'):
        folder = os.path.join(os.path.expandvars("%AppData%"), "Avorion", "moddata")

    else:
        raise Exception("Unsupported OS: " + sys.platform)

    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', "-f", help='The folder containing the .csv files to load', default=folder)
    parser.add_argument('--seed', help='The seed of the galaxy to load the files for', default="*")
    parser.add_argument('x', type=int, help='Current position x-coordinate, from which distances are measured. ')
    parser.add_argument('y', type=int, help='Current position y-coordinate, from which distances are measured. ')
    parser.add_argument('--orderBy', '-o',
                        help='Order in which entrys are displayed. Example \'win DESC\' for descending,  \'dist ASC\' '
                             'for ascending')
    parser.add_argument('--limit', '-l', type=int, default=15, help='Number of routes to show')
    subparsers = parser.add_subparsers(title='Sub-commands', dest='cmd')

    # create the parser for the "routes" command
    parser_a = subparsers.add_parser('routes', aliases=['route'],
                                     help='Displays good trade routes according to the specified criteria')

    parser_a.add_argument('--maxStartDist', '-s', type=int,
                          help='Maximal distance to the start (=buy) point of the route. Needs -x and -y to be set', default=999999999)
    parser_a.add_argument('--maxDist', '-d', type=int,
                          help='Maximal distance between start and end of route. Needs -x and -y to be set', default=999999999)
    parser_a.add_argument('--maxBudget', '-b', type=int, help='Maximal cost allowed for the initial buy', default=999999999)
    parser_a.add_argument('--minWin', '-w', type=int, help='Minimal profit allowed', default=0)

    # create the parser for the "find" command
    parser_b = subparsers.add_parser('find', aliases=['findGood'],
                                     help='Find a station selling the selected good')
    parser_b.add_argument('good', help='The good you want to buy')
    parser_b.add_argument('--maxDist', type=int, help='Max distance to station')
    parser_b.add_argument('--minMargin', choices='XYZ', help='Min amount of the selected good')

    parsed_args = parser.parse_args()

    main(parsed_args)
