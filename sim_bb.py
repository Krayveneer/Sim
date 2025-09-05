import numpy as np
import random
import math

# Mice Data taken from tsitu's CRE
class MiceData:
    def __init__(self):
        # Mice attraction rate
        self.mice_dict = {}

        # SB mice
        self.mice_dict = {
                # Normal mice
                # Beanstalk
                ("SB","Beanstalk"): {
                    "attractions": [0.4829, 0.4686, 0.0485],
                    "powers": [12000,13000,4000],
                    "effects": [1,1,1],
                    "names": ["Budrich Thomborn",
                              "Leafton Beanwell",
                              "Herbaceous Bravestalk"]},
                # Dungeon
                ("SB","Dungeon"): {
                    "attractions": [0.2594, 0.3474, 0.3932],
                    "powers": [15000,20000,30000],
                    "effects": [1,1,1],
                    "names": ["Peaceful Prisoner",
                              "Diminutive Detainee",
                              "Smug Smuggler"]},
                ("Beanster","Dungeon"): {
                    "attractions": [0.3090, 0.4448, 0.2462],
                    "powers": [16200,17300,19040],
                    "effects": [1,1,1],
                    "names": ["Cell Sweeper",
                              "Jovial Jailor",
                              "Lethargic Guard"]},
                ("Lavish","Dungeon"): {
                    "attractions": [0.5070, 0.4930],
                    "powers": [25185,23140],
                    "effects": [1,1],
                    "names": ["Gate Keeper",
                              "Key Master"]},
                ("Royal","Dungeon"): {
                    "attractions": [1.0],
                    "powers": [70300],
                    "effects": [1.5],
                    "names": ["Wrathful Warden"]},
                # Ballroom
                ("SB","Ballroom"): {
                    "attractions": [0.2642, 0.3423, 0.3935],
                    "powers": [22000,24000,33000],
                    "effects": [1,1,1],
                    "names": ["Whimsical Waltzer",
                              "Sassy Salsa Dancer",
                              "Baroque Dancer"]},
                ("Beanster","Ballroom"): {
                    "attractions": [0.3092, 0.3956, 0.2952],
                    "powers": [19000,21000,23000],
                    "effects": [1,1,1],
                    "names": ["Obstinate Oboist",
                              "Peevish Piccoloist",
                              "Sultry Saxophonist"]},
                ("Lavish","Ballroom"): {
                    "attractions": [0.5051, 0.4949],
                    "powers": [33090,30520],
                    "effects": [1,1],
                    "names": ["Violent Violinist",
                              "Chafed Cellist"]},
                ("Royal","Ballroom"): {
                    "attractions": [1.0],
                    "powers": [77925],
                    "effects": [1.5],
                    "names": ["Treacherous Tubaist"]},
                # Great Hall
                ("SB","Great Hall"): {
                    "attractions": [0.2515, 0.3464, 0.4021],
                    "powers": [28000,32000,38000],
                    "effects": [1,1,1],
                    "names": ["Clumsy Cupbearer",
                              "Plotting Page",
                              "Scheming Squire"]},
                ("Beanster","Great Hall"): {
                    "attractions": [0.2635, 0.3903, 0.3462],
                    "powers": [25000,31000,29000],
                    "effects": [1,1,1],
                    "names": ["Vindictive Viscount",
                              "Baroness von Bean",
                              "Cagey Countess"]},
                ("Lavish","Great Hall"): {
                    "attractions": [0.5046, 0.4954],
                    "powers": [34550,36600],
                    "effects": [1,1],
                    "names": ["Dastardly Duchess",
                              "Malicious Marquis"]},
                ("Royal","Great Hall"): {
                    "attractions": [1.0],
                    "powers": [86363],
                    "effects": [1.5],
                    "names": ["Pernicious Prince"]},
                # Boss mice
                ("Boss","Beanstalk"): {
                    "powers": [80900],
                    "effects": [4],
                    "names": ["Vinneus Stalkhome"]},
                ("Boss","Dungeon"): {
                    "powers": [104250],
                    "effects": [3],
                    "names": ["Dungeon Master"]},
                ("Boss","Ballroom"): {
                    "powers": [184600],
                    "effects": [4],
                    "names": ["Malevolent Maestro"]},
                ("Boss","Great Hall"): {
                    "powers": [222150],
                    "effects": [3],
                    "names": ["Mythical Giant King"]}
            }
    
    # Randomly draw a mice from the AR pool
    def get_mouse(self, cheese, zone):
        data = self.mice_dict[(cheese,zone)]
        ar = data["attractions"]
        idx = np.random.choice(len(ar), p=np.array(ar)/sum(ar))
        return (data["powers"][idx], data["effects"][idx], data["names"][idx])

    # Get the boss
    def get_boss(self, zone):
        return self.mice_dict[("Boss",zone)]

    # Compute the catch rate
    def catch_rate(self, trap_power, trap_luck, mouse_power, mouse_eff):
        return min(1, (trap_power*mouse_eff + 2*(math.floor(trap_luck*min(mouse_eff,1.4))**2)) / (mouse_power + trap_power*mouse_eff))

# Simulator for Beanstalk 
def simulate_beanstalk(trap_power, trap_luck, use_ref, use_cc, n_runs=10000):
    mice = MiceData()
    hunts_needed = []
    beans_collected = []
    ferts_collected = []

    # Room distribution
    room_types = ["Standard", "Super", "Extreme", "Ultimate"]
    room_probs = [0.05,0.18,0.70,0.07]
    room_multi = {"Standard":1, "Super":2, "Extreme":4, "Ultimate":8}

    # Run loop
    for _ in range(n_runs):
        hunts = 0
        beans = 0
        ferts = 0

        # Pick a room
        room = np.random.choice(room_types, p=room_probs)
        multiplier = room_multi[room]

        # Run 20 guaranteed hunts
        for _ in range(20):
            hunts += 1

            # Get the mouse from the pool
            m_pow, m_eff, m_nam = mice.get_mouse("Beanstalk")

            # Simulate a catch
            catch = mice.catch_rate(trap_power, trap_luck, m_pow, m_eff)
            if random.random() < catch:
                beans += multiplier # Normal mice drop

        # Catch the boss
        boss = mice.get_boss("Beanstalk")
        b_pow, b_eff, b_name = boss["powers"][0], boss["effects"][0], boss["names"][0]
        # Hunt until caught
        caught = False
        while not caught:
            hunts += 1
            catch = mice.catch_rate(trap_power, trap_luck, b_pow, b_eff)
            if random.random() < catch:
                beans += multiplier + 20 # Boos mice drop
                ferts += 1
                caught = True

        # Apply loot modifier
        if use_cc:
            beans *= 2
        if use_ref:
            ferts *= 2
            
        # Append result
        hunts_needed.append(hunts)
        beans_collected.append(beans)
        ferts_collected.append(ferts)

    # Return result
    return np.mean(hunts_needed), np.std(hunts_needed), hunts_needed, np.mean(beans_collected), np.std(beans_collected), beans_collected, np.mean(ferts_collected), np.std(ferts_collected), ferts_collected

