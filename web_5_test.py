import aiohttp
import asyncio
import sys
from datetime import  datetime, timedelta
import time


def print_result(result):
    return {result['date']: {'EUR': {'sale': result['exchangeRate'][8]['saleRateNB'],
    'purchase': result['exchangeRate'][8]['purchaseRateNB']},
    'USD': {'sale': result['exchangeRate']
    [23]['saleRateNB'], 'purchase': result['exchangeRate'][23]['purchaseRateNB']}}}


async def result(date, session):
    url = f'https://api.privatbank.ua/p24api/exchange_rates?date={date}'
    try:
        async with session.get(url) as response:
            if response.status == 200:
                result_temp = await response.json()
                return print_result(result_temp)
            else:
                return f'error status : {response.status}'
    except aiohttp.ClientConnectorError:
        return 'Connection error'

async def get_list_of_exchange(days):
    async with aiohttp.ClientSession() as session:
        today = datetime.now().date()
        start_day = (datetime.now().date() + timedelta(days=1)) - timedelta(days)
        exchange_list = []
        if days > 10:
            return 'Max exchange days = 10, enter 1-10'
        while start_day <= today:
            exchange_list.append(asyncio.ensure_future(result(start_day.strftime('%d.%m.%Y'), session)))
            start_day += timedelta(days=1)
        orig = await asyncio.gather(*exchange_list)
        return orig





if __name__ == '__main__':
    sys.argv[1] = int(sys.argv[1])
    tim = time.time()
    print(asyncio.run(get_list_of_exchange(sys.argv[1])))
    print(time.time() - tim)
