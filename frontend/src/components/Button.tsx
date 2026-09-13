import React, { type ButtonHTMLAttributes } from 'react'
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

// Utility for merging Tailwind classes
function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  isLoading?: boolean
}

const variants = {
  primary: 'bg-primary-600 text-white hover:bg-primary-700 active:bg-primary-800',
  secondary: 'bg-secondary-600 text-white hover:bg-secondary-700 active:bg-secondary-800',
  outline: 'border-2 border-neutral-300 text-neutral-700 hover:border-neutral-400 hover:text-neutral-900',
  danger: 'bg-error-600 text-white hover:bg-error-700 active:bg-error-800',
}

const sizes = {
  sm: 'px-3 py-1.5 text-sm rounded-md',
  md: 'px-4 py-2 text-base rounded-lg shadow-card-sm',
  lg: 'px-6 py-3 text-lg rounded-xl shadow-card hover:shadow-card-lg',
}

export function Button({
  children,
  className,
  variant = 'primary',
  size = 'md',
  isLoading,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2',
        variants[variant],
        sizes[size],
        isLoading ? 'opacity-70 cursor-not-allowed' : '',
        className,
      )}
      disabled={isLoading || props.disabled}
      {...props}
    >
      {isLoading && (
        <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-current" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V8A8 8 0 012 12z" />
        </svg>
      )}
      {children}
    </button>
  )
}

export default Button
