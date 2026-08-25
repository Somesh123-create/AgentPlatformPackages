from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from agent_auth.jwt import JWTManager
from agent_auth.models import CurrentUser


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def create_auth_dependency(
    jwt_manager: JWTManager,
):
    async def get_current_user(
        token: str = Depends(oauth2_scheme),
    ) -> CurrentUser:

        payload = jwt_manager.decode_access_token(token)

        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )

        user_id = payload.get("sub")
        role = payload.get("role")

        if not user_id or not role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        try:
            user_id = int(user_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user ID",
            )

        return CurrentUser(
            user_id=user_id,
            role=role,
        )

    return get_current_user