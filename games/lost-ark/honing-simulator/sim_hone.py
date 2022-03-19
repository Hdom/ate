import numpy as np
import matplotlib.pyplot as plt
import math

tier3wep = [['1304', '+1', 100, [138, 32, 4, 0, 15860, 0]],
 ['1307', '+2', 100, [138, 32, 4, 0, 16240, 0]],
 ['1310', '+3', 100, [198, 32, 6, 0, 16640, 0]],
 ['1315', '+4', 100, [198, 46, 6, 2, 17040, 0]],
 ['1320', '+5', 100, [198, 46, 6, 2, 17460, 0]],
 ['1325', '+6', 100, [198, 46, 6, 2, 17900, 0]],
 ['1330', '+7', 60, [258, 60, 8, 4, 18320, 120]],
 ['1335', '+8', 45, [258, 60, 8, 4, 18780, 120]],
 ['1340', '+9', 30, [258, 60, 8, 4, 19240, 120]],
 ['1345', '+10', 30, [320, 74, 10, 4, 19720, 120]],
 ['1350', '+11', 30, [320, 74, 10, 4, 20200, 120]],
 ['1355', '+12', 15, [320, 74, 10, 4, 20700, 120]],
 ['1360', '+13', 15, [380, 88, 10, 6, 21200, 120]],
 ['1365', '+14', 15, [380, 88, 12, 6, 21720, 120]],
 ['1370', '+15', 10, [380, 88, 12, 6, 22260, 120]]]

tier3armor = [['1304', '+1', 100, [82, 22, 2, 0, 11100, 0]],
 ['1307', '+2', 100, [82, 22, 2, 0, 11380, 0]],
 ['1310', '+3', 100, [82, 22, 4, 0, 11660, 0]],
 ['1315', '+4', 100, [120, 32, 4, 2, 11960, 0]],
 ['1320', '+5', 100, [120, 32, 4, 2, 12240, 0]],
 ['1325', '+6', 100, [120, 32, 4, 2, 12540, 0]],
 ['1330', '+7', 60, [156, 42, 4, 2, 12840, 70]],
 ['1335', '+8', 45, [156, 42, 4, 2, 13160, 70]],
 ['1340', '+9', 30, [156, 42, 4, 2, 13480, 70]],
 ['1345', '+10', 30, [192, 50, 6, 4, 13820, 70]],
 ['1350', '+11', 30, [192, 50, 6, 4, 14140, 70]],
 ['1355', '+12', 15, [192, 50, 6, 4, 14500, 70]],
 ['1360', '+13', 15, [228, 60, 6, 4, 14860, 70]],
 ['1365', '+14', 15, [228, 60, 8, 4, 15220, 70]],
 ['1370', '+15', 10, [228, 60, 8, 4, 15600, 70]]]



def tier3_sim_hone(hone_level, additional_prob, materials, type_, flag):
    book = 10 if flag else 0
    pity = 0 # initial_prob * 0.465
    hones = 0
    percents = np.random.uniform(0, 1, size=15)
    
    if type_:
        required_materials = list(filter(lambda x: x[1] == hone_level ,tier3armor))[0]
    else:
        required_materials = list(filter(lambda x: x[1] == hone_level ,tier3wep))[0]
    
    if not np.all(np.array(materials) > np.array(required_materials[-1])):
        return False, required_materials[-1], hones
    
    sim_materials = np.asarray(materials.copy())
    initial_prob = required_materials[2]
    
    first_prob = initial_prob
    max_additional = initial_prob * 2
    
    while pity != 100:
        if not np.all(sim_materials > required_materials[-1]):
            return False, required_materials[-1], hones
        
        if (initial_prob + min(max_additional, additional_prob)) + book > percents[hones] * 100:
            break
#         print("base prob:", initial_prob, "pity:", pity)
        pity = min(100, pity + (initial_prob + min(max_additional, additional_prob) + book)  * 0.465)
        initial_prob = initial_prob + (first_prob * 0.1)
        max_additional = max_additional + (first_prob * 0.1)
        
        sim_materials -= required_materials[-1]
        hones += 1
    return True, required_materials[-1], hones


def sim_hone():
    """
    honor shards, honor leap stones, fusion material, silver, gold
    """
    shared_materials = [20826, 173, 106, 3 * 10**7, 12300]
    
    """
    guardian and destruction stones are held seperately from the honing material
    """
    armor_stones = 3811
    wep_stones = 1214
    
    
    print([armor_stones, *shared_materials])
    """
    current gear level
    """
    current_gear = [9,9,9,9,9,9]
    
    
    """
    amount of hones
    """
    for i in range(1):
        """
        for each gear piece
        """
        for gear in current_gear:
            """
            sim hone, tier3_sim_hone(GEAR_LEVEL, ADDITITONAL HONE %, CURRENT MATERIAL, ARMOR_OR_WEP, USE_BOOK)
            """
            results = [tier3_sim_hone(f"+{gear}", 8, [armor_stones, *shared_materials], True, True) for i in range(10000)]
            
            hones = np.mean(list(map(lambda x: x[2], results))) # number of hones required in each sim
            success = np.mean(list(map(lambda x: x[0], results))) # how many sims succeeded

            plt.boxplot(list(map(lambda x: x[2], results)), True, vert=False)
            plt.show()
        
            """
            Right now I am choosing to continue with the idea being that I take away the average success rate away from the current material
            """
            shared_materials -= np.asarray(results[0][1][1:]) * math.ceil(hones)
            armor_stones -= results[0][1][0] * math.ceil(hones)
            
            print(hones, math.ceil(hones), success)
            
            # shared_materials

    print(shared_materials, armor_stones)

sim_hone()