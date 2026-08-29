# Jarvis design context

## Product and scene

Jarvis is a lightweight browser voice assistant for students using ordinary Windows laptops. It is used at a desk in a dim room, where the looping cyberpunk city video provides atmosphere while the interface must stay legible and task-focused.

## Visual direction

- **Register:** compact field console; cinematic background, disciplined information modules.
- **Signature:** independently positionable HUD modules and a central voice orb. A right-click opens a small Move/Fix position menu; position is saved only after Fix position is selected.
- **Composition:** conversation sits mid-right, status and activity cluster on the left, and the local briefing occupies the lower field. The background video remains unobstructed between modules.
- **Motion:** video and the bottom audio signal field provide the ambient motion. Panel movement is direct, deliberate, and respects reduced-motion preferences.

## Runtime tokens

`app/frontend/src/styles/global.css` is the sole runtime token owner. All interface modules use the values below through CSS custom properties.

| Token | Value | Role |
| --- | --- | --- |
| `--ink` | `#03050c` | deep canvas and fallback background |
| `--surface` | `rgba(5, 14, 30, .76)` | panel surface |
| `--line` | `rgba(104, 235, 255, .52)` | technical borders |
| `--cyan` | `#65e9ff` | labels and focused controls |
| `--ready` | `#53f2c5` | online/ready state |
| `--danger` | `#ff6b91` | errors |

## Interaction contract

- All dashboard modules are movable on desktop. Right-click opens Move or Fix position; selecting Move enables the module’s dedicated drag handle.
- The central orb is also the primary hold-to-talk control and can be repositioned using the same Move/Fix interaction as the other modules.
- The drag handle also supports Arrow keys for small movements, Enter or Escape to fix its current position, and a visible status label while moving.
- Fixed positions are stored locally under a versioned Jarvis layout key. No position data is sent to the API.
- On narrow screens, modules return to document flow and remain usable without dragging.
- The browser-owned native voice selector remains intentional: its system popup is acceptable for this lightweight student tool.

## Accessibility and performance

- Core controls use native buttons, inputs, and select elements with visible focus states.
- The video is decorative, muted, and never captures pointer events.
- `prefers-reduced-motion` suppresses non-essential panel and visualizer animation.
