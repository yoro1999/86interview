import os
import sys
import django

# Setup Django Environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.orders.models import Order, OrderItem
from apps.products.models import SKU
from services.order_import_service import OrderImportService
from services.sku_service import SKUService

def test_order_import_and_sku_flow():
    print("=" * 60)
    print("开始测试：业务服务层第一阶段 (Order Import & SKU Caching)")
    print("=" * 60)

    # 1. 模拟导入需求文档中的 Order 1
    order1_payload = {
        "order_no": "PO-20251130-00072",
        "order_date": "30/11/25",
        "status": "Completed",
        "company_name": "V22 Dispensary",
        "customer_name": "Jason Hu",
        "phone_number": "0481 735 488",
        "email": "Jason@aerishealth.au",
        "address": "125 Toorak Road, South Yarra VIC 3141",
        "items": [
            {"sku_code": "TBAMET10", "quantity": 3, "tracking_no": "Track 1"},
            {"sku_code": "TBAMET28", "quantity": 1, "tracking_no": "Track 1"},
            {"sku_code": "TBOPAL28", "quantity": 1, "tracking_no": "Track 1"},
            {"sku_code": "HARNIG", "quantity": 4, "tracking_no": "Track 1"},
            {"sku_code": "LELCBD100", "quantity": 6, "tracking_no": "Track 1"},
        ]
    }

    print("\n[Step 1] 测试 OrderImportService 导入 Order 1...")
    order1 = OrderImportService.import_order(order1_payload)
    print(f"✅ 成功成功创建订单: {order1.order_no} | 客户: {order1.customer_name}")
    print(f"   包含订单明细数量: {order1.items.count()} 项")

    # 2. 测试 SKU Service (首次查询，体验 SQL Provider 检索与本地缓存)
    print("\n[Step 2] 测试 SKUService 动态检索与缓存 (首次查询 SKU: TBAMET10)...")
    sku_service = SKUService()
    
    # 确认数据库中该 SKU 是否已存在
    sku_in_db_before = SKU.objects.filter(sku_code="TBAMET10").exists()
    print(f"   查询前数据库缓存中是否存在 TBAMET10: {sku_in_db_before}")

    sku_instance1 = sku_service.get_or_fetch_sku("TBAMET10")
    print(f"✅ 检索成功！获得 SKU 对象: {sku_instance1.sku_code}")
    print(f"   名称 (ProductName -> name): {sku_instance1.name}")
    print(f"   价格 (RRP -> price): ${sku_instance1.price}")
    print(f"   描述 (Description -> description): {sku_instance1.description}")

    sku_in_db_after = SKU.objects.filter(sku_code="TBAMET10").exists()
    print(f"   查询后数据库缓存中是否存在 TBAMET10: {sku_in_db_after}")

    # 3. 测试二次查询 (应当直接命中本地 DB 缓存)
    print("\n[Step 3] 测试二次查询 (应当从 products.SKU 缓存直接获取)...")
    sku_instance2 = sku_service.get_or_fetch_sku("TBAMET10")
    print(f"✅ 二次检索成功！从本地 DB 获取对象: {sku_instance2}")

    # 4. 为 Order 1 中所有 SKU 批量抓取/缓存
    print("\n[Step 4] 为 Order 1 中所有 SKU 执行自动同步与缓存...")
    for item in order1.items.all():
        sku_obj = sku_service.get_or_fetch_sku(item.sku_code)
        print(f"   - SKU: {sku_obj.sku_code} | 名称: {sku_obj.name} | 单价: ${sku_obj.price}")

    print("\n" + "=" * 60)
    print("🎉 所有第一阶段业务服务层功能验证完成！")
    print("=" * 60)

if __name__ == '__main__':
    test_order_import_and_sku_flow()
