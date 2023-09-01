import asyncio
import websockets

async def receive_notifications():
    uri = "ws://10.11.1.100:8000/ws" 
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(f"Received notification: {message}")

async def main():
    while True:
        try:
            await receive_notifications()
        except websockets.ConnectionClosed:
            print("La conexión WebSocket se cerró. Intentando reconectar en 5 segundos...")
            await asyncio.sleep(5)

# Ejecutar el bucle de eventos principal
if __name__ == "__main__":
    asyncio.run(main())
