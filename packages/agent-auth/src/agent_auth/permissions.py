from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from agent_auth.models import CurrentUser


def require_roles(
        *allowed_roles: str,
    ) -> Callable:

    async def dependency(
        current_user: CurrentUser = Depends(),
    ) -> CurrentUser:

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )

        return current_user

    return dependency