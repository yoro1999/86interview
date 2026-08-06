import os
import sys
import json
import django

# Setup Django Environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from rest_framework.test import APIClient

def test_process_order_pipeline():
    print("=" * 80)
    print("测试新处理流程 API: POST /api/orders/process/")
    print("=" * 80)

    client = APIClient()
    sample_dir = os.path.join(os.path.dirname(__file__), "sample_data")
    order_file_path = os.path.join(sample_dir, "order_sample.json")
    sku_file_path = os.path.join(sample_dir, "sku_sample.json")

    with open(order_file_path, "rb") as f_order, open(sku_file_path, "rb") as f_sku:
        response = client.post(
            "/api/orders/process/",
            {
                "order_file": f_order,
                "sku_file": f_sku
            },
            format="multipart"
        )

    print(f"HTTP Status Code: {response.status_code}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()
    assert "header" in data
    assert "items" in data
    assert "tracking" in data
    assert "summary" in data
    assert "status_checks" in data

    print("\n---------------- Pipeline 返回结果 Payload (Excerpt) ----------------")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print("---------------------------------------------------------------------")

    print("\n✅ POST /api/orders/process/ Pipeline 测试通过！")
    print("=" * 80)

if __name__ == '__main__':
    test_process_order_pipeline()