# Simulator for Dungeon
def simulate_dungeon(trap_power, trap_luck, use_ref, use_cc, cheese, target_room_type, use_key, gquill, feather, n_runs=10000):
    mice = MiceData()
    hunts_needed = []
    lbean_collected = []
    mbean_collected = []
    mysts_collected = []
    ferts_collected = []
    hunts_other = []
    hunts_royal = []
    noise_raised = []
    harps_played = []

    # Apply cheese multiplier
    cheese_multiplier = {"SB":1, "Beanster":2, "Lavish":4, "Royal":16}

    # Room setup
    room_types = ["lavish","magic", "mysteries"]
    if use_key:
        room_probs = [0.287+0.441+0.133,
                      0.062+0.022+0.009,
                      0.037+0.009]
        room_dicts = {
            "lavish": [0.287,0.441,0.133],
            "magic": [0.062,0.022,0.009],
            "mysteries": [0.037,0.009,0.0]}
        name_denom = ["Super","Extreme","Ultimate"]
        mult_denom = [2,4,8]
    else:
        room_probs = [0.043+0.261+0.272+0.130,
                      0.065+0.043+0.022+0.022,
                      0.087+0.054]
        room_dicts = {
            "lavish": [0.043,0.261,0.272,0.130],
            "magic": [0.065,0.043,0.022,0.022],
            "mysteries": [0.087,0.054,0.0,0.0]}
        name_denom = ["Standard","Super","Extreme","Ultimate"]
        mult_denom = [1,2,4,8]

    # Check if the target room exists in this stage
    has_target = target_room_type in room_types if target_room_type else False

    # Run loop
    for _ in range(n_runs):
        hunts, lbean, mbean, mysts, ferts, other_hunt, royal_hunt = 0, 0, 0, 0, 0, 0, 0
        noise = 0
        noise_raise = 0
        harps_spent_total = 0
        boss_caught = False

        # If the target room is not in this stage, chase room 1
        if not has_target:
            # As long as the boss is not caught
            while not boss_caught:
                # Pick a room type
                room_type = np.random.choice(room_types, p=np.array(room_probs)/sum(room_probs))
                denom = np.random.choice(name_denom, p=np.array(room_dicts[room_type])/sum(room_dicts[room_type]))
                denom_idx = name_denom.index(denom)
                room_multiplier = mult_denom[denom_idx]

                # Apply cheese and CC multiplier to loot
                active_cheese = cheese
                if denom == "Ultimate":
                    active_cheese = "Royal" # Switch to royal at Ultimate Room
                loot_multi = cheese_multiplier[active_cheese] * room_multiplier
                if use_cc: loot_multi *= 2
                if feather: 
                    loot_multi *= 2
                    if gquill:
                        loot_multi *= 2
                
                # Run the room
                steps = 0
                while steps < 20:
                    # Check if using (leaping) lavish
                    if active_cheese == "Lavish":
                        step = 5
                    else:
                        step = 1
                    # Add up the actual hunts
                    hunts += 1
                    # Add up the cheese usage
                    if active_cheese == "Royal":
                        royal_hunt += 1
                    else:
                        other_hunt += 1
                    # Add up the actual steps
                    steps += step
                    # Always add full noise
                    if denom != "Ultimate" and room_type != target_room_type:
                        noise += loot_multi
                    # Simulate catch
                    m_pow, m_eff, m_name = mice.get_mouse(cheese,"Dungeon")
                    if random.random() < mice.catch_rate(trap_power, trap_luck, m_pow, m_eff):
                        # Assume CC when using Royal
                        loot_gain = loot_multi
                        if denom == "Ultimate":
                            loot_gain *= 2
                        # Collect loot by room type
                        if room_type == "lavish": lbean += loot_gain
                        elif room_type == "magic": mbean += loot_gain
                        elif room_type == "mysteries": mysts += loot_gain

                # Chase hunts
                loot_gain = 2 * loot_multi
                for _ in range(20):
                    hunts += 1
                    other_hunt += 1
                    m_pow, m_eff, m_name = mice.get_mouse("Beanster", "Dungeon")
                    if random.random() < mice.catch_rate(trap_power, trap_luck, m_pow, m_eff):
                        if room_type == "lavish": lbean += loot_gain
                        elif room_type == "magic": mbean += loot_gain
                        elif room_type == "mysteries": mysts += loot_gain

                # Boss hunts
                boss = mice.get_boss("Dungeon")
                b_pow, b_eff = boss["powers"][0], boss["effects"][0]
                caught = False
                while not caught:
                    hunts += 1
                    other_hunt += 1
                    if random.random() < mice.catch_rate(trap_power, trap_luck, b_pow, b_eff):
                        # Guaranteed boss loot
                        mbean += 40 # Doubled because always CC for boss
                        ferts += 5
                        # Loot by room type
                        if room_type == "lavish": lbean += loot_gain
                        elif room_type == "magic": mbean += loot_gain
                        elif room_type == "mysteries": mysts += loot_gain
                        # Mark boss is caught
                        caught = True
                        boss_caught = True
            
                # If not full, make noise with harp
                noise_raise += noise
                if denom != "Ultimate":
                    harps_spent_total += (300 - noise)

        # If the target room is in this stage
        else:
            # As long as the boss is not caught
            while not boss_caught:
                # Pick a room type
                room_type = np.random.choice(room_types, p=np.array(room_probs)/sum(room_probs))
                denom = np.random.choice(name_denom, p=np.array(room_dicts[room_type])/sum(room_dicts[room_type]))
                denom_idx = name_denom.index(denom)
                room_multiplier = mult_denom[denom_idx]

                # Apply cheese and CC multiplier to loot
                active_cheese = cheese
                if denom == "Ultimate" and room_type == target_room_type:
                    active_cheese = "Royal" # Switch to royal at Ultimate Room
                loot_multi = cheese_multiplier[active_cheese] * room_multiplier
                if use_cc: loot_multi *= 2
                if feather: 
                    loot_multi *= 2
                    if gquill:
                        loot_multi *= 2
                
                # Run the room
                steps = 0
                while steps < 20:
                    # Check if using (leaping) lavish
                    if active_cheese == "Lavish":
                        step = 5
                    else:
                        step = 1
                    # Add up the actual hunts
                    hunts += 1
                    # Add up the cheese usage
                    if active_cheese == "Royal":
                        royal_hunt += 1
                    else:
                        other_hunt += 1
                    # Add up the actual steps
                    steps += step
                    # Always add full noise
                    if denom != "Ultimate" and room_type != target_room_type:
                        noise += loot_multi
                    # Simulate catch
                    m_pow, m_eff, m_name = mice.get_mouse(cheese,"Dungeon")
                    if random.random() < mice.catch_rate(trap_power, trap_luck, m_pow, m_eff):
                        # Assume CC when using Royal
                        loot_gain = loot_multi
                        if denom == "Ultimate":
                            loot_gain *= 2
                        # Collect loot by room type
                        if room_type == "lavish": lbean += loot_gain
                        elif room_type == "magic": mbean += loot_gain
                        elif room_type == "mysteries": mysts += loot_gain

                # Check noise at the end of room
                # if noise >= 200
                # Check Ultimate Room and trigger Giant chase
                if denom == "Ultimate" and room_type == target_room_type:
                    # Assume CC used when using Royal and giant chase gives base 2
                    loot_gain = 4 * loot_multi
                    # Chase hunts
                    for _ in range(20):
                        hunts += 1
                        royal_hunt += 1
                        m_pow, m_eff, m_name = mice.get_mouse("Royal", "Dungeon")
                        if random.random() < mice.catch_rate(trap_power, trap_luck, m_pow, m_eff):
                            if room_type == "lavish": lbean += loot_gain
                            elif room_type == "magic": mbean += loot_gain
                            elif room_type == "mysteries": mysts += loot_gain

                    # Boss hunts
                    boss = mice.get_boss("Dungeon")
                    b_pow, b_eff = boss["powers"][0], boss["effects"][0]
                    caught = False
                    while not caught:
                        hunts += 1
                        other_hunt += 1
                        if random.random() < mice.catch_rate(trap_power, trap_luck, b_pow, b_eff):
                            # Guaranteed boss loot
                            mbean += 40 # Doubled because always CC for boss
                            ferts += 5
                            # Loot by room type
                            if room_type == "lavish": lbean += loot_gain
                            elif room_type == "magic": mbean += loot_gain
                            elif room_type == "mysteries": mysts += loot_gain
                            # Mark boss is caught
                            caught = True
                            boss_caught = True
            
                # If not ultimate room, remove noise with harps
                noise_raise += noise
                harps_spent_total += noise
                noise = 0
        
        if use_ref: ferts *= 2
        hunts_needed.append(hunts)
        lbean_collected.append(lbean)
        mbean_collected.append(mbean)
        mysts_collected.append(mysts)
        ferts_collected.append(ferts)
        hunts_other.append(other_hunt)
        hunts_royal.append(royal_hunt)
        noise_raised.append(noise_raise)
        harps_played.append(harps_spent_total)

    return np.mean(hunts_needed), np.std(hunts_needed), hunts_needed, np.mean(lbean_collected), np.std(lbean_collected), lbean_collected, np.mean(mbean_collected), np.std(mbean_collected), mbean_collected, np.mean(mysts_collected), np.std(mysts_collected), mysts_collected, np.mean(ferts_collected), np.std(ferts_collected), ferts_collected, np.mean(hunts_other), np.std(hunts_other), hunts_other, np.mean(hunts_royal), np.std(hunts_royal), hunts_royal, np.mean(noise_raised), np.std(noise_raised), noise_raised, np.mean(harps_played), np.std(harps_played), harps_played

