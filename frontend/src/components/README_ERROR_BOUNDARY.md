# 🎯 Error Boundary Component

A React error boundary that provides user-friendly error handling and graceful degradation when errors occur in your application.

## Features

- ✅ **User-Friendly UI**: Professional, animated error page with clear messaging
- ✅ **Auto-Fallback**: Automatically switches to fallback UI after 300ms
- ✅ **Reload Button**: One-click reload button to recover from errors
- ✅ **Technical Details Toggle**: Hidden stack trace accessible for debugging
- ✅ **Dark Mode Support**: Adapts to system preference automatically
- ✅ **Accessibility**: ARIA labels and semantic HTML

## Usage

### Basic Usage

```tsx
// src/components/ErrorBoundary.tsx (copy if needed)
import { ErrorBoundary } from './ErrorBoundary';

function App() {
  return (
    <ErrorBoundary>
      <AppContent />
    </ErrorBoundary>
  );
}
```

### Wrap Main Application

Add to `src/main.tsx`:

```tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import '@fontsource/inter';
import './styles/typography.css';
import './styles/colors-vibe.css';
import ErrorBoundary from './components/ErrorBoundary';

// ... other imports

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);
root.render(
  <ErrorBoundary>
    <App />
  </ErrorBoundary>
);
```

### With Custom Fallback

```tsx
<ErrorBoundary fallback={<MyCustomFallback />} >
  <AppContent />
</ErrorBoundary>
```

## Anatomy of the Error Page

```
┌─────────────────────────────────────────┐
│            🎯 Something went wrong!      │
│         We encountered an unexpected     │
│          error. This should be...       │
│                                     ↻    │
│              Reload Application          │
│         ⟫Show technical details⟭        │
│                                         │
│  [Stack Trace for Debugging]             │
│                                         │
│      Please check your browser console   │
└─────────────────────────────────────────┘
```

## File Structure

```
src/components/
├── ErrorBoundary.tsx    # Main component and fallback UI
├── ErrorBoundary.css    # Styles for error state
└── README_ERROR_BOUNDARY.md  # Documentation
```

## Component Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | ReactNode | - | Your application content to protect |
| `fallback` | ReactNode | Defined UI | Optional custom fallback component |

## State Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `refreshApp()` | Promise\<void\> | Reloads the page |
| `reset()` | void | Clears error and reloads |

## Styling

The error boundary uses your app's color system:

- **Background**: `--surface-inverted-20` (off-white/light gray)
- **Title**: `--semantic-error-600` (red/pink)
- **Description**: `--text-on-darker-500` (muted text)
- **Reload Button**: `--semantic-success-500` (green)

## Best Practices

1. **Wrap Root Component**: Always wrap your main app in ErrorBoundary
2. **Keep It High-Level**: Don't use for individual components - let React handle component-level errors
3. **Log Errors**: Already logs to console automatically via componentDidCatch
4. **Custom Fallbacks**: For production, consider custom error tracking (Sentry, etc.)

## Testing the Error Boundary

To verify it works:

```bash
# Run your dev server
npm run build          # or npm run preview

# Intentionally trigger an error by:
# 1. Breaking a component
# 2. Accessing undefined properties
# 3. Using invalid async code
```

## Future Enhancements

- Integration with error tracking services (Sentry, LogRocket)
- Custom error reporting dialogs
- Analytics integration
- Offline fallback handling