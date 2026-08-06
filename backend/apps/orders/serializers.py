from rest_framework import serializers
from apps.orders.models import Order, OrderItem
from apps.tracking.models import Tracking
from apps.products.models import SKU

class TrackingSerializer(serializers.ModelSerializer):
    """
    物流追踪 Serializer
    对应返回: tracking_no, logistics_company, status, last_update
    """
    class Meta:
        model = Tracking
        fields = ['tracking_no', 'logistics_company', 'status', 'last_update']


class OrderItemDetailSerializer(serializers.Serializer):
    """
    订单项明细 Serializer (包含 SKU 详细信息与计算出来的行总价)
    """
    sku_code = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField(allow_blank=True, allow_null=True)
    quantity = serializers.IntegerField()
    unit_price = serializers.FloatField()
    line_total = serializers.FloatField()
    image_url = serializers.URLField(allow_blank=True, allow_null=True)
    tracking_no = serializers.CharField(allow_blank=True, allow_null=True)


class SummarySerializer(serializers.Serializer):
    """
    费用 Summary Serializer
    """
    subtotal = serializers.FloatField()
    gst = serializers.FloatField()
    shipment_fee = serializers.FloatField()
    total = serializers.FloatField()


class OrderHeaderSerializer(serializers.ModelSerializer):
    """
    订单 Header Serializer
    对应返回: order_no, order_date, status, company_name, customer_name, phone, email, address
    """
    phone = serializers.CharField(source='phone_number')

    class Meta:
        model = Order
        fields = [
            'order_no',
            'order_date',
            'status',
            'company_name',
            'customer_name',
            'phone',
            'email',
            'address'
        ]


class OrderDetailResponseSerializer(serializers.Serializer):
    """
    订单详情完整响应 Serializer
    封装 Header、SKU Items 列表、Tracking 列表及 Summary
    """
    header = OrderHeaderSerializer(source='*')
    items = OrderItemDetailSerializer(many=True)
    tracking = TrackingSerializer(many=True)
    summary = SummarySerializer()
