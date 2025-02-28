import random 

def bullscows(d: str, z: str) -> (int, int): 
    cows = sum([1 for c in set(d) if c in set(z)])
    bulls = sum ([1 for i in range(len(d)) if d[i]==z[i]])
    return (bulls, cows-bulls)

def ask(promt, valid): 
    print(promt)
    st=input()
    if valid:
        while st not in valid: 
            print(promt)
            st=input()
    return st 

def inform(format_string: str, bulls: int, cows: int) -> None: 
    print(format_string.format(bulls, cows))

def gameplay(a: callable, inf: callable, words: list[str]) -> int: 
    s = random.choice(words)
    asks=0
    while 1: 
        b, c = bullscows(a("Введите слово:", words), s); asks+=1
        inf("Быки: {}, Коровы: {}", b, c)
        if b == len(s): break; 
    print(asks)