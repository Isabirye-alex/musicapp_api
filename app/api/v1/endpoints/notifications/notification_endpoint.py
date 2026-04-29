from fastapi import APIRouter, HTTPException
from firebase_admin import messaging
from app.schemas.notification_schema import (
    SendToTopicRequest,
    SendToMultipleRequest,
    SendToTokenRequest,
)

router = APIRouter()


@router.post("/notify/token")
async def send_to_token(request: SendToTokenRequest):
    """Send push notification to a single device."""
    try:
        message = messaging.Message(
            token=request.token,
            notification=messaging.Notification(
                title=request.notification.title,
                body=request.notification.body,
                image=request.notification.image_url,
            ),
            data=request.data or {},
            android=messaging.AndroidConfig(
                priority="high",
                notification=messaging.AndroidNotification(
                    sound="default",
                    click_action="FLUTTER_NOTIFICATION_CLICK",
                ),
            ),
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(sound="default"),
                ),
            ),
        )

        response = messaging.send(message)
        return {"success": True, "message_id": response}

    except messaging.UnregisteredError:
        raise HTTPException(status_code=404, detail="Device token is no longer valid.")
    except messaging.SenderIdMismatchError:
        raise HTTPException(
            status_code=400, detail="Token does not match the sender ID."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/notify/topic")
async def send_to_topic(request: SendToTopicRequest):
    """Send push notification to all devices subscribed to a topic."""
    try:
        message = messaging.Message(
            topic=request.topic,
            notification=messaging.Notification(
                title=request.notification.title,
                body=request.notification.body,
                image=request.notification.image_url,
            ),
            data=request.data or {},
            android=messaging.AndroidConfig(
                priority="high",
                notification=messaging.AndroidNotification(
                    sound="default",
                    click_action="FLUTTER_NOTIFICATION_CLICK",
                ),
            ),
        )

        response = messaging.send(message)
        return {"success": True, "message_id": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/notify/multicast")
async def send_to_multiple(request: SendToMultipleRequest):
    """Send push notification to multiple devices (up to 500 tokens)."""
    if len(request.tokens) > 500:
        raise HTTPException(status_code=400, detail="Maximum 500 tokens per request.")
    try:
        message = messaging.MulticastMessage(
            tokens=request.tokens,
            notification=messaging.Notification(
                title=request.notification.title,
                body=request.notification.body,
                image=request.notification.image_url,
            ),
            data=request.data or {},
            android=messaging.AndroidConfig(
                priority="high",
                notification=messaging.AndroidNotification(
                    sound="default",
                    click_action="FLUTTER_NOTIFICATION_CLICK",
                ),
            ),
        )

        response = messaging.send_each_for_multicast(message)
        return {
            "success": True,
            "sent": response.success_count,
            "failed": response.failure_count,
            "responses": [
                {
                    "token": request.tokens[i],
                    "success": r.success,
                    "error": str(r.exception) if r.exception else None,
                }
                for i, r in enumerate(response.responses)
            ],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
