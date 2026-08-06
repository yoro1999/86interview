import React, { useState } from 'react';
import { Upload, FileText, Package, Key, Play, Edit3, Code, Trash2 } from 'lucide-react';

interface ManualSKUItem {
  sku_code: string;
  quantity: number;
  assigned_tracking: string;
}

interface UploadSectionProps {
  onProcess: (
    orderFile: File | null,
    skuFile: File | null,
    presetOrderNo?: string,
    manualPayload?: any,
    orderJsonText?: string,
    skuJsonText?: string
  ) => void;
  isProcessing: boolean;
}

export const UploadSection: React.FC<UploadSectionProps> = ({ onProcess, isProcessing }) => {
  const [inputMode, setInputMode] = useState<'upload' | 'code' | 'manual'>('upload');

  // File upload state
  const [orderFile, setOrderFile] = useState<File | null>(null);
  const [skuFile, setSkuFile] = useState<File | null>(null);
  const [showConfig, setShowConfig] = useState<boolean>(false);

  // JSON Code text state
  const [orderJsonText, setOrderJsonText] = useState<string>(
    JSON.stringify(
      {
        order_no: "PO-20251130-00072",
        order_date: "2025-11-30",
        status: "Completed",
        company_name: "V22 Dispensary",
        customer_name: "Jason Hu",
        phone: "0481 735 488",
        email: "Jason@aerishealth.au",
        address: "125 Toorak Road, South Yarra VIC 3141",
        items: [
          { sku_code: "TBAMET10", quantity: 3, assigned_tracking: "Track 1" },
          { sku_code: "TBAMET28", quantity: 1, assigned_tracking: "Track 1" },
          { sku_code: "TBOPAL28", quantity: 1, assigned_tracking: "Track 1" }
        ]
      },
      null,
      2
    )
  );

  const [skuJsonText, setSkuJsonText] = useState<string>('');

  // Manual Form State
  const [manualHeader, setManualHeader] = useState({
    order_no: 'PO-20251130-00072',
    order_date: '2025-11-30',
    status: 'Completed',
    company_name: 'V22 Dispensary',
    customer_name: 'Jason Hu',
    phone: '0481 735 488',
    email: 'Jason@aerishealth.au',
    address: '125 Toorak Road, South Yarra VIC 3141'
  });

  const [manualItems, setManualItems] = useState<ManualSKUItem[]>([
    { sku_code: 'TBAMET10', quantity: 3, assigned_tracking: 'Track 1' },
    { sku_code: 'TBAMET28', quantity: 1, assigned_tracking: 'Track 1' },
    { sku_code: 'TBOPAL28', quantity: 1, assigned_tracking: 'Track 1' }
  ]);

  // Credentials inputs
  const [auspostKey, setAuspostKey] = useState<string>('8ba91b84-ca46-40e6-9680-77e55e3c5942');
  const [tntUsername, setTntUsername] = useState<string>('CIT00000000000134449');

  const handleOrderFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setOrderFile(e.target.files[0]);
    }
  };

  const handleSkuFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSkuFile(e.target.files[0]);
    }
  };

  const handleAddManualItem = () => {
    setManualItems([...manualItems, { sku_code: '', quantity: 1, assigned_tracking: 'Track 1' }]);
  };

  const handleRemoveManualItem = (index: number) => {
    const updated = [...manualItems];
    updated.splice(index, 1);
    setManualItems(updated);
  };

  const handleManualItemChange = (index: number, field: keyof ManualSKUItem, value: any) => {
    const updated = [...manualItems];
    updated[index] = { ...updated[index], [field]: value };
    setManualItems(updated);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputMode === 'upload') {
      onProcess(orderFile, skuFile);
    } else if (inputMode === 'code') {
      onProcess(null, null, undefined, undefined, orderJsonText, skuJsonText);
    } else {
      const payload = {
        ...manualHeader,
        items: manualItems
      };
      onProcess(null, skuFile, undefined, payload);
    }
  };

  return (
    <div className="card upload-section-card">
      <div className="upload-header">
        <div>
          <h2 className="upload-title">Order Processing Console</h2>
          <p className="upload-subtitle">
            Upload Order/SKU files, paste raw JSON text, or fill manual order details to execute the automated processing pipeline.
          </p>
        </div>
      </div>

      {/* Input Mode Selector Tabs */}
      <div className="input-mode-tabs">
        <button
          type="button"
          className={`mode-tab-btn ${inputMode === 'upload' ? 'active' : ''}`}
          onClick={() => setInputMode('upload')}
        >
          <Upload size={14} /> Upload Order Files
        </button>
        <button
          type="button"
          className={`mode-tab-btn ${inputMode === 'code' ? 'active' : ''}`}
          onClick={() => setInputMode('code')}
        >
          <Code size={14} /> JSON Code Mode
        </button>
        <button
          type="button"
          className={`mode-tab-btn ${inputMode === 'manual' ? 'active' : ''}`}
          onClick={() => setInputMode('manual')}
        >
          <Edit3 size={14} /> Manual Form Mode
        </button>
      </div>

      <form onSubmit={handleSubmit} className="upload-form">
        {inputMode === 'upload' ? (
          /* Mode 1: File Upload */
          <div className="upload-dropzone-grid">
            <div className="dropzone-card">
              <div className="dropzone-icon-box blue">
                <FileText size={22} />
              </div>
              <div className="dropzone-info">
                <h3 style={{ fontSize: '0.9rem', fontWeight: 600 }}>Order File Upload</h3>
                <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Supports .json, .xlsx, .csv order files</p>
              </div>
              <label className="file-input-label">
                <Upload size={14} />
                <span>{orderFile ? orderFile.name : 'Choose Order File'}</span>
                <input type="file" accept=".json,.csv,.xlsx" onChange={handleOrderFileChange} />
              </label>
            </div>

            <div className="dropzone-card">
              <div className="dropzone-icon-box purple">
                <Package size={22} />
              </div>
              <div className="dropzone-info">
                <h3 style={{ fontSize: '0.9rem', fontWeight: 600 }}>SKU File Upload (Optional)</h3>
                <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Supports .json, .xlsx, .csv catalog</p>
              </div>
              <label className="file-input-label purple" style={{ color: '#9333ea', borderColor: '#d8b4fe' }}>
                <Upload size={14} />
                <span>{skuFile ? skuFile.name : 'Choose SKU File'}</span>
                <input type="file" accept=".json,.csv,.xlsx" onChange={handleSkuFileChange} />
              </label>
            </div>
          </div>
        ) : inputMode === 'code' ? (
          /* Mode 2: Direct JSON Code Input */
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px', marginBottom: '16px' }}>
            <div>
              <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>
                Order JSON Text
              </label>
              <textarea
                rows={8}
                placeholder="Paste Order JSON code text..."
                value={orderJsonText}
                onChange={(e) => setOrderJsonText(e.target.value)}
                className="code-textarea"
              />
            </div>
            <div>
              <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>
                SKU Reference JSON Text (Optional)
              </label>
              <textarea
                rows={8}
                placeholder="Paste SKU JSON reference text..."
                value={skuJsonText}
                onChange={(e) => setSkuJsonText(e.target.value)}
                className="code-textarea"
              />
            </div>
          </div>
        ) : (
          /* Mode 3: Manual Form Input */
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginBottom: '16px' }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '12px' }}>
              <div>
                <label style={{ fontSize: '0.725rem', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '2px' }}>
                  Order Number
                </label>
                <input
                  type="text"
                  style={{ width: '100%', padding: '6px 10px', borderRadius: '6px', border: '1px solid var(--border-card)', background: '#f8fafc' }}
                  value={manualHeader.order_no}
                  onChange={(e) => setManualHeader({ ...manualHeader, order_no: e.target.value })}
                />
              </div>
              <div>
                <label style={{ fontSize: '0.725rem', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '2px' }}>
                  Order Date
                </label>
                <input
                  type="date"
                  style={{ width: '100%', padding: '6px 10px', borderRadius: '6px', border: '1px solid var(--border-card)', background: '#f8fafc' }}
                  value={manualHeader.order_date}
                  onChange={(e) => setManualHeader({ ...manualHeader, order_date: e.target.value })}
                />
              </div>
              <div>
                <label style={{ fontSize: '0.725rem', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '2px' }}>
                  Status
                </label>
                <input
                  type="text"
                  style={{ width: '100%', padding: '6px 10px', borderRadius: '6px', border: '1px solid var(--border-card)', background: '#f8fafc' }}
                  value={manualHeader.status}
                  onChange={(e) => setManualHeader({ ...manualHeader, status: e.target.value })}
                />
              </div>
              <div>
                <label style={{ fontSize: '0.725rem', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '2px' }}>
                  Company Name
                </label>
                <input
                  type="text"
                  style={{ width: '100%', padding: '6px 10px', borderRadius: '6px', border: '1px solid var(--border-card)', background: '#f8fafc' }}
                  value={manualHeader.company_name}
                  onChange={(e) => setManualHeader({ ...manualHeader, company_name: e.target.value })}
                />
              </div>
              <div>
                <label style={{ fontSize: '0.725rem', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '2px' }}>
                  Customer Name
                </label>
                <input
                  type="text"
                  style={{ width: '100%', padding: '6px 10px', borderRadius: '6px', border: '1px solid var(--border-card)', background: '#f8fafc' }}
                  value={manualHeader.customer_name}
                  onChange={(e) => setManualHeader({ ...manualHeader, customer_name: e.target.value })}
                />
              </div>
              <div style={{ gridColumn: '1 / -1' }}>
                <label style={{ fontSize: '0.725rem', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '2px' }}>
                  Delivery Address
                </label>
                <input
                  type="text"
                  style={{ width: '100%', padding: '6px 10px', borderRadius: '6px', border: '1px solid var(--border-card)', background: '#f8fafc' }}
                  value={manualHeader.address}
                  onChange={(e) => setManualHeader({ ...manualHeader, address: e.target.value })}
                />
              </div>
            </div>

            {/* Dynamic SKU Items list */}
            <div style={{ background: '#f8fafc', padding: '12px', borderRadius: '8px', border: '1px solid var(--border-card)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                <span style={{ fontSize: '0.85rem', fontWeight: 700 }}>SKU Line Items</span>
                <button
                  type="button"
                  style={{ background: '#ecfdf5', color: '#047857', border: '1px solid #a7f3d0', padding: '4px 10px', borderRadius: '6px', fontSize: '0.75rem', fontWeight: 600, cursor: 'pointer' }}
                  onClick={handleAddManualItem}
                >
                  + Add SKU Row
                </button>
              </div>

              {manualItems.map((item, idx) => (
                <div key={idx} style={{ display: 'flex', gap: '8px', marginBottom: '8px', alignItems: 'center' }}>
                  <input
                    type="text"
                    placeholder="SKU Code (e.g. TBAMET10)"
                    style={{ flex: 1, padding: '6px 8px', borderRadius: '4px', border: '1px solid #cbd5e1', fontSize: '0.8rem' }}
                    value={item.sku_code}
                    onChange={(e) => handleManualItemChange(idx, 'sku_code', e.target.value)}
                  />
                  <input
                    type="number"
                    min="1"
                    style={{ width: '70px', padding: '6px 8px', borderRadius: '4px', border: '1px solid #cbd5e1', fontSize: '0.8rem' }}
                    value={item.quantity}
                    onChange={(e) => handleManualItemChange(idx, 'quantity', parseInt(e.target.value) || 1)}
                  />
                  <input
                    type="text"
                    placeholder="Tracking (e.g. Track 1)"
                    style={{ flex: 1, padding: '6px 8px', borderRadius: '4px', border: '1px solid #cbd5e1', fontSize: '0.8rem' }}
                    value={item.assigned_tracking}
                    onChange={(e) => handleManualItemChange(idx, 'assigned_tracking', e.target.value)}
                  />
                  <button
                    type="button"
                    style={{ background: '#fef2f2', color: '#dc2626', border: '1px solid #fecaca', padding: '6px 8px', borderRadius: '4px', cursor: 'pointer' }}
                    onClick={() => handleRemoveManualItem(idx)}
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Tracking API Configuration Bar */}
        <div style={{ marginTop: '10px' }}>
          <button
            type="button"
            style={{ background: 'none', border: 'none', color: 'var(--text-secondary)', fontSize: '0.8rem', fontWeight: 600, cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: '6px' }}
            onClick={() => setShowConfig(!showConfig)}
          >
            <Key size={14} />
            <span>Tracking API Configuration Credentials</span>
          </button>
        </div>

        {showConfig && (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '12px', marginTop: '10px', background: '#f8fafc', padding: '12px', borderRadius: '8px', border: '1px solid var(--border-card)' }}>
            <div>
              <label style={{ fontSize: '0.7rem', color: 'var(--text-muted)', display: 'block', marginBottom: '2px' }}>StarTrack API Key</label>
              <input
                type="text"
                style={{ width: '100%', padding: '6px 8px', borderRadius: '4px', border: '1px solid #cbd5e1', fontSize: '0.8rem' }}
                value={auspostKey}
                onChange={(e) => setAuspostKey(e.target.value)}
              />
            </div>
            <div>
              <label style={{ fontSize: '0.7rem', color: 'var(--text-muted)', display: 'block', marginBottom: '2px' }}>TNT Username</label>
              <input
                type="text"
                style={{ width: '100%', padding: '6px 8px', borderRadius: '4px', border: '1px solid #cbd5e1', fontSize: '0.8rem' }}
                value={tntUsername}
                onChange={(e) => setTntUsername(e.target.value)}
              />
            </div>
          </div>
        )}

        {/* Primary Action Button */}
        <div style={{ marginTop: '16px', display: 'flex', justifyContent: 'flex-end' }}>
          <button type="submit" className="process-primary-btn" disabled={isProcessing}>
            <Play size={16} />
            <span>{isProcessing ? 'Processing Pipeline...' : 'Process Order'}</span>
          </button>
        </div>
      </form>
    </div>
  );
};
