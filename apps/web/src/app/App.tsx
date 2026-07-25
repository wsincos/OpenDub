import { Github, Menu, X } from "lucide-react";
import { useState } from "react";
import { NavLink, Navigate, Route, Routes } from "react-router-dom";

import { TaskExplorerPage } from "../features/explore/TaskExplorerPage";
import { ComparisonLabPage } from "../features/compare/ComparisonLabPage";
import { MethodAtlasPage } from "../features/methods/MethodAtlasPage";
import { MethodCanvasPage } from "../features/methods/MethodCanvasPage";
import { StudioApp } from "./StudioApp";
import "./app-shell.css";

export function OpenDubApp() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="atlas-app">
      <header className="atlas-nav">
        <NavLink className="atlas-brand" to="/explore"><span>OD</span><strong>OpenDub</strong><small>METHOD ATLAS</small></NavLink>
        <button aria-expanded={menuOpen} aria-label="Toggle navigation" className="nav-menu-button" onClick={() => setMenuOpen((open) => !open)} type="button">
          {menuOpen ? <X size={18} /> : <Menu size={18} />}
        </button>
        <nav className={menuOpen ? "is-open" : ""} aria-label="OpenDub primary navigation">
          <NavItem label="Explore" to="/explore" onNavigate={() => setMenuOpen(false)} />
          <NavItem label="Methods" to="/methods" onNavigate={() => setMenuOpen(false)} />
          <NavItem label="Compare" to="/compare" onNavigate={() => setMenuOpen(false)} />
          <NavItem label="Studio" to="/studio" onNavigate={() => setMenuOpen(false)} />
        </nav>
        <a aria-label="OpenDub repository" className="repo-link" href="https://github.com/wsincos/OpenDub" rel="noreferrer" target="_blank"><Github size={16} /> <span>Repository</span></a>
      </header>
      <Routes>
        <Route element={<Navigate replace to="/explore" />} path="/" />
        <Route element={<TaskExplorerPage />} path="/explore" />
        <Route element={<MethodAtlasPage />} path="/methods" />
        <Route element={<MethodCanvasPage />} path="/methods/:methodSlug" />
        <Route element={<ComparisonLabPage />} path="/compare" />
        <Route element={<StudioApp />} path="/studio" />
        <Route element={<Navigate replace to="/explore" />} path="*" />
      </Routes>
    </div>
  );
}

function NavItem({ label, onNavigate, to }: { label: string; onNavigate: () => void; to: string }) {
  return <NavLink className={({ isActive }) => isActive ? "is-active" : ""} onClick={onNavigate} to={to}>{label}</NavLink>;
}
