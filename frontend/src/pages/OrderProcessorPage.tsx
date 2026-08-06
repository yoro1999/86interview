import React, { useState } from 'react';
import { processOrderFiles } from '../services/api';
import { OrderDetailResponse } from '../types/order';
import { UploadSection } from '../components/UploadSection';
import { ProcessingStatus } from '../components/ProcessingStatus';
import { OrderHeader } from '../components/OrderHeader';
import { SKUList } from '../components/SKUList';
import { TrackingCard } from '../components/TrackingCard';
import { SummaryCard } from '../components/SummaryCard';
import { Loader2, AlertCircle, RefreshCw, Cpu, Inbox, Download } from 'lucide-react';

export const OrderProcessorPage: React.FC = () => {
  const [data, setData] = useState<OrderDetailResponse | null>(null);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleProcessOrder = async (
    orderFile: File | null,
    skuFile: File | null,
    presetOrderNo?: string,
    manualPayload?: any,
    orderJsonText?: string,
    skuJsonText?: string
  ) => {
    setIsProcessing(true);
    setError(null);
    try {
      const response = await processOrderFiles(
        orderFile,
        skuFile,
        presetOrderNo,
        manualPayload,
        orderJsonText,
        skuJsonText
      );
      setData(response);
    } catch (err: any) {
      console.error('Order processing failed:', err);
      setError(err.response?.data?.error || 'Failed to process order input or connect to server.');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleExportJson = () => {
    if (!data) return;
    const jsonString = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `order_result_${data.header.order_no || 'payload'}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="app-container">
      {/* Top Bar */}
      <header className="top-navbar">
        <div className="navbar-content">
          <div className="brand-logo">
            <Cpu size={24} color="#2563eb" />
            <span className="brand-title">Order Processing Console</span>
            <span className="workflow-badge">Automated Pipeline</span>
          </div>
        </div>
      </header>

      {/* Main Content Layout */}
      <main className="main-content">
        <div className="dashboard-layout">
          {/* 1. Upload & Input Configuration Section */}
          <UploadSection onProcess={handleProcessOrder} isProcessing={isProcessing} />

          {/* 2. Processing Status Stepper */}
          <ProcessingStatus statusChecks={data?.status_checks} isProcessing={isProcessing} />

          {/* Error State Notice */}
          {error && (
            <div className="state-card error-state">
              <AlertCircle size={36} color="#ef4444" />
              <h3>Processing Error</h3>
              <p>{error}</p>
              <button
                className="retry-btn"
                onClick={() => handleProcessOrder(null, null, 'PO-20251130-00072')}
              >
                <RefreshCw size={14} /> Retry Processing
              </button>
            </div>
          )}

          {/* 3. Result Section / Empty State */}
          {isProcessing ? (
            <div className="state-card loading-state">
              <Loader2 className="spinner" size={40} />
              <h3 style={{ fontSize: '1.05rem', fontWeight: 700 }}>Processing Pipeline Active...</h3>
              <p>Executing Order Parsing, SKU Data Matching (SQL Provider & Local), Tax & Line Total Calculation, and Logistics API Synchronization.</p>
            </div>
          ) : data ? (
            <div className="result-section-group">
              <div className="result-section-title" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span className="bullet-point"></span>
                  <h2>Processing Result Output</h2>
                </div>

                {/* Small Export JSON Result Button */}
                <button
                  type="button"
                  className="export-json-btn"
                  onClick={handleExportJson}
                  title="Export JSON Result File"
                >
                  <Download size={14} /> Export Result JSON
                </button>
              </div>

              {/* Order Header Summary */}
              <OrderHeader header={data.header} />

              {/* SKU Details Table */}
              <SKUList items={data.items} />

              {/* Bottom Grid: Tracking & Financial Summary */}
              <div className="bottom-grid">
                <TrackingCard trackingList={data.tracking} />
                <SummaryCard summary={data.summary} />
              </div>
            </div>
          ) : (
            /* Initial Empty State Card */
            <div className="state-card empty-state">
              <Inbox size={44} color="#94a3b8" />
              <h3 style={{ fontSize: '1.05rem', fontWeight: 700 }}>Ready to Process Order</h3>
              <p>
                No order data processed yet. Please choose <b>Upload Order Files</b>, <b>JSON Code Mode</b>, or <b>Manual Form Mode</b> above to execute the pipeline.
              </p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};
