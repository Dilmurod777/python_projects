import requests


def get_rates(curr):
    try:
        rates = requests.get(f'http://www.floatrates.com/daily/{curr.lower()}.json').json()

        if curr.lower() == 'usd':
            return {'usd': 1, 'eur': rates['eur']['rate']}
        elif curr.lower() == 'eur':
            return {'usd': rates['usd']['rate'], 'eur': 1}

        return {'usd': rates['usd']['rate'], 'eur': rates['eur']['rate']}
    except:
        raise Exception('Something went wrong. Please, check your input!')


cache = {'usd': get_rates('usd'), 'eur': get_rates('eur')}

fromCurr = input("Enter currency you have (empty to exit): ")
fromRates = get_rates(fromCurr)

while True:
    toCurr = input("Enter currency to convert to (empty to exit): ")
    if toCurr.strip() == '':
        break

    amount = input("Enter amount to convert ((empty to exit)): ")
    if amount.strip() == '':
        break
    amount = float(amount)

    print('Checking the cache...')
    if toCurr.lower() not in cache:
        print('Sorry, but it is not in the cache!')
        cache[toCurr.lower()] = get_rates(toCurr)
    else:
        print('Oh! It is in the cache!')

    toRates = cache[toCurr.lower()]
    convAmount = round(amount * fromRates['usd'] / toRates['usd'], 2)
    print(f'You recieved {convAmount} {toCurr}')

print("You successfully exited the program.")