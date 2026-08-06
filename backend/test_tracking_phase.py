import os
import sys
import django

# Setup Django Environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.tracking.models import Tracking
from services.tracking_service import TrackingService
from integrations.logistics.auspost_client import AusPostClient
from integrations.logistics.tnt_client import TNTClient

def test_tracking_service_flows():
    print("=" * 70)
    print("开始测试：Tracking API 集成与 TrackingService 归一化同步")
    print("=" * 70)

    # 0. 验证配置读取 (Environment Variable Check)
    print("\n[Step 0] 检查物流 API 凭证与环境变量读入...")
    auspost_client = AusPostClient()
    tnt_client = TNTClient()
    
    print(f"   AusPost/StarTrack API Key (Env): {auspost_client.api_key[:8]}... (Account: {auspost_client.account_no})")
    print(f"   TNT Username (Env):               {tnt_client.username} (Account: {tnt_client.account_no})")

    tracking_service = TrackingService()

    # 1. 测试 StarTrack/AusPost 追踪流程 (Track 1 & Track 2)
    print("\n[Step 1] 测试 StarTrack/AusPost 追踪流程 (Track 1: 2FWZ50008569)...")
    track1_result = tracking_service.sync_tracking_info("2FWZ50008569", "StarTrack/Auspost")
    
    print("   StarTrack/AusPost 统一格式返回:")
    print(f"   - 单号 (tracking_no):       {track1_result['tracking_no']}")
    print(f"   - 物流商 (logistics_company): {track1_result['logistics_company']}")
    print(f"   - 状态 (status):           {track1_result['status']}")
    print(f"   - 更新时间 (last_update):    {track1_result['last_update']}")

    # 验证数据库记录
    db_track1 = Tracking.objects.get(tracking_no="2FWZ50008569")
    print(f"✅ 成功写入数据库 Tracking 表: {db_track1}")
    assert db_track1.logistics_company == "StarTrack/Auspost"

    # 2. 测试 TNT 追踪流程 (Track 3)
    print("\n[Step 2] 测试 TNT 追踪流程 (Track 3: 305506914)...")
    track3_result = tracking_service.sync_tracking_info("305506914", "TNT")

    print("   TNT 统一格式返回:")
    print(f"   - 单号 (tracking_no):       {track3_result['tracking_no']}")
    print(f"   - 物流商 (logistics_company): {track3_result['logistics_company']}")
    print(f"   - 状态 (status):           {track3_result['status']}")
    print(f"   - 更新时间 (last_update):    {track3_result['last_update']}")

    # 验证数据库记录
    db_track3 = Tracking.objects.get(tracking_no="305506914")
    print(f"✅ 成功写入数据库 Tracking 表: {db_track3}")
    assert db_track3.logistics_company == "TNT"

    print("\n" + "=" * 70)
    print("🎉 StarTrack/AusPost 与 TNT 物流追踪流程与归一化测试全部通过！")
    print("=" * 70)

if __name__ == '__main__':
    test_tracking_service_flows()
