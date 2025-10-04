from dataclasses import dataclass
from typing import Dict, List, Optional
import numpy as np
import random
import math
import pdb
import sys

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

# Result Storage
@dataclass
class SimResult:
    hunts: List[int]
    loot: Dict[str, List[int]]

    def mean(self) -> Dict[str, float]:
        return {key: float(np.mean(vals)) for key, vals in {**self.loot, "hunts": self.hunts}.items()}
    def std(self) -> Dict[str, float]:
        return {key: float(np.std(vals)) for key, vals in {**self.loot, "hunts": self.hunts}.items()}

# Do hunt simulation
def do_sim(mice: MiceData,
           trap_power: int,
           trap_luck: int,
           n_hunts: int,
           cheese: str,
           zone: str,
           loot_multi: int,
           room_type: Optional[str] = None,
           ) -> Dict[str, List[int]]:
    
    # Result dictionary
    out = {"beans": 0, "ferts": 0, "harps": 0,
           "mbean": 0, "lbean": 0, "rbean": 0, "mysts": 0, 
           "norms": 0, "bster": 0, "llavi": 0, "royal": 0,
           "geggs": 0, "noise": 0, "harps_spent": 0}
    
    # Loop over runs
    for _ in range(n_hunts):
        m_pow, m_eff, _ = mice.get_mouse(cheese, zone)
        if random.random() < mice.catch_rate(trap_power, trap_luck, m_pow, m_eff):
            # Generic counters
            ## Count cheese spent for Beanstalk run
            if cheese == "SB": out["norms"] += 1
            ## Count cheese spent for Castle run
            if cheese == "Beanster": out["bster"] += 1
            if cheese == "Lavish": out["llavi"] += 1
            if cheese == "Royal": out["royal"] += 1

            # Zone specific counters
            if zone == "Beanstalk":
                out["beans"] += loot_multi
            elif zone == "Dungeon":
                if room_type == "lavish": out["lbean"] += loot_multi
                elif room_type == "magic": out["mbean"] += loot_multi
                elif room_type == "mysteries": out["mysts"] += loot_multi
            elif zone == "Ballroom":
                if room_type == "royal": out["rbean"] += loot_multi
                elif room_type == "harps": out["harps"] += loot_multi
                elif room_type == "mysteries": out["mysts"] += loot_multi
            elif zone == "Great Hall":
                out["geggs"] += loot_multi
            
    return out

# Merge the result
def merge_loot(*dicts: Dict[str, int]) -> Dict[str, int]:
    out = {}
    for d in dicts:
        for keys, vals in d.items():
            if keys not in out:
                out[keys] = 0
            out[keys] += vals
    return out

# Simulator for Beanstalk 
def simulate_beanstalk(trap_power: int, trap_luck: int, use_ref: bool, n_runs: int=1000) -> SimResult:
    # Fetch mice data
    mice = MiceData()

    # Initialize results dictionary
    results = {
        "hunts": [],
        "beans": [],
        "ferts": []}

    # Room distribution
    room_types = ["Standard", "Super", "Extreme", "Ultimate"]
    room_probs = [0.05, 0.18, 0.70, 0.07]
    room_multi = {"Standard": 1, "Super": 2, "Extreme": 4, "Ultimate": 8}

    for _ in range(n_runs):
        run_loot = {keys: 0 for keys in results if keys != "hunts"}
        hunts = 0

        # Pick a room
        room = np.random.choice(room_types, p=np.array(room_probs)/sum(room_probs))
        multiplier = room_multi[room]

        # 20 guaranteed hunts
        hunts += 20
        loot = do_sim(mice, trap_power, trap_luck, 20, "SB", "Beanstalk", multiplier)
        run_loot = merge_loot(run_loot, loot)

        # Boss fight
        boss = mice.get_boss("Beanstalk")
        b_pow, b_eff = boss["powers"][0], boss["effects"][0]
        boss_caught = False
        while not boss_caught:
            hunts += 1
            if random.random() < mice.catch_rate(trap_power, trap_luck, b_pow, b_eff):
                run_loot["beans"] += multiplier + 20
                run_loot["ferts"] += 1
                boss_caught = True

        # If using refractor base, double ferts
        if use_ref:
            run_loot["ferts"] *= 2

        # Append results
        results["hunts"].append(run_loot.get("hunts", hunts))
        for keys, vals in run_loot.items():
            results.setdefault(keys, []).append(vals)

    return SimResult(results["hunts"], {keys: results[keys] for keys in results if keys != "hunts"})

