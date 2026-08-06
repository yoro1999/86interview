import React from 'react';
import { TrackingInfo } from '../types/order';
import { Truck, Clock, ShieldCheck, Activity, CheckCircle2, MapPin } from 'lucide-react';

interface TrackingCardProps {
  trackingList: TrackingInfo[];
}

export const TrackingCard: React.FC<TrackingCardProps> = ({ trackingList }) => {
  return (
    <div className="card tracking-card">
      <div className="section-title-bar">
        <div className="section-icon tracking-icon-bg">
          <Truck size={20} />
        </div>
        <h2>Logistics & Multi-Event Tracking Progress</h2>
      </div>

      <div className="tracking-grid">
        {trackingList.map((track) => (
          <div key={track.tracking_no} className="tracking-item-card">
            {/* Header */}
            <div className="tracking-item-header">
              <div className="carrier-info">
                <ShieldCheck size={18} className="carrier-icon" />
                <span className="carrier-name">{track.logistics_company}</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span className="status-chip">{track.status}</span>
                <span
                  title={track.data_source === 'real_api' ? 'Live API Response' : 'Development Fallback Response'}
                  style={{
                    fontSize: '0.7rem',
                    padding: '2px 8px',
                    borderRadius: '10px',
                    background: track.data_source === 'real_api' ? 'rgba(16, 185, 129, 0.15)' : 'rgba(245, 158, 11, 0.15)',
                    color: track.data_source === 'real_api' ? '#10b981' : '#f59e0b',
                    border: `1px solid ${track.data_source === 'real_api' ? 'rgba(16, 185, 129, 0.3)' : 'rgba(245, 158, 11, 0.3)'}`
                  }}
                >
                  <Activity size={10} style={{ display: 'inline', marginRight: '4px' }} />
                  {track.data_source === 'real_api' ? 'Real API' : 'Dev Fallback'}
                </span>
              </div>
            </div>

            {/* Tracking Number */}
            <div className="tracking-number-box">
              <span className="tn-label">Tracking Number</span>
              <div className="tn-value">{track.tracking_no}</div>
            </div>

            {/* Multi-Event Timeline Progress */}
            {track.events && track.events.length > 0 && (
              <div className="tracking-timeline-container">
                <div className="timeline-title">Shipment Progress Timeline</div>
                <div className="timeline-list">
                  {track.events.map((ev, idx) => (
                    <div key={idx} className={`timeline-event-item ${ev.completed ? 'completed' : 'pending'}`}>
                      <div className="timeline-node">
                        <CheckCircle2 size={16} />
                      </div>
                      <div className="timeline-content">
                        <div className="event-status">{ev.status}</div>
                        <div className="event-details">
                          <MapPin size={12} /> <span>{ev.location}</span>
                          {ev.timestamp && <span className="event-time">• {ev.timestamp}</span>}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Footer */}
            <div className="tracking-item-footer">
              <Clock size={14} />
              <span>Last Update: {new Date(track.last_update).toLocaleString()}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
