import { useEffect, useState } from "react";

/** Charset used while a glyph is decoding. */
const CHARS =
  "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_-+=[]{}|;:,.<>?";

const BLOCK = "\u2592";
const STAGGER_MS = 70;
const CHAR_DURATION_MS = 900;

type Phase = "hidden" | "playing" | "done";

/**
 * "Decoder" reveal: characters flicker through random glyphs and settle
 * front-to-back (stagger). While hidden, shows solid cover blocks.
 * Respects prefers-reduced-motion (instant settle).
 */
export function DecoderText({
  text,
  revealed,
  className,
}: {
  text: string;
  revealed: boolean;
  className?: string;
}) {
  const [phase, setPhase] = useState<Phase>("hidden");
  const [display, setDisplay] = useState(
    BLOCK.repeat(text.length) || BLOCK,
  );

  useEffect(() => {
    if (revealed && phase === "hidden") {
      if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        setPhase("done");
      } else {
        setPhase("playing");
      }
    } else if (!revealed && phase !== "hidden") {
      setPhase("hidden");
      setDisplay(BLOCK.repeat(text.length) || BLOCK);
    }
  }, [revealed, text]);

  useEffect(() => {
    if (phase !== "playing") return;

    const t0 = performance.now();
    let raf = 0;

    const tick = (now: number) => {
      let out = "";
      let unsettled = false;

      for (let i = 0; i < text.length; i++) {
        const start = i * STAGGER_MS;
        const t = (now - t0 - start) / CHAR_DURATION_MS;
        if (t <= 0) {
          out += BLOCK;
          unsettled = true;
        } else if (t < 1) {
          out += CHARS[Math.floor(Math.random() * CHARS.length)];
          unsettled = true;
        } else {
          out += text[i];
        }
      }

      setDisplay(out);
      if (unsettled) {
        raf = requestAnimationFrame(tick);
      } else {
        setPhase("done");
      }
    };

    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [phase, text]);

  if (phase !== "done") {
    return <span className={className}>{display}</span>;
  }

  return (
    <span className={className} data-slot="decoder-done">
      {text}
    </span>
  );
}
