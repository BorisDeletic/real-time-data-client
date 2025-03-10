from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime

class ClobApiKeyCreds(BaseModel):
    key: str
    secret: str
    passphrase: str

class GammaAuth(BaseModel):
    address: str

class Subscription(BaseModel):
    topic: str
    type: str
    filters: Optional[str] = None
    clob_auth: Optional[ClobApiKeyCreds] = None
    gamma_auth: Optional[GammaAuth] = None

class SubscriptionMessage(BaseModel):
    subscriptions: List[Subscription]

class Message(BaseModel):
    topic: str
    type: str
    timestamp: int
    payload: Dict[str, Any]

class Trade(BaseModel):
    asset: str = Field(description="ERC1155 token ID of conditional token being traded")
    bio: str = Field(description="Bio of the user of the trade")
    conditionId: str = Field(description="Id of market which is also the CTF condition ID")
    eventSlug: str = Field(description="Slug of the event")
    icon: str = Field(description="URL to the market icon image")
    name: str = Field(description="Name of the user of the trade")
    outcome: str = Field(description="Human readable outcome of the market")
    outcomeIndex: int = Field(description="Index of the outcome")
    price: float = Field(description="Price of the trade")
    profileImage: str = Field(description="URL to the user profile image")
    profileImageOptimized: Optional[str] = None
    proxyWallet: str = Field(description="Address of the user proxy wallet")
    pseudonym: str = Field(description="Pseudonym of the user")
    side: Literal["BUY", "SELL"] = Field(description="Side of the trade (BUY/SELL)")
    size: int = Field(description="Size of the trade")
    slug: str = Field(description="Slug of the market")
    timestamp: int = Field(description="Timestamp of the trade")
    title: str = Field(description="Title of the event")
    transactionHash: str = Field(description="Hash of the transaction")

class Comment(BaseModel):
    id: str = Field(description="Unique identifier of comment")
    body: str = Field(description="Content of the comment")
    parentEntityType: Literal["Event", "Series"] = Field(description="Type of the parent entity")
    parentEntityID: int = Field(description="ID of the parent entity")
    parentCommentID: Optional[str] = Field(description="ID of the parent comment")
    userAddress: str = Field(description="Address of the user")
    replyAddress: Optional[str] = Field(description="Address of the reply user")
    createdAt: str = Field(description="Creation timestamp")
    updatedAt: str = Field(description="Last update timestamp")

class Reaction(BaseModel):
    id: str = Field(description="Unique identifier of reaction")
    commentID: int = Field(description="ID of the comment")
    reactionType: str = Field(description="Type of the reaction")
    icon: str = Field(description="Icon representing the reaction")
    userAddress: str = Field(description="Address of the user")
    createdAt: str = Field(description="Creation timestamp") 