EXP_NEEDED = [100000, 150000, 250000, 500000, 750000, 1000000, 1250000, 1500000, 2000000, 2500000, 2500000, 2500000, 2500000, 2500000, 3000000]
# A list of amount of XP required for leveling up in each of the beginning levels (1-15).

def getLevel(exp):
    level = 0

    for i in range(1000):
    # Increment by one from zero to the level cap.
        need = 0
        if  i >= len(EXP_NEEDED):
            need = EXP_NEEDED[len(EXP_NEEDED) - 1]
        else:
            need = EXP_NEEDED[i]
        # Determine the current amount of XP required to level up,
        # in regards to the "i" variable.
   
        if (exp - need) < 0:
            return ((level + (exp / need)) * 100) / 100
        # If the remaining exp < the total amount of XP required for the next level,
        # return their level using this formula.

        level += 1
        exp -= need
        # Otherwise, increase their level by one,
        # and subtract the required amount of XP to level up,
        # from the total amount of XP that the guild had.

    return 1000
    # This should never happen...