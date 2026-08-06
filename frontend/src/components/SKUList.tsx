import React from 'react';
import { SKUItem } from '../types/order';
import { Package, Truck } from 'lucide-react';

interface SKUListProps {
  items: SKUItem[];
}

export const SKUList: React.FC<SKUListProps> = ({ items }) => {
  const getSvgPlaceholder = (skuCode: string) => {
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="150" height="150" viewBox="0 0 150 150"><rect width="150" height="150" fill="%236366f1"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="white" font-size="16" font-family="sans-serif">${skuCode}</text></svg>`;
    return `data:image/svg+xml;utf8,${svg}`;
  };

  return (
    <div className="card sku-list-card">
      <div className="section-title-bar">
        <div className="section-icon">
          <Package size={20} />
        </div>
        <h2>SKU Items & Product Line Details</h2>
        <span className="count-tag">{items.length} Lines</span>
      </div>

      <div className="table-responsive">
        <table className="sku-table">
          <thead>
            <tr>
              <th>Image</th>
              <th>SKU Code</th>
              <th>Name & Description</th>
              <th className="text-center">Quantity</th>
              <th className="text-right">Price per Unit</th>
              <th className="text-right">Line Total</th>
              <th className="text-center">Tracking No</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => {
              const srcUrl = item.image_url && !item.image_url.includes('placeholder.com')
                ? item.image_url
                : getSvgPlaceholder(item.sku_code);

              return (
                <tr key={item.sku_code}>
                  <td className="image-cell">
                    <div className="product-image-box">
                      <img
                        src={srcUrl}
                        alt={item.name}
                        onError={(e) => {
                          (e.target as HTMLImageElement).src = getSvgPlaceholder(item.sku_code);
                        }}
                      />
                    </div>
                  </td>
                  <td>
                    <span className="sku-code-pill">{item.sku_code}</span>
                  </td>
                  <td className="desc-cell">
                    <div className="product-name">{item.name}</div>
                    <div className="product-desc">{item.description || 'Standard product specification'}</div>
                  </td>
                  <td className="text-center font-bold">
                    <span className="qty-badge">{item.quantity}</span>
                  </td>
                  <td className="text-right font-mono">
                    ${item.unit_price.toFixed(2)}
                  </td>
                  <td className="text-right font-mono line-total">
                    ${item.line_total.toFixed(2)}
                  </td>
                  <td className="text-center">
                    <span className="tracking-pill">
                      <Truck size={14} />
                      {item.tracking_no || 'Unassigned'}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
