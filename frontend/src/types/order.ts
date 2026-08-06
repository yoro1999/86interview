export interface OrderHeader {
  order_no: string;
  order_date: string;
  status: string;
  company_name: string;
  customer_name: string;
  phone: string;
  email: string;
  address: string;
}

export interface SKUItem {
  sku_code: string;
  name: string;
  description: string;
  quantity: number;
  unit_price: number;
  line_total: number;
  weight?: number;
  width?: number;
  length?: number;
  height?: number;
  volume?: number;
  image_url: string | null;
  tracking_no: string;
  data_source?: string;
}

export interface TrackingEvent {
  status: string;
  location: string;
  timestamp: string;
  completed: boolean;
}

export interface TrackingInfo {
  tracking_no: string;
  logistics_company: string;
  status: string;
  last_update: string;
  data_source?: string;
  events?: TrackingEvent[];
}

export interface ShipmentDetails {
  origin_postcode: string;
  destination_postcode: string;
  chargeable_weight_kg: number;
  gross_weight_kg: number;
  volumetric_weight_kg: number;
  zone_name: string;
}

export interface OrderSummary {
  subtotal: number;
  gst: number;
  shipment_fee: number;
  total: number;
  shipment_details?: ShipmentDetails;
}

export interface StatusChecks {
  order_file_loaded: boolean;
  sku_data_matched: boolean;
  price_calculated: boolean;
  tracking_api_completed: boolean;
}

export interface OrderDetailResponse {
  header: OrderHeader;
  items: SKUItem[];
  tracking: TrackingInfo[];
  summary: OrderSummary;
  status_checks?: StatusChecks;
}
