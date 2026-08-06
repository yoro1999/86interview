from datetime import datetime
from django.db import transaction
from apps.orders.models import Order, OrderItem

class OrderImportService:
    """
    订单导入服务 (Order Import Service)
    职责：
    1. 提供订单文件/数据读取入口接口。
    2. 解析订单头数据，创建或更新 Order 实体。
    3. 解析订单项数据，创建 OrderItem 关联实体（包含 SKU 编码、数量及 Assigned Tracking）。
    """

    @staticmethod
    @transaction.atomic
    def import_order(order_payload: dict) -> Order:
        """
        从字典或已解析的订单数据结构中导入 Order 与 OrderItem。

        :param order_payload: 包含订单头与订单明细列表的数据结构。
        示例 payload:
        {
            "order_no": "PO-20251130-00072",
            "order_date": "2025-11-30", # 或 datetime/date 对象 / "30/11/25"
            "status": "Completed",
            "company_name": "V22 Dispensary",
            "customer_name": "Jason Hu",
            "phone_number": "0481 735 488",
            "email": "Jason@aerishealth.au",
            "address": "125 Toorak Road, South Yarra VIC 3141",
            "items": [
                {"sku_code": "TBAMET10", "quantity": 3, "tracking_no": "Track 1"},
                {"sku_code": "TBAMET28", "quantity": 1, "tracking_no": "Track 1"},
            ]
        }
        """
        order_no = order_payload.get('order_no')
        if not order_no:
            raise ValueError("订单编号 (order_no) 不能为空")

        raw_date = order_payload.get('order_date')
        if isinstance(raw_date, str):
            # 支持 YYYY-MM-DD 或 DD/MM/YY 格式转换
            try:
                if '/' in raw_date:
                    parts = raw_date.split('/')
                    if len(parts[2]) == 2:
                        year = f"20{parts[2]}"
                    else:
                        year = parts[2]
                    parsed_date = datetime.strptime(f"{parts[0]}/{parts[1]}/{year}", "%d/%m/%Y").date()
                else:
                    parsed_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
            except Exception:
                parsed_date = datetime.now().date()
        else:
            parsed_date = raw_date

        # 创建或更新 Order 头实体
        order, _ = Order.objects.update_or_create(
            order_no=order_no,
            defaults={
                'order_date': parsed_date,
                'status': order_payload.get('status', 'Pending'),
                'company_name': order_payload.get('company_name', ''),
                'customer_name': order_payload.get('customer_name', ''),
                'phone_number': order_payload.get('phone_number', ''),
                'email': order_payload.get('email', ''),
                'address': order_payload.get('address', ''),
            }
        )

        # 清理原有的 OrderItem (重新导入时全量更新)
        order.items.all().delete()

        # 创建 OrderItem 明细实体
        items_data = order_payload.get('items', [])
        order_items = []
        for item_info in items_data:
            order_item = OrderItem(
                order=order,
                sku_code=item_info.get('sku_code', ''),
                quantity=int(item_info.get('quantity', 1)),
                tracking_no=item_info.get('tracking_no', '')
            )
            order_items.append(order_item)

        if order_items:
            OrderItem.objects.bulk_create(order_items)

        return order
