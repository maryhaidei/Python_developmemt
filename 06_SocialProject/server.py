import asyncio
from cowsay import list_cows, cowsay
import shlex

connected_users = {}

async def handler(input_stream, output_stream):
    client_addr = output_stream.get_extra_info("peername")
    print(f'Connection from {client_addr}')
    current_user = None
    user_message_queue = asyncio.Queue()
    read_command = asyncio.create_task(input_stream.readline())
    get_message = asyncio.create_task(user_message_queue.get())

    while not input_stream.at_eof():
        completed, running = await asyncio.wait(
            [read_command, get_message],
            return_when=asyncio.FIRST_COMPLETED
        )

        for task in completed:
            if task is read_command:
                read_command = asyncio.create_task(input_stream.readline())
                client_data = task.result().decode().strip()
                if not client_data:
                    continue
                
                command_parts = shlex.split(client_data)
                
                if not command_parts:
                    continue
                
                if command_parts[0] == 'who':
                    online_users = '\n'.join(connected_users) if connected_users else "No active users"
                    output_stream.write(f"Online users:\n{online_users}\n".encode())
                
                elif command_parts[0] == 'cows':
                    available = sorted(set(list_cows()) - set(connected_users))
                    output_stream.write(f"Available names:\n{' '.join(available)}\n".encode())
                
                elif len(command_parts) > 1 and command_parts[0] == 'login':
                    desired_name = command_parts[1]
                    if desired_name in connected_users:
                        output_stream.write(b'Name already taken\n')
                    else:
                        current_user = desired_name
                        connected_users[current_user] = user_message_queue
                        print(f"{client_addr} authenticated as {current_user}")
                
                elif current_user:
                    if command_parts[0] == 'say' and len(command_parts) > 2:
                        target_user = command_parts[1]
                        if target_user in connected_users:
                            message = ' '.join(command_parts[2:])
                            await connected_users[target_user].put(
                                cowsay(message, cow=current_user)
                            )
                        else:
                            output_stream.write(f'User {target_user} not found\n'.encode())
                    
                    elif command_parts[0] == 'yield' and len(command_parts) > 1:
                        broadcast_message = ' '.join(command_parts[1:])
                        for username, queue in connected_users.items():
                            if username != current_user:
                                await queue.put(
                                    cowsay(broadcast_message, cow=current_user)
                                )
                    
                    elif command_parts[0] == 'quit':
                        print(f"{client_addr} logging out as {current_user}")
                        del connected_users[current_user]
                        current_user = None
                
                else:
                    output_stream.write(b'Please login first\n')
                
                await output_stream.drain()
            
            elif task is get_message:
                get_message = asyncio.create_task(user_message_queue.get())
                output_stream.write(f"{task.result()}\n".encode())
                await output_stream.drain()
    
    read_command.cancel()
    get_message.cancel()
    if current_user in connected_users:
        del connected_users[current_user]
    await output_stream.wait_closed()
    print(f"Client {client_addr} disconnected")

async def run_server():
    print("Initializing server...")
    server_instance = await asyncio.start_server(
        handler,
        host='0.0.0.0',
        port=1337
    )
    print("Server ready for connections")
    try:
        await server_instance.serve_forever()
    finally:
        print("Shutting down server")

asyncio.run(run_server())