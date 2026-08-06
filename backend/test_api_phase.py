import os
import sys
import json
import django

# Setup Django Environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from rest_framework.test import APIClient

def test_order_detail_api():
    print("=" * 75)
    print("开始测试：REST API 阶段 — GET /api/orders/{order_no}/")
    print("=" * 75)

    client = APIClient()

    # 1. 测试 Order 1: GET /api/orders/PO-20251130-00072/
    order_no1 = "PO-20251130-00072"
    url1 = f"/api/orders/{order_no1}/"
    print(f"\n[Test 1] 发起 HTTP GET 请求: {url1}")
    
    response1 = client.get(url1)
    print(f"HTTP Status Code: {response1.status_code}")
    assert response1.status_code == 200, f"Expected 200, got {response1.status_code}"

    data1 = response1.json()
    
    # 断言结构包含 header, items, tracking, summary
    assert "header" in data1
    assert "items" in data1
    assert "tracking" in data1
    assert "summary" in data1

    print("\n---------------- REST API 返回的 JSON 响应样例 (PO-20251130-00072) ----------------")
    print(json.dumps(data1, indent=2, ensure_ascii=False))
    print("----------------------------------------------------------------------------------")

    # 2. 测试 Order 2: GET /api/orders/PO-20251202-00046/
    order_no2 = "PO-20251202-00046"
    url2 = f"/api/orders/{order_no2}/"
    print(f"\n[Test 2] 发起 HTTP GET 请求: {url2}")
    response2 = client.get(url2)
    print(f"HTTP Status Code: {response2.status_code}")
    assert response2.status_code == 200, f"Expected 200, got {response2.status_code}"

    print("\n✅ 所有 REST API 测试断言通过！")
    print("=" * 75)

if __name__ == '__main__':
    test_order_detail_api()
