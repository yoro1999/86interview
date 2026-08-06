import logging
from datetime import datetime
from typing import Dict, Any, Optional
from apps.tracking.models import Tracking
from integrations.logistics.auspost_client import AusPostClient
from integrations.logistics.tnt_client import TNTClient

logger = logging.getLogger(__name__)

class TrackingService:
    """
    物流追踪业务服务 (Tracking Service)
    文件路径：services/tracking_service.py
    职责：
    1. 根据物流公司 (StarTrack/AusPost 或 TNT) 识别并调用对应 Client。
    2. 统一将各物流商返回的结构归一化，包含多节点进度时间轴 (events)。
    3. 保存至 tracking.Tracking 数据库模型。
    """

    def __init__(self, auspost_client: Optional[AusPostClient] = None, tnt_client: Optional[TNTClient] = None):
        self.auspost_client = auspost_client or AusPostClient()
        self.tnt_client = tnt_client or TNTClient()

    def sync_tracking_info(self, tracking_no: str, logistics_company: str) -> Dict[str, Any]:
        if not tracking_no or not logistics_company:
            raise ValueError("tracking_no 与 logistics_company 均不能为空")

        clean_tracking_no = tracking_no.strip()
        clean_company = logistics_company.strip()
        company_lower = clean_company.lower()

        if 'startrack' in company_lower or 'auspost' in company_lower:
            raw_result = self.auspost_client.fetch_tracking_info(clean_tracking_no)
            unified_data = self._normalize_auspost_response(raw_result, clean_tracking_no, clean_company)
        elif 'tnt' in company_lower:
            raw_result = self.tnt_client.fetch_tracking_info(clean_tracking_no)
            unified_data = self._normalize_tnt_response(raw_result, clean_tracking_no, clean_company)
        else:
            unified_data = {
                "tracking_no": clean_tracking_no,
                "logistics_company": clean_company,
                "status": "In Transit",
                "last_update": datetime.now().isoformat(),
                "data_source": "development_fallback",
                "events": [
                    {"status": "Order Placed", "location": "Warehouse", "timestamp": "2025-11-30", "completed": True},
                    {"status": "In Transit", "location": "Carrier Facility", "timestamp": "2025-12-02", "completed": True}
                ]
            }

        # 保存/更新至 tracking.Tracking 表
        tracking_obj, _ = Tracking.objects.update_or_create(
            tracking_no=unified_data["tracking_no"],
            defaults={
                "logistics_company": unified_data["logistics_company"],
                "status": unified_data["status"],
            }
        )

        return unified_data

    def _normalize_auspost_response(self, raw_result: Dict[str, Any], tracking_no: str, company: str) -> Dict[str, Any]:
        raw_resp = raw_result.get("raw_response", {})
        status = raw_resp.get("status", "In Transit")
        last_update = raw_resp.get("last_update", datetime.now().isoformat())
        data_source = raw_result.get("data_source", "development_fallback")
        events = raw_result.get("events", [])

        return {
          "tracking_no": tracking_no,
          "logistics_company": company,
          "status": status,
          "last_update": str(last_update),
          "data_source": data_source,
          "events": events
        }

    def _normalize_tnt_response(self, raw_result: Dict[str, Any], tracking_no: str, company: str) -> Dict[str, Any]:
        raw_resp = raw_result.get("raw_response", {})
        status = raw_resp.get("status_description", "In Transit")
        last_update = raw_resp.get("timestamp", datetime.now().isoformat())
        data_source = raw_result.get("data_source", "development_fallback")
        events = raw_result.get("events", [])

        return {
          "tracking_no": tracking_no,
          "logistics_company": company,
          "status": status,
          "last_update": str(last_update),
          "data_source": data_source,
          "events": events
        }
