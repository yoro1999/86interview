import logging
from typing import Dict, Any, List
from services.sku_service import SKUService

logger = logging.getLogger(__name__)

class SKUMatcher:
    """
    SKU 匹配服务 (SKU Matcher Service)
    文件路径：services/sku_matcher.py
    职责：
    1. 接收 Order Items 列表与解析出的 SKU 字典映射。
    2. SKU 检索抽象层 (SKUService Abstraction):
       - Primary: 调用 SQL Website/API 数据源 (product_list / https://tinyurl.com/2zp5p54a) 检索产品信息。
       - Fallback: 当 SQL 源检索失败或为空时，退化使用上传的 Local SKU File 中的数据。
    """

    def __init__(self, sku_service=None):
        self.sku_service = sku_service or SKUService()

    def match_and_enrich_items(
        self,
        order_items: List[Dict[str, Any]],
        parsed_sku_map: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        匹配并富化订单项 (Primary: SQL API -> Fallback: Local SKU File)。
        """
        enriched_items: List[Dict[str, Any]] = []

        for item in order_items:
            code = item["sku_code"].strip().upper()
            qty = item["quantity"]
            tracking_no = item.get("tracking_no", "Track 1")

            sku_data = None
            sku_source = "sql_api"

            # Primary: 优先调用 SKUService 查询 SQL Website/API 数据源
            try:
                sql_sku_obj = self.sku_service.get_or_fetch_sku(code)
                if sql_sku_obj:
                    sku_data = {
                        "sku_code": sql_sku_obj.sku_code,
                        "name": sql_sku_obj.name,
                        "description": sql_sku_obj.description,
                        "price": float(sql_sku_obj.price),
                        "weight": 0.2,
                        "width": 5.0,
                        "length": 10.0,
                        "height": 5.0,
                        "volume": 250.0,
                        "image_url": sql_sku_obj.image_url,
                        "source": "sql_api"
                    }
                    logger.info(f"[SKUMatcher] Primary: 成功通过 SQL Website/API 匹配 SKU: {code}")
            except Exception as e:
                logger.warning(f"[SKUMatcher] Primary SQL 查询异常/缺失 (SKU: {code}): {e}")

            # Fallback: 若 SQL API 未命中，退化至上传的 Local SKU File
            if not sku_data and code in parsed_sku_map:
                sku_data = parsed_sku_map[code]
                sku_data["source"] = "local_sku_file"
                sku_source = "local_sku_file"
                logger.info(f"[SKUMatcher] Fallback: 使用 Local SKU File 匹配 SKU: {code}")

            # Default Backup: 防爆默认值
            if not sku_data:
                svg_xml = f'<svg xmlns="http://www.w3.org/2000/svg" width="150" height="150" viewBox="0 0 150 150"><rect width="150" height="150" fill="%236366f1"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="white" font-size="16" font-family="sans-serif">{code}</text></svg>'
                sku_data = {
                    "sku_code": code,
                    "name": f"Product {code}",
                    "description": "Standard product description",
                    "price": 50.0,
                    "weight": 0.2,
                    "width": 5.0,
                    "length": 10.0,
                    "height": 5.0,
                    "volume": 250.0,
                    "image_url": f"data:image/svg+xml;utf8,{svg_xml}",
                    "source": "default_fallback"
                }

            unit_price = float(sku_data["price"])
            line_total = round(unit_price * qty, 2)

            enriched_items.append({
                "sku_code": code,
                "name": sku_data["name"],
                "description": sku_data.get("description", ""),
                "quantity": qty,
                "unit_price": unit_price,
                "line_total": line_total,
                "weight": sku_data.get("weight", 0.2),
                "width": sku_data.get("width", 5.0),
                "length": sku_data.get("length", 10.0),
                "height": sku_data.get("height", 5.0),
                "volume": sku_data.get("volume", 250.0),
                "image_url": sku_data.get("image_url"),
                "tracking_no": tracking_no,
                "data_source": sku_data.get("source", sku_source)
            })

        return enriched_items
