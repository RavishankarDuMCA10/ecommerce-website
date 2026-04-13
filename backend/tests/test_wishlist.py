import pytest
import bson
from datetime import datetime
from unittest.mock import patch, AsyncMock, MagicMock

from tests.conftest import TEST_BUYER_USER_ID, TEST_PRODUCT_ID, make_async_iter

BUYER_USER_DB = {"_id": bson.ObjectId(TEST_BUYER_USER_ID), "role": "buyer"}

PRODUCT_DB = {
    "_id": bson.ObjectId(TEST_PRODUCT_ID),
    "title": "Test T-Shirt",
    "description": "A cool T-shirt",
    "price": 500,
    "category": "TSHIRT",
    "slug": "test-t-shirt",
    "images": [{"image_url": "http://example.com/img.jpg"}],
    "created_at": datetime.now(),
}

WISHLIST_ENTRY = {
    "_id": bson.ObjectId(),
    "user_id": TEST_BUYER_USER_ID,
    "product_id": TEST_PRODUCT_ID,
}

TOGGLE_PAYLOAD = {"product_id": TEST_PRODUCT_ID, "user_id": TEST_BUYER_USER_ID}


# ─── POST /api/v1/wishlist/toggle ─────────────────────────────────────────────


class TestToggleWishlist:
    URL = "/api/v1/wishlist/toggle"

    def test_no_token_returns_401(self, client):
        res = client.post(self.URL, json=TOGGLE_PAYLOAD)
        assert res.status_code == 401

    def test_adds_product_when_not_in_wishlist(self, client, buyer_headers):
        with (
            patch("config.db.user_collection") as mock_coll,
            patch("services.wishListService.wishlist_collection") as mock_wc,
        ):
            mock_coll.find_one = AsyncMock(return_value=BUYER_USER_DB)
            mock_wc.find_one = AsyncMock(return_value=None)
            mock_wc.insert_one = AsyncMock(return_value=MagicMock())
            res = client.post(self.URL, json=TOGGLE_PAYLOAD, headers=buyer_headers)

        assert res.status_code == 200
        assert "added" in res.json()["msg"]

    def test_removes_product_when_already_in_wishlist(self, client, buyer_headers):
        with (
            patch("config.db.user_collection") as mock_coll,
            patch("services.wishListService.wishlist_collection") as mock_wc,
        ):
            mock_coll.find_one = AsyncMock(return_value=BUYER_USER_DB)
            mock_wc.find_one = AsyncMock(return_value=WISHLIST_ENTRY)
            mock_wc.find_one_and_delete = AsyncMock(return_value=WISHLIST_ENTRY)
            res = client.post(self.URL, json=TOGGLE_PAYLOAD, headers=buyer_headers)

        assert res.status_code == 200
        assert "removed" in res.json()["msg"]


# ─── GET /api/v1/wishlist/get ─────────────────────────────────────────────────


class TestGetWishlist:
    URL = "/api/v1/wishlist/get"

    def test_no_token_returns_401(self, client):
        res = client.get(self.URL)
        assert res.status_code == 401

    def test_returns_empty_list(self, client, buyer_headers):
        with (
            patch("config.db.user_collection") as mock_coll,
            patch("services.wishListService.wishlist_collection") as mock_wc,
        ):
            mock_coll.find_one = AsyncMock(return_value=BUYER_USER_DB)
            mock_wc.find.return_value = make_async_iter([])
            res = client.get(self.URL, headers=buyer_headers)

        assert res.status_code == 200
        assert res.json() == []

    def test_returns_products_in_wishlist(self, client, buyer_headers):
        with (
            patch("config.db.user_collection") as mock_coll,
            patch("services.wishListService.wishlist_collection") as mock_wc,
            patch("services.wishListService.product_collection") as mock_pc,
        ):
            mock_coll.find_one = AsyncMock(return_value=BUYER_USER_DB)
            mock_wc.find.return_value = make_async_iter([WISHLIST_ENTRY])
            mock_pc.find_one = AsyncMock(return_value={**PRODUCT_DB})
            res = client.get(self.URL, headers=buyer_headers)

        assert res.status_code == 200
        data = res.json()
        assert len(data) == 1
        assert data[0]["title"] == "Test T-Shirt"


# ─── GET /api/v1/wishlist/get/{product_id} ────────────────────────────────────


class TestGetWishlistItem:
    def _url(self, product_id: str = TEST_PRODUCT_ID):
        return f"/api/v1/wishlist/get/{product_id}"

    def test_no_token_returns_401(self, client):
        res = client.get(self._url())
        assert res.status_code == 401

    def test_returns_true_when_item_exists(self, client, buyer_headers):
        with (
            patch("config.db.user_collection") as mock_coll,
            patch("services.wishListService.wishlist_collection") as mock_wc,
        ):
            mock_coll.find_one = AsyncMock(return_value=BUYER_USER_DB)
            mock_wc.find_one = AsyncMock(return_value=WISHLIST_ENTRY)
            res = client.get(self._url(), headers=buyer_headers)

        assert res.status_code == 200
        assert res.json() == {"exist": True}

    def test_returns_false_when_item_absent(self, client, buyer_headers):
        with (
            patch("config.db.user_collection") as mock_coll,
            patch("services.wishListService.wishlist_collection") as mock_wc,
        ):
            mock_coll.find_one = AsyncMock(return_value=BUYER_USER_DB)
            mock_wc.find_one = AsyncMock(return_value=None)
            res = client.get(self._url(), headers=buyer_headers)

        assert res.status_code == 200
        assert res.json() == {"exist": False}


# ─── DELETE /api/v1/wishlist/delete/{product_id} ──────────────────────────────


class TestDeleteFromWishlist:
    def _url(self, product_id: str = TEST_PRODUCT_ID):
        return f"/api/v1/wishlist/delete/{product_id}"

    def test_no_token_returns_401(self, client):
        res = client.delete(self._url())
        assert res.status_code == 401

    def test_success(self, client, buyer_headers):
        with (
            patch("config.db.user_collection") as mock_coll,
            patch("services.wishListService.wishlist_collection") as mock_wc,
        ):
            mock_coll.find_one = AsyncMock(return_value=BUYER_USER_DB)
            mock_wc.find_one_and_delete = AsyncMock(return_value=WISHLIST_ENTRY)
            res = client.delete(self._url(), headers=buyer_headers)

        assert res.status_code == 200
        assert "removed" in res.json()["msg"]
