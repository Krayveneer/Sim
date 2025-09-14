from dataclasses import dataclass
from typing import Dict, List, Optional
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
            ferts *= 2

        # Append results
        results["hunts"].append(hunts)
        for keys in run_loot:
            results.setdefault(keys, []).append(run_loot[keys])

    return SimResult(results["hunts"], {keys: results[keys] for keys in results.items() if keys != "hunts"})

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
    results["hunts"].append(run_loot["hunts"])
    for keys in run_loot:
        if keys != "hunts":
            results[keys].append(run_loot[keys])

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
    results["hunts"].append(run_loot["hunts"])
    for keys in run_loot:
        if keys != "hunts":
            results[keys].append(run_loot[keys])

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
                        run_loot["ferts"] += 10
                        run_loot["geggs"] += 2048
                        boss_caught = True

        # Double ferts if using refractor base
        if use_ref:
            run_loot["fert"] *= 2

        # Append results
        results["hunts"].append(hunts)
        for keys in run_loot:
            results.setdefault(keys, []).append(run_loot[keys])

    return SimResult(results["hunts"], {keys: results[keys] for keys in results if keys != "hunts"})


# Plan a chain of stages
def plan_chain(inventory, trap_power, trap_luck, use_ref, goal, n_runs=1000):
    # Stage fertilizer costs
    stage_cost = {"Beanstalk": 0, "Dungeon": 1, "Ballroom": 12, "Great Hall": 100}
    
    # Initialize tracking variables
    chain = []
    total_hunts = 0
    hunts_with_royal = 0
    hunts_with_lavish = 0
    hunts_with_beanster = 0
    hunts_with_stalk = 0
    noise_summary = 0
    harps_summary = 0
    # Current loot summary
    loot_summary = {
        "royal_cheese": inventory.get("royal_cheese", 0),
        "lavish_cheese": inventory.get("lavish_cheese", 0),
        "lavish_beans": inventory.get("lavish_beans", 0),
        "magic_beans": inventory.get("magic_beans", 0),
        "royal_beans": inventory.get("royal_beans", 0),
        "golden_harps": inventory.get("golden_harps", 0),
        "golden_eggs": inventory.get("golden_eggs", 0),
        "mysts": inventory.get("mysts", 0),
        "fertilizers": inventory.get("fertilizers", 0)
    }

    fert_have = loot_summary["fertilizers"]

    # Helper functions for each stage
    def run_beanstalk():
        nonlocal total_hunts, fert_have, hunts_with_stalk
        mean_h, _, _, mean_beans, _, _, mean_ferts, _, _ = simulate_beanstalk(trap_power, trap_luck, use_ref, n_runs)
        total_hunts += mean_h
        hunts_with_stalk += mean_h
        loot_summary["magic_beans"] += mean_beans
        loot_summary["fertilizers"] += mean_ferts
        fert_have += mean_ferts
        chain.append("Beanstalk")

    def run_dungeon():
        nonlocal total_hunts, fert_have, hunts_with_royal, hunts_with_lavish, hunts_with_beanster, noise_summary, harps_summary
        res = simulate_dungeon(trap_power, trap_luck, use_ref, None, n_runs)
        (mean_h, _, _, mean_lbean, _, _, mean_mbean, _, _, mean_mysts, _, _, mean_ferts, _, _, mean_beanster, _, _, mean_lavish, _, _, mean_royal, _, _, mean_noise, _, _, mean_harps_spent, _, _) = res
        total_hunts += mean_h
        hunts_with_royal += mean_royal
        hunts_with_lavish += mean_lavish
        hunts_with_beanster += mean_beanster
        noise_summary += mean_noise
        harps_summary += mean_harps_spent
        loot_summary["lavish_beans"] += mean_lbean
        loot_summary["magic_beans"] += mean_mbean
        loot_summary["mysts"] += mean_mysts
        loot_summary["fertilizers"] += mean_ferts
        fert_have += mean_ferts
        chain.append("Dungeon")
        loot_summary["golden_harps"] -= mean_harps_spent
        loot_summary["royal_cheese"] -= mean_royal
        loot_summary["lavish_cheese"] -= mean_lavish

    def run_ballroom():
        nonlocal total_hunts, fert_have, hunts_with_royal, hunts_with_lavish, hunts_with_beanster, noise_summary, harps_summary
        res = simulate_ballroom(trap_power, trap_luck, use_ref, None, n_runs)
        (mean_h, _, _, mean_rbean, _, _, mean_harps, _, _, mean_mysts, _, _, mean_ferts, _, _, mean_beanster, _, _, mean_lavish, _, _, mean_royal, _, _, mean_noise, _, _, mean_harps_spent, _, _) = res
        total_hunts += mean_h
        hunts_with_royal += mean_royal
        hunts_with_lavish += mean_lavish
        hunts_with_beanster += mean_beanster
        noise_summary += mean_noise
        harps_summary += mean_harps_spent
        loot_summary["royal_beans"] += mean_rbean
        loot_summary["golden_harps"] += mean_harps
        loot_summary["mysts"] += mean_mysts
        loot_summary["fertilizers"] += mean_ferts
        fert_have += mean_ferts
        chain.append("Ballroom")
        loot_summary["golden_harps"] -= mean_harps_spent
        loot_summary["royal_cheese"] -= mean_royal
        loot_summary["lavish_cheese"] -= mean_lavish

    def run_greathall():
        nonlocal total_hunts, fert_have, hunts_with_royal, hunts_with_lavish, noise_summary, harps_summary
        res = simulate_greathall(trap_power, trap_luck, use_ref, n_runs)
        (mean_h, _, _, mean_eggs, _, _, mean_ferts, _, _, mean_lavish, _, _, mean_royal, _, _, mean_noise, _, _, mean_harps_spent, _, _) = res
        total_hunts += mean_h
        hunts_with_royal += mean_royal
        hunts_with_lavish += mean_lavish
        noise_summary += mean_noise
        harps_summary += mean_harps_spent
        loot_summary["golden_eggs"] += mean_eggs
        loot_summary["fertilizers"] += mean_ferts
        fert_have += mean_ferts
        chain.append("Great Hall")
        loot_summary["golden_harps"] -= mean_harps_spent
        loot_summary["royal_cheese"] -= mean_royal
        loot_summary["lavish_cheese"] -= mean_lavish

    def run_harp_farm():
        nonlocal total_hunts, fert_have, hunts_with_royal, hunts_with_lavish, hunts_with_beanster, noise_summary, harps_summary
        res = simulate_ballroom(trap_power, trap_luck, use_ref, "harps", n_runs)
        (mean_h, _, _, mean_rbean, _, _, mean_harps, _, _, mean_mysts, _, _, mean_ferts, _, _, mean_beanster, _, _, mean_lavish, _, _, mean_royal, _, _, mean_noise, _, _, mean_harps_spent, _, _) = res
        total_hunts += mean_h
        hunts_with_royal += mean_royal
        hunts_with_lavish += mean_lavish
        hunts_with_beanster += mean_beanster
        noise_summary += mean_noise
        harps_summary += mean_harps_spent
        loot_summary["royal_beans"] += mean_rbean
        loot_summary["golden_harps"] += mean_harps
        loot_summary["mysts"] += mean_mysts
        loot_summary["fertilizers"] += mean_ferts
        fert_have += mean_ferts
        chain.append("Ballroom (harp farm)")
        loot_summary["golden_harps"] -= mean_harps_spent
        loot_summary["royal_cheese"] -= mean_royal
        loot_summary["lavish_cheese"] -= mean_lavish

    def run_lavish_farm():
        nonlocal total_hunts, fert_have, hunts_with_royal, hunts_with_lavish, hunts_with_beanster, noise_summary, harps_summary
        res = simulate_dungeon(trap_power, trap_luck, use_ref, "lavish", n_runs)
        (mean_h, _, _, mean_lbean, _, _, mean_mbean, _, _, mean_mysts, _, _, mean_ferts, _, _, mean_beanster, _, _, mean_lavish, _, _, mean_royal, _, _, mean_noise, _, _, mean_harps_spent, _, _) = res
        total_hunts += mean_h
        hunts_with_royal += mean_royal
        hunts_with_lavish += mean_lavish
        hunts_with_beanster += mean_beanster
        noise_summary += mean_noise
        harps_summary += mean_harps_spent
        loot_summary["lavish_beans"] += mean_lbean
        loot_summary["magic_beans"] += mean_mbean
        loot_summary["mysts"] += mean_mysts
        loot_summary["fertilizers"] += mean_ferts
        fert_have += mean_ferts
        chain.append("Dungeon (lavish run)")
        loot_summary["golden_harps"] -= mean_harps_spent
        loot_summary["royal_cheese"] -= mean_royal
        loot_summary["lavish_cheese"] -= mean_lavish

    def refill_lavish(fert_have):
        # Repeat until lavish cheese >= 1000
        while loot_summary["lavish_cheese"] < 1000:
            # Always try to craft as many pairs as possible
            pairs = min(loot_summary["lavish_beans"] // 16, loot_summary["golden_harps"] // 64)
            crafted = pairs * 2
            if pairs > 0:
                loot_summary["lavish_cheese"] += crafted
                loot_summary["lavish_beans"] -= pairs * 16
                loot_summary["golden_harps"] -= pairs * 64
            # If not enough harps for next craft, farm harps
            elif loot_summary["golden_harps"] < 64:
                # Check for fertilizer for Ballroom
                if fert_have < stage_cost["Ballroom"]:
                    # Farm fertilizer first
                    while fert_have < stage_cost["Dungeon"]:
                        run_beanstalk()
                    fert_have -= stage_cost["Dungeon"]
                    loot_summary["fertilizers"] -= stage_cost["Dungeon"]
                    run_dungeon()
                fert_have -= stage_cost["Ballroom"]
                loot_summary["fertilizers"] -= stage_cost["Ballroom"]
                run_harp_farm()
            # If not enough lavish beans for next craft, farm lavish beans
            elif loot_summary["lavish_beans"] < 16:
                # Check for fertilizer for Dungeon
                if fert_have < stage_cost["Dungeon"]:
                    run_beanstalk()
                    fert_have += loot_summary["fertilizers"]
                fert_have -= stage_cost["Dungeon"]
                loot_summary["fertilizers"] -= stage_cost["Dungeon"]
                run_lavish_farm()
            else:
                # Should not reach here, but break to avoid infinite loop
                break

    while loot_summary["golden_eggs"] < goal:
        # Ensure lavish cheese is refilled before proceeding
        refill_lavish(fert_have)
        # If harps are low, farm harps first
        while loot_summary["golden_harps"] < 5000:
            # Check if enough fertilizer for Ballroom
            if fert_have < stage_cost["Ballroom"]:
                # Farm fertilizer first
                while fert_have < stage_cost["Dungeon"]:
                    run_beanstalk()
                fert_have -= stage_cost["Dungeon"]
                loot_summary["fertilizers"] -= stage_cost["Dungeon"]
                run_dungeon()
            fert_have -= stage_cost["Ballroom"]
            loot_summary["fertilizers"] -= stage_cost["Ballroom"]
            run_harp_farm()
        # If not enough fertilizer for Great Hall, farm it
        while fert_have < stage_cost["Great Hall"]:
            # If not enough for Ballroom, farm Dungeon
            while fert_have < stage_cost["Ballroom"]:
                # If not enough for Dungeon, farm Beanstalk
                while fert_have < stage_cost["Dungeon"]:
                    run_beanstalk()
                fert_have -= stage_cost["Dungeon"]
                loot_summary["fertilizers"] -= stage_cost["Dungeon"]
                run_dungeon()
            fert_have -= stage_cost["Ballroom"]
            loot_summary["fertilizers"] -= stage_cost["Ballroom"]
            run_ballroom()
        # Now run Great Hall
        fert_have -= stage_cost["Great Hall"]
        loot_summary["fertilizers"] -= stage_cost["Great Hall"]
        run_greathall()

    return chain, total_hunts, hunts_with_royal, hunts_with_lavish, hunts_with_beanster, hunts_with_stalk, noise_summary, harps_summary, loot_summary

# Main
if __name__ == "__main__":
    # Input parameter
    # Setup
    print(f"========== Input your setup ==========")
    trap_power = int(input("Enter Trap Power: "))
    trap_luck = int(input("Enter Trap Luck: "))
    use_ref = int(input("(At least Ruby) Refractor Base? (1=yes, 0=no): "))
    
    # Plan chain mode prereq
    print("\n========== Input your inventory ==========")
    inventory = {
        "lavish_cheese": int(input("Current Leaping Lavish Cheese: ")),
        "royal_cheese": int(input("Current Royal Beanster Cheese: ")),
        "lavish_beans": int(input("Current Lavish Beans: ")),
        "magic_beans": int(input("Current Magic Beans: ")),
        "royal_beans": int(input("Current Royal Beans: ")),
        "golden_harps": int(input("Current Golden Harps: ")),
        "golden_eggs": int(input("Current Golden Eggs: ")),
        #"mysteries": int(input("Current Mystery Loot: ")),
        "fertilizers": int(input("Current Fabled Fertilizers: "))
    }
    # Target
    print("========== Input your target ==========")
    goal = int(input("Number of target loot: "))
    
    # Plan the chain run
    chain, total_hunts, total_royal, total_lavish, total_beanster, total_sb, total_noise, total_harps, loot_summary = plan_chain(
        inventory, trap_power, trap_luck, use_ref, goal, n_runs=10000)

    print("\n========== Plan Run Result ==========")
    print(f"Planned chain: {' -> '.join(chain)}")
    print("========== Plan Run Result ==========")
    print(f"Total average hunts: {total_hunts:.2f}")
    print(f"Average hunts with SB+ (beanstalk): {total_sb:.2f}")
    print(f"Average hunts with Beanster: {total_beanster:.2f}")
    print(f"Average hunts with Lavish: {total_lavish:.2f}")
    print(f"Average hunts with Royal: {total_royal:.2f}")
    print(f"Average noise raised during the run: {total_noise:.2f}")
    print(f"Average harps required for the run: {total_harps:.2f}")
    print("\n========== Plan Run Result ==========")
    print("Average final loot gained:")
    for k, v in loot_summary.items():
        if v > 0:
            print(f"  {k}: {v:.2f}")
