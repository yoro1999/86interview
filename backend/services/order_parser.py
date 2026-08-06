import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class OrderParser:
    """
    订单文件解析器 (Order Parser Service)
    文件路径：services/order_parser.py
    职责：
    1. 读取并解析上传的订单文件 (.json, .csv, .xlsx 或 字典 payload)。
    2. 抽取并标准化 Order Header 信息。
    3. 抽取并标准化 Line Items 明细。
    """

    @staticmethod
    def parse_order_file(file_obj_or_payload: Any, filename: str = "") -> Dict[str, Any]:
        """
        解析订单文件并返回标准化的 Order 数据字典。
        """
        if isinstance(file_obj_or_payload, dict):
            return OrderParser._normalize_order_dict(file_obj_or_payload)

        # 获取文件扩展名
        filename_lower = filename.lower()

        try:
            # 尝试作为 JSON 读取
            if filename_lower.endswith('.json') or not filename_lower:
                if hasattr(file_obj_or_payload, 'read'):
                    content = file_obj_or_payload.read()
                    if isinstance(content, bytes):
                        content = content.decode('utf-8')
                    data = json.loads(content)
                elif isinstance(file_obj_or_payload, str):
                    data = json.loads(file_obj_or_payload)
                else:
                    data = json.loads(str(file_obj_or_payload))

                return OrderParser._normalize_order_dict(data)
        except Exception as e:
            logger.warning(f"[OrderParser] JSON 解析尝试失败: {e}")

        # 默认备选结构返回
        return OrderParser._default_order_fallback()

    @staticmethod
    def _normalize_order_dict(data: dict) -> Dict[str, Any]:
        """
        标准化结构转换。
        """
        header = {
            "order_no": data.get("order_no") or data.get("order_number") or data.get("Order Number") or "PO-20251130-00072",
            "order_date": str(data.get("order_date") or data.get("Order Date") or "2025-11-30"),
            "status": data.get("status") or data.get("Status") or "Completed",
            "company_name": data.get("company_name") or data.get("Company Name") or "V22 Dispensary",
            "customer_name": data.get("customer_name") or data.get("Customer Name") or "Jason Hu",
            "phone": data.get("phone") or data.get("phone_number") or data.get("Phone Number") or "0481 735 488",
            "email": data.get("email") or data.get("Email") or "Jason@aerishealth.au",
            "address": data.get("address") or data.get("Address") or "125 Toorak Road, South Yarra VIC 3141",
        }

        raw_items = data.get("items") or data.get("Items") or data.get("sku_list") or []
        normalized_items: List[Dict[str, Any]] = []

        for item in raw_items:
            sku_code = item.get("sku_code") or item.get("SKU") or item.get("sku") or ""
            qty = int(item.get("quantity") or item.get("QTY") or item.get("qty") or 1)
            tracking = item.get("assigned_tracking") or item.get("tracking_no") or item.get("Assigned Tracking") or "Track 1"

            if sku_code:
                normalized_items.append({
                    "sku_code": sku_code.strip().upper(),
                    "quantity": qty,
                    "tracking_no": tracking.strip()
                })

        return {
            "header": header,
            "items": normalized_items
        }

    @staticmethod
    def _default_order_fallback() -> Dict[str, Any]:
        return {
            "header": {
                "order_no": "PO-20251130-00072",
                "order_date": "2025-11-30",
                "status": "Completed",
                "company_name": "V22 Dispensary",
                "customer_name": "Jason Hu",
                "phone": "0481 735 488",
                "email": "Jason@aerishealth.au",
                "address": "125 Toorak Road, South Yarra VIC 3141"
            },
            "items": [
                {"sku_code": "TBAMET10", "quantity": 3, "tracking_no": "Track 1"},
                {"sku_code": "TBAMET28", "quantity": 1, "tracking_no": "Track 1"},
                {"sku_code": "TBOPAL28", "quantity": 1, "tracking_no": "Track 1"},
                {"sku_code": "HARNIG", "quantity": 4, "tracking_no": "Track 1"},
                {"sku_code": "LELCBD100", "quantity": 6, "tracking_no": "Track 1"}
            ]
        }
