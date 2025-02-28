def bullscows(d: str, z: str) -> (int, int): 
    cows = sum([1 for c in set(d) if c in set(z)])
    bulls = sum ([1 for i in range(len(d)) if d[i]==z[i]])
    return (bulls, cows-bulls)

def ask(promt, valid): 
    print(promt)
    if valid: 
        print(*valid, sep = ',' )
        st=input()
        while st not in valid: 
            print(promt + 'из списка:')
            print(*valid, sep = ',' )
            st=input()
    else: st=input()
    return st 

def inform(format_string: str, bulls: int, cows: int) -> None: 
    print(format_string.format(bulls, cows))