import React from 'react';
import { StatusChecks } from '../types/order';
import { CheckCircle2, Circle, Loader2 } from 'lucide-react';

interface ProcessingStatusProps {
  statusChecks?: StatusChecks;
  isProcessing: boolean;
}

export const ProcessingStatus: React.FC<ProcessingStatusProps> = ({ statusChecks, isProcessing }) => {
  const steps = [
    { key: 'order_file_loaded', label: 'Order file loaded & parsed' },
    { key: 'sku_data_matched', label: 'SKU data matched & enriched' },
    { key: 'price_calculated', label: 'Price & tax calculated' },
    { key: 'tracking_api_completed', label: 'Tracking API status synchronized' },
  ];

  return (
    <div className="card status-stepper-card">
      <div className="status-stepper-header">
        <h3 className="stepper-title">Processing Status Pipeline</h3>
        {isProcessing && (
          <span className="processing-badge">
            <Loader2 size={14} className="spinner" /> Processing
          </span>
        )}
      </div>

      <div className="stepper-grid">
        {steps.map((step) => {
          const isDone = isProcessing || (statusChecks && (statusChecks as any)[step.key]);
          return (
            <div key={step.key} className={`step-item ${isDone ? 'done' : ''}`}>
              <div className="step-icon">
                {isDone ? (
                  <CheckCircle2 size={20} color="#10b981" />
                ) : (
                  <Circle size={20} color="#64748b" />
                )}
              </div>
              <span className="step-label">{step.label}</span>
              <span className="check-mark">{isDone ? '✓' : ''}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
