import asyncio
import websockets
import json
import jwt

from api.GetStateOrder import get_state_order


async def handle_websocket(websocket, path):
    # This function will handle WebSocket connections
    print("[+] Client connected")

    try:
        while True:
            # Receive message from the client
            response = await websocket.recv()

            response_json = json.loads(response)

            token = response_json["jwt"]

            decoded_token = jwt.decode(token, options={"verify_signature": False})

            id_client = decoded_token["id"]

            response = get_state_order(token, id_client)

            response_json = json.dumps(response)

            await websocket.send(response_json)

            print(f"[+] Sent response to client: {response_json}")
    except websockets.exceptions.ConnectionClosedError as e:
        print("[-] Client disconnected")
    except Exception as e:
        print(f"[-] Error: {e}")

def main():
    port = 8765

    # Create a WebSocket server
    start_server = websockets.serve(handle_websocket, "localhost", port)

    # Start the server
    print(f"[+] Currently on port {port}")
    print(f"[+] Running at ws://localhost:8765")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
