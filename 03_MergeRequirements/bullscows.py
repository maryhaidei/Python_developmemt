import random 
import sys 
import urllib.request
import typing
import cowsay

def bullscows(d: str, z: str) -> (int, int): 
    cows = sum(min(z.count(l),z.count(l)) for l in set([l for l in d+z if l in d and l in z]))
    bulls = sum ([1 for i in range(len(d)) if d[i]==z[i]])
    return (bulls, cows-bulls)

def ask(promt, valid): 
    print(cowsay.cowsay(promt,cow=random.choice(cowsay.list_cows())))
    st=input()
    if valid:
        while st not in valid: 
            print(cowsay.cowsay(promt,cow=random.choice(cowsay.list_cows())))
            st=input()
    return st 

def inform(format_string: str, bulls: int, cows: int) -> None: 
    print(cowsay.cowsay(format_string.format(bulls, cows), cow=random.choice(cowsay.list_cows())))

def gameplay(a: typing.Callable[[str, typing.Optional[typing.List[str]]], str],
             inf: typing.Callable[[str, int, int], None],
             words: typing.List[str]) -> int:
    s = random.choice(words)
    asks=0
    while 1: 
        b, c = bullscows(a("Введите слово:", words), s); asks+=1
        inf("Быки: {}, Коровы: {}", b, c)
        if b == len(s): break; 
    return asks

def read_dict(dit, l): 
    if dit.startswith(('http://', 'https://')):
        with urllib.request.urlopen(dit) as resp:
            cont = resp.read().decode('utf-8')
    else:
        with open(dit, 'r', encoding='utf-8') as file:
            cont = file.read()
    ret = [word.strip() for word in cont.split() if word.strip()]  
    return [r for r in ret if len(r)==l]

def main(): 
    lenth=5
    if len(sys.argv)<2 :
        print("Использование: python -m bullscows словарь длина")
        return 
    if len(sys.argv)>2 : 
        try: 
            lenth=int(sys.argv[-1])
        except : 
            print("Длина слова - натуральное число")
    dit = read_dict(sys.argv[-2], lenth)
    if not dit: 
        print("В словаре нет слов длинны ", lenth)
        return 
    print('Вы угадали слово! Количество попыток:', gameplay(ask, inform, dit))
    
if __name__ == "__main__":
    main() 