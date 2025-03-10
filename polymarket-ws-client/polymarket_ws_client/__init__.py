"""
Polymarket WebSocket Client
~~~~~~~~~~~~~~~~~~~~~~~~~

A Python WebSocket client for connecting to Polymarket's real-time data streaming service.
"""

from .client import PolymarketWSClient
from .models import (
    Message,
    SubscriptionMessage,
    Subscription,
    ClobApiKeyCreds,
    GammaAuth,
    Trade,
    Comment,
    Reaction
)

__version__ = "0.1.0"
__all__ = [
    'PolymarketWSClient',
    'Message',
    'SubscriptionMessage',
    'Subscription',
    'ClobApiKeyCreds',
    'GammaAuth',
    'Trade',
    'Comment',
    'Reaction'
] 