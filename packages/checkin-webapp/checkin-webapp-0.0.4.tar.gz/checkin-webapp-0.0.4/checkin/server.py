import asyncio
import datetime
import argparse

# Create a server that listens on port 8888
_HOST = "localhost"
_PORT = 8888

async def serve(port = _PORT, host = _HOST):
    # Create a TCP server
    print(f"Starting server on port: {port} and host: {host}")
    server = await asyncio.start_server(handle_client, host, port)

    # Run the server indefinitely
    async with server:
        await server.serve_forever()

# Handle incoming client connections
async def handle_client(reader, writer, buffer_size_kb = 100):

    counter = 0
    end_counter = 5
    loop = True
    kb = 1024


    while loop:
        # Read data from the client

        now = datetime.datetime.now()

        if now.second % 2 == 0:

            if counter > end_counter:
                loop = False
                break

            counter += 1

        data = await reader.read(buffer_size_kb * kb)
        if not data:
            break

        # Decode the received message
        message = data.decode().strip()

        # response = handle_json(message)

        print(f"=== Received message: {message}")

        # Send a response back to the client
        writer.write(message.encode())
        await writer.drain()

    # Close the connection
    writer.close()

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--port")
    parser.add_argument("--host")

    args = parser.parse_args()

    if args.port and args.host:
        asyncio.run(serve(args.port, args.host))
    elif args.port:
        asyncio.run(serve(port=args.port))
    elif args.host:
        asyncio.run(serve(host=args.host))
    else:
        asyncio.run(serve())

if __name__ == '__main__':
    main()