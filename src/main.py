import asyncio
import websockets
import json
import jwt
import re
import time

from GetStateOrder import get_state_order


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

            response_to_str = json.dumps(response)

            pattern_state_value = r'"order_state"\s*:\s*(\d+)'

            # Search for the pattern_order_value in the JSON string
            match = re.search(pattern_state_value, response_to_str)

            if match:
                # Extract the value associated with the "order_state" key
                order_state_value = match.group(1)

                await websocket.send(response_to_str)

                print(f"[+] First response to the client: {response_to_str}")

                new_state_value = order_state_value

                while True:
                    time.sleep(2)

                    new_response = get_state_order(token, id_client)

                    new_response_to_str = json.dumps(new_response)

                    new_match = re.search(pattern_state_value, new_response_to_str)

                    new_state_value = new_match.group(1)

                    if new_state_value == order_state_value:
                        await asyncio.create_task(websocket.send(new_response_to_str))
                        pass
                    else:
                        await asyncio.create_task(websocket.send(new_response_to_str))
                        order_state_value = new_state_value
            else:
                await websocket.send(json.dumps({"error": "No order state found"}))
    except websockets.exceptions.ConnectionClosedError as e:
        await websocket.close()
        print("[-] Client disconnected")
    except Exception as e:
        await websocket.close()
        print(f"[-] Error: {e}")


def main():
    port = 8765

    # Create a WebSocket server
    start_server = websockets.serve(handle_websocket, "0.0.0.0", port)

    # Start the server
    print(f"[+] Currently on port {port}")
    print(f"[+] Running at ws://localhost:8765")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
