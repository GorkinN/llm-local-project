import React from 'react'
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

type BadgeVariant = 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'info' | 'neutral'

interface BadgeProps extends React.HTMLAttributes<HTMLDivElement | HTMLSpanElement> {
  variant?: BadgeVariant
  children: React.ReactNode
  size?: 'sm' | 'md' | 'lg'
}

const variants = {
  primary: 'bg-primary-100 text-primary-800 border border-primary-200',
  secondary: 'bg-secondary-100 text-secondary-800 border border-secondary-200',
  success: 'bg-success-100 text-success-800 border border-success-200',
  warning: 'bg-warning-100 text-warning-800 border border-warning-200',
  error: 'bg-error-100 text-error-800 border border-error-200',
  info: 'bg-info-100 text-info-800 border border-info-200',
  neutral: 'bg-neutral-100 text-neutral-800 border border-neutral-200',
}

const sizes = {
  sm: 'px-2 py-0.5 text-xs rounded-full',
  md: 'px-3 py-1 text-sm rounded-full',
  lg: 'px-4 py-1.5 text-base rounded-lg',
}

export function Badge({
  className,
  variant = 'neutral',
  children,
  size = 'md',
  ...props
}: BadgeProps) {
  const Component = props.as || 'div'
  
  if (props.as === 'span') {
    return <span {...props} className={cn(
      'inline-flex items-center font-medium',
      variants[variant],
      sizes[size],
      className,
    )}>
      {children}
    </span>
  }

  return <div {...props} className={cn(
    'inline-flex items-center font-medium',
    variants[variant],
    sizes[size],
    className,
  )}>
    {children}
  </div>
}

export function StatusBadge({ variant, children }: { variant: BadgeVariant; children?: React.ReactNode }) {
  return <Badge variant={variant}>{children}</Badge>
}

export default Badge
