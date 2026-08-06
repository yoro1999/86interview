# 系统三大增强计划书 (ENHANCEMENT_PLAN.md)

## 1. 当前实现与题目要求对比分析

### 1.1 符合题目的部分 (Satisfied Requirements)
* ✅ **文件解析与匹配 (Section 5.1.a/b)**：`order_parser.py` 与 `sku_parser.py` 支持解析订单与 SKU 数据。
* ✅ **精确费用计算 (Section 2 & 5.1.c)**：`calculation_service.py` 严格实现 Line Total、Subtotal、GST 10% 与 Total。
* ✅ **物流 API Integration (Section 3 & 5.1.d)**：`auspost_client.py` (StarTrack/AusPost) 与 `tnt_client.py` (TNT) 封装 HTTP Client，凭证从环境变量读取。
* ✅ **结果可视输出 (Section 5.2)**：UI 包含 Order Summary、SKU Details Table、Tracking Information 和 Financial Summary。
* ✅ **单向 Processing Pipeline 架构 (Section 5)**：架构严格遵循上传/输入 -> 解析 -> 匹配 -> 计算 -> Tracking -> Result Payload。

### 1.2 当前缺失/待增强的部分 (Gaps to Address)
1. 前端缺少 **`Manual Input` (手动表单录入) 模式** 选项（包含 Order Header 表单、动态增加/删除 SKU 行与 Tracking 映射）。
2. 物流 Client 请求 Adapter 结构与 Mock 回退的日志反馈与结构对齐需显式增强。
3. SKU 匹配逻辑需明确声明 `Local SKU File` 优先、`SQL Website/API` (https://tinyurl.com/2zp5p54a) 兜底的双层策略链。

---

## 2. 修改计划

### 增强 1: Input Mode 选择 (`Upload Files` vs `Manual Input`)
* **Frontend (`UploadSection.tsx`)**:
  * 增加 Tab 选择：`Upload Files` (文件上传) 与 `Manual Input` (手动表单)。
  * `Manual Input` 模式下提供 Order Header 表单输入、动态 SKU 列表项新增/删除按钮、Tracking 单号及 Carrier 映射。
  * 提交时将其转换为与上传文件完全一致的 JSON 数据结构，发送至后端的同一个 Pipeline 接口 (`POST /api/orders/process/`)。

### 增强 2: 检查 Tracking API Integration
* **Backend (`auspost_client.py`, `tnt_client.py`, `tracking_service.py`)**:
  * 确保发起真实的 HTTP GET 请求。
  * 当测试床网络或 endpoint 返回非 200 时，保留 Client Adapter 结构，记录 warning 并回退返回规范字段，保证主流程不中断。

### 增强 3: 多源 SKU 查找策略 (Local SKU File + SQL Provider)
* **Backend (`sku_matcher.py` & `sku_service.py`)**:
  * Level 1：优先匹配 Local SKU File 中的名称、单价 (RRP)、描述与尺寸。
  * Level 2：若 File 中缺失，自动触发调用 SQL Product Client (`https://tinyurl.com/2zp5p54a`) 补全。
