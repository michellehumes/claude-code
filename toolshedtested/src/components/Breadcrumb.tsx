import Link from 'next/link'

interface BreadcrumbItem {
  name: string
  href?: string
}

interface BreadcrumbProps {
  items: BreadcrumbItem[]
}

export default function Breadcrumb({ items }: BreadcrumbProps) {
  return (
    <nav
      aria-label="Breadcrumb"
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '6px',
        flexWrap: 'wrap',
        marginBottom: '24px',
        fontFamily: 'IBM Plex Mono, monospace',
        fontSize: '11px',
        fontWeight: 500,
        letterSpacing: '0.06em',
        textTransform: 'uppercase',
        color: 'var(--text-muted)',
      }}
    >
      {items.map((item, index) => {
        const isLast = index === items.length - 1
        return (
          <span
            key={index}
            style={{ display: 'flex', alignItems: 'center', gap: '6px' }}
          >
            {item.href && !isLast ? (
              <Link
                href={item.href}
                style={{
                  color: 'var(--text-muted)',
                  textDecoration: 'none',
                  transition: 'color 0.2s',
                }}
              >
                {item.name}
              </Link>
            ) : (
              <span style={{ color: isLast ? 'var(--text-secondary)' : 'var(--text-muted)' }}>
                {item.name}
              </span>
            )}
            {!isLast && (
              <span style={{ color: 'var(--border)', userSelect: 'none' }}>/</span>
            )}
          </span>
        )
      })}
    </nav>
  )
}
