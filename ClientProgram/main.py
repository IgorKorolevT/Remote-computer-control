import asyncio
import websockets
import json

name = "aswdaw"

async def websocket_client():
    # Define headers for authentication
    headers = {
        "name": name,
        "password": "12345"
    }

    # Connect to the WebSocket server
    uri = "ws://127.0.0.1:8000/ws/computer/"
    try:
        async with websockets.connect(uri, additional_headers=headers) as ws:
            print("Connection opened")

            # Send initial message
            # initial_message = json.dumps({"message": "Hello, server!", "user": "client"})
            # await ws.send(initial_message)
            # print(f"Sent initial message: {initial_message}")

            # Main loop to receive and respond to messages
            async for message in ws:
                try:
                    data = json.loads(message)
                    print(f"Received: {data}")
                    message = data["message"]
                    json_response = json.dumps({"message": message.upper(), "channel_user": data["channel_user"]})
                    print(f"Sending response: {json_response}")
                    await ws.send(json_response)
                    print("Message sent successfully")
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                except Exception as e:
                    print(f"Error in message handling: {e}")

    except websockets.exceptions.ConnectionClosed as e:
        print(f"WebSocket closed: {e.code}, {e.reason}")
    except Exception as e:
        print(f"Connection error: {e}")

# Run the WebSocket client
asyncio.run(websocket_client())