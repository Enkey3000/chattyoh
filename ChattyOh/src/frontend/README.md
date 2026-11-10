# Frontend prototype

`index.html` is the supplied standalone ChattyOh desktop preview. It is an existing single-file HTML prototype, not a production React/Next.js application. Open it in a current browser to inspect the UI.

`desktop-shell/chattyoh-desktop/` preserves the supplied Electron wrapper and its renderer source. The desktop shell has native integration code; review its own README before running or packaging it.

The current implementation uses browser/local storage and includes simulated or incomplete features. It has no production API or account system. See `src/backend plan/ChattyOh Inc — Full Platform Audit (Nov 1, 2026) (1).md` for known issues and `docs/architecture.md` for the proposed migration direction.
