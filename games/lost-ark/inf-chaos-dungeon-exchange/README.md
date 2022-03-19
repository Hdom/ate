# Infinite Chaos Dungeon Exchange

Accurate as of: 03/19/2022

Contact: [@Morl0ck](https://github.com/Morl0ck)

## Overview

This exchange gold calculator was created to maximize the amount of gold you can make from running infinite chaos dungeons, using the `Shard of Purification` material you acquire.

## Usage

1. Edit the file `farmable_items.json`
   - Set the price of the materials in the json and how many exchanges you have made.
2. 
    ```python
    cd inf-chaos-dungeon-exchange
    python ./maximize.py --time-per-run 2 --shards-per-run 150
    ```

## Contribution

I was not able to generate the list of costs for all materials. I have provided the most I was able to purchase. If you have the values for the extra purchases please create a PR for the json files within `Exchanges` so that the calculator has more information. Thanks.