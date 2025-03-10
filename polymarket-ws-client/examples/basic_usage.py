import logging
from polymarket_ws_client import PolymarketWSClient
from polymarket_ws_client.models import SubscriptionMessage, Subscription, Trade

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def on_connect(client):
    """Callback when connection is established."""
    print("Connected to Polymarket WebSocket server")
    
    # Subscribe to activity trades
    subscription = SubscriptionMessage(
        subscriptions=[
            Subscription(
                topic="activity",
                type="trades"
            )
        ]
    )
    
    # Since we're using async/await, we can directly await the subscription
    await client.subscribe(subscription)

async def on_message(client, message):
    """Callback for handling incoming messages."""
    print(f"\nReceived message:")
    print(f"Topic: {message.topic}")
    print(f"Type: {message.type}")
    print(f"Timestamp: {message.timestamp}")
    
    # If the payload is a Trade, it will be automatically parsed
    if isinstance(message.payload, Trade):
        trade = message.payload
        print(f"\nTrade Details:")
        print(f"Asset: {trade.asset}")
        print(f"Price: {trade.price}")
        print(f"Size: {trade.size}")
        print(f"Side: {trade.side}")
        print(f"Transaction Hash: {trade.transactionHash}")
    else:
        print(f"Payload: {message.payload}")
    print("---")

def main():
    # Create client instance
    # You can optionally provide a Web3 provider URL for blockchain interaction
    client = PolymarketWSClient(
        on_connect=on_connect,
        on_message=on_message,
        # web3_provider="https://mainnet.infura.io/v3/YOUR-PROJECT-ID"
    )
    
    # Run the client (this will block until disconnected)
    try:
        client.run()
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == "__main__":
    main() 