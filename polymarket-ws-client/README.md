# Polymarket WebSocket Client

A Python WebSocket client for connecting to Polymarket's real-time data streaming service. This client provides a modern, async-first implementation with Web3 integration and strong typing support.

## Features

- 🔄 Real-time WebSocket data streaming
- 🔗 Web3 integration for blockchain interaction
- ✨ Modern async/await API
- 🔒 Type-safe with Pydantic models
- 🔄 Automatic reconnection handling
- 💓 Ping/Pong heartbeat mechanism
- 📝 Comprehensive logging
- 🎯 Topic-based subscription management

## Installation

```bash
pip install polymarket-ws-client
```

## Quick Start

Here's a simple example of how to use the client:

```python
from polymarket_ws_client import PolymarketWSClient
from polymarket_ws_client.models import SubscriptionMessage, Subscription

def on_connect(client):
    # Subscribe to trades when connected
    subscription = SubscriptionMessage(
        subscriptions=[
            Subscription(
                topic="activity",
                type="trades"
            )
        ]
    )
    
    # Note: We're in a callback, so we need to use asyncio
    import asyncio
    loop = asyncio.get_event_loop()
    loop.create_task(client.subscribe(subscription))

def on_message(client, message):
    print(f"Received: {message.topic} - {message.type}")
    print(f"Payload: {message.payload}")

# Create and run the client
client = PolymarketWSClient(
    on_connect=on_connect,
    on_message=on_message
)
client.run()
```

## Advanced Usage

### With Web3 Integration

```python
client = PolymarketWSClient(
    on_connect=on_connect,
    on_message=on_message,
    web3_provider="https://mainnet.infura.io/v3/YOUR-PROJECT-ID"
)
```

### Subscribing to Multiple Topics

```python
subscription = SubscriptionMessage(
    subscriptions=[
        Subscription(
            topic="activity",
            type="trades"
        ),
        Subscription(
            topic="comments",
            type="*",  # Subscribe to all comment types
            filters='{"parentEntityID": 100, "parentEntityType": "Event"}'
        )
    ]
)
```

### With Authentication

```python
from polymarket_ws_client.models import ClobApiKeyCreds, GammaAuth

subscription = SubscriptionMessage(
    subscriptions=[
        Subscription(
            topic="your_topic",
            type="your_type",
            clob_auth=ClobApiKeyCreds(
                key="your_api_key",
                secret="your_secret",
                passphrase="your_passphrase"
            ),
            gamma_auth=GammaAuth(
                address="your_ethereum_address"
            )
        )
    ]
)
```

## Message Types

The client supports the following message types:

### Trade

```python
class Trade(BaseModel):
    asset: str                      # ERC1155 token ID
    bio: str                        # User bio
    conditionId: str               # Market ID
    eventSlug: str                 # Event slug
    icon: str                      # Market icon URL
    name: str                      # User name
    outcome: str                   # Market outcome
    outcomeIndex: int             # Outcome index
    price: float                   # Trade price
    profileImage: str             # User profile image URL
    proxyWallet: str              # User proxy wallet
    side: Literal["BUY", "SELL"]  # Trade side
    size: int                      # Trade size
    timestamp: int                # Trade timestamp
    transactionHash: str          # Transaction hash
```

### Comment

```python
class Comment(BaseModel):
    id: str
    body: str
    parentEntityType: Literal["Event", "Series"]
    parentEntityID: int
    userAddress: str
    createdAt: str
    updatedAt: str
```

### Reaction

```python
class Reaction(BaseModel):
    id: str
    commentID: int
    reactionType: str
    icon: str
    userAddress: str
    createdAt: str
```

## Configuration

The client can be configured with the following parameters:

- `host`: WebSocket server URL (default: "wss://ws-live-data.polymarket.com")
- `ping_interval`: Interval for ping messages in milliseconds (default: 5000)
- `auto_reconnect`: Whether to automatically reconnect on disconnection (default: True)
- `web3_provider`: Optional Web3 provider URL for blockchain interaction
- `on_connect`: Callback function when connection is established
- `on_message`: Callback function for handling incoming messages

## Development

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/yourusername/polymarket-ws-client.git
cd polymarket-ws-client

# Install dependencies
pip install -r requirements.txt

# Run the example
python examples/basic_usage.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 