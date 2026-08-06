from django.db import models

class Order(models.Model):
    """
    订单主表模型 (Order Header)
    来源：需求文档 Section 1 "Order Details"
    作用：存储订单编号、日期、状态及客户基本联系信息与送货地址。
    """
    # 订单号：唯一标识符 (例如: PO-20251130-00072)
    order_no = models.CharField(
        max_length=64,
        primary_key=True,
        verbose_name="订单编号",
        help_text="来源: Order Details 表格中的 Order No 字段"
    )
    
    # 订单日期 (例如: 30/11/25)
    order_date = models.DateField(
        verbose_name="订单日期",
        help_text="来源: Order Details 表格中的 Order Date 字段"
    )
    
    # 订单状态 (例如: Completed, In Transit)
    status = models.CharField(
        max_length=32,
        verbose_name="订单状态",
        help_text="来源: Order Details 表格中的 Status 字段"
    )
    
    # 订购公司名称 (例如: V22 Dispensary)
    company_name = models.CharField(
        max_length=128,
        verbose_name="公司名称",
        help_text="来源: Order Details 表格中的 Company Name 字段"
    )
    
    # 客户姓名 (例如: Jason Hu)
    customer_name = models.CharField(
        max_length=128,
        verbose_name="客户姓名",
        help_text="来源: Order Details 表格中的 Customer Name 字段"
    )
    
    # 客户联系电话 (例如: 0481 735 488)
    phone_number = models.CharField(
        max_length=32,
        verbose_name="联系电话",
        help_text="来源: Order Details 表格中的 Phone Number 字段"
    )
    
    # 客户电子邮箱 (例如: Jason@aerishealth.au)
    email = models.EmailField(
        verbose_name="电子邮箱",
        help_text="来源: Order Details 表格中的 Email 字段"
    )
    
    # 送货地址 (例如: 125 Toorak Road, South Yarra VIC 3141)
    address = models.TextField(
        verbose_name="配送地址",
        help_text="来源: Order Details 表格中的 Address 字段"
    )

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = "订单列表"

    def __str__(self):
        return f"Order {self.order_no} ({self.customer_name})"


class OrderItem(models.Model):
    """
    订单商品明细模型 (Order Item Line)
    来源：需求文档 Section 2 "SKU Details & Calculations"
    作用：关联订单主表，存储包含的 SKU 编码、购买数量及分配的包裹 Tracking 编号。
    """
    # 关联订单
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="所属订单",
        help_text="来源: SKU Details 表格中的 Order # 外键关联"
    )
    
    # SKU 代码 (例如: TBAMET10)
    sku_code = models.CharField(
        max_length=32,
        verbose_name="SKU 编码",
        help_text="来源: SKU Details 表格中的 SKU 字段"
    )
    
    # 购买数量 QTY (例如: 3)
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="购买数量",
        help_text="来源: SKU Details 表格中的 QTY 字段"
    )
    
    # 分配的包裹 Tracking 编号/名称 (例如: Track 1, Track 2, Track 3)
    tracking_no = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name="物流追踪单号/标识",
        help_text="来源: SKU Details 表格中的 Assigned Tracking 字段"
    )

    class Meta:
        verbose_name = "订单项"
        verbose_name_plural = "订单项列表"

    def __str__(self):
        return f"{self.order.order_no} - {self.sku_code} (x{self.quantity})"
