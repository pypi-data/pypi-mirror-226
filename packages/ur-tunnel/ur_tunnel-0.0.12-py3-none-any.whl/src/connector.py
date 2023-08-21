import asyncio
import base64
import json
import socket
import ssl
from datetime import datetime

import aiohttp
import certifi
import websockets
from src.http_delivery import LocalRequest, LocalResponse
from src.server_config import http_base_url, ws_base_url


class ConnectToServer:
    def __init__(
            self,
            local_port: int,
            project_name: str,
            is_local: bool,
    ) -> None:
        self._local_port = local_port
        self._ssl_context = None if is_local else ssl.create_default_context(cafile=certifi.where())
        self._retries = 0

        # Construct the base and socket URLs
        self._local_base_url = f'http://localhost:{local_port}'
        self._server_host_url = http_base_url(is_local)
        self._project_url = f"{self._server_host_url}/{project_name}"
        self._socket_url = f"{ws_base_url(is_local)}/ws/{project_name}"

        # Other properties
        self._websocket: websockets.WebSocketClientProtocol = None

    @classmethod
    async def create(
            cls,
            local_port: int,
            project_name: str,
            is_local: bool,
    ) -> None:
        connect_to_server = cls(local_port, project_name, is_local)
        await connect_to_server._connect()

    async def _connect(self) -> None:
        """Connect to the server and begin listening for requests."""
        print(f"Tunneling port {self._local_port} to {self._project_url}...")
        try:
            async with websockets.connect(self._socket_url, ssl=self._ssl_context) as websocket:
                self._print("Connected to the server.")
                self._websocket = websocket
                try:
                    await self._handle_messages()

                except websockets.exceptions.ConnectionClosedError as error:
                    # Error codes:
                    # 1000: Normal closure
                    # 1001: Going away
                    # 1002: Protocol error
                    # 1003: Unsupported data
                    # 1005: No status code
                    # 1006: Abnormal closure
                    # 1007: Invalid frame payload data
                    # 1008: Policy violation
                    # 1009: Message too big
                    # 1010: Missing extension
                    # 1011: Internal error
                    # 1012: Service restart
                    # 1013: Try again later
                    # 1014: Bad gateway
                    # 1015: TLS handshake error
                    self._print(
                        f"Connection closed: {error.reason or error.code}")
                    if error.code not in [1000, 1013]:
                        await self._retry_connect()
            
                except asyncio.TimeoutError:
                    self._print("Timed out waiting for a ping.")
                    await self._retry_connect()

        except asyncio.TimeoutError:
            self._print("Timed out attempting to connect to the server.")
            await self._retry_connect()

        except socket.gaierror:
            self._print("Check your internet connection.")
            await self._retry_connect()

        except ConnectionRefusedError:
            self._print(f"Failed to connect to the socket at {self._socket_url}.")
    
        except Exception as error:
            if "Connect call failed" in str(error):
                self._print(f"Connection failed: {error}")
                await self._retry_connect()
            else:
                self._print(f"An error occurred while trying to establish a connection: {error}")

    async def _retry_connect(self) -> None:
        """Retry connecting to the server."""
        await self._websocket.close()
        self._retries += 1
        if self._retries > 10:
            raise Exception('Failed to connect to server')
        print('Reconnecting...')
        await asyncio.sleep(3)
        await self._connect()

    async def _handle_messages(self) -> None:
        while True:
            # Wait for a message with a timeout
            message = await asyncio.wait_for(self._websocket.recv(), timeout=10)
            if message == 'ping':
                await self._websocket.send('pong')
                continue
            request_data = json.loads(message)
            if 'id' not in request_data:
                # Show the system message
                print(request_data.get('message'))
                continue
            request_to_localhost = self._handle_websocket_request(request_data)
            asyncio.create_task(request_to_localhost)

    async def _handle_websocket_request(self, request_data: LocalRequest) -> None:
        """Process a single websocket request."""
        try:
            # Extract details from the parsed JSON
            request_id = request_data["id"]
            method = request_data["method"]
            headers = request_data.get("headers", {})
            body = request_data.get("body", None)
            path = request_data.get("path", "")
            query = request_data.get("query", "")
            if query:
                path += f'?{query}'
    
            print('Incoming request:', method, f'/{path}')
    
            # Make the request based on the extracted method, path, headers, and body
            async with (aiohttp.ClientSession(
                    auto_decompress=False,
            ) as session):
                try:
                    response = await session.request(
                        method=method,
                        url=f'{self._local_base_url}/{path}',
                        headers=headers,
                        data=body,
                        allow_redirects=False,
                        ssl=False,
                    )
    
                    response_headers = dict(response.headers)
                    # Check if the response status is a redirect (e.g., 301, 302, 303, 307, or 308)
                    if 300 <= response.status < 400 and \
                            response.headers.get('Location','').startswith(self._server_host_url):
                        response_headers['Location'] = response.headers['Location'].replace(
                            self._server_host_url, self._project_url, 1)

                    # Convert headers and content to a JSON structure
                    response_data: LocalResponse = {
                        "request_id": request_id,
                        "headers": response_headers,
                        "content": base64.b64encode(await response.read()).decode('utf-8'),
                        "status_code": response.status,
                    }
    
                except Exception as error:
                    print(error)
                    response_data: LocalResponse = {
                        "request_id": request_id,
                        "headers": {
                            'Content-Type': 'text/plain'
                        },
                        "content": base64.b64encode(str(error).encode('utf-8')).decode('utf-8'),
                        "status_code": 500,
                    }
                response_json = json.dumps(response_data)
                await self._websocket.send(response_json)
        except Exception as error:
            print(error)

    @staticmethod
    def _print(message: str) -> None:
        """Print a message with the current datetime."""
        print(f"[{datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}] {message}")


class WebSocketDisconnect(Exception):
    """Raised when the websocket connection is closed."""
    pass