# Simulator for Ballroom
def simulate_ballroom(trap_power, trap_luck, use_ref, use_cc, cheese, target_room_type, use_key, ruby_removal, gquill, feather, n_runs=10000):
    mice = MiceData()
    hunts_needed = []
    rbean_collected = []
    harps_collected = []
    mysts_collected = []
    ferts_collected = []
    hunts_other = []
    hunts_royal = []
    noise_raised = []
    harps_played = []

    # Apply cheese multiplier
    cheese_multiplier = {"SB":1, "Beanster":2, "Lavish":4, "Royal":16}

    # Room setup
    if ruby_removal:
        room_types = ["harps", "mysteries"]
        if use_key:
            room_probs = [0.282+0.313+0.137,
                          0.145+0.053+0.069]
            room_dicts = {
                "harps": [0.282,0.313,0.137],
                "mysteries": [0.145,0.053,0.069]}
            name_denom = ["Super","Extreme","Ultimate"]
            mult_denom = [2,4,8]
        else:
            room_probs = [0.208+0.174+0.221+0.087,
                          0.168+0.054+0.047+0.040]
            room_dicts = {
                "harps": [0.208,0.174,0.221,0.087],
                "mysteries": [0.168,0.054,0.047,0.040]}
            name_denom = ["Standard","Super","Extreme","Ultimate"]
            mult_denom = [1,2,4,8]
    else:
        room_types = ["royal", "harps", "mysteries"]
        if use_key:
            room_probs = [0.417+0.250+0.083,
                          0.067+0.088+0.029,
                          0.025+0.021+0.021]
            room_dicts = {
                "royal": [0.417,0.250,0.083],
                "harps": [0.067,0.088,0.029],
                "mysteries": [0.025,0.021,0.021]}
            name_denom = ["Super","Extreme","Ultimate"]
            mult_denom = [2,4,8]
        else:
            room_probs = [0.070+0.334+0.201+0.067,
                          0.070+0.054+0.070+0.023,
                          0.057+0.020+0.017+0.017]
            room_dicts = {
                "royal": [0.070,0.334,0.201,0.067],
                "harps": [0.070,0.054,0.070,0.023],
                "mysteries": [0.057,0.020,0.017,0.017]}
            name_denom = ["Standard","Super","Extreme","Ultimate"]
            mult_denom = [1,2,4,8]

    # Check if the target room exists in this stage
    has_target = target_room_type in room_types if target_room_type else False

    # Run loop
    for _ in range(n_runs):
        hunts, rbean, harps, mysts, ferts, other_hunt, royal_hunt = 0, 0, 0, 0, 0, 0, 0
        noise = 0
        noise_raise = 0
        harps_spent_total = 0
        boss_caught = False

        # If the target room is not in this stage, chase asap
        if not has_target:
            # As long as the boss is not caught
            while not boss_caught:
                # Pick a room type
                room_type = np.random.choice(room_types, p=np.array(room_probs)/sum(room_probs))
                denom = np.random.choice(name_denom, p=np.array(room_dicts[room_type])/sum(room_dicts[room_type]))
                denom_idx = name_denom.index(denom)
                room_multiplier = mult_denom[denom_idx]

                # Apply cheese and CC multiplier to loot
                active_cheese = cheese
                if denom == "Ultimate":
                    active_cheese = "Royal" # Switch to royal at Ultimate Room
                loot_multi = cheese_multiplier[active_cheese] * room_multiplier
                if use_cc: loot_multi *= 2
                if feather: 
                    loot_multi *= 2
                    if gquill:
                        loot_multi *= 2

                # Run the room
                steps = 0
                while steps < 20:
                    # Check if using (leaping) lavish
                    if active_cheese == "Lavish":
                        step = 5
                    else:
                        step = 1
                    # Add up the actual hunts
                    hunts += 1
                    # Add up the cheese usage
                    if active_cheese == "Royal":
                        royal_hunt += 1
                    else:
                        other_hunt += 1
                    # Add up the actual steps
                    steps += step
                    # Always add full noise
                    if denom != "Ultimate" and room_type != target_room_type:
                        noise += loot_multi
                    # Simulate catch
                    m_pow, m_eff, m_name = mice.get_mouse(cheese,"Ballroom")
                    if random.random() < mice.catch_rate(trap_power, trap_luck, m_pow, m_eff):
                        # Assume CC when using Royal
                        loot_gain = loot_multi
                        if denom == "Ultimate":
                            loot_gain *= 2
                        # Collect loot by room type
                        if room_type == "royal": rbean += loot_gain
                        elif room_type == "harps": harps += loot_gain
                        elif room_type == "mysteries": mysts += loot_gain

                # Chase hunts
                loot_gain = 2 * loot_multi
                for _ in range(20):
                    hunts += 1
                    other_hunt += 1
                    m_pow, m_eff, m_name = mice.get_mouse("Beanster", "Ballroom")
                    if random.random() < mice.catch_rate(trap_power, trap_luck, m_pow, m_eff):
                        if room_type == "royal": rbean += loot_gain
                        elif room_type == "harps": harps += loot_gain
                        elif room_type == "mysteries": mysts += loot_gain

                # Boss hunts
                boss = mice.get_boss("Ballroom")
                b_pow, b_eff = boss["powers"][0], boss["effects"][0]
                caught = False
                while not caught:
                    hunts += 1
                    other_hunt += 1
                    if random.random() < mice.catch_rate(trap_power, trap_luck, b_pow, b_eff):
                        # Guaranteed boss loot
                        ferts += 20
                        # Loot by room type
                        if room_type == "royal": rbean += loot_gain
                        elif room_type == "harps": harps += loot_gain
                        elif room_type == "mysteries": mysts += loot_gain
                        # Mark boss is caught
                        caught = True
                        boss_caught = True
            
            # If not full, make noise with harp
            noise_raise += noise
            if denom != "Ultimate":
                harps_spent_total += (400 - noise)

        # If the target room is in this stage
        else:
            # As long as the boss is not caught
            while not boss_caught:
                # Pick a room type
                room_type = np.random.choice(room_types, p=np.array(room_probs)/sum(room_probs))
                denom = np.random.choice(name_denom, p=np.array(room_dicts[room_type])/sum(room_dicts[room_type]))
                denom_idx = name_denom.index(denom)
                room_multiplier = mult_denom[denom_idx]

                # Apply cheese and CC multiplier to loot
                active_cheese = cheese
                if denom == "Ultimate" and room_type == target_room_type:
                    active_cheese = "Royal" # Switch to royal at Ultimate Room
                loot_multi = cheese_multiplier[active_cheese] * room_multiplier
                if use_cc: loot_multi *= 2
                if feather: 
                    loot_multi *= 2
                    if gquill:
                        loot_multi *= 2

                # Run the room
                steps = 0
                while steps < 20:
                    # Check if using (leaping) lavish
                    if active_cheese == "Lavish":
                        step = 5
                    else:
                        step = 1
                    # Add up the actual hunts
                    hunts += 1
                    # Add up the cheese usage
                    if active_cheese == "Royal":
                        royal_hunt += 1
                    else:
                        other_hunt += 1
                    # Add up the actual steps
                    steps += step
                    # Always add full noise
                    if denom != "Ultimate" and room_type != target_room_type:
                        noise += loot_multi
                    # Simulate catch
                    m_pow, m_eff, m_name = mice.get_mouse(cheese,"Ballroom")
                    if random.random() < mice.catch_rate(trap_power, trap_luck, m_pow, m_eff):
                        # Assume CC when using Royal
                        loot_gain = loot_multi
                        if denom == "Ultimate":
                            loot_gain *= 2
                        # Collect loot by room type
                        if room_type == "royal": rbean += loot_gain
                        elif room_type == "harps": harps += loot_gain
                        elif room_type == "mysteries": mysts += loot_gain
 
                # Check noise at the end of room
                # if noise >= 200
                # Check Ultimate Room and trigger Giant chase
                if denom == "Ultimate" and room_type == target_room_type:
                    # Assume CC used when using Royal and giant chase gives base 2
                    loot_gain = 4 * loot_multi
                    # Chase hunts
                    for _ in range(20):
                        hunts += 1
                        royal_hunt += 1
                        m_pow, m_eff, m_name = mice.get_mouse("Royal", "Ballroom")
                        if random.random() < mice.catch_rate(trap_power, trap_luck, m_pow, m_eff):
                            if room_type == "royal": rbean += loot_gain
                            elif room_type == "harps": harps += loot_gain
                            elif room_type == "mysteries": mysts += loot_gain

                    # Boss hunts
                    boss = mice.get_boss("Ballroom")
                    b_pow, b_eff = boss["powers"][0], boss["effects"][0]
                    caught = False
                    while not caught:
                        hunts += 1
                        other_hunt += 1
                        if random.random() < mice.catch_rate(trap_power, trap_luck, b_pow, b_eff):
                            # Guaranteed boss loot
                            ferts += 20
                            # Loot by room type
                            if room_type == "royal": rbean += loot_gain
                            elif room_type == "harps": harps += loot_gain
                            elif room_type == "mysteries": mysts += loot_gain
                            # Mark boss is caught
                            caught = True
                            boss_caught = True
            
                # If not ultimate room, remove noise with harps
                noise_raise += noise
                harps_spent_total += noise
                noise = 0

        if use_ref: ferts *= 2
        hunts_needed.append(hunts)
        rbean_collected.append(rbean)
        harps_collected.append(harps)
        mysts_collected.append(mysts)
        ferts_collected.append(ferts)
        hunts_other.append(other_hunt)
        hunts_royal.append(royal_hunt)
        noise_raised.append(noise_raise)
        harps_played.append(harps_spent_total)

    return np.mean(hunts_needed), np.std(hunts_needed), hunts_needed, np.mean(rbean_collected), np.std(rbean_collected), rbean_collected, np.mean(harps_collected), np.std(harps_collected), harps_collected, np.mean(mysts_collected), np.std(mysts_collected), mysts_collected, np.mean(ferts_collected), np.std(ferts_collected), ferts_collected, np.mean(hunts_other), np.std(hunts_other), hunts_other, np.mean(hunts_royal), np.std(hunts_royal), hunts_royal, np.mean(noise_raised), np.std(noise_raised), noise_raised, np.mean(harps_played), np.std(harps_played), harps_played

