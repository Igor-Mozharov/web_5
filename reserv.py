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


async def main(date):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.privatbank.ua/p24api/exchange_rates?date={date}') as response:
            # print('Response:', response.status)
            # print('Content-type:', response.headers['content-type'])
            # print('Cookies:', response.cookies)
            # print(response.ok)
            result_temp = await response.json()
            return print_result(result_temp)

async def get_list_of_exchange(days):
    today = datetime.now().date()
    start_day = (datetime.now().date() + timedelta(days=1)) - timedelta(days)
    exchange_list = []
    if days > 10:
        return 'Max exchange days = 10, enter 1-10'
    while start_day <= today:
        exchange_list.append(await main(start_day.strftime('%d.%m.%Y')))
        start_day += timedelta(days=1)
    return  exchange_list




if __name__ == '__main__':
    sys.argv[1] = int(sys.argv[1])
    tim = time.time()
    print(asyncio.run(get_list_of_exchange(sys.argv[1])))
    print(time.time() - tim)
