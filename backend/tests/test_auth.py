import pytest
import bson
import bcrypt
from unittest.mock import patch, AsyncMock, MagicMock

from tests.conftest import make_token, TEST_BUYER_USER_ID

_OBJ_ID = bson.ObjectId(TEST_BUYER_USER_ID)

VALID_USER = {
    "name": "Alice",
    "email": "alice@example.com",
    "password": "secret123",
    "role": "buyer",
}

VALID_ADDRESS = {
    "pin_code": "110001",
    "city": "Delhi",
    "state": "Delhi",
    "country": "India",
    "landmark": "Near Gate",
}

TEST_ADDRESS_ID = "507f1f77bcf86cd799439020"


def _auth() -> dict:
    return {"Authorization": f"Bearer {make_token(TEST_BUYER_USER_ID)}"}


def _hashed(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


# ─── Register ─────────────────────────────────────────────────────────────────

REGISTER_URL = "/api/v1/auth/register"


class TestRegister:
    def test_success(self, client):
        mock_insert = MagicMock(inserted_id=_OBJ_ID)
        with (
            patch("services.authService.user_collection") as mock_uc,
            patch("services.authService.profile_collection") as mock_pc,
        ):
            mock_uc.find_one = AsyncMock(return_value=None)
            mock_uc.insert_one = AsyncMock(return_value=mock_insert)
            mock_pc.insert_one = AsyncMock(return_value=MagicMock())
            res = client.post(REGISTER_URL, json=VALID_USER)

        assert res.status_code == 200
        body = res.json()
        assert body["message"] == "User registered successfully"
        assert "token" in body

    def test_duplicate_email_returns_400(self, client):
        with patch("services.authService.user_collection") as mock_uc:
            mock_uc.find_one = AsyncMock(
                return_value={"_id": _OBJ_ID, "email": "alice@example.com"}
            )
            res = client.post(REGISTER_URL, json=VALID_USER)

        assert res.status_code == 400
        assert "Email already exists" in res.json()["detail"]

    def test_invalid_email_returns_422(self, client):
        res = client.post(REGISTER_URL, json={**VALID_USER, "email": "not-an-email"})
        assert res.status_code == 422

    def test_short_password_returns_422(self, client):
        res = client.post(REGISTER_URL, json={**VALID_USER, "password": "abc"})
        assert res.status_code == 422

    def test_missing_fields_returns_422(self, client):
        res = client.post(REGISTER_URL, json={"email": "alice@example.com"})
        assert res.status_code == 422


# ─── Login ────────────────────────────────────────────────────────────────────

LOGIN_URL = "/api/v1/auth/login"


class TestLogin:
    def test_success(self, client):
        user = {
            "_id": _OBJ_ID,
            "email": "alice@example.com",
            "password": _hashed("secret123"),
        }
        with patch("services.authService.user_collection") as mock_uc:
            mock_uc.find_one = AsyncMock(return_value=user)
            res = client.post(
                LOGIN_URL,
                json={"email": "alice@example.com", "password": "secret123"},
            )

        assert res.status_code == 200
        body = res.json()
        assert body["message"] == "Login Successfull"
        assert "token" in body

    def test_user_not_found_returns_400(self, client):
        with patch("services.authService.user_collection") as mock_uc:
            mock_uc.find_one = AsyncMock(return_value=None)
            res = client.post(
                LOGIN_URL,
                json={"email": "nobody@example.com", "password": "secret123"},
            )

        assert res.status_code == 400
        assert "User Not Exist" in res.json()["detail"]

    def test_wrong_password_returns_400(self, client):
        user = {
            "_id": _OBJ_ID,
            "email": "alice@example.com",
            "password": _hashed("correctpass"),
        }
        with patch("services.authService.user_collection") as mock_uc:
            mock_uc.find_one = AsyncMock(return_value=user)
            res = client.post(
                LOGIN_URL,
                json={"email": "alice@example.com", "password": "wrongpass"},
            )

        assert res.status_code == 400
        assert "Invalid Credentials" in res.json()["detail"]

    def test_invalid_email_returns_422(self, client):
        res = client.post(
            LOGIN_URL, json={"email": "bad-email", "password": "secret123"}
        )
        assert res.status_code == 422


# ─── Profile ──────────────────────────────────────────────────────────────────

PROFILE_URL = "/api/v1/auth/profile"


class TestProfile:
    def test_no_token_returns_401(self, client):
        res = client.get(PROFILE_URL)
        assert res.status_code == 401

    def test_invalid_token_returns_401(self, client):
        res = client.get(PROFILE_URL, headers={"Authorization": "Bearer invalid.token"})
        assert res.status_code == 401

    def test_success(self, client):
        user = {"_id": _OBJ_ID, "email": "alice@example.com", "role": "buyer"}
        profile = {
            "_id": bson.ObjectId(),
            "user_id": TEST_BUYER_USER_ID,
            "name": "Alice",
            "avatar": None,
            "address": [],
        }
        with (
            patch("services.authService.user_collection") as mock_uc,
            patch("services.authService.profile_collection") as mock_pc,
        ):
            mock_uc.find_one = AsyncMock(return_value=user)
            mock_pc.find_one = AsyncMock(return_value=profile)
            res = client.get(PROFILE_URL, headers=_auth())

        assert res.status_code == 200
        body = res.json()
        assert body["email"] == "alice@example.com"
        assert body["name"] == "Alice"

    def test_user_not_found_returns_400(self, client):
        with patch("services.authService.user_collection") as mock_uc:
            mock_uc.find_one = AsyncMock(return_value=None)
            res = client.get(PROFILE_URL, headers=_auth())

        assert res.status_code == 400


# ─── Update Basic Details ──────────────────────────────────────────────────────

UPDATE_DETAILS_URL = "/api/v1/auth/update-basic-details"


class TestUpdateBasicDetails:
    def test_no_token_returns_401(self, client):
        res = client.put(UPDATE_DETAILS_URL, json={"name": "Bob"})
        assert res.status_code == 401

    def test_success(self, client):
        with patch("services.authService.profile_collection") as mock_pc:
            mock_pc.find_one_and_update = AsyncMock(return_value=MagicMock())
            res = client.put(UPDATE_DETAILS_URL, json={"name": "Bob"}, headers=_auth())

        assert res.status_code == 200
        assert res.json()["msg"] == "Basic details updated successfully"

    def test_missing_name_returns_422(self, client):
        res = client.put(UPDATE_DETAILS_URL, json={}, headers=_auth())
        assert res.status_code == 422


# ─── Add Address ──────────────────────────────────────────────────────────────

ADD_ADDRESS_URL = "/api/v1/auth/add-address"


class TestAddAddress:
    def test_no_token_returns_401(self, client):
        res = client.post(ADD_ADDRESS_URL, json=VALID_ADDRESS)
        assert res.status_code == 401

    def test_success(self, client):
        profile = {"user_id": TEST_BUYER_USER_ID, "name": "Alice", "address": []}
        with patch("services.authService.profile_collection") as mock_pc:
            mock_pc.find_one = AsyncMock(return_value=profile)
            mock_pc.find_one_and_update = AsyncMock(return_value=MagicMock())
            res = client.post(ADD_ADDRESS_URL, json=VALID_ADDRESS, headers=_auth())

        assert res.status_code == 200
        assert res.json()["msg"] == "New address added successfully"

    def test_profile_not_found_returns_400(self, client):
        with patch("services.authService.profile_collection") as mock_pc:
            mock_pc.find_one = AsyncMock(return_value=None)
            res = client.post(ADD_ADDRESS_URL, json=VALID_ADDRESS, headers=_auth())

        assert res.status_code == 400

    def test_missing_fields_returns_422(self, client):
        res = client.post(ADD_ADDRESS_URL, json={"city": "Delhi"}, headers=_auth())
        assert res.status_code == 422


# ─── Delete Address ───────────────────────────────────────────────────────────


class TestDeleteAddress:
    def _url(self):
        return f"/api/v1/auth/delete-address/{TEST_ADDRESS_ID}"

    def test_no_token_returns_401(self, client):
        res = client.delete(self._url())
        assert res.status_code == 401

    def test_success(self, client):
        profile = {
            "user_id": TEST_BUYER_USER_ID,
            "address": [{"_id": TEST_ADDRESS_ID, "city": "Delhi"}],
        }
        with patch("services.authService.profile_collection") as mock_pc:
            mock_pc.find_one = AsyncMock(return_value=profile)
            mock_pc.find_one_and_update = AsyncMock(return_value=MagicMock())
            res = client.delete(self._url(), headers=_auth())

        assert res.status_code == 200
        assert res.json()["msg"] == "Address deleted successfully"

    def test_profile_not_found_returns_400(self, client):
        with patch("services.authService.profile_collection") as mock_pc:
            mock_pc.find_one = AsyncMock(return_value=None)
            res = client.delete(self._url(), headers=_auth())

        assert res.status_code == 400
