"""
Author: Anton Scheutz Godin

This code solves the following problem:
"Write something in any language that figures out at what date and at what price to buy and sell the
index in order to get the highest return. Only one buy and one sell transaction is allowed.
Should work in O(n)"

Output:
Buy at 1247 (date: 20160628)
Sell at 1468.16 (date: 20161011)
"""

import json
import requests



def load_price_history_data(url="http://www.modularfinance.se/api/puzzles/index-trader.json"):
    """
    Loads price history data from the puzzle API and returns it as a list of dict
    """
    r = requests.get(url)
    return json.loads(r.content)['data'][::-1]


def get_optimal_interval(price_history):
    """
    This function takes a list of dicts (each at least containing the keys 'high', 'low', 'quote_date'),
    and returns the optimal time buy and sell the stock, given that only one buy and one sell transaction
    is allowed.

    Time complexity: O(n)
    """

    if len(price_history) == 0:
        raise ValueError('Empty dataset')

    elif len(price_history) == 1:  # trivial case
        return {'buy': price_history[0], 'sell': price_history[0]}

    else:
        buy = price_history[0]
        sell = price_history[0]
        difference = 0  # the difference between sell and buy price.

        for day in price_history:

            # First, we continuously keep track of the lowest price point we have seen so far
            if buy['open'] > day['low']:
                buy = day

            # Second, evaluate if the period [buy, current_day_in_loop] is the most attractive investment
            # we have seen so far
            if day['high'] - buy['low'] > difference:
                difference = day['high'] - buy['low']
                sell = day

        return {'buy': {'date': buy['quote_date'], 'price': buy['low']},
                'sell': {'date': sell['quote_date'], 'price': sell['high']}
                }


if __name__ == "__main__":
    price_history = load_price_history_data()

    results = get_optimal_interval(price_history)

    print "Buy at {price} (date: {date})".format(**results['buy'])
    print "Buy at {price} (date: {date})".format(**results['sell'])
