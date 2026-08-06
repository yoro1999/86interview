import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class SKUParser:
    """
    SKU 文件解析器 (SKU Parser Service)
    文件路径：services/sku_parser.py
    职责：
    1. 读取解析上传的 SKU 文件 (.json, .csv, .xlsx 或 List[Dict])。
    2. 返回以 sku_code 为 Key 的标准化索引字典映射。
    """

    @staticmethod
    def parse_sku_file(file_obj_or_payload: Any, filename: str = "") -> Dict[str, Dict[str, Any]]:
        """
        解析 SKU 字典文件，返回 { sku_code: SKU_Details }。
        """
        if isinstance(file_obj_or_payload, list):
            return SKUParser._normalize_sku_list(file_obj_or_payload)
        elif isinstance(file_obj_or_payload, dict):
            if "skus" in file_obj_or_payload:
                return SKUParser._normalize_sku_list(file_obj_or_payload["skus"])
            return SKUParser._normalize_sku_list([file_obj_or_payload])

        filename_lower = filename.lower()

        try:
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

                if isinstance(data, list):
                    return SKUParser._normalize_sku_list(data)
                elif isinstance(data, dict):
                    return SKUParser._normalize_sku_list(data.get("skus", [data]))
        except Exception as e:
            logger.warning(f"[SKUParser] SKU 文件 JSON 解析异常: {e}")

        return {}

    @staticmethod
    def _normalize_sku_list(items: List[dict]) -> Dict[str, Dict[str, Any]]:
        sku_map: Dict[str, Dict[str, Any]] = {}

        for item in items:
            raw_code = item.get("sku_code") or item.get("SKU") or item.get("sku") or ""
            if not raw_code:
                continue

            clean_code = str(raw_code).strip().upper()
            svg_xml = f'<svg xmlns="http://www.w3.org/2000/svg" width="150" height="150" viewBox="0 0 150 150"><rect width="150" height="150" fill="%236366f1"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="white" font-size="16" font-family="sans-serif">{clean_code}</text></svg>'

            img_val = item.get("image_url") or item.get("image")
            if not img_val or "placeholder.com" in str(img_val):
                img_val = f"data:image/svg+xml;utf8,{svg_xml}"

            sku_map[clean_code] = {
                "sku_code": clean_code,
                "name": item.get("name") or item.get("ProductName") or f"Product {clean_code}",
                "description": item.get("description") or item.get("Description") or "",
                "price": float(item.get("price") or item.get("RRP") or 0.0),
                "weight": float(item.get("weight") or item.get("Volumetric_GrossWeight") or 0.2),
                "width": float(item.get("width") or 5.0),
                "length": float(item.get("length") or 10.0),
                "height": float(item.get("height") or 5.0),
                "volume": float(item.get("volume") or 250.0),
                "image_url": img_val
            }

        return sku_map
