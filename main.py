import asyncio

from pprint import pprint

from matcher.matcher import Matcher
from notification.notify import Notify


def main():
    cnpj = '61889727000166'

    matcher = Matcher(cnpj)
    matches = matcher.find_matching_bids()

    notifier = Notify()
    asyncio.run(notifier.send_message(matches))
    
    #pprint(result)

if __name__ == "__main__":
    main()

