import json
import asyncio
import logging
import ssl
import certifi
from typing import Optional, Callable, Dict, Any, Union
from websockets import connect, WebSocketClientProtocol
from web3 import Web3
from .models import (
    Message, SubscriptionMessage, Trade, Comment,
    Reaction, ClobApiKeyCreds, GammaAuth
)

logger = logging.getLogger(__name__)

DEFAULT_HOST = "wss://ws-live-data.polymarket.com"
DEFAULT_PING_INTERVAL = 5000  # milliseconds

PayloadType = Union[Trade, Comment, Reaction, Dict[str, Any]]

class PolymarketWSClient:
    def __init__(
        self,
        on_connect: Optional[Callable[['PolymarketWSClient'], None]] = None,
        on_message: Optional[Callable[['PolymarketWSClient', Message], None]] = None,
        host: str = DEFAULT_HOST,
        ping_interval: int = DEFAULT_PING_INTERVAL,
        auto_reconnect: bool = True,
        web3_provider: Optional[str] = None,
        ssl_verify: bool = True
    ):
        """
        Initialize the Polymarket WebSocket client.
        
        Args:
            on_connect: Callback function when connection is established
            on_message: Callback function for handling incoming messages
            host: WebSocket server URL
            ping_interval: Interval for ping messages in milliseconds
            auto_reconnect: Whether to automatically reconnect on disconnection
            web3_provider: Optional Web3 provider URL for blockchain interaction
            ssl_verify: Whether to verify SSL certificates (default: True)
        """
        self.host = host
        self.ping_interval = ping_interval / 1000  # Convert to seconds
        self.auto_reconnect = auto_reconnect
        self.on_connect_callback = on_connect
        self.on_message_callback = on_message
        self.websocket: Optional[WebSocketClientProtocol] = None
        self.ping_task: Optional[asyncio.Task] = None
        self.running = False
        self.ssl_verify = ssl_verify
        
        # Initialize Web3 if provider is specified
        self.web3 = Web3(Web3.HTTPProvider(web3_provider)) if web3_provider else None

    async def connect(self):
        """Connect to the WebSocket server."""
        while True:
            try:
                # Configure SSL context
                ssl_context = None
                if self.host.startswith("wss://"):
                    ssl_context = ssl.create_default_context()
                    if self.ssl_verify:
                        ssl_context.load_verify_locations(certifi.where())
                    else:
                        ssl_context.check_hostname = False
                        ssl_context.verify_mode = ssl.CERT_NONE

                async with connect(
                    self.host,
                    ssl=ssl_context
                ) as websocket:
                    self.websocket = websocket
                    self.running = True
                    logger.info(f"Connected to {self.host}")
                    
                    if self.on_connect_callback:
                        await asyncio.get_event_loop().run_in_executor(
                            None, self.on_connect_callback, self
                        )

                    # Start ping loop
                    self.ping_task = asyncio.create_task(self._ping_loop())
                    
                    try:
                        await self._message_loop()
                    except Exception as e:
                        logger.error(f"Message loop error: {e}")
                    finally:
                        if self.ping_task:
                            self.ping_task.cancel()
                            
            except Exception as e:
                logger.error(f"Connection error: {e}")
                if not self.auto_reconnect:
                    break
                await asyncio.sleep(5)  # Wait before reconnecting
                
            if not self.auto_reconnect:
                break

    async def _ping_loop(self):
        """Send periodic ping messages to keep the connection alive."""
        while self.running:
            try:
                await self.websocket.ping()
                await asyncio.sleep(self.ping_interval)
            except Exception as e:
                logger.error(f"Ping error: {e}")
                break

    def _parse_payload(self, topic: str, payload_type: str, payload: Dict[str, Any]) -> PayloadType:
        """Parse the message payload into the appropriate type."""
        try:
            if topic == "activity" and payload_type == "trades":
                return Trade(**payload)
            elif topic == "comments":
                if payload_type in ["comment_created", "comment_removed"]:
                    return Comment(**payload)
                elif payload_type in ["reaction_created", "reaction_removed"]:
                    return Reaction(**payload)
            return payload
        except Exception as e:
            logger.warning(f"Failed to parse payload: {e}")
            return payload

    async def _message_loop(self):
        """Handle incoming messages."""
        async for message in self.websocket:
            if not message:
                continue
                
            try:
                data = json.loads(message)
                if isinstance(data, dict) and "payload" in data:
                    topic = data.get("topic", "")
                    msg_type = data.get("type", "")
                    
                    # Parse the payload into the appropriate type
                    parsed_payload = self._parse_payload(
                        topic, msg_type, data.get("payload", {})
                    )
                    
                    msg = Message(
                        topic=topic,
                        type=msg_type,
                        timestamp=data.get("timestamp", 0),
                        payload=parsed_payload
                    )
                    
                    if self.on_message_callback:
                        await asyncio.get_event_loop().run_in_executor(
                            None, self.on_message_callback, self, msg
                        )
                else:
                    logger.debug(f"Received message: {message}")
            except json.JSONDecodeError:
                logger.error(f"Failed to parse message: {message}")
            except Exception as e:
                logger.error(f"Error processing message: {e}")

    async def disconnect(self):
        """Disconnect from the WebSocket server."""
        self.running = False
        if self.websocket:
            await self.websocket.close()

    async def subscribe(self, msg: SubscriptionMessage):
        """Subscribe to topics."""
        if not self.websocket:
            raise RuntimeError("Not connected to WebSocket server")
            
        try:
            subscription_dict = {
                "action": "subscribe",
                **msg.model_dump()
            }
            await self.websocket.send(json.dumps(subscription_dict))
            logger.info(f"Subscribed to {msg.subscriptions}")
        except Exception as e:
            logger.error(f"Subscribe error: {e}")
            await self.websocket.close()

    async def unsubscribe(self, msg: SubscriptionMessage):
        """Unsubscribe from topics."""
        if not self.websocket:
            raise RuntimeError("Not connected to WebSocket server")
            
        try:
            subscription_dict = {
                "action": "unsubscribe",
                **msg.model_dump()
            }
            await self.websocket.send(json.dumps(subscription_dict))
            logger.info(f"Unsubscribed from {msg.subscriptions}")
        except Exception as e:
            logger.error(f"Unsubscribe error: {e}")
            await self.websocket.close()

    def run(self):
        """Run the client in the current thread."""
        asyncio.get_event_loop().run_until_complete(self.connect()) 