import asyncio
from websockets import connect
from urllib.request import urlopen, Request


async def receive(websocket):
    while True:
        message = await websocket.recv()
        print('Message from server', message)

async def send(websocket):
    while True: 
        await websocket.send(input('Type command which will be sent to server!'))
        print('Message sent!')
        await asyncio.sleep(0)

async def client(uri):
    async with connect(uri) as websocket:
        consumer_task = asyncio.ensure_future(receive(websocket))
        producer_task = asyncio.ensure_future(send(websocket))
        done, pending = await asyncio.wait([consumer_task, producer_task], return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
           task.cancel()
        await asyncio.Future() 
    print('Finished')

async def oneshot_connection(uri):
    async with connect(uri) as websocket:
        await websocket.close()


loop = asyncio.new_event_loop()

while True:
    cmd = input('Command, [create_game, join, terminate]\n') 

    if cmd == 'join':
        session_id = input('Input session id')
        loop.run_until_complete(client(f"ws://localhost:2137/join_to_game?session_id={session_id}"))
        
    elif cmd == 'create_game' or cmd == 'cg':
        uri = "ws://localhost:2137/create_game"
        loop.run_until_complete(oneshot_connection(uri))
        print('Created game')
        
        
    elif cmd == 'terminate' or cmd == 'tm':
        session_id = input('Input session id')
        uri = f"ws://localhost:2137/terminate_game?session_id={session_id}"
        loop.run_until_complete(oneshot_connection(uri))
        print('Game terminated')

    else:
        print('Command not supported!')

