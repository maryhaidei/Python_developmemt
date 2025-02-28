def bullscows(d: str, z: str) -> (int, int): 
    cows = sum([1 for c in set(d) if c in set(z)])
    bulls = sum ([1 for i in range(len(d)) if d[i]==z[i]])
    return (bulls, cows-bulls)

    