import pytest
import jwt
import bson
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from config.Env import ENVConfig
from app import app

TEST_BUYER_USER_ID = "507f1f77bcf86cd799439011"
TEST_SELLER_USER_ID = "507f1f77bcf86cd799439012"
TEST_PRODUCT_ID = "507f1f77bcf86cd799439013"


def make_token(user_id: str) -> str:
    return jwt.encode(
        {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(days=2),
            "iat": datetime.utcnow(),
        },
        ENVConfig.JWT_AUTH_SECRET_KEY,
        algorithm=ENVConfig.ALGORITHMS,
    )


def make_async_iter(items):
    async def gen():
        for item in items:
            yield item

    return gen()


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def buyer_token():
    return make_token(TEST_BUYER_USER_ID)


@pytest.fixture
def seller_token():
    return make_token(TEST_SELLER_USER_ID)


@pytest.fixture
def buyer_headers(buyer_token):
    return {"Authorization": f"Bearer {buyer_token}"}


@pytest.fixture
def seller_headers(seller_token):
    return {"Authorization": f"Bearer {seller_token}"}
