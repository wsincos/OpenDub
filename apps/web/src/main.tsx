import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { StudioShell } from "./app/shell/StudioShell";
import "./styles/tokens.css";
import "./styles/globals.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <StudioShell />
  </StrictMode>,
);