# Simulator for Great Hall
def simulate_greathall(trap_power, trap_luck, use_ref, use_cc, cheese, use_key, gquill, feather, n_runs=10000):
    mice = MiceData()
    hunts_needed = []
    geggs_collected = []
    ferts_collected = []
    hunts_other = []
    hunts_royal = []
    noise_raised = []
    harps_played = []

    # Apply cheese multiplier
    cheese_multiplier = {"SB":1, "Beanster":2, "Lavish":4, "Royal":16}

    # Room distribution
    if use_key:
        room_types = ["Super", "Extreme", "Ultimate"]
        room_probs = [0.580, 0.245, 0.175]
        room_multi = {"Super":2, "Extreme":4, "Ultimate":8}
    else:
        room_types = ["Standard", "Super", "Extreme", "Ultimate"]
        room_probs = [0.258, 0.484, 0.193, 0.065]
        room_multi = {"Standard":1, "Super":2, "Extreme":4, "Ultimate":8}

    # Run loop
    for _ in range(n_runs):
        hunts, geggs, ferts, other_hunt, royal_hunt = 0, 0, 0, 0, 0
        noise = 0
        noise_raise = 0
        harps_spent_total = 0
        boss_caught = False

        # As long as the boss is not caught
        while not boss_caught:
            # Pick a room
            denom = np.random.choice(room_types, p=room_probs)
            room_multiplier = room_multi[denom]

            # Apply cheese and CC multiplier to loot
            active_cheese = cheese
            if denom == "Ultimate":
                active_cheese = "Royal" # Switch to royal at Ultimate Room
            loot_multi = cheese_multiplier[active_cheese] * room_multiplier
            if use_cc: loot_multi *= 2
            if feather: 
                loot_multi *= 2
                if gquill:
                    loot_multi *= 2

            # Run the room
            steps = 0
            while steps < 20:
                # Check if using (leaping) lavish
                if active_cheese == "Lavish":
                    step = 5
                else:
                    step = 1
                # Add up the actual hunts
                hunts += 1
                # Add up the cheese usage
                if active_cheese == "Royal":
                    royal_hunt += 1
                else:
                    other_hunt += 1
                # Add up the actual steps
                steps += step
                # Always add full noise
                if denom != "Ultimate":
                    noise += loot_multi
                # Simulate catch
                m_pow, m_eff, m_name = mice.get_mouse(cheese,"Ballroom")
                if random.random() < mice.catch_rate(trap_power, trap_luck, m_pow, m_eff):
                    # Assume CC when using Royal
                    loot_gain = loot_multi
                    if denom == "Ultimate":
                        loot_gain *= 2
                    # Collect loot by room type
                    geggs += loot_gain

            # Save the raised noise
            noise_raise += noise
            # If not ultimate room, remove noise with harps
            if denom != "Ultimate":
                harps_spent_total += noise
                noise = 0

            # Check noise at the end of room
            # if noise >= 200
            # Check Ultimate Room and trigger Giant chase
            if denom == "Ultimate":
                # Assume CC used when using Royal and giant chase gives base 2
                loot_gain = 4 * loot_multi
                # Chase hunts
                for _ in range(20):
                    hunts += 1
                    royal_hunt += 1
                    m_pow, m_eff, m_name = mice.get_mouse("Royal", "Ballroom")
                    if random.random() < mice.catch_rate(trap_power, trap_luck, m_pow, m_eff):
                        geggs += loot_gain
                        
                # Boss hunts
                boss = mice.get_boss("Ballroom")
                b_pow, b_eff = boss["powers"][0], boss["effects"][0]
                caught = False
                while not caught:
                    hunts += 1
                    other_hunt += 1
                    if random.random() < mice.catch_rate(trap_power, trap_luck, b_pow, b_eff):
                        # Guaranteed boss loot
                        ferts += 10
                        # Loot by room type
                        geggs += loot_gain
                        # Mark boss is caught
                        caught = True
                        boss_caught = True
        
        if use_ref: ferts *= 2
        hunts_needed.append(hunts)
        geggs_collected.append(geggs)
        ferts_collected.append(ferts)
        hunts_other.append(other_hunt)
        hunts_royal.append(royal_hunt)
        noise_raised.append(noise_raise)
        harps_played.append(harps_spent_total)

    return np.mean(hunts_needed), np.std(hunts_needed), hunts_needed, np.mean(geggs_collected), np.std(geggs_collected), geggs_collected, np.mean(ferts_collected), np.std(ferts_collected), ferts_collected, np.mean(hunts_other), np.std(hunts_other), hunts_other, np.mean(hunts_royal), np.std(hunts_royal), hunts_royal, np.mean(noise_raised), np.std(noise_raised), noise_raised, np.mean(harps_played), np.std(harps_played), harps_played

