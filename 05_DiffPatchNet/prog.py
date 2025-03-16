import asyncio
import cowsay
import shlex

clients = {}

async def Exec(cmd: str):
       nonlocal buffer, login, stopped
       match shlex.split(cmd):
              case ["login", _login]:
                     if (_login in cowsay.list_cows() and _login not in clients and buffer not in clients.values()):
                            login = _login
                            clients[login] = buffer
                            await buffer.put("Login successful")
                     else:
                            await buffer.put("Login failed")
              case ["who"]:
                     await buffer.put('\n'.join(clients))
              case ["cows"]:
                     await buffer.put('\n'.join(n for n in cowsay.list_cows() if n not in clients))
              case ["say", dst, msg]:
                     if login in clients and dst in clients:
                            await clients[dst].put(cowsay.cowsay(msg, cow=login))
                     else:
                            await buffer.put("Sending failed")
              case ["yield", msg]:
                     if login in clients:
                            for dst in clients.values():
                                   if dst is not buffer:
                                          await dst.put(cowsay.cowsay(msg, cow=login))
                                   else:
                                          await buffer.put("Sending failed")
              case ["quit"]:
                     if login in clients:
                            del clients[login]
                            del buffer
                            stopped = True
 
async def cowChat(reader, writer):
       pass     
 
async def main():
       server = await asyncio.start_server(cowChat, "localhost", 1337)
       async with server: 
              await server.serve_forever()
 
asyncio.run(main())