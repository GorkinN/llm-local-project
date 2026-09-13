import React from 'react'
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

interface InputProps extends Omit<React.HTMLAttributes<HTMLInputElement>, 'label'> {
  label?: string
  error?: string
  prefix?: React.ReactNode
  suffix?: React.ReactNode
}

export function Input({
  className,
  label,
  error,
  prefix,
  suffix,
  ...props
}: InputProps) {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-neutral-700 mb-1.5">
          {label}
        </label>
      )}
      <div className="relative">
        {prefix && (
          <div className="absolute left-3 top-1/2 -translate-y-1/2 text-neutral-400">
            {prefix}
          </div>
        )}
        <input
          className={cn(
            'w-full px-4 py-2.5 rounded-lg border bg-white transition-colors',
            prefix ? 'pl-10' : '',
            suffix ? 'pr-10' : '',
            error
              ? 'border-error-500 text-error-900 placeholder-error-300 focus:border-error-500 focus:ring-2 focus:ring-error-200'
              : 'border-neutral-300 text-neutral-900 placeholder-neutral-400 focus:border-primary-500 focus:ring-2 focus:ring-primary-200',
            props.disabled ? 'bg-neutral-50 cursor-not-allowed opacity-60' : '',
            className,
          )}
          disabled={props.disabled}
          {...props}
        />
        {suffix && (
          <div className="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-400">
            {suffix}
          </div>
        )}
      </div>
      {error && <p className="mt-1.5 text-sm text-error-600">{error}</p>}
    </div>
  )
}

export default Input
