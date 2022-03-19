import sys
import argparse
import json


def load(fi):
  ex = open(fi['FilePath'])
  temp = json.load(ex)
  ex.close()
  fi['Exchanges'] = temp['Exchanges']


def calculateProfit(farmableItem, shardsAvailable):
  runningSumAlreadyExchanged = 0
  if (farmableItem['ExchangesMade'] is not None and farmableItem['ExchangesMade'] > 0):
    runningSumAlreadyExchanged = farmableItem['Exchanges'][farmableItem['ExchangesMade']]['RunningSum']
  maxExchange = [ex for ex in farmableItem['Exchanges'] if ex['Number'] > farmableItem['ExchangesMade'] and (
    ex['RunningSum'] - runningSumAlreadyExchanged) <= shardsAvailable][-1]['Number']
  farmableItem['ExchangesCount'] = 0 if maxExchange is None else maxExchange - \
    farmableItem['ExchangesMade']
  farmableItem['Profit'] = farmableItem['ExchangesCount'] * \
    farmableItem['Price']

def run(timePerRun, shardsPerRun, hoursRunning):
  shardsAvailable = 60 / timePerRun * shardsPerRun * hoursRunning

  if (shardsAvailable == 0):
    sys.exit("Coudn't calculate shardsAvailable. Possibly missing an argument?")

  print(f'With {shardsAvailable} shards after {hoursRunning} hours you are able to exchange:')

  f = open('./farmable_items.json')
  data = json.load(f)
  f.close()

  for fi in data['FarmableItems']:
    load(fi)
    calculateProfit(fi, shardsAvailable)

  sortedFarmableItems = sorted(
    data['FarmableItems'], key=lambda farmableItem: farmableItem['Profit'], reverse=True)

  for fi in sortedFarmableItems:
    print(f"{fi['ExchangesCount']} {fi['Name']} for {fi['Profit']} gold profit.")

def main(argv):
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--time-per-run", required=True, type=int, help="amount of time it takes to complete a run (in minutes)")
  parser.add_argument("-s", "--shards-per-run", required=True, type=int, help="amount of shards you receive after completing a run")
  parser.add_argument("-o", "--hours-running", type=float, help="amount of hours you want to simulate", default=1.0)
  args = parser.parse_args(argv)

  run(args.time_per_run, args.shards_per_run, args.hours_running)


if __name__ == "__main__":
    main(sys.argv[1:])