# Simulator for Room 1 Retreat
def simulate_r1r(mice: MiceData, trap_power: int, trap_luck: int, 
                room_types: List[str], room_probs: List[float], room_dicts: Dict[str, List[float]],
                denom_names: List[str], denom_mults: List[int],
                loot_keys: Dict[str, str], boss_reward: Dict[str, int], noise_cap: int, zone: str) -> Dict[str, int]:
    # Initialize results dictionary
    results = {
        "hunts": 0, "mbean": 0, "lbean": 0, "rbean": 0, "harps": 0, "mysts": 0, 
        "ferts": 0, "bster": 0, "llavi": 0, "royal": 0, "noise": 0, "harps_spent": 0}
    boss_caught = False

    # Roll for the room
    room_type = np.random.choice(room_types, p=np.array(room_probs)/sum(room_probs))
    denom = np.random.choice(denom_names, p=np.array(room_dicts[room_type])/sum(room_dicts[room_type]))
    multiplier = denom_mults[denom_names.index(denom)]

    # Leaping lavish cheese for 4 hunts
    for _ in range(4):
        results["hunts"] += 1
        results["llavi"] += 1
        results["noise"] += 4 * multiplier # 4 from (leaping) lavish
        m_pow, m_eff, _ = mice.get_mouse("Lavish", zone)
        if random.random() < mice.catch_rate(trap_power, trap_luck, m_pow, m_eff):
            results[loot_keys[room_type]] += 4 * multiplier
    # Expend harps to fill noise meter
    results["harps_spent"] += (noise_cap - results["noise"])

    # Beanster cheese for 20 hunts
    for _ in range(19):
        results["hunts"] += 1
        results["bster"] += 1
        m_pow, m_eff, _ = mice.get_mouse("Beanster", zone)
        if random.random() < mice.catch_rate(trap_power, trap_luck, m_pow, m_eff):
            results[loot_keys[room_type]] += 2 * multiplier # 1 from beanster, 1 from chase 

    # Boss fight
    boss = mice.get_boss(zone)
    while not boss_caught:
        results["hunts"] += 1
        results["bster"] += 1
        if random.random() < mice.catch_rate(trap_power, trap_luck, boss["powers"][0], boss["effects"][0]):
            for k, v in boss_reward.items():
                results[k] += v
            results[loot_keys[room_type]] += 2 * multiplier
            boss_caught = True
        
    return results

# Simulator for farming a specific loot
def simulate_farm(mice: MiceData, trap_power: int, trap_luck: int, 
                  room_types: List[str], room_probs: List[float], room_dicts: Dict[str, List[float]],
                  denom_names: List[str], denom_mults: List[int],
                  loot_keys: Dict[str, str], boss_reward: Dict[str, int],
                  target_loot: Optional[str], zone: str) -> Dict[str, int]:
    # Initialize results dictionary
    results = {
        "hunts": 0, "mbean": 0, "lbean": 0, "rbean": 0, "harps": 0, "mysts": 0, 
        "ferts": 0, "bster": 0, "llavi": 0, "royal": 0, "noise": 0, "harps_spent": 0}
    boss_caught = False

    while not boss_caught:
        # Roll for the room
        room_type = np.random.choice(room_types, p=np.array(room_probs)/sum(room_probs))
        denom = np.random.choice(denom_names, p=np.array(room_dicts[room_type])/sum(room_dicts[room_type]))
        multiplier = denom_mults[denom_names.index(denom)]

        # Leaping lavish cheese for 4 hunts
        for _ in range(4):
            results["hunts"] += 1
            results["llavi"] += 1
            results["noise"] += 16 * multiplier # 4 from (leaping) lavish, 4 from feather and quill
            m_pow, m_eff, _ = mice.get_mouse("Lavish", zone)
            if random.random() < mice.catch_rate(trap_power, trap_luck, m_pow, m_eff):
                results[loot_keys[room_type]] += 16 * multiplier

        # Spend harps to erase noise
        results["harps_spent"] += results["noise"]
        results["noise"] = 0

        # Check for ultimate room
        if denom == "Ultimate" and room_type == target_loot:
            # Use Royal cheese for 20 hunts
            for _ in range(20):
                results["hunts"] += 1
                results["royal"] += 1
                m_pow, m_eff, _ = mice.get_mouse("Royal", zone)
                if random.random() < mice.catch_rate(trap_power, trap_luck, m_pow, m_eff):
                    results[loot_keys[room_type]] += 1024 # 16 from cheese, 2 from CC, 4 from feather and quill
            # Giant chase
            for _ in range(19):
                results["hunts"] += 1
                results["royal"] += 1
                m_pow, m_eff, _ = mice.get_mouse("Royal", zone)
                if random.random() < mice.catch_rate(trap_power, trap_luck, m_pow, m_eff):
                    results[loot_keys[room_type]] += 2048
            # Boss fight
            boss = mice.get_boss(zone)
            while not boss_caught:
                results["hunts"] += 1
                results["royal"] += 1
                if random.random() < mice.catch_rate(trap_power, trap_luck, boss["powers"][0], boss["effects"][0]):
                    for keys, vals in boss_reward.items():
                        results[keys] += vals
                    results[loot_keys[room_type]] += 2048
                    boss_caught = True

    return results

