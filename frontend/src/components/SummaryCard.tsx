import React from 'react';
import { OrderSummary } from '../types/order';
import { Calculator, DollarSign, Truck, Info } from 'lucide-react';

interface SummaryCardProps {
  summary: OrderSummary;
}

export const SummaryCard: React.FC<SummaryCardProps> = ({ summary }) => {
  const details = summary.shipment_details;

  return (
    <div className="card summary-card">
      <div className="section-title-bar">
        <div className="section-icon summary-icon-bg">
          <Calculator size={20} />
        </div>
        <h2>Financial Summary</h2>
      </div>

      <div className="summary-rows">
        {/* 1. Subtotal */}
        <div className="summary-row">
          <span className="summary-label">Subtotal</span>
          <span className="summary-value font-mono">${summary.subtotal.toFixed(2)}</span>
        </div>

        {/* 2. GST */}
        <div className="summary-row">
          <span className="summary-label">GST (10% of Subtotal)</span>
          <span className="summary-value font-mono">${summary.gst.toFixed(2)}</span>
        </div>

        {/* 3. Shipment Fee (Bonus Calculation Display) */}
        <div className="summary-row flex-column">
          <div className="fee-header-row">
            <span className="summary-label fee-label">
              <Truck size={14} color="#38bdf8" />
              <span>Shipment Fee (Bonus Estimate)</span>
            </span>
            <span className="summary-value font-mono fee-value">
              ${summary.shipment_fee.toFixed(2)}
            </span>
          </div>

          {details && (
            <div className="shipment-badge-details">
              <span>
                <Info size={12} className="info-icon-inline" />
                Weight: {details.chargeable_weight_kg} kg ({details.zone_name})
              </span>
              <span>Postcode {details.origin_postcode} to {details.destination_postcode}</span>
            </div>
          )}
        </div>

        <hr className="divider" />

        {/* 4. Total Amount */}
        <div className="summary-row total-row">
          <div className="total-label-group">
            <DollarSign size={20} className="total-icon" />
            <span className="total-label">Total Amount</span>
          </div>
          <span className="total-value font-mono">${summary.total.toFixed(2)}</span>
        </div>
      </div>
    </div>
  );
};
