import React from 'react'
import { Link } from 'react-router-dom'

interface CardProps extends Omit<React.HTMLAttributes<HTMLDivElement>, 'as'> {
  href?: string
  title?: React.ReactNode
  description?: React.ReactNode
  children?: React.ReactNode
  hover?: boolean
  onClick?: React.MouseEventHandler<HTMLDivElement>
}

export function Card({
  className,
  href,
  title,
  description,
  children,
  hover = true,
  onClick,
}: CardProps) {
  const baseStyles = 'bg-white rounded-xl border border-neutral-200 shadow-card transition-all duration-200'

  // Content with optional sections
  const content: React.ReactNode = (
    <>
      {title && <h3 className="text-xl font-semibold mb-2 text-neutral-800">{title}</h3>}
      {description && <p className="mb-4 text-sm text-neutral-600">{description}</p>}
      {children}
    </>
  )

  if (onClick) {
    // onClick only - use div
    return (
      <div className={baseStyles + ' ' + (hover ? 'hover:shadow-card-lg hover:-translate-y-0.5' : '') + ' ' + className} onClick={onClick}>
        {content}
      </div>
    )
  } else if (href) {
    // Has href - use Link
    return (
      <Link to={href} className={baseStyles + ' ' + (hover ? 'hover:shadow-card-lg hover:-translate-y-0.5 hover:border-primary-300 cursor-pointer' : '') + ' ' + className}>
        {content}
      </Link>
    )
  } else {
    // No href/onClick - use plain div
    return (
      <div className={baseStyles + ' ' + (hover ? 'hover:shadow-card-lg hover:-translate-y-0.5' : '')}>
        {content}
      </div>
    )
  }
}

export default Card
