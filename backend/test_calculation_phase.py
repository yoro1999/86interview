import os
import sys
import django

# Setup Django Environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from services.order_import_service import OrderImportService
from services.calculation_service import CalculationService

def test_calculation_service_multi_sku():
    print("=" * 70)
    print("开始测试：Calculation Service 费用计算引擎 (多 SKU 订单)")
    print("=" * 70)

    # 1. 导入包含 5 项不同 SKU 的 Order 1 Payload
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
            {"sku_code": "TBAMET10", "quantity": 3, "tracking_no": "Track 1"}, # 3 * $49.00 = 147.00
            {"sku_code": "TBAMET28", "quantity": 1, "tracking_no": "Track 1"}, # 1 * $99.00 = 99.00
            {"sku_code": "TBOPAL28", "quantity": 1, "tracking_no": "Track 1"}, # 1 * $120.00 = 120.00
            {"sku_code": "HARNIG", "quantity": 4, "tracking_no": "Track 1"},   # 4 * $85.00 = 340.00
            {"sku_code": "LELCBD100", "quantity": 6, "tracking_no": "Track 1"},# 6 * $150.00 = 900.00
        ]
    }

    print("\n[Step 1] 导入测试订单 Order 1...")
    order1 = OrderImportService.import_order(order1_payload)
    print(f"✅ 成功导入订单: {order1.order_no}")

    # 2. 执行 CalculationService 计算
    print("\n[Step 2] 执行 CalculationService 进行费用结算...")
    calc_service = CalculationService()
    result = calc_service.calculate_order_summary(order1)

    print("\n---------------- SKU 明细行计算 ----------------")
    expected_subtotal = 0.0
    for line in result["line_items"]:
        sku_code = line["sku_code"]
        name = line["name"]
        qty = line["quantity"]
        unit_price = line["price"]
        line_total = line["line_total"]
        expected_line_total = round(unit_price * qty, 2)
        expected_subtotal += line_total
        print(f"SKU: {sku_code:<10} | 单价: ${unit_price:>6.2f} | 数量: {qty:>2} | 行总价: ${line_total:>7.2f}")
        assert abs(line_total - expected_line_total) < 0.001, f"Line total mismatch for {sku_code}"

    summary = result["summary"]
    subtotal = summary["subtotal"]
    gst = summary["gst"]
    shipment_fee = summary["shipment_fee"]
    total = summary["total"]

    print("\n---------------- 费用 Summary 汇总 ----------------")
    print(f"  小计 (Subtotal):      ${subtotal:>8.2f}")
    print(f"  消费税 (GST 10%):      ${gst:>8.2f}")
    print(f"  运费 (Shipment Fee):  ${shipment_fee:>8.2f}")
    print(f"  订单总额 (Total):     ${total:>8.2f}")
    print("--------------------------------------------------")

    # 验证公式断言
    expected_subtotal = round(expected_subtotal, 2)
    expected_gst = round(subtotal * 0.10, 2)
    expected_total = round(subtotal + expected_gst + shipment_fee, 2)

    assert abs(subtotal - expected_subtotal) < 0.001, f"Subtotal mismatch: got {subtotal}, expected {expected_subtotal}"
    assert abs(gst - expected_gst) < 0.001, f"GST mismatch: got {gst}, expected {expected_gst}"
    assert abs(total - expected_total) < 0.001, f"Total mismatch: got {total}, expected {expected_total}"

    print("\n✅ 所有数学计算与断言校验通过！")
    print("=" * 70)

if __name__ == '__main__':
    test_calculation_service_multi_sku()