# Plan a chain of stages
# We're stingy and lazy, so no key or ruby removal will be used for this section
def plan_chain(target_loot, inventory, trap_power, trap_luck, use_ref, use_cc, gquill, feather, cheese, goal, n_runs=1000, harp_threshold=5000):
    # Fert costs
    stage_cost = {"Beanstalk":0, "Dungeon":1, "Ballroom":12, "Great Hall":100}
    fert_gain = {
        "Beanstalk": 2 if use_ref else 1,
        "Dungeon": 10 if use_ref else 5,
        "Ballroom": 40 if use_ref else 20,
        "Great Hall": 20 if use_ref else 10}
    stage_loot = {
        "beans": "Beanstalk",
        "lavish": "Dungeon",
        "magic": "Dungeon",
        "mysteries": "Dungeon",
        "royal": "Ballroom",
        "harps": "Ballroom",
        "eggs": "Great Hall"}

    # Check loot in what stage
    t = target_loot.strip().lower()
    if t not in stage_loot:
        raise ValueError(f"Unknown loot '{target_loot}'. Valid loot: {list(stage_loot.keys())}")
    required_stage = stage_loot[t]

    # Inventory
    fert_have = inventory.get("fertilizers", 0)
    chain = []
    total_hunts = 0
    hunts_with_royal = 0
    hunts_with_other = 0
    hunts_with_stalk = 0
    noise_summary = 0
    harps_summary = 0

    # Initiate initial loot
    loot_key_map = {
        "beans": "magic_beans",   # beanstalk beans
        "lavish": "lavish_beans",
        "magic": "magic_beans",
        "mysteries": "mysteries",
        "royal": "royal_beans",
        "harps": "golden_harps",
        "eggs": "golden_eggs"}
    loot_key = loot_key_map[t]
    loot_summary = {
        "lavish_beans": inventory.get("lavish_beans", 0),
        "magic_beans": inventory.get("magic_beans", 0),
        "royal_beans": inventory.get("royal_beans", 0),
        "golden_harps": inventory.get("golden_harps", 0),
        "golden_eggs": inventory.get("golden_eggs", 0),
        "mysteries": inventory.get("mysteries", 0),
        "fertilizers": inventory.get("fertilizers", 0)}

    # Function to call for each stage
    def run_beanstalk():
        nonlocal total_hunts, fert_have, hunts_with_stalk
        mean_h, mean_beans, mean_ferts = simulate_beanstalk(trap_power, trap_luck, use_ref, use_cc, n_runs)
        total_hunts += mean_h
        hunts_with_stalk += mean_h
        loot_summary["magic_beans"] += mean_beans
        loot_summary["fertilizers"] += mean_ferts
        fert_have += mean_ferts
        chain.append("Beanstalk")

    def run_dungeon(cheese, target_room=None, tag="Dungeon"):
        nonlocal total_hunts, fert_have, hunts_with_royal, hunts_with_other, noise_summary, harps_summary
        res = simulate_dungeon(trap_power, trap_luck, use_ref, use_cc, cheese, t, use_key=0, gquill=gquill, feather=feather, n_runs=n_runs)
        # unpack
        mean, std, dist, mean_lbean, std_lbean, dist_lbean, mean_mbean, std_mbean, dist_mbean, mean_mysts, std_mysts, dist_mysts, mean_fert, std_fert, dist_fert, mean_other, std_other, dist_other, mean_royal, std_royal, dist_royal, mean_noise, std_noise, dist_noise, mean_remov, std_remov, dist_remov = res
        total_hunts += mean
        hunts_with_royal += mean_royal
        hunts_with_other += mean_other
        noise_summary += mean_noise
        harps_summary += mean_remov
        loot_summary["lavish_beans"] += mean_lbean
        loot_summary["magic_beans"] += mean_mbean
        loot_summary["mysteries"] += mean_mysts
        loot_summary["fertilizers"] += mean_fert
        fert_have += mean_fert
        chain.append(f"{tag}({cheese})")
        loot_summary["golden_harps"] -= mean_remov
        #if loot_summary["golden_harps"] < 0:
        #    raise ValueError("Not enough Golden Harps to sustain. Do a Harp run in Ballroom.")

    def run_ballroom(cheese, target_room=None, tag="Ballroom"):
        nonlocal total_hunts, fert_have, hunts_with_royal, hunts_with_other, noise_summary, harps_summary
        res = simulate_ballroom(trap_power, trap_luck, use_ref, use_cc, cheese, t, use_key=0, ruby_removal=0, gquill=gquill, feather=feather, n_runs=n_runs)
        mean, std, dist, mean_rbean, std_rbean, dist_rbean, mean_harps, std_harps, dist_harps, mean_mysts, std_mysts, dist_mysts, mean_fert, std_fert, dist_fert, mean_other, std_other, dist_other, mean_royal, std_royal, dist_royal, mean_noise, std_noise, dist_noise, mean_remov, std_remov, dist_remov = res
        total_hunts += mean
        hunts_with_royal += mean_royal
        hunts_with_other += mean_other
        noise_summary += mean_noise
        harps_summary += mean_remov
        loot_summary["royal_beans"] += mean_rbean
        loot_summary["golden_harps"] += mean_harps
        loot_summary["mysteries"] += mean_mysts
        loot_summary["fertilizers"] += mean_fert
        fert_have += mean_fert
        chain.append(f"{tag}({cheese})")
        loot_summary["golden_harps"] -= mean_remov
        #if loot_summary["golden_harps"] < 0:
        #    raise ValueError("Not enough Golden Harps to sustain. Do a Harp run in Ballroom.")

    def run_greathall(cheese):
        nonlocal total_hunts, fert_have, hunts_with_royal, hunts_with_other, noise_summary, harps_summary
        res = simulate_greathall(trap_power, trap_luck, use_ref, use_cc, cheese, use_key=1, gquill=1, feather=1, n_runs=n_runs)
        mean, std, dist, mean_eggs, std_eggs, dist_eggs, mean_fert, std_fert, dist_fert, mean_other, std_other, dist_other, mean_royal, std_royal, dist_royal, mean_noise, std_noise, dist_noise, mean_remov, std_remov, dist_remov = res
        total_hunts += mean
        hunts_with_royal += mean_royal
        hunts_with_other += mean_other
        noise_summary += mean_noise
        harps_summary += mean_remov
        loot_summary["golden_eggs"] += mean_eggs
        loot_summary["fertilizers"] += mean_fert
        fert_have += mean_fert
        chain.append(f"Great Hall({cheese})")
        loot_summary["golden_harps"] -= mean_remov
        if loot_summary["golden_harps"] < 0:
            raise ValueError("Not enough Golden Harps to sustain. Do a Harp run in Ballroom.")

    # Start planning
    # Do beanstalk if no fert
    if fert_have <= 0:
        run_beanstalk()

    while loot_summary[loot_key] < goal:
        # Harp check
        if loot_summary["golden_harps"] < harp_threshold:
            # Do Ballroom 
            while fert_have < stage_cost["Ballroom"]:
                if fert_have < stage_cost["Dungeon"]:
                    run_beanstalk()
                fert_have -= stage_cost["Dungeon"]
                run_dungeon(cheese)
            fert_have -= stage_cost["Ballroom"]
            run_ballroom(cheese, target_room="harps", tag="Ballroom(Harp run)")
        
        if required_stage == "Dungeon":
            # Dungeon costs 1 fert
            while fert_have < stage_cost["Dungeon"]:
                run_beanstalk()
            fert_have -= stage_cost["Dungeon"]
            loot_summary["fertilizers"] -= stage_cost["Dungeon"]
            run_dungeon(cheese, t)

        elif required_stage == "Ballroom":
            # Ballroom costs 12 fert
            while fert_have < stage_cost["Ballroom"]:
                # Check if we need beanstalk run
                if fert_have < stage_cost["Dungeon"]:
                    run_beanstalk()
                # Then run dungeon
                fert_have -= stage_cost["Dungeon"]
                loot_summary["fertilizers"] -= stage_cost["Dungeon"]
                run_dungeon(cheese)
            fert_have -= stage_cost["Ballroom"]
            loot_summary["fertilizers"] -= stage_cost["Ballroom"]
            run_ballroom(cheese, t)

        elif required_stage == "Great Hall":
            # Check if you can get into Ballroom or not
            while fert_have < stage_cost["Ballroom"]:
                # Check if we need beanstalk run
                if fert_have < stage_cost["Dungeon"]:
                    run_beanstalk()
                # Then run dungeon
                fert_have -= stage_cost["Dungeon"]
                loot_summary["fertilizers"] -= stage_cost["Dungeon"]
                run_dungeon(cheese)
            # Check if you can get into Great Hall or not
            while fert_have < stage_cost["Great Hall"]:
                fert_have -= stage_cost["Ballroom"]
                loot_summary["fertilizers"] -= stage_cost["Ballroom"]
                run_ballroom(cheese)
            fert_have -= stage_cost["Great Hall"]
            loot_summary["fertilizers"] -= stage_cost["Great Hall"]
            run_greathall(cheese)
        # Otherwise, just chill in beanstalk
        elif required_stage == "Beanstalk":
            run_beanstalk()

    return chain, total_hunts, hunts_with_royal, hunts_with_other, hunts_with_stalk, noise_summary, harps_summary, loot_summary

