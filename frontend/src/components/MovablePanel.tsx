import { CSSProperties, KeyboardEvent, MouseEvent, PointerEvent, ReactNode, useEffect, useRef, useState } from "react";

type Point = { x: number; y: number };

type MovablePanelProps = {
  children: ReactNode;
  className: string;
  defaultPosition: Point;
  id: string;
  label: string;
};

const storagePrefix = "jarvis.panel-layout.v1.";

function clamp(point: Point) {
  return {
    x: Math.max(8, Math.min(point.x, window.innerWidth - 56)),
    y: Math.max(8, Math.min(point.y, window.innerHeight - 56)),
  };
}

function loadPosition(id: string, fallback: Point) {
  try {
    const saved = window.localStorage.getItem(`${storagePrefix}${id}`);
    if (!saved) return fallback;
    const position = JSON.parse(saved) as Point;
    return Number.isFinite(position.x) && Number.isFinite(position.y) ? clamp(position) : fallback;
  } catch {
    return fallback;
  }
}

export function MovablePanel({ children, className, defaultPosition, id, label }: MovablePanelProps) {
  const panelRef = useRef<HTMLDivElement | null>(null);
  const firstMenuItemRef = useRef<HTMLButtonElement | null>(null);
  const dragOrigin = useRef<Point | null>(null);
  const draggedRef = useRef(false);
  const [position, setPosition] = useState(() => loadPosition(id, defaultPosition));
  const [moving, setMoving] = useState(false);
  const [menu, setMenu] = useState<Point | null>(null);

  useEffect(() => {
    const onResize = () => setPosition((current) => clamp(current));
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  useEffect(() => {
    if (!menu) return;
    firstMenuItemRef.current?.focus();
    const dismiss = () => setMenu(null);
    window.addEventListener("pointerdown", dismiss, { once: true });
    return () => window.removeEventListener("pointerdown", dismiss);
  }, [menu]);

  function openMenu(event: MouseEvent<HTMLDivElement>) {
    event.preventDefault();
    const rect = panelRef.current?.getBoundingClientRect();
    setMenu({
      x: event.clientX || rect?.left || position.x,
      y: event.clientY || rect?.top || position.y,
    });
  }

  function beginMove() {
    setMoving(true);
    setMenu(null);
  }

  function fixPosition() {
    try {
      window.localStorage.setItem(`${storagePrefix}${id}`, JSON.stringify(position));
    } catch {
      // Storage can be unavailable in private browsing; the fixed position still works for this session.
    }
    setMoving(false);
    setMenu(null);
  }

  function startDrag(event: PointerEvent<HTMLButtonElement>) {
    if (!moving) return;
    draggedRef.current = false;
    dragOrigin.current = { x: event.clientX - position.x, y: event.clientY - position.y };
    event.currentTarget.setPointerCapture(event.pointerId);
  }

  function drag(event: PointerEvent<HTMLButtonElement>) {
    if (!moving || !dragOrigin.current) return;
    draggedRef.current = true;
    setPosition(clamp({ x: event.clientX - dragOrigin.current.x, y: event.clientY - dragOrigin.current.y }));
  }

  function endDrag() {
    dragOrigin.current = null;
  }

  function activateHandle() {
    if (draggedRef.current) {
      draggedRef.current = false;
      return;
    }
    fixPosition();
  }

  function nudge(event: KeyboardEvent<HTMLButtonElement>) {
    if (!moving) return;
    const amount = event.shiftKey ? 24 : 8;
    const adjustment: Record<string, Point> = {
      ArrowDown: { x: 0, y: amount },
      ArrowLeft: { x: -amount, y: 0 },
      ArrowRight: { x: amount, y: 0 },
      ArrowUp: { x: 0, y: -amount },
    };
    if (event.key === "Enter" || event.key === "Escape") {
      event.preventDefault();
      fixPosition();
      return;
    }
    const delta = adjustment[event.key];
    if (!delta) return;
    event.preventDefault();
    setPosition((current) => clamp({ x: current.x + delta.x, y: current.y + delta.y }));
  }

  return (
    <div
      ref={panelRef}
      className={`movable-panel ${className} ${moving ? "is-moving" : ""}`}
      style={{ "--panel-x": `${position.x}px`, "--panel-y": `${position.y}px` } as CSSProperties}
      onContextMenu={openMenu}
    >
      {moving && (
        <button
          type="button"
          className="panel-move-handle"
          aria-label={`Move ${label}. Drag, use arrow keys to nudge, then press Enter to fix position.`}
          onClick={activateHandle}
          onKeyDown={nudge}
          onPointerDown={startDrag}
          onPointerMove={drag}
          onPointerUp={endDrag}
          onPointerCancel={endDrag}
        >
          DRAG TO MOVE
        </button>
      )}
      {children}
      {menu && (
        <div className="panel-context-menu" role="menu" aria-label={`${label} panel options`} style={{ left: menu.x, top: menu.y }} onPointerDown={(event) => event.stopPropagation()}>
          {!moving ? <button ref={firstMenuItemRef} type="button" role="menuitem" onClick={beginMove}>Move</button> : <button ref={firstMenuItemRef} type="button" role="menuitem" onClick={fixPosition}>Fix position</button>}
        </div>
      )}
    </div>
  );
}
