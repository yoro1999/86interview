import re
import logging
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Any, List, Optional
from apps.orders.models import Order
from services.sku_service import SKUService

logger = logging.getLogger(__name__)

class CalculationService:
    """
    订单费用计算引擎服务 (Calculation Service)
    文件路径：services/calculation_service.py
    职责：
    1. 接收 Order 实体或 Order 编号。
    2. 通过 SKUService 获取每个 SKU 的价格。
    3. Line Total = SKU price * quantity。
    4. Subtotal = sum(all line totals)。
    5. GST = Subtotal * 10%。
    6. Bonus 运费估算 (Shipment Fee Estimator):
       - 原寄件地址邮编：2111 (Ryde, NSW)
       - 从送货地址提取 4 位邮编
       - 基于 SKU 重量 (Weight) 与尺寸 (Length x Width x Height / 5000) 计算计费重量
       - 结合跨州/本州费率计算估算运费
    7. Total = Subtotal + GST + Shipment Fee。
    """

    def __init__(self, sku_service: Optional[SKUService] = None):
        self.sku_service = sku_service or SKUService()

    @staticmethod
    def estimate_shipment_fee(items: List[Dict[str, Any]], address: str = "") -> Dict[str, Any]:
        """
        Bonus 运费估算逻辑 (PDF Section 4 Rules)
        """
        origin_postcode = "2111"  # Ryde, NSW

        # 抽取收件地址 4 位邮编
        match = re.search(r'\b(\d{4})\b', address or "")
        dest_postcode = match.group(1) if match else "3000"

        gross_weight = 0.0
        volumetric_weight = 0.0

        for item in items:
            qty = float(item.get("quantity", 1))
            w = float(item.get("weight", 0.2))
            length = float(item.get("length", 10.0))
            width = float(item.get("width", 5.0))
            height = float(item.get("height", 5.0))

            gross_weight += w * qty
            # 体积重标准公式 (L x W x H / 5000)
            volumetric_weight += ((length * width * height) / 5000.0) * qty

        chargeable_weight = max(gross_weight, volumetric_weight)

        # 依据邮编匹配费率区段 (Zone Rate Matrix)
        if dest_postcode.startswith('2'):
            base_rate = 8.50
            per_kg_rate = 1.20
            zone_name = "Intrastate (NSW/ACT)"
        elif dest_postcode.startswith(('3', '4', '5')):
            base_rate = 14.50
            per_kg_rate = 2.20
            zone_name = "Interstate (VIC/QLD/SA)"
        else:
            base_rate = 22.00
            per_kg_rate = 3.50
            zone_name = "Remote Interstate (WA/TAS/NT)"

        fee = base_rate + (chargeable_weight * per_kg_rate)
        fee_rounded = round(fee, 2)

        return {
            "shipment_fee": fee_rounded,
            "origin_postcode": origin_postcode,
            "destination_postcode": dest_postcode,
            "chargeable_weight_kg": round(chargeable_weight, 2),
            "gross_weight_kg": round(gross_weight, 2),
            "volumetric_weight_kg": round(volumetric_weight, 2),
            "zone_name": zone_name
        }

    def calculate_order_summary(self, order: Order) -> Dict[str, Any]:
        """
        计算给定订单的金额明细与汇总。
        """
        if not order:
            raise ValueError("传入的订单实体不能为空")

        line_items_result: List[Dict[str, Any]] = []
        subtotal_decimal = Decimal('0.00')

        for item in order.items.all():
            sku_code = item.sku_code
            quantity = item.quantity

            sku_info = self.sku_service.get_or_fetch_sku(sku_code)

            unit_price = Decimal(str(sku_info.price)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            qty_decimal = Decimal(str(quantity))
            
            line_total = (unit_price * qty_decimal).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            subtotal_decimal += line_total

            line_items_result.append({
                "sku_code": sku_info.sku_code,
                "name": sku_info.name,
                "quantity": quantity,
                "price": float(unit_price),
                "line_total": float(line_total),
                "weight": 0.2,
                "length": 10.0,
                "width": 5.0,
                "height": 5.0
            })

        subtotal = subtotal_decimal.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        gst = (subtotal * Decimal('0.10')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # 估算运费
        shipping_result = self.estimate_shipment_fee(line_items_result, order.address)
        shipment_fee = Decimal(str(shipping_result["shipment_fee"]))

        total = (subtotal + gst + shipment_fee).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        return {
            "order_no": order.order_no,
            "line_items": line_items_result,
            "summary": {
                "subtotal": float(subtotal),
                "gst": float(gst),
                "shipment_fee": float(shipment_fee),
                "total": float(total),
                "shipment_details": shipping_result
            }
        }
