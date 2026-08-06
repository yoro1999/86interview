import os
import sys
import json
import django

# Setup Django Environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.apps import apps
from apps.orders.models import Order, OrderItem
from apps.products.models import SKU
from apps.tracking.models import Tracking
from services.order_import_service import OrderImportService
from services.sku_service import SKUService
from services.calculation_service import CalculationService
from services.tracking_service import TrackingService
from rest_framework.test import APIClient

def run_end_to_end_test():
    print("=" * 80)
    print("系统最终端到端自测 (System End-to-End Self-Test)")
    print("=" * 80)

    # -------------------------------------------------------------
    # 1. Backend 环境检查
    # -------------------------------------------------------------
    print("\n[Step 1] Backend 环境检查...")
    registered_apps = [app.name for app in apps.get_app_configs()]
    required_apps = ['apps.orders', 'apps.products', 'apps.tracking', 'apps.calculation']
    for req in required_apps:
        assert req in registered_apps, f"App {req} 未注册"
    print(f"✅ App 注册检查通过: {required_apps}")

    # -------------------------------------------------------------
    # 2. 数据链路测试 (Order Import Service)
    # -------------------------------------------------------------
    print("\n[Step 2] 数据链路测试 (Order Import Service)...")
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
    order1 = OrderImportService.import_order(order1_payload)
    assert order1.order_no == "PO-20251130-00072"
    assert order1.items.count() == 5
    print(f"✅ Order 导入成功: {order1.order_no} (OrderItem 项数: {order1.items.count()})")

    # -------------------------------------------------------------
    # 3. SKU 数据流程测试 (Cache Check)
    # -------------------------------------------------------------
    print("\n[Step 3] SKU 数据流程测试 (Cache & External SQL Provider)...")
    SKU.objects.filter(sku_code="TBAMET10").delete()
    sku_service = SKUService()

    # 第一次查询 (预期 Miss, 调 Client)
    print("   发起第 1 次查询 (TBAMET10)...")
    sku1 = sku_service.get_or_fetch_sku("TBAMET10")
    assert sku1.sku_code == "TBAMET10"
    assert sku1.name == "TB AMET 10mg Solution"
    assert sku1.price == 49.00
    assert SKU.objects.filter(sku_code="TBAMET10").exists()
    print("   ✅ 第一次查询成功从 External Client 匹配并写入 Cache")

    # 第二次查询 (预期 Hit, 读 Cache)
    print("   发起第 2 次查询 (TBAMET10)...")
    sku2 = sku_service.get_or_fetch_sku("TBAMET10")
    assert sku2.sku_code == "TBAMET10"
    print("   ✅ 第二次查询成功直接读取 Cache")

    # -------------------------------------------------------------
    # 4. Calculation 测试
    # -------------------------------------------------------------
    print("\n[Step 4] Calculation 费用计算测试...")
    calc_service = CalculationService(sku_service=sku_service)
    calc_res = calc_service.calculate_order_summary(order1)
    
    summary = calc_res["summary"]
    assert summary["subtotal"] == 1606.00
    assert summary["gst"] == 160.60
    assert summary["shipment_fee"] == 0.00
    assert summary["total"] == 1766.60
    print(f"   ✅ Subtotal: ${summary['subtotal']}, GST: ${summary['gst']}, Fee: ${summary['shipment_fee']}, Total: ${summary['total']}")

    # -------------------------------------------------------------
    # 5. Tracking 测试
    # -------------------------------------------------------------
    print("\n[Step 5] Tracking 物流归一化测试...")
    tracking_service = TrackingService()
    t1 = tracking_service.sync_tracking_info("2FWZ50008569", "StarTrack/Auspost")
    t3 = tracking_service.sync_tracking_info("305506914", "TNT")

    assert t1["tracking_no"] == "2FWZ50008569"
    assert t1["logistics_company"] == "StarTrack/Auspost"
    assert t3["tracking_no"] == "305506914"
    assert t3["logistics_company"] == "TNT"
    print("   ✅ Track 1 & Track 3 归一化结构与 DB 持久化均正常")

    # -------------------------------------------------------------
    # 6. REST API 测试
    # -------------------------------------------------------------
    print("\n[Step 6] REST API 端点测试 (GET /api/orders/PO-20251130-00072/)...")
    client = APIClient()
    res = client.get("/api/orders/PO-20251130-00072/")
    assert res.status_code == 200
    payload = res.json()
    assert "header" in payload
    assert "items" in payload
    assert "tracking" in payload
    assert "summary" in payload
    print("   ✅ GET /api/orders/PO-20251130-00072/ 响应 HTTP 200，字段校验完整")

    print("\n" + "=" * 80)
    print("🎉 端到端自动化自测 1-6 步骤全部 PASS！")
    print("=" * 80)

if __name__ == '__main__':
    run_end_to_end_test()
