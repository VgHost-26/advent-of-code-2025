import * as React from "react";

/** SSR-safe-ish media query hook (client-only dashboard). */
export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = React.useState(
    () => window.matchMedia(query).matches
  );

  React.useEffect(() => {
    const mq = window.matchMedia(query);
    const onChange = (event: MediaQueryListEvent) => setMatches(event.matches);
    setMatches(mq.matches);
    mq.addEventListener("change", onChange);
    return () => mq.removeEventListener("change", onChange);
  }, [query]);

  return matches;
}
