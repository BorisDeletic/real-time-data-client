# Real time data client

This client provides a wrapper to connect to the `real-time-data-streaming` `WebSocket` service.

## How to use it

Here is a quick example about how to connect to the service and start receiving messages (you can find more in the folder `examples/`):

```typescript
import { RealTimeDataClient } from "../src/client";
import { RawData } from "ws";

const onMessage = (event: RawData): void => {
    console.log(event.toString());
};

const onConnect = (client: RealTimeDataClient): void => {
    // Subscribe to a topic
    client.subscribe({
        subscriptions: [
            {
                topic: "activity",
                type: "trades",
            },
        ],
    });
};

new RealTimeDataClient(onMessage, onConnect).connect();
```
