import React, { useState, useEffect } from 'react';
import { fetchOrderDetail } from '../services/api';
import { OrderDetailResponse } from '../types/order';
import { OrderHeader } from '../components/OrderHeader';
import { SKUList } from '../components/SKUList';
import { TrackingCard } from '../components/TrackingCard';
import { SummaryCard } from '../components/SummaryCard';
import { Search, Loader2, AlertCircle, RefreshCw } from 'lucide-react';

export const OrderDetailsPage: React.FC = () => {
  const [selectedOrderNo, setSelectedOrderNo] = useState<string>('PO-20251130-00072');
  const [inputOrderNo, setInputOrderNo] = useState<string>('PO-20251130-00072');
  const [data, setData] = useState<OrderDetailResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = async (orderNo: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetchOrderDetail(orderNo);
      setData(response);
    } catch (err: any) {
      console.error('Failed to load order details:', err);
      setError(err.response?.data?.error || 'Failed to connect to backend server or fetch order details.');
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData(selectedOrderNo);
  }, [selectedOrderNo]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputOrderNo.trim()) {
      setSelectedOrderNo(inputOrderNo.trim());
    }
  };

  return (
    <div className="app-container">
      {/* Top Navbar & Header */}
      <header className="top-navbar">
        <div className="navbar-content">
          <div className="brand-logo">
            <span className="logo-icon">📦</span>
            <span className="brand-title">Order Details & Tracking System</span>
          </div>

          <form onSubmit={handleSearchSubmit} className="search-bar-form">
            <div className="search-input-wrapper">
              <Search size={18} className="search-icon" />
              <input
                type="text"
                placeholder="Enter Order No (e.g. PO-20251130-00072)..."
                value={inputOrderNo}
                onChange={(e) => setInputOrderNo(e.target.value)}
              />
            </div>
            <button type="submit" className="search-button">
              Search
            </button>
          </form>

          <div className="quick-switch-buttons">
            <button
              className={`preset-btn ${selectedOrderNo === 'PO-20251130-00072' ? 'active' : ''}`}
              onClick={() => {
                setSelectedOrderNo('PO-20251130-00072');
                setInputOrderNo('PO-20251130-00072');
              }}
            >
              Order 1
            </button>
            <button
              className={`preset-btn ${selectedOrderNo === 'PO-20251202-00046' ? 'active' : ''}`}
              onClick={() => {
                setSelectedOrderNo('PO-20251202-00046');
                setInputOrderNo('PO-20251202-00046');
              }}
            >
              Order 2
            </button>
          </div>
        </div>
      </header>

      {/* Main Content View */}
      <main className="main-content">
        {loading ? (
          <div className="state-card loading-state">
            <Loader2 className="spinner" size={40} />
            <p>Fetching order & logistics details from backend API...</p>
          </div>
        ) : error ? (
          <div className="state-card error-state">
            <AlertCircle size={40} color="#ef4444" />
            <h3>Unable to Load Order</h3>
            <p>{error}</p>
            <button className="retry-btn" onClick={() => loadData(selectedOrderNo)}>
              <RefreshCw size={16} /> Retry
            </button>
          </div>
        ) : data ? (
          <div className="dashboard-layout">
            {/* 1. Order Header Section */}
            <OrderHeader header={data.header} />

            {/* 2. SKU Product Table Section */}
            <SKUList items={data.items} />

            {/* Grid for Tracking and Summary Cards */}
            <div className="bottom-grid">
              {/* 3. Tracking Section */}
              <TrackingCard trackingList={data.tracking} />

              {/* 4. Summary Section */}
              <SummaryCard summary={data.summary} />
            </div>
          </div>
        ) : null}
      </main>
    </div>
  );
};
