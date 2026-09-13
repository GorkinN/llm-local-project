import React, { Component, ErrorInfo, ReactNode } from 'react';
import './ErrorBoundary.css';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: string | null;
  errorComponent: ReactNode | null;
}

/**
 * Custom Error Boundary Component
 * Displays a user-friendly error page when errors occur in the component tree
 */
export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
    errorComponent: null,
  };

  // Public method to safely reload the application after an error
  async refreshApp(): Promise<void> {
    window.location.reload();
  }

  // Method to clear the current error and reload
  public reset(): void {
    this.setState({ hasError: false, error: null, errorComponent: null });
    setTimeout(() => {
      if (window) window.location.reload();
    }, 50);
  }

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error: error?.message || 'An unexpected error occurred', errorComponent: null };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    console.error('ErrorBoundary caught an error:', error.message);
    console.error('Error component stack:', errorInfo.componentStack);

    // Show fallback UI after a short delay
    setTimeout(() => {
      this.setState({ hasError: true, errorComponent: null });
    }, 300);
  }

  public render(): ReactNode {
    if (this.state.hasError) {
      return this.state.errorComponent || <FallbackUI error={this.state.error} refresh={this.refreshApp()} />;
    }

    // Render children when no error occurred
    const { children, fallback } = this.props;
    
    // If a custom fallback was provided and no error currently displayed, render it
    if (fallback !== undefined) {
      return <>{fallback}</>;
    }

    return <>{children}</>;
  }
}

/**
 * Fallback UI Component
 * Displays when an unhandled React error occurs in a component tree
 */
interface FallbackUIProps extends React.HTMLAttributes<HTMLDivElement> {
  error: string;
  refresh: () => void | Promise<void>;
}

const FallbackUI: React.FC<FallbackUIProps> = ({ error, refresh, style, ...props }) => {
  return (
    <div 
      className="error-boundary__fallback"
      role="alert"
      aria-label="Error occurred. This will be resolved shortly."
      style={{ ...style }}
      {...props}
    >
      <div className="error-boundary__container">
        {/* Error Icon */}
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          viewBox="0 0 24 24" 
          fill="none" 
          stroke="currentColor" 
          strokeWidth="1.5" 
          strokeLinecap="round" 
          strokeLinejoin="round"
          className="error-boundary__icon"
        >
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="12" />
          <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>

        {/* Error Message */}
        <div className="error-boundary__message">
          <h2 className="error-boundary__title">
            Something went wrong! 🎯
          </h2>
          <p className="error-boundary__description">
            We encountered an unexpected error. This should be resolved shortly.
          </p>
        </div>

        {/* Reload Button */}
        <button
          type="button"
          onClick={refresh}
          className="error-boundary__reload-btn"
          style={{ 
            cursor: 'pointer',
            outline: 'none'
          }}
          aria-label="Reload application to resolve error"
          title="Click to reload application"
        >
          ↻ Reload Application
        </button>

        {/* Technical Details Toggle */}
        {typeof window !== 'undefined' && (
          <details className="error-boundary__details">
            <summary 
              style={{ cursor: 'pointer', color: '#6b7280' }}
              type="button"
            >
              Show technical details
            </summary>
            <div className="error-boundary__technical-details">
              <pre
                className="error-boundary__error-output"
                aria-label="Technical error message and stack trace for debugging"
                style={{ 
                  whiteSpace: 'pre-wrap',
                  wordBreak: 'break-word'
                }}
              >
                {error && (error.message || '') + (error.stack ? '\n\n' + error.stack : '')}
              </pre>
            </div>
          </details>
        )}

        {/* Debug Info Footer */}
        <p className="error-boundary__footer">
          Please check your browser console for additional information.
        </p>
      </div>
    </div>
  );
};

export default ErrorBoundary;
