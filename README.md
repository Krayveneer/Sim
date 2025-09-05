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
- Condensed Creativity is not used with any cheese other than the Royal Beanster
- Leaping Lavish Beanster is used in any room that is not an Ultimate Target room
- Royal Beanster and Condensed Creativity are used in Ultimate Target room
- Royal Ruby Refractor Base (or its subsequent series) is used to double the Fabled Fertilizer output during the Giant fight
- Room 1 Retreat strategy is employed for purely Fabled Fertilizer farming
- Room 1 Retreat strategy utilizes Leaping Lavish Beanster to end the room and Beanster during Giant chase
- Do Golden Harps farming run when Golden Harps fall below the threshold of 5000
- Do Lavish Beans farming run when Leaping Lavish Beanster falls below the threshold of 1000
- Do Royal Beans farming run when Royal Beanster falls below the threshold of 1000
- Beanster cheese are assumed to have been bought in the marketplace

## Features

- Simulates leaping and chase through rooms with custom trap power and trap luck
- Uses of refractor base can be toggled
- Plans a chain of castles that needs to be done to reach Golden Goose Eggs target
- Outputs average for hunts with a given cheese, harps used, and compounded final loot gain