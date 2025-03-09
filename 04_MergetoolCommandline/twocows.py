import cmd
import shlex
from cowsay import cowsay,cowthink,list_cows,make_bubble

def parse_line(words):
    if not words: raise ValueError('Необходимо передавать сообщение коровки')
    message=words[0]
    kwargs={}
    if len(words)>=2: character=words[1]
    else: character='cow'
    for arg in words[2:]:
        key,value=arg.split('=', 1)
        kwargs[key]=value
    return message, character, kwargs

def get_max_str(a):
    m=0; k=0
    for b in a: 
        if b=='\n' : m=m if m>=k else k; k=0
        k+=1
    return m

def merge_cow(cow1, cow2): 
    new=''
    m = get_max_str(cow1); e = 0; s = 0; 
    l1=cow1.count('\n')
    l2=cow2.count('\n') 
    if l1<l2: cow1 = '\n'*(l2-l1)+cow1
    elif l2<l1: cow2 = '\n'*(l2-l1)+cow2 
    cow1+='\n'; cow2+='\n'
    for a in cow1: 
        if a=='\n': 
            new+=cow1[s:e]+' '*(m-(e-s))+cow2[:(e2:=cow2.index('\n')+1)]
            s=e+1; e+=1; cow2=cow2[e2:]
        else: e+=1
    return new

def cow_main(args):
    words=shlex.split(args)
    if 'reply' in words:
        Words=words[:words.index('reply')]
        message1,character1, kwargs1=parse_line(Words)
        Words=words[words.index('reply')+1:]
        message2,character2, kwargs2=parse_line(Words)
        return message1,character1, kwargs1,message2,character2, kwargs2     
    else:
        raise ValueError('Добавьте reply') 

class CowsayShell(cmd.Cmd):
    intro='Добро пожаловать в оболочку twocows!\nВведите help или ? для получения списка команд\n'
    prompt='twocows> '
    
    def do_list_cows(self,args):
        """usage: list_cows\nСписок всех коровок из модуля cowsay"""
        print(list_cows())
    
    def do_make_bubble(self, text):
        """usage: make_bubble \'text\'\nРисует фразу в облачке (0-0)"""
        if not text: raise ValueError('Вы не ввели текст для облачка (0_0)')
        print(make_bubble(text))
        
    def do_cowsay(self, args):
        """usage: cowsay сообщение [название [параметр=значение …]] reply ответ [название [[параметр=значение …]]\nРисует говорящую коровку"""
        try:
            message1,character1, kwargs1,message2,character2, kwargs2=cow_main(args)
            print(merge_cow(cowsay(message1,character1, **kwargs1),cowsay(message2,character2, **kwargs2)))
        except Exception as e:
            print('Возникла ошибка при выполнении:',e)
    
    def do_cowthink(self, args):
        """usage: cowthink сообщение [название [параметр=значение …]] reply ответ [название [[параметр=значение …]]\nРисует думающую коровку"""
        try:
            message1,character1, kwargs1,message2,character2, kwargs2=cow_main(args)
            print(merge_cow(cowthink(message1,character1, **kwargs1),cowthink(message2,character2, **kwargs2)))
        except Exception as e:
            print('Возникла ошибка при выполнении:',e)   
    
    def do_EOF(self, args):
        return True

    def postloop(self):
        print("Возвращайтесь скорее!")

CowsayShell().cmdloop()

#4 юзаджа перепишешь
#3 функции переименуешь
#доработать merge_cow
# вынести три функции за пределы класса