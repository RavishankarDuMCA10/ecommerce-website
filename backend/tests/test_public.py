import pytest
import bson
from datetime import datetime
from unittest.mock import patch, AsyncMock

from tests.conftest import TEST_PRODUCT_ID, make_async_iter

_PRODUCT_DB = {
    # No _id — the real query uses {"_id": 0} projection
    "title": "Test T-Shirt",
    "description": "A cool T-shirt",
    "price": 500,
    "category": "TSHIRT",
    "slug": "test-t-shirt",
    "images": [
        {"image_url": "http://example.com/img.jpg", "public_id": "products/img"}
    ],
    "user": {"name": "Seller"},
    "created_at": datetime.now(),
    "updated_at": datetime.now(),
}


def _product_copy():
    """Return a fresh copy so the service can safely mutate (del product['images'])."""
    return {**_PRODUCT_DB, "images": list(_PRODUCT_DB["images"])}


# ─── GET /api/v1/products ─────────────────────────────────────────────────────


class TestGetAllProducts:
    URL = "/api/v1/products"

    def test_returns_empty_list(self, client):
        with patch("services.publicService.product_collection") as mock_pc:
            mock_pc.find.return_value = make_async_iter([])
            res = client.get(self.URL)

        assert res.status_code == 200
        assert res.json() == []

    def test_returns_product_list(self, client):
        with patch("services.publicService.product_collection") as mock_pc:
            mock_pc.find.return_value = make_async_iter([_product_copy()])
            res = client.get(self.URL)

        assert res.status_code == 200
        data = res.json()
        assert len(data) == 1
        assert data[0]["title"] == "Test T-Shirt"
        assert "image" in data[0]
        assert "images" not in data[0]

    def test_search_query_is_accepted(self, client):
        with patch("services.publicService.product_collection") as mock_pc:
            mock_pc.find.return_value = make_async_iter([])
            res = client.get(self.URL, params={"search": "shirt"})

        assert res.status_code == 200

    def test_category_query_is_accepted(self, client):
        with patch("services.publicService.product_collection") as mock_pc:
            mock_pc.find.return_value = make_async_iter([])
            res = client.get(self.URL, params={"category": "TSHIRT"})

        assert res.status_code == 200


# ─── GET /api/v1/product/{slug} ───────────────────────────────────────────────


class TestGetProductBySlug:
    def _url(self, slug: str = "test-t-shirt"):
        return f"/api/v1/product/{slug}"

    def test_product_found(self, client):
        product = {
            "_id": bson.ObjectId(TEST_PRODUCT_ID),
            "title": "Test T-Shirt",
            "description": "A cool T-shirt",
            "price": 500,
            "category": "TSHIRT",
            "slug": "test-t-shirt",
            "images": [
                {"image_url": "http://example.com/img.jpg", "public_id": "p/img"}
            ],
            "user": {"name": "Seller"},
            "created_at": datetime.now(),
        }
        with patch("services.publicService.product_collection") as mock_pc:
            mock_pc.find_one = AsyncMock(return_value=product)
            res = client.get(self._url())

        assert res.status_code == 200
        body = res.json()
        assert body["title"] == "Test T-Shirt"
        assert "image" in body
        assert "images" not in body

    def test_product_not_found_returns_400(self, client):
        with patch("services.publicService.product_collection") as mock_pc:
            mock_pc.find_one = AsyncMock(return_value=None)
            res = client.get(self._url("nonexistent-slug"))

        # Service raises HTTPException(404), but the controller re-raises as 400
        assert res.status_code == 400
