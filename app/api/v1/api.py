from fastapi import APIRouter

from app.api.v1.endpoints.auth.fetch_users import router as fetch_users_router
from app.api.v1.endpoints.auth.google_sign_in import router as google_sign_in_router
from app.api.v1.endpoints.auth.login import router as login_router
from app.api.v1.endpoints.auth.sign_up import router as signup_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.notifications.notification_endpoint import (
    router as notification_router,
)
from app.api.v1.endpoints.songs.favorite_songs import router as favorite_songs_router
from app.api.v1.endpoints.songs.get_all_platform_songs import (
    router as all_songs_router,
)
from app.api.v1.endpoints.songs.get_all_user_songs import (
    router as fetch_user_songs_router,
)
from app.api.v1.endpoints.songs.get_recently_played_songs import (
    router as get_recently_played_songs_router,
)
from app.api.v1.endpoints.songs.insert_recently_played_songs_endpoint import (
    router as insert_recently_played_songs_router,
)
from app.api.v1.endpoints.songs.song import router as song_router
from app.api.v1.endpoints.tokens.register_token import router as register_token_router
from app.api.v1.endpoints.user.user_delete import router as user_delete_router
from app.api.v1.endpoints.user.user_update import router as user_update_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(signup_router, prefix="/auth", tags=["Auth"])
api_router.include_router(login_router, prefix="/auth", tags=["Auth"])
api_router.include_router(fetch_users_router, prefix="/auth", tags=["Auth"])
api_router.include_router(google_sign_in_router, prefix="/auth", tags=["Auth"])

api_router.include_router(song_router, prefix="/songs", tags=["Songs"])
api_router.include_router(fetch_user_songs_router, prefix="/songs", tags=["Songs"])
api_router.include_router(all_songs_router, prefix="/songs/platform", tags=["Songs"])
api_router.include_router(favorite_songs_router, prefix="/songs", tags=["Songs"])
api_router.include_router(
    get_recently_played_songs_router,
    prefix="/songs/recent/page",
    tags=["Recently Played"],
)
api_router.include_router(
    insert_recently_played_songs_router,
    prefix="/songs/recent/new",
    tags=["Recently Played"],
)

api_router.include_router(user_update_router, prefix="/users", tags=["Users"])
api_router.include_router(user_delete_router, prefix="/users", tags=["Users"])
api_router.include_router(
    notification_router,
    prefix="/notifications",
    tags=["Notifications"],
)
api_router.include_router(
    register_token_router,
    prefix="/tokens",
    tags=["Notifications"],
)