# Simulator for Dungeon
def simulate_dungeon(trap_power: int, trap_luck: int, use_ref: bool, target_loot: Optional[str]=None, n_runs: int=1000) -> SimResult:
    # Fetch mice data
    mice = MiceData()
    
    # Initialize results dictionary
    results = {
        "hunts": [], "lbean": [], "mbean": [], "mysts": [], "ferts": [],
        "bster": [], "llavi": [], "royal": [], "noise": [], "harps_spent": []}

    # Room 1 Retreat parameter
    r1r_params = dict(
        room_types = ["lavish", "magic", "mysteries"],
        room_probs = [0.706, 0.152, 0.141],
        room_dicts = {
            "lavish": [0.043, 0.261, 0.272, 0.130],
            "magic": [0.065, 0.043, 0.022, 0.022],
            "mysteries": [0.087, 0.054, 0.0, 0.0]},
        denom_names = ["Standard", "Super", "Extreme", "Ultimate"],
        denom_mults = [1, 2, 4, 8],
        loot_keys = {"lavish": "lbean", "magic": "mbean", "mysteries": "mysts"},
        boss_reward = {"mbean": 20, "ferts": 5},
        noise_cap = 200)
    
    # Ultimate Target Farming parameter
    farm_params = dict(
        room_types = ["lavish", "magic", "mysteries"],
        room_probs = [0.861, 0.093, 0.046],
        room_dicts = {
            "lavish": [0.287, 0.441, 0.133],
            "magic": [0.062, 0.022, 0.009],
            "mysteries": [0.037, 0.009, 0.0]},
        denom_names = ["Super", "Extreme", "Ultimate"],
        denom_mults = [2, 4, 8],
        loot_keys = {"lavish": "lbean", "magic": "mbean", "mysteries": "mysts"},
        boss_reward = {"mbean": 20, "ferts": 5})

    # Simulate run
    for i in range(n_runs):
        if target_loot is None:
            # Default to R1R
            run_loot = simulate_r1r(mice, trap_power, trap_luck, **r1r_params, zone = "Dungeon")
        else:
            # Find ultimate target room to farm
            run_loot = simulate_farm(mice, trap_power, trap_luck, **farm_params, target_loot = target_loot, zone = "Dungeon")
    
        # Double ferts if using refractor base
        if use_ref:
            run_loot["ferts"] *= 2

        # Append results
        results["hunts"].append(run_loot.get("hunts"))
        for keys, vals in run_loot.items():
            results.setdefault(keys, []).append(vals)

    return SimResult(results["hunts"], {keys: results[keys] for keys in results if keys != "hunts"})

