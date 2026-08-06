import axios from 'axios';
import { OrderDetailResponse } from '../types/order';

const API_BASE_URL = '/api/orders';

export const fetchOrderDetail = async (orderNo: string): Promise<OrderDetailResponse> => {
  const cleanOrderNo = orderNo.trim().toUpperCase();
  const response = await axios.get<OrderDetailResponse>(`${API_BASE_URL}/${cleanOrderNo}/`);
  return response.data;
};

export const processOrderFiles = async (
  orderFile?: File | null,
  skuFile?: File | null,
  orderNoFallback?: string,
  manualOrderPayload?: any,
  orderJsonText?: string,
  skuJsonText?: string
): Promise<OrderDetailResponse> => {
  const formData = new FormData();

  if (orderJsonText && orderJsonText.trim()) {
    formData.append('order_json_text', orderJsonText.trim());
    if (skuJsonText && skuJsonText.trim()) {
      formData.append('sku_json_text', skuJsonText.trim());
    }
  } else if (manualOrderPayload) {
    formData.append('order_file', new Blob([JSON.stringify(manualOrderPayload)], { type: 'application/json' }), 'manual_order.json');
  } else {
    if (orderFile) {
      formData.append('order_file', orderFile);
    }
    if (skuFile) {
      formData.append('sku_file', skuFile);
    }
    if (!orderFile && !skuFile && orderNoFallback) {
      formData.append('order_no', orderNoFallback);
    }
  }

  const response = await axios.post<OrderDetailResponse>(`${API_BASE_URL}/process/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};
