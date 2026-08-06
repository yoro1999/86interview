from django.db import models

class SKU(models.Model):
    """
    SKU (Stock-Keeping-Unit) 商品字典模型
    来源：需求文档 Section 2 "SKU Details & Calculations" 及 SQL 数据库
    作用：存储商品唯一编码、商品名称、详细描述、单价（含 GST）及商品图片 URL。
    """
    # SKU 唯一代码 (例如: TBAMET10)
    sku_code = models.CharField(
        max_length=32,
        primary_key=True,
        verbose_name="SKU 编号",
        help_text="来源: SKU Details & SQL 数据库中的 SKU 代码主键"
    )
    
    # 商品名称 / 简述 (例如: TB AMET 10mg)
    name = models.CharField(
        max_length=128,
        verbose_name="商品名称",
        help_text="来源: Final Output 要求中的 Name 字段"
    )
    
    # 商品详细描述
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="商品描述",
        help_text="来源: Final Output 要求中的 Description 字段"
    )
    
    # 商品单价 (含 GST，例如: 49.00)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="商品单价",
        help_text="来源: Final Output 要求中的 Price per unit (Note: 价格已包含 GST)"
    )
    
    # 商品图片 URL / 占位图
    image_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="商品图片链接",
        help_text="来源: Section 2 Images for SKUs (真实图片 URL 或占位图 URL)"
    )

    class Meta:
        verbose_name = "SKU 商品"
        verbose_name_plural = "SKU 商品列表"

    def __str__(self):
        return f"{self.sku_code} - {self.name} (${self.price})"