# Simulator for Ballroom
def simulate_ballroom(trap_power: int, trap_luck: int, use_ref: bool, target_loot: Optional[str]=None, n_runs: int=1000) -> SimResult:
    # Fetch mice data
    mice = MiceData()

    # Initialize results dictionary
    results = {
        "hunts": [], "rbean": [], "harps": [], "mysts": [], "ferts": [],
        "bster": [], "llavi": [], "royal": [], "noise": [], "harps_spent": []}

    # Room 1 Retreat parameters
    r1r_params = dict(
        room_types = ["royal", "harps", "mysteries"],
        room_probs = [0.672, 0.184, 0.144],
        room_dicts = {
            "royal": [0.070, 0.334, 0.201, 0.067],
            "harps": [0.070, 0.054, 0.070, 0.023],
            "mysteries": [0.057, 0.020, 0.017, 0.017]},
        denom_names = ["Standard", "Super", "Extreme", "Ultimate"],
        denom_mults = [1, 2, 4, 8],
        loot_keys = {"royal": "rbean", "harps": "harps", "mysteries": "mysts"},
        boss_reward = {"ferts": 20},
        noise_cap = 400)
    
    # Ultimate Target Farming parameters
    farm_params = dict(
        room_types = ["royal", "harps", "mysteries"],
        room_probs = [0.509, 0.359, 0.132],
        room_dicts = {
            "royal": [0.417,0.250,0.083],
            "harps": [0.067,0.088,0.029],
            "mysteries": [0.025,0.021,0.020]},
        denom_names = ["Super", "Extreme", "Ultimate"],
        denom_mults = [2, 4, 8],
        loot_keys = {"royal": "rbean", "harps": "harps", "mysteries": "mysts"},
        boss_reward = {"ferts": 20})
    
    # Simulate runs
    for _ in range(n_runs):
        if target_loot is None:
            # Default to R1R
            run_loot = simulate_r1r(mice, trap_power, trap_luck, **r1r_params, zone = "Ballroom")
        else:
            # Find ultimate target room to farm
            run_loot = simulate_farm(mice, trap_power, trap_luck, **farm_params, target_loot = target_loot, zone = "Ballroom")
    
        # Double ferts if using refractor base
        if use_ref:
            run_loot["ferts"] *= 2

        # Append results
        results["hunts"].append(run_loot.get("hunts"))
        for keys, vals in run_loot.items():
            results.setdefault(keys, []).append(vals)

    return SimResult(results["hunts"], {keys: results[keys] for keys in results if keys != "hunts"})

# Simulator for Great Hall
def simulate_greathall(trap_power: int, trap_luck: int, use_ref: bool, n_runs: int=1000) -> SimResult:
    # Fetch mice data
    mice = MiceData()

    # Initialize results dictionary
    results = {
        "hunts": [], "mbean": [], "lbean": [], "rbean": [],
        "geggs": [], "ferts": [], "llavi": [], "royal": [],
        "noise": [], "harps_spent": []}

    # Room setup (always use key in Great Hall)
    room_types = ["Super", "Extreme", "Ultimate"]
    room_probs = [0.580, 0.245, 0.175]
    room_multi = {"Super": 2, "Extreme": 4, "Ultimate": 8}

    for _ in range(n_runs):
        run_loot = {keys: 0 for keys in results if keys != "hunts"}
        hunts = 0
        boss_caught = False

        # Loop until boss caught (i.e. ultimate room found and completed)
        while not boss_caught:
            # Pick a room
            denom = np.random.choice(room_types, p=np.array(room_probs)/sum(room_probs))
            room_multiplier = room_multi[denom]

            # Leaping lavish cheese for 4 hunts
            for _ in range(4):
                hunts += 1
                run_loot["llavi"] += 1
                run_loot["noise"] += 16 * room_multiplier # 4 from (leaping) lavish, 4 from feather and quill
                m_pow, m_eff, _ = mice.get_mouse("Lavish", "Great Hall")
                if random.random() < mice.catch_rate(trap_power, trap_luck, m_pow, m_eff):
                    run_loot["geggs"] += 16 * room_multiplier
            
            # Reduce noise with harps
            run_loot["harps_spent"] += run_loot["noise"]
            run_loot["noise"] = 0

            # If Ultimate room, do 20 hunts with royal cheese, 20 hunts of chase, then boss
            if denom == "Ultimate":
                # 20 hunts with royal cheese
                for _ in range(20):
                    hunts += 1
                    run_loot["royal"] += 1
                    m_pow, m_eff, _ = mice.get_mouse("Royal", "Great Hall")
                    if random.random() < mice.catch_rate(trap_power, trap_luck, m_pow, m_eff):
                        run_loot["geggs"] += 1024
                
                # Giant chase: another 19 hunts with royal cheese
                for _ in range(19):
                    hunts += 1
                    run_loot["royal"] += 1
                    m_pow, m_eff, _ = mice.get_mouse("Royal", "Great Hall")
                    if random.random() < mice.catch_rate(trap_power, trap_luck, m_pow, m_eff):
                        run_loot["geggs"] += 2048

                # Boss fight
                boss = mice.get_boss("Great Hall")
                while not boss_caught:
                    hunts += 1
                    run_loot["royal"] += 1
                    if random.random() < mice.catch_rate(trap_power, trap_luck, boss["powers"][0], boss["effects"][0]):
                        run_loot["mbean"] += 100
                        run_loot["lbean"] += 100
                        run_loot["rbean"] += 100
                        #run_loot["ferts"] += 10 # Disabled as fert from MGK is not guaranteed
                        run_loot["geggs"] += 2048
                        boss_caught = True

        # Double ferts if using refractor base
        if use_ref:
            run_loot["ferts"] *= 2

        # Append results
        results["hunts"].append(run_loot.get("hunts", hunts))
        for keys, vals in run_loot.items():
            results.setdefault(keys, []).append(vals)

    return SimResult(results["hunts"], {keys: results[keys] for keys in results if keys != "hunts"})

