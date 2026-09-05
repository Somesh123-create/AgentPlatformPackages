from dataclasses import dataclass
from inspect import signature

import pytest

from agent_auth import (
    JWTManager,
    authenticate_user,
    hash_password,
    verify_password,
)
from agent_auth.dependencies import create_auth_dependency
from agent_auth.exceptions import InvalidPasswordError
from agent_auth.permissions import require_roles


@dataclass
class User:
    id: int
    role: str
    password_hash: str


def test_password_helpers_round_trip_and_reject_long_passwords():
    password_hash = hash_password("pässword")

    assert verify_password("pässword", password_hash)
    assert not verify_password("wrong", password_hash)

    with pytest.raises(InvalidPasswordError):
        hash_password("x" * 73)


@pytest.mark.asyncio
async def test_authenticate_user_is_model_and_repository_agnostic():
    user = User(7, "ADMIN", hash_password("secret"))

    async def load_user(identifier: str):
        return user if identifier == "admin@example.com" else None

    manager = JWTManager("secret")
    token = await authenticate_user(
        "admin@example.com",
        "secret",
        load_user,
        manager,
    )

    assert manager.decode_access_token(token)["sub"] == "7"
    assert manager.decode_access_token(token)["role"] == "ADMIN"


@pytest.mark.asyncio
async def test_authenticate_user_rejects_unknown_or_wrong_credentials():
    user = User(7, "USER", hash_password("secret"))

    async def load_user(identifier: str):
        return user

    manager = JWTManager("secret")

    with pytest.raises(ValueError):
        await authenticate_user("user@example.com", "wrong", load_user, manager)


def test_role_dependency_uses_the_configured_current_user_dependency():
    async def current_user_dependency():
        return User(7, "ADMIN", "unused")

    dependency = require_roles(
        "ADMIN",
        current_user_dependency=current_user_dependency,
    )

    current_user_parameter = signature(dependency).parameters["current_user"]
    assert current_user_parameter.default.dependency is (
        current_user_dependency
    )


def test_auth_dependency_factory_uses_custom_token_url():
    dependency = create_auth_dependency(
        JWTManager("secret"),
        token_url="/session/login",
    )

    token_parameter = signature(dependency).parameters["token"]
    assert token_parameter.default.dependency.model.flows.password.tokenUrl == (
        "/session/login"
    )