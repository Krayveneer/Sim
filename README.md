# sim_toc.py / sim_toc.ipynb

## Overview

`sim_toc.py` is a simulator for computing the average number of encyclopaedia volumes during a Final Draft Derby run in the Table of Content. It simulates writing sessions following the catch rates for Bitter Grammarian and Mythweaver calculated from the input trap power, trap luck, and word boosters. 

`sim_toc.ipynb` is the Jupyter notebook version of the same code. 

## Features

- Simulates writing sessions with custom trap power, trap luck, and word boosters.
- Calculates catch rates for Bitter Grammarian and Mythweaver.
- Supported writing prior to encyclopaedia (< 4000 words)
- Supported word boosters: Condensed Creativity, Silver Quill, Gold Quill, Rainbow Quill.
- Outputs average and maximum values for hunts, words, Mythweavers caught, volumes written, and Gnawbel Prizes.
- Outputs possible volume distribution per run

# sim_bb.py

## Overview

`sim_bb.py` is a simulator for planning a chain of castle runs in Bountiful Beanstalk to reach a target amount of Golden Goose Eggs. It simulates a run through a room in a castle following the catch rates for the mice in each castle calculated from the input trap power and trap luck. It then creates a chain of castles to go through to reach the targeted number of Golden Goose Eggs. 

## Assumptions

Several assumptions have been made during the writing of this code:
- A minimum of 100 Royal Beanster must be in the inventory
    - Casually farm Royal Ruby Bean to fulfil this quota before using the simulator
- A minimum of XX Leaping Lavish Beanster must be in the inventory
    - Casually farm Lavish Lapis Bean and Golden Harps to fulfill this quota before using the simulator
- Leaping Lavish Beanster is used in any room that is not an Ultimate Target room
- Room 1 Retreat strategy: 
    - This is employed for purely Fabled Fertilizer farming
    - This forcibly utilizes Golden Harps to maximize noise upon the 3rd hunt to trigger Giant chase
    - This utilizes Leaping Lavish Beanster to end the room and Beanster/SB/Gouda during Giant chase
- Farming Run strategy: 
    - This employs Golden Goose Feather (with Golden Quill) and Giant's Golden Key 
    - This forcibly utilizes Golden Harps to reduce noise to zero (Auto Harp preferable) until reaching Ultimate Target room
    - This utilizes Royal Beanster and Condensed Creativity upon reaching Ultimate Target room
- Logic check:
    - Always check for Fabled Fertilizer to enter a particular stage, and do R1R at the stage below it if found lacking
    - Always check that Golden Harps is always more than 5.000, and do Golden Harps farming run if found lacking
    - Always check that Royal Beanster is always more than 100, and do Royal Ruby Bean farming run if found lacking
    - Always check that Leaping Lavish Beanster is always more than XX, and do Lavish Lapis Bean and Golden Harp farming runs if found lacking
- Beanster cheeses are assumed to have been bought in the marketplace, or in stock in abundance

## Features

- Simulates leaping and chase through rooms with custom trap power and trap luck
- Uses of refractor base can be toggled
- Plans a chain of castles that needs to be done to reach Golden Goose Eggs target
- Outputs average for hunts at a given stage, stage chains, and compounded final loot gain