# Plan a chain of stages
def plan_chain(trap_power: int, trap_luck: int, use_ref: bool, target_eggs: int, inventory: Dict[str, int]) -> List[Dict[str, int]]:
    # Precompute average runs for each stage
    beanstalk = simulate_beanstalk(trap_power, trap_luck, use_ref, 1000)
    r1r_dungeon = simulate_dungeon(trap_power, trap_luck, use_ref, None, 1000)
    r1r_ballroom = simulate_ballroom(trap_power, trap_luck, use_ref, None, 1000)
    lbean_farm = simulate_dungeon(trap_power, trap_luck, use_ref, "lavish", 1000)
    mbean_farm = simulate_dungeon(trap_power, trap_luck, use_ref, "magic", 1000)
    rbean_farm = simulate_ballroom(trap_power, trap_luck, use_ref, "royal", 1000)
    harps_farm = simulate_ballroom(trap_power, trap_luck, use_ref, "harps", 1000)
    run_greathall = simulate_greathall(trap_power, trap_luck, use_ref, 1000)

    # Store precomputed average
    avg_beanstalk = beanstalk.mean()
    avg_r1r_dungeon = r1r_dungeon.mean()
    avg_r1r_ballroom = r1r_ballroom.mean()
    avg_lbean_farm = lbean_farm.mean()
    avg_mbean_farm = mbean_farm.mean()
    avg_rbean_farm = rbean_farm.mean()
    avg_harps_farm = harps_farm.mean()
    avg_run_greathall = run_greathall.mean()

    # Print out averages for reference
    precomp = {
        "Beanstalk": avg_beanstalk,
        "Dungeon (R1R)": avg_r1r_dungeon,
        "Ballroom (R1R)": avg_r1r_ballroom,
        "Dungeon (Lapis)": avg_lbean_farm,
        "Dungeon (Magic)": avg_mbean_farm,
        "Ballroom (Royal)": avg_rbean_farm,
        "Ballroom (Harps)": avg_harps_farm,
        "Great Hall": avg_run_greathall}

    print("\n========== Print Average Yield per Run ==========")
    header = f"{'Stage':17} | {'royal':5} | {'llavi':5} | {'bster':5} | {'mbean':5} | {'lbean':5} | {'rbean':5} | {'harps+':5} | {'harps-':5}"
    print(header)
    print("-" * len(header))
    for stage, loot in precomp.items():
        royal = int(loot.get("royal", 0))
        llavi = int(loot.get("llavi", 0))
        bster = int(loot.get("bster", 0))
        mbean = int(loot.get("mbean", 0))
        lbean = int(loot.get("lbean", 0))
        rbean = int(loot.get("rbean", 0))
        harps = int(loot.get("harps", 0))
        harps_spent = int(loot.get("harps_spent", 0))
        print(f"{stage:17} | {royal:<5} | {llavi:<5} | {bster:<5} | {mbean:<5} | {lbean:<5} | {rbean:<5} | {harps:<5} | {harps_spent:<5}")    

    # Setup initial inventory
    inv = inventory.copy()
    egg_count = inv.get("geggs", 0)
    chain: List[Dict[str, int]] = []

    # Fert costs
    fert_costs = {"Dungeon": 1, "Ballroom": 12, "Great Hall": 100}

    # Stage count
    stage_counts = {}

    # Loop until target eggs reached
    while egg_count < target_eggs:
        stage = None
        loot = None
        fert_spent = 0

        # Define threshold
        threshold_harps = 15000
        threshold_royal = 150
        threshold_llavi = 250

        # Threshold breakdown
        # Royal beanster check
        craftable_royal = min(inv["rbean"] // 128, inv["lbean"] // 64)
        if craftable_royal > 0 and inv["royal"] < threshold_royal:
            inv["royal"] += craftable_royal * 2
            inv["rbean"] -= craftable_royal * 128
            inv["lbean"] -= craftable_royal * 64
        deficit_royal = max(threshold_royal - inv["royal"], 0)
        deficit_royal_rbean = deficit_royal * 128
        deficit_royal_lbean = deficit_royal * 64
        # Leaping lavish beanster check
        max_llavi_harps = max((inv["harps"] - threshold_harps) // 64, 0)
        craftable_llavi = min(inv["lbean"] // 16, max_llavi_harps)
        if craftable_llavi > 0 and inv["llavi"] < threshold_llavi:
            inv["llavi"] += craftable_llavi * 2
            inv["harps"] -= craftable_llavi * 64
            inv["lbean"] -= craftable_llavi * 16
        deficit_llavi = max(threshold_llavi - inv["llavi"], 0)
        deficit_llavi_harps = deficit_llavi * 64
        deficit_llavi_lbean = deficit_llavi * 16

        # Farming run logic
        # Check for royal beanster deficit
        if inv["rbean"] < deficit_royal_rbean or inv["lbean"] < deficit_royal_lbean:
            if inv["rbean"] < deficit_royal_rbean:
                if inv["ferts"] < fert_costs["Dungeon"]:
                    stage = "Beanstalk"
                    loot = avg_beanstalk
                    fert_spent = 0
                elif inv["ferts"] < fert_costs["Ballroom"]:
                    stage = "Dungeon (R1R)"
                    loot = avg_r1r_dungeon
                    fert_spent = fert_costs["Dungeon"]
                else:
                    stage = "Ballroom (Royal)"
                    loot = avg_rbean_farm
                    fert_spent = fert_costs["Ballroom"]
            else:
                if inv["ferts"] < fert_costs["Dungeon"]:
                    stage = "Beanstalk"
                    loot = avg_beanstalk
                    fert_spent = 0
                else:
                    stage = "Dungeon (Lapis)"
                    loot = avg_lbean_farm
                    fert_spent = fert_costs["Dungeon"]
        # Check for leaping lavish beanster deficit
        elif inv["harps"] < deficit_llavi_harps or inv["lbean"] < deficit_llavi_lbean:
            if inv["harps"] < deficit_llavi_harps:
                if inv["ferts"] < fert_costs["Dungeon"]:
                    stage = "Beanstalk"
                    loot = avg_beanstalk
                    fert_spent = 0
                elif inv["ferts"] < fert_costs["Ballroom"]:
                    stage = "Dungeon (R1R)"
                    loot = avg_r1r_dungeon
                    fert_spent = fert_costs["Dungeon"]
                else:
                    stage = "Ballroom (Harps)"
                    loot = avg_harps_farm
                    fert_spent = fert_costs["Ballroom"]
            else:
                if inv["ferts"] < fert_costs["Dungeon"]:
                    stage = "Beanstalk"
                    loot = avg_beanstalk
                    fert_spent = 0
                else:
                    stage = "Dungeon (Lapis)"
                    loot = avg_lbean_farm
                    fert_spent = fert_costs["Dungeon"]
        # Check for harps
        elif inv["harps"] < threshold_harps:
            if inv["ferts"] < fert_costs["Dungeon"]:
                stage = "Beanstalk"
                loot = avg_beanstalk
                fert_spent = 0
            elif inv["ferts"] < fert_costs["Ballroom"]:
                stage = "Dungeon (R1R)"
                loot = avg_r1r_dungeon
                fert_spent = fert_costs["Dungeon"]
            else:
                stage = "Ballroom (Harps)"
                loot = avg_harps_farm
                fert_spent = fert_costs["Ballroom"]
        # If we have enough resources, go to Greathall
        else:
            if inv["ferts"] < fert_costs["Dungeon"]:
                stage = "Beanstalk"
                loot = avg_beanstalk
                fert_spent = 0
            elif inv["ferts"] < fert_costs["Ballroom"]:
                stage = "Dungeon (R1R)"
                loot = avg_r1r_dungeon
                fert_spent = fert_costs["Dungeon"]
            elif inv["ferts"] < fert_costs["Great Hall"]:
                stage = "Ballroom (R1R)"
                loot = avg_r1r_ballroom
                fert_spent = fert_costs["Ballroom"]
            else:
                stage = "Great Hall"
                loot = avg_run_greathall
                fert_spent = fert_costs["Great Hall"]

        # Deduct fert spent
        inv["ferts"] -= fert_spent
        
        # Update inventory
        consumed = {"royal", "llavi"}
        if loot:
            # Subtract the used cheese
            for keys, vals in loot.items():
                if keys in consumed:
                    inv[keys] -= int(vals)
            # Subtract harps spent
            if "harps_spent" in loot:
                inv["harps"] -= int(loot["harps_spent"])
            # Add the loot gained
            for keys, vals in loot.items():
                if keys not in consumed and keys != "harps_spent" and keys != "hunts":
                    inv[keys] = inv.get(keys, 0) + int(vals)
            # Update egg count
            if "geggs" in loot:
                egg_count += int(loot["geggs"])
        # Append stage counts
        stage_counts[stage] = stage_counts.get(stage, 0) + 1

        # Append result
        chain.append({"stage": stage, "eggs": egg_count, "harps_spent": int(loot.get("harps_spent", 0)), **{keys: int(vals) for keys, vals in loot.items() if keys not in ("hunts", "harps_spent")}, "inv": inv.copy(), "summary": stage_counts})
        
    return chain

# Main
if __name__ == "__main__":
    # Input parameter
    # Setup
    print(f"========== Input your setup ==========")
    trap_power = int(input("Enter Trap Power: "))
    trap_luck = int(input("Enter Trap Luck: "))
    use_ref = bool(int(input("(At least Ruby) Refractor Base? (1=yes, 0=no): ")))
    
    # Plan chain mode prereq
    print("\n========== Input your inventory ==========")
    inventory = {
        "llavi": int(input("Current Leaping Lavish Cheese: ")),
        "royal": int(input("Current Royal Beanster Cheese: ")),
        "lbean": int(input("Current Lavish Beans: ")),
        "mbean": int(input("Current Magic Beans: ")),
        "rbean": int(input("Current Royal Beans: ")),
        "harps": int(input("Current Golden Harps: ")),
        "geggs": int(input("Current Golden Eggs: ")),
        "ferts": int(input("Current Fabled Fertilizers: "))}
    
    # Target
    print("\n========== Input your target ==========")
    goal = int(input("Number of target eggs: "))
    
    # Plan the chain run
    chain = plan_chain(trap_power, trap_luck, use_ref, goal, inventory)

    # Print result
    print("\n========== Plan Run Result ==========")
    if "error" in chain[0]:
        print(chain[0]["error"])
        exit(1)
    print(f"Planned chain to reach {goal} eggs:")
    if "summary" in chain[-1]:
        for stage, count in chain[-1]["summary"].items():
            print(f"{stage:17} : {count}")
    print("========== Chain Breakdown ==========")
    header = f"{'Stage':17} | {'royal':7} | {'llavi':7} | {'mbean':7} | {'lbean':7} | {'rbean':7} | {'harps':7} | {'geggs':7} | {'ferts':7}"
    print(header)
    print("-" * len(header))
    for step in chain:
        inv = step["inv"]
        print(f"{step['stage']:17} | "
            f"{inv.get('royal',0):7} | {inv.get('llavi',0):7} | "
            f"{inv.get('mbean',0):7} | {inv.get('lbean',0):7} | {inv.get('rbean',0):7} | "
            f"{inv.get('harps',0):7} | {inv.get('geggs',0):7} | {inv.get('ferts',0):7}")
    #print("========== Final Inventory ==========")
    #print(chain[-1]["inv"])
    