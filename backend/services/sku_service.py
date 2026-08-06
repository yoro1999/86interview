import logging
from typing import Optional
from apps.products.models import SKU
from integrations.sku.sql_product_client import SQLProductClient

logger = logging.getLogger(__name__)

class SKUService:
    """
    SKU 业务与缓存服务 (SKU Service)
    文件路径：services/sku_service.py
    职责：
    1. 接收 sku_code。
    2. 查询本地 products.SKU 数据库缓存。
    3. 若缓存不存在，调用 SQL Product Client 查询外部 product_list 数据。
    4. 执行字段转换映射：
       - SKU -> sku_code
       - ProductName -> name
       - RRP -> price
       - Description -> description
    5. 保存映射后的数据至 products.SKU 本地缓存。
    6. 返回标准化的 SKU 对象。
    """

    def __init__(self, sql_client: Optional[SQLProductClient] = None):
        self.sql_client = sql_client or SQLProductClient()

    def get_or_fetch_sku(self, sku_code: str) -> SKU:
        """
        获取 SKU 详情：优先读取本地缓存，未命中时发起 SQL 查询并写库缓存。

        :param sku_code: SKU 编码 (如 'TBAMET10')
        :return: apps.products.models.SKU 实例
        """
        if not sku_code:
            raise ValueError("SKU 编码不能为空")

        clean_sku = sku_code.strip().upper()

        # 1. 尝试查询本地 DB 缓存
        cached_sku = SKU.objects.filter(sku_code=clean_sku).first()
        if cached_sku:
            logger.info(f"[SKUService] 本地缓存命中: {clean_sku}")
            return cached_sku

        # 2. 缓存未命中，调用 SQL Product Client 检索外部 SQL 数据源
        logger.info(f"[SKUService] 本地缓存未命中，调用 SQL Client 检索: {clean_sku}")
        raw_sql_data = self.sql_client.query_product_by_sku(clean_sku)

        if not raw_sql_data:
            raise ValueError(f"外部 SQL 数据源中未找到 SKU: {clean_sku}")

        # 3. 字段转换映射 (Field Transformation Mapping)
        mapped_sku_code = str(raw_sql_data.get('SKU', clean_sku)).strip().upper()
        mapped_name = str(raw_sql_data.get('ProductName', f"Product {clean_sku}"))
        mapped_price = float(raw_sql_data.get('RRP', 0.0))
        mapped_description = str(raw_sql_data.get('Description', ''))

        # 生成本地内联 SVG 占位图，规避 via.placeholder.com 网络阻断错误
        svg_xml = f'<svg xmlns="http://www.w3.org/2000/svg" width="150" height="150" viewBox="0 0 150 150"><rect width="150" height="150" fill="%236366f1"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="white" font-size="16" font-family="sans-serif">{mapped_sku_code}</text></svg>'
        image_url = f"data:image/svg+xml;utf8,{svg_xml}"

        # 4. 保存至 products.SKU 本地数据库缓存
        sku_instance, created = SKU.objects.update_or_create(
            sku_code=mapped_sku_code,
            defaults={
                'name': mapped_name,
                'price': mapped_price,
                'description': mapped_description,
                'image_url': image_url
            }
        )

        status_str = "已创建本地缓存" if created else "已更新本地缓存"
        logger.info(f"[SKUService] {status_str}: {mapped_sku_code}")

        return sku_instance
