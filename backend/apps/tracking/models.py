from django.db import models

class Tracking(models.Model):
    """
    物流追踪记录模型 (Logistics Tracking Record)
    来源：需求文档 Section 3 "Tracking Information" 及 API 返回数据
    作用：记录运单号、对应的物流服务商、最新追踪状态及最新更新时间。
    """
    # 运单号 (例如: 2FWZ50008569, 305506914)
    tracking_no = models.CharField(
        max_length=64,
        primary_key=True,
        verbose_name="追踪单号",
        help_text="来源: Section 3 Tracking Information 表格中的 Tracking No"
    )
    
    # 物流公司 (例如: StarTrack/Auspost, TNT)
    logistics_company = models.CharField(
        max_length=64,
        verbose_name="物流公司",
        help_text="来源: Section 3 Tracking Information 表格中的 Logistics Company"
    )
    
    # 当前物流状态 (例如: In Transit, Delivered, Processing)
    status = models.CharField(
        max_length=64,
        blank=True,
        default="Pending",
        verbose_name="物流状态",
        help_text="来源: 物流 API 返回的 current status 字段"
    )
    
    # 物流状态最后更新时间
    last_update = models.DateTimeField(
        auto_now=True,
        verbose_name="最后更新时间",
        help_text="来源: 物流 API 返回的 last update 字段"
    )

    class Meta:
        verbose_name = "物流追踪"
        verbose_name_plural = "物流追踪列表"

    def __str__(self):
        return f"{self.logistics_company} ({self.tracking_no}) - Status: {self.status}"
