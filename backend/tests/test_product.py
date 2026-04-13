import pytest
import bson
from datetime import datetime
from unittest.mock import patch, AsyncMock, MagicMock

from tests.conftest import (
    TEST_SELLER_USER_ID,
    TEST_BUYER_USER_ID,
    TEST_PRODUCT_ID,
    make_async_iter,
)

SELLER_USER_DB = {"_id": bson.ObjectId(TEST_SELLER_USER_ID), "role": "seller"}
BUYER_USER_DB = {"_id": bson.ObjectId(TEST_BUYER_USER_ID), "role": "buyer"}

PRODUCT_DB = {
    "_id": bson.ObjectId(TEST_PRODUCT_ID),
    "title": "Test T-Shirt",
    "description": "A cool T-shirt",
    "price": 500,
    "category": "TSHIRT",
    "slug": "test-t-shirt____abc123",
    "images": [
        {"image_url": "http://example.com/img.jpg", "public_id": "products/img"}
    ],
    "user": {"name": "Seller", "user_id": TEST_SELLER_USER_ID},
    "created_at": datetime.now(),
    "updated_at": datetime.now(),
}

VALID_FORM = {
    "title": "Test T-Shirt",
    "description": "A cool T-shirt",
    "price": "500",
    "category": "TSHIRT",
}


# ─── GET /api/v1/product/all-products ─────────────────────────────────────────


class TestAllProducts:
    URL = "/api/v1/product/all-products"

    def test_no_token_returns_401(self, client):
        res = client.get(self.URL)
        assert res.status_code == 401

    def test_buyer_role_returns_400(self, client, buyer_headers):
        with patch("config.db.user_collection") as mock_coll:
            mock_coll.find_one = AsyncMock(return_value=BUYER_USER_DB)
            res = client.get(self.URL, headers=buyer_headers)

        assert res.status_code == 400
        assert "seller" in res.json()["detail"]

    def test_seller_returns_empty_list(self, client, seller_headers):
        with (
            patch("config.db.user_collection") as mock_coll,
            patch("services.productService.product_collection") as mock_pc,
        ):
            mock_coll.find_one = AsyncMock(return_value=SELLER_USER_DB)
            mock_pc.find.return_value = make_async_iter([])
            res = client.get(self.URL, headers=seller_headers)

        assert res.status_code == 200
        assert res.json() == []

    def test_seller_returns_product_list(self, client, seller_headers):
        with (
            patch("config.db.user_collection") as mock_coll,
            patch("services.productService.product_collection") as mock_pc,
        ):
            mock_coll.find_one = AsyncMock(return_value=SELLER_USER_DB)
            mock_pc.find.return_value = make_async_iter([{**PRODUCT_DB}])
            res = client.get(self.URL, headers=seller_headers)

        assert res.status_code == 200
        data = res.json()
        assert len(data) == 1
        assert data[0]["title"] == PRODUCT_DB["title"]


# ─── DELETE /api/v1/product/delete/{productId} ────────────────────────────────


class TestDeleteProduct:
    def _url(self, product_id: str = TEST_PRODUCT_ID):
        return f"/api/v1/product/delete/{product_id}"

    def test_no_token_returns_401(self, client):
        res = client.delete(self._url())
        assert res.status_code == 401

    def test_success(self, client, seller_headers):
        with (
            patch("config.db.user_collection") as mock_coll,
            patch("services.productService.product_collection") as mock_pc,
            patch("cloudinary.uploader.destroy"),
        ):
            mock_coll.find_one = AsyncMock(return_value=SELLER_USER_DB)
            mock_pc.find_one_and_delete = AsyncMock(return_value={**PRODUCT_DB})
            res = client.delete(self._url(), headers=seller_headers)

        assert res.status_code == 200
        assert res.json()["msg"] == "Product deleted successfully"

    def test_product_not_found_returns_400(self, client, seller_headers):
        with (
            patch("config.db.user_collection") as mock_coll,
            patch("services.productService.product_collection") as mock_pc,
        ):
            mock_coll.find_one = AsyncMock(return_value=SELLER_USER_DB)
            mock_pc.find_one_and_delete = AsyncMock(return_value=None)
            res = client.delete(self._url(), headers=seller_headers)

        assert res.status_code == 400


# ─── POST /api/v1/product/add-product ─────────────────────────────────────────


class TestAddProduct:
    URL = "/api/v1/product/add-product"

    def test_no_token_returns_401(self, client):
        res = client.post(
            self.URL,
            data=VALID_FORM,
            files=[("images", ("test.jpg", b"img", "image/jpeg"))],
        )
        assert res.status_code == 401

    def test_missing_required_form_field_returns_422(self, client, seller_headers):
        with patch("config.db.user_collection") as mock_coll:
            mock_coll.find_one = AsyncMock(return_value=SELLER_USER_DB)
            res = client.post(
                self.URL,
                data={"description": "No title or price"},
                files=[("images", ("test.jpg", b"img", "image/jpeg"))],
                headers=seller_headers,
            )

        assert res.status_code == 422

    def test_seller_adds_product_successfully(self, client, seller_headers):
        with (
            patch("config.db.user_collection") as mock_coll,
            patch("services.productService.product_collection") as mock_pc,
            patch("services.productService.profile_collection") as mock_prof,
            patch("cloudinary.uploader.upload") as mock_upload,
        ):
            mock_coll.find_one = AsyncMock(return_value=SELLER_USER_DB)
            mock_prof.find_one = AsyncMock(
                return_value={"name": "Seller", "user_id": TEST_SELLER_USER_ID}
            )
            mock_pc.insert_one = AsyncMock(return_value=MagicMock())
            mock_upload.return_value = {
                "secure_url": "http://example.com/img.jpg",
                "public_id": "products/img",
            }
            res = client.post(
                self.URL,
                data=VALID_FORM,
                files=[("images", ("test.jpg", b"fakeimagecontent", "image/jpeg"))],
                headers=seller_headers,
            )

        assert res.status_code == 200
        assert res.json()["msg"] == "Product added successfully"
