import { DOMAIN_COLORS, type GraphLink, type GraphNode } from './types';

interface CrossDomainLinksProps {
  links: GraphLink[];
}

export function CrossDomainLinks({ links }: CrossDomainLinksProps) {
  const crossDomainLinks = links.filter((link) => {
    const source = link.source as GraphNode;
    const target = link.target as GraphNode;
    return source.domain !== target.domain;
  });

  return (
    <g className="cross-domain-links">
      {crossDomainLinks.map((link, i) => {
        const source = link.source as GraphNode;
        const target = link.target as GraphNode;
        const gradientId = `cross-domain-gradient-${i}`;

        return (
          <g key={`cross-${source.id}-${target.id}`}>
            <defs>
              <linearGradient
                id={gradientId}
                x1={source.x}
                y1={source.y}
                x2={target.x}
                y2={target.y}
                gradientUnits="userSpaceOnUse"
              >
                <stop offset="0%" stopColor={DOMAIN_COLORS[source.domain]} />
                <stop offset="100%" stopColor={DOMAIN_COLORS[target.domain]} />
              </linearGradient>
            </defs>
            <line
              x1={source.x ?? 0}
              y1={source.y ?? 0}
              x2={target.x ?? 0}
              y2={target.y ?? 0}
              stroke={`url(#${gradientId})`}
              strokeWidth={2}
              strokeDasharray="4,4"
              opacity={0.6}
            />
          </g>
        );
      })}
    </g>
  );
}

interface DomainLinkProps {
  links: GraphLink[];
  showCrossDomain?: boolean;
}

export function DomainLinks({ links, showCrossDomain = true }: DomainLinkProps) {
  return (
    <g className="domain-links">
      {links.map((link) => {
        const source = link.source as GraphNode;
        const target = link.target as GraphNode;
        const isCrossDomain = source.domain !== target.domain;

        if (isCrossDomain && !showCrossDomain) return null;

        return (
          <line
            key={`${source.id}-${target.id}`}
            x1={source.x ?? 0}
            y1={source.y ?? 0}
            x2={target.x ?? 0}
            y2={target.y ?? 0}
            stroke={isCrossDomain ? '#6b7280' : DOMAIN_COLORS[source.domain]}
            strokeWidth={isCrossDomain ? 1 : 1.5}
            strokeDasharray={isCrossDomain ? '4,4' : undefined}
            opacity={isCrossDomain ? 0.4 : 0.6}
          />
        );
      })}
    </g>
  );
}
