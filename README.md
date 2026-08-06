# Order Processing System

## Sample Test Files
- Order 1: sample_data/order_1.json (PO-20251130-00072)
- Order 2: sample_data/order_2.json (PO-20251202-00046)
- SKU Catalog: sample_data/sku_list.json (All 9 SKUs)

## a. How to Run Your Code

### Prerequisites
- Python 3.10+
- Node.js 18+

### 1. Start Backend
```bash
cd order-tracking-system
python3 -m venv backend/venv
source backend/venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r backend/requirements.txt
PYTHONPATH=backend USE_SQLITE=True python backend/manage.py migrate
PYTHONPATH=backend USE_SQLITE=True python backend/manage.py runserver 8000
```
Backend API runs at: http://localhost:8000/api/orders/process/

### 2. Start Frontend
```bash
cd order-tracking-system/frontend
npm install
npm run dev
```
Frontend runs at: http://localhost:3000/

### 3. Run Pipeline Tests
```bash
PYTHONPATH=backend USE_SQLITE=True python backend/test_pipeline_phase.py
```

## b. Dependencies

### Backend
- Django >= 5.0
- djangorestframework >= 3.14
- requests >= 2.31
- openpyxl >= 3.1
- pandas >= 2.0
- python-dotenv >= 1.0

### Frontend
- React 18
- TypeScript 5
- Vite 6
- lucide-react
- axios

## c. Assumptions Made

### 1. Shipping Calculation
- Origin Postcode: 2111 (Ryde, NSW).
- Destination Postcode: Extracted from delivery address using regex.
- Volumetric Weight: (Length x Width x Height / 5000) x Quantity.
- Gross Weight: Weight x Quantity.
- Chargeable Weight: max(Gross Weight, Volumetric Weight).
- Rate Matrix:
  - NSW/ACT (2xxx): Base $8.50 + $1.20/kg
  - VIC/QLD/SA (3xxx, 4xxx, 5xxx): Base $14.50 + $2.20/kg
  - WA/TAS/NT (6xxx, 7xxx, 0xxx): Base $22.00 + $3.50/kg

### 2. SKU Lookup Strategy
- Primary: SQL Website/API endpoint (https://tinyurl.com/2zp5p54a / product_list).
- Fallback: Local SKU catalog file (sample_data/sku_list.json).
- Image Fallback: Inline SVG Data URIs when external URL is unreachable.

### 3. Logistics Tracking API
- StarTrack / AusPost API: Key 8ba91b84-ca46-40e6-9680-77e55e3c5942, Account 04456017.
- TNT API: Username CIT00000000000134449, Account 30023444.
- Tracking Timeline: Normalizes multi-event status updates with mock fallback support.
