import asyncio
import websockets

# List of connected clients
clients = set()
messages = []  # List holding messages and sender

async def handle_client(websocket):
    # Add new client
    clients.add(websocket)

    try:
        # Send existing messages to the new client
        for message in messages:
            await websocket.send(message)

        # Listen for messages
        async for message in websocket:
            messages.append(message)  # Store message in history
            
            # Broadcast to all clients
            await asyncio.gather(*(client.send(message) for client in clients))
    except:
        pass
    finally:
        clients.remove(websocket)  # Remove client on disconnect


async def main():
    async with websockets.serve(handle_client, "localhost", 8765):
        await asyncio.Future() # Fun forever

if __name__ == "__main__":
    # Start WebSocket server
    asyncio.run(main()) 
# end main


