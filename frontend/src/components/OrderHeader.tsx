import React from 'react';
import { OrderHeader as OrderHeaderType } from '../types/order';
import { Building2, User, Phone, Mail, MapPin } from 'lucide-react';

interface OrderHeaderProps {
  header: OrderHeaderType;
}

export const OrderHeader: React.FC<OrderHeaderProps> = ({ header }) => {
  return (
    <div className="card order-header-card">
      <div className="order-header-top">
        <div>
          <span className="order-label">Order Details</span>
          <h1 className="order-number">{header.order_no}</h1>
        </div>

        <div className="order-header-meta">
          <span className="info-badge">Date: {header.order_date}</span>
          <span className="info-badge status">{header.status}</span>
        </div>
      </div>

      <hr className="divider" />

      <div className="order-header-grid">
        <div className="info-group">
          <div className="info-icon">
            <Building2 size={18} />
          </div>
          <div>
            <label>Company Name</label>
            <div className="primary-text">{header.company_name}</div>
          </div>
        </div>

        <div className="info-group">
          <div className="info-icon">
            <User size={18} />
          </div>
          <div>
            <label>Customer Name</label>
            <div className="primary-text">{header.customer_name}</div>
          </div>
        </div>

        <div className="info-group">
          <div className="info-icon">
            <Phone size={18} />
          </div>
          <div>
            <label>Phone Number</label>
            <div className="primary-text">{header.phone}</div>
          </div>
        </div>

        <div className="info-group">
          <div className="info-icon">
            <Mail size={18} />
          </div>
          <div>
            <label>Email Address</label>
            <div className="primary-text">{header.email}</div>
          </div>
        </div>
      </div>

      <div className="address-section">
        <MapPin size={18} color="#818cf8" style={{ marginTop: '2px', flexShrink: 0 }} />
        <div>
          <label>Delivery Address</label>
          <div className="address-text">{header.address}</div>
        </div>
      </div>
    </div>
  );
};
