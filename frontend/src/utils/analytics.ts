declare global {
  interface Window {
    gtag: (
      command: 'config' | 'event',
      targetId: string,
      params?: { [key: string]: any }
    ) => void;
  }
}

export const GA_TRACKING_ID = 'G-Q259WQ17SR';

const hasConsent = () => {
  return localStorage.getItem('cookie-consent') === 'accepted';
};

// Log page views
export const pageview = (url: string) => {
  if (!hasConsent()) return;
  
  window.gtag('config', GA_TRACKING_ID, {
    page_path: url,
    cookie_flags: 'max-age=7200;secure;samesite=none'
  });
};

// Log specific events
export const event = ({ action, category, label, value }: {
  action: string;
  category: string;
  label: string;
  value?: number;
}) => {
  if (!hasConsent()) return;

  window.gtag('event', action, {
    event_category: category,
    event_label: label,
    value: value,
    cookie_flags: 'max-age=7200;secure;samesite=none'
  });
}; 