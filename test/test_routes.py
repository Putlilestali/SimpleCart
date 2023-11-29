import json

from .settings import DEFAULT_PRICE
from api.utils import (
    get_price,
    get_subtotal,
    apply_promo
)


def test_product_detail_api(client):
    id = 3
    response = client.get(f"/api/products/{id}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert id == data.get('id')
    assert DEFAULT_PRICE * id


def test_product_api(client):
    response = client.get("/api/products")
    assert response.status_code == 200

def test_post_cart(client):
    
    # Buat test produk
    product_data = {
        'id': 1,
        'name': 'Test Product',
        'price': DEFAULT_PRICE
    }
    client.post('/api/products', data=json.dumps(product_data), content_type='application/json')

    # Buat test keranjang
    cart_data = {
        'cart_items': [
            {'product_id': 1, 'qty': 2},
            # Tambahkan lebih banyak item jika diperlukan
        ]
    }

    # Posting test keranjang
    response = client.post('/api/cart', data=json.dumps(cart_data), content_type='application/json')

    # Periksa apakah respon berhasil (kode status 200 untuk OK)
    assert response.status_code == 200  # Dengan asumsi kreasi yang berhasil akan menghasilkan 200

    # Pembersihan: Hapus produk uji dan keranjang jika diperlukan
    client.delete(f'/api/products/{product_data["id"]}')

    # Periksa apakah respon.json tidak Ada sebelum mengakses cart_id
    if response.json:
        client.delete(f'/api/cart/{response.json["cart_id"]}')
    else:
        print("Warning: response.json is None")