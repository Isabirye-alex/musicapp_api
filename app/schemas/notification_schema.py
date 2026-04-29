from pydantic import BaseModel

class NotificationPayload(BaseModel):
    title: str
    body: str
    image_url: Optional[str] = None

class SendToTokenRequest(BaseModel):
    token: str                              # single device FCM token
    notification: NotificationPayload
    data: Optional[dict] = None            # extra key-value data payload

class SendToTopicRequest(BaseModel):
    topic: str                             # e.g. "news", "alerts"
    notification: NotificationPayload
    data: Optional[dict] = None

class SendToMultipleRequest(BaseModel):
    tokens: list[str]                      # up to 500 tokens
    notification: NotificationPayload
    data: Optional[dict] = None