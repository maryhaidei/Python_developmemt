import cmd
import shlex
import readline
import threading
import sys
import socket

def msg_sendreciever(client, socket):
    while response := socket.recv(1024).rstrip().decode():
        print(f"\n{response}\n{client.prompt}{readline.get_line_buffer()}", end="", flush=True)

class cmd_client(cmd.Cmd):

    prompt = ">> "

    def __init__(self, socket, complete_socket):
        self.socket = socket
        self.complete_socket = complete_socket
        return super().__init__()
    
    def do_cows(self, args):
        self.socket.sendall('cows\n'.encode())    
    
    def do_login(self, args):
        self.socket.sendall(('login'+args+'\n').encode())    

    def do_who(self, args):
        self.socket.sendall('who\n'.encode())
        
    def emptyline(self):
        pass   
    
    def do_say(self, args):
        rcv, message = shlex.split(args)
        self.socket.sendall(('say'+rcv+ f'"{message}"\n').encode())    
        
    def complete_login(self, text, line, bi, ei):
        words = (line[:ei] + '.').split()
        self.complete_socket.sendall('cows\n'.encode())
        DICT = shlex.split(self.complete_socket.recv(1024).decode())[2:]

        return [c for c in DICT if c.startswith(text)]

    def complete_say(self, text, line, bi, ei):
        words = (line[:ei] + '.').split()
        self.complete_socket.sendall('who\n'.encode())
        DICT = shlex.split(self.complete_socket.recv(1024).decode())[:-3]

        return [c for c in DICT if c.startswith(text)]

    def do_yield(self, args):
        self.socket.sendall(('yield'+args+'\n').encode())
        
    def do_quit(self, args):
        self.socket.sendall('quit\n'.encode())
    
    def do_EOF(self, args):
        return 1    

host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as compl:
        s.connect((host, port))
        compl.connect((host, port))
        client = cmd_client(s, compl)
        request = threading.Thread(target = msg_sendreciever, args = (client, client.socket))
        request.start()
        cliet.cmdloop()