# Main
if __name__ == "__main__":
    # Input parameter
    # Setup
    print(f"\n========== Input your setup ==========")
    trap_power = int(input("Enter Trap Power: "))
    trap_luck = int(input("Enter Trap Luck: "))
    use_cc = int(input("Condensed Creativity? (1=yes, 0=no): "))
    use_ref = int(input("(At least Ruby) Refractor Base? (1=yes, 0=no): "))
    gquill = int(input("Has Golden Quill? (1=yes, 0=no): "))
    feather = int(input("Golden Goose Feather? (1=yes, 0=no): "))
    
    # Pick sim mode
    mode = input("Select Stage (Beanstalk / Dungeon / Ballroom / Great Hall / Plan): ").strip()
    # Sim for Beanstalk stage
    if mode.lower() == "beanstalk":
        # Simulate run
        mean, std, dist, mean_bean, std_bean, dist_bean, mean_fert, std_fert, dist_fert = simulate_beanstalk(trap_power, trap_luck, use_ref, use_cc)
        # Print result
        print(f"\n========== Simulation Result ==========")
        print(f"Beanstalk average hunts to catch Vinneus: {mean:.2f} ± {std:.2f}")
        print(f"Min hunts: {min(dist)}, Max hunts: {max(dist)}")
        print(f"Average beans collected: {mean_bean:.2f} ± {std_bean:.2f}")
        print(f"Min beans: {min(dist_bean)}, Max beans: {max(dist_bean)}")
        print(f"Average Fabled Fertilizer collected: {mean_fert:.2f} ± {std_fert:.2f}")
        print(f"Min fertilizer: {min(dist_fert)}, Max fertilizer: {max(dist_fert)}")
    # Sim for Dungeon stage
    elif mode.lower() == "dungeon":
        # Use key
        use_key = int(input("Giant Key? (1=yes, 0=no): "))
        # Pick cheese
        cheese_input = input("Cheese type (SB / Beanster / Lavish / Royal): ")
        # Normalize to match dictionary keys
        cheese_map = {
            "sb": "SB",
            "beanster": "Beanster",
            "lavish": "Lavish",
            "royal": "Royal"}
        if cheese_input not in cheese_map:
            raise ValueError("Invalid cheese! Use SB / Beanster / Lavish / Royal")
        cheese = cheese_map[cheese_input]
        # Simulate run
        mean, std, dist, mean_lbean, std_lbean, dist_lbean, mean_mbean, std_mbean, dist_mbean, mean_mysts, std_mysts, dist_mysts, mean_fert, std_fert, dist_fert = simulate_dungeon(trap_power, trap_luck, use_ref, use_cc, cheese, use_key, gquill, feather)
        # Print result
        print(f"\n========== Simulation Result ==========")
        print(f"Dungeon average hunts: {mean:.2f} ± {std:.2f}")
        print(f"Min hunts: {min(dist)}, Max hunts: {max(dist)}")
        print(f"Average lavish beans collected: {mean_lbean:.2f} ± {std_lbean:.2f}")
        print(f"Min lavish beans: {min(dist_lbean)}, Max lavish beans: {max(dist_lbean)}")
        print(f"Average magic beans collected: {mean_mbean:.2f} ± {std_mbean:.2f}")
        print(f"Min magic beans: {min(dist_mbean)}, Max magic beans: {max(dist_mbean)}")
        print(f"Average mystery loot collected: {mean_mysts:.2f} ± {std_mysts:.2f}")
        print(f"Min mystery loot: {min(dist_mysts)}, Max mystery loot: {max(dist_mysts)}")
        print(f"Average Fabled Fertilizer collected: {mean_fert:.2f} ± {std_fert:.2f}")
        print(f"Min fertilizer: {min(dist_fert)}, Max fertilizer: {max(dist_fert)}")
    # Sim for Ballroom stage
    elif mode.lower() == "ballroom":
        # Use key
        use_key = int(input("Giant Key? (1=yes, 0=no): "))
        # Ruby removal
        ruby_removal = int(input("Ruby Removal? (1=yes, 0=no): "))
        # Pick cheese
        cheese_input = input("Cheese type (SB / Beanster / Lavish / Royal): ")
        # Normalize to match dictionary keys
        cheese_map = {
            "sb": "SB",
            "beanster": "Beanster",
            "lavish": "Lavish",
            "royal": "Royal"}
        if cheese_input not in cheese_map:
            raise ValueError("Invalid cheese! Use SB / Beanster / Lavish / Royal")
        cheese = cheese_map[cheese_input]
        # Simulate run
        mean, std, dist, mean_rbean, std_rbean, dist_rbean, mean_harps, std_harps, dist_harps, mean_mysts, std_mysts, dist_mysts, mean_fert, std_fert, dist_fert = simulate_ballroom(trap_power, trap_luck, use_ref, use_cc, cheese, use_key, ruby_removal, gquill, feather)
        # Print result
        print(f"\n========== Simulation Result ==========")
        print(f"Ballroom average hunts: {mean:.2f} ± {std:.2f}")
        print(f"Min hunts: {min(dist)}, Max hunts: {max(dist)}")
        print(f"Average royal beans collected: {mean_rbean:.2f} ± {std_rbean:.2f}")
        print(f"Min royal beans: {min(dist_rbean)}, Max royal beans: {max(dist_rbean)}")
        print(f"Average golden harps collected: {mean_harps:.2f} ± {std_harps:.2f}")
        print(f"Min golden harps: {min(dist_harps)}, Max golden harps: {max(dist_harps)}")
        print(f"Average mystery loot collected: {mean_mysts:.2f} ± {std_mysts:.2f}")
        print(f"Min mystery loot: {min(dist_mysts)}, Max mystery loot: {max(dist_mysts)}")
        print(f"Average Fabled Fertilizer collected: {mean_fert:.2f} ± {std_fert:.2f}")
        print(f"Min fertilizer: {min(dist_fert)}, Max fertilizer: {max(dist_fert)}")
    # Sim for Great Hall stage
    elif mode.lower() == "great hall":
        # Use key
        use_key = int(input("Giant Key? (1=yes, 0=no): "))
        # Pick cheese
        cheese_input = input("Cheese type (SB / Beanster / Lavish / Royal): ")
        # Normalize to match dictionary keys
        cheese_map = {
            "sb": "SB",
            "beanster": "Beanster",
            "lavish": "Lavish",
            "royal": "Royal"}
        if cheese_input not in cheese_map:
            raise ValueError("Invalid cheese! Use SB / Beanster / Lavish / Royal")
        cheese = cheese_map[cheese_input]
        # Simulate run
        mean, std, dist, mean_eggs, std_eggs, dist_eggs, mean_fert, std_fert, dist_fert = simulate_greathall(trap_power, trap_luck, use_ref, use_cc, cheese, use_key, gquill, feather)
        # Print result
        print(f"\n========== Simulation Result ==========")
        print(f"Great Hall average hunts: {mean:.2f} ± {std:.2f}")
        print(f"Min hunts: {min(dist)}, Max hunts: {max(dist)}")
        print(f"Average golden eggs collected: {mean_eggs:.2f} ± {std_eggs:.2f}")
        print(f"Min golden eggs: {min(dist_eggs)}, Max golden eggs: {max(dist_eggs)}")
        print(f"Average Fabled Fertilizer collected: {mean_fert:.2f} ± {std_fert:.2f}")
        print(f"Min fertilizer: {min(dist_fert)}, Max fertilizer: {max(dist_fert)}")
    # Sim for planning chain run
    elif mode.lower() == "plan":
        # Inventory
        print(f"\n========== Input your inventory ==========")
        inventory = {
            "lavish_beans": int(input("Current Lavish Beans: ")),
            "magic_beans": int(input("Current Magic Beans: ")),
            "royal_beans": int(input("Current Royal Beans: ")),
            "golden_harps": int(input("Current Golden Harps: ")),
            "golden_eggs": int(input("Current Golden Eggs: ")),
            #"mysteries": int(input("Current Mystery Loot: ")),
            "fertilizers": int(input("Current Fabled Fertilizers: "))}
        # Target
        print(f"\n========== Input your target ==========")
        target_loot = input("Target loot (magic/lavish/royal/harps/eggs): ").strip().lower()
        goal = int(input("Number of target loot: "))
        # Determine cheese
        cheese_input = input("Cheese type (sb/beanster/(leaping)lavish/royal): ")
        # Normalize to match dictionary keys
        cheese_map = {
            "sb": "SB",
            "beanster": "Beanster",
            "lavish": "Lavish",
            "royal": "Royal"}
        if cheese_input not in cheese_map:
            raise ValueError("Invalid cheese! Use SB/Beanster/Lavish/Royal")
        cheese = cheese_map[cheese_input]
        
        # Plan the chain run
        chain, total_hunts, total_royal, total_other, total_sb, total_noise, total_harps, loot_summary = plan_chain(target_loot, inventory, trap_power, trap_luck, use_ref, use_cc, gquill, feather, cheese, goal, n_runs=1000, harp_threshold=5000)

        print(f"\n========== Plan Run Result ==========")
        print(f"Planned chain: {' -> '.join(chain)}")
        print(f"\n========== Plan Run Result ==========")
        print(f"Total average hunts: {total_hunts:.2f}")
        print(f"Average hunts with SB+ (beanstalk): {total_sb:.2f}")
        print(f"Average hunts with {cheese}: {total_other:.2f}")
        print(f"Average hunts with Royal: {total_royal:.2f}")
        print(f"Average noise raised during the run: {total_noise:.2f}")
        print(f"Average harps required for the run: {total_harps:.2f}")
        print(f"\n========== Plan Run Result ==========")
        print("Average final loot gained:")
        for k, v in loot_summary.items():
            if v > 0:
                print(f"  {k}: {v:.2f}")
        
    # Raise error for other models
    else:
        raise ValueError("Invalid Setup")
