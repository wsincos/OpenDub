import { FormEvent, useEffect, useState } from "react";
import { FolderOpen, Plus, RefreshCw, ServerCrash } from "lucide-react";

import { createProject, getProject, listProjects, Project, ProjectSummary } from "../api/client";
import { StudioShell } from "./shell/StudioShell";
import "./studio-app.css";

type ViewState = "home" | "studio";

export function StudioApp() {
  const [projects, setProjects] = useState<ProjectSummary[]>([]);
  const [selected, setSelected] = useState<Project | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [view, setView] = useState<ViewState>("home");

  async function refresh() {
    setLoading(true);
    setError(null);
    try {
      setProjects(await listProjects());
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Could not reach the local API.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { void refresh(); }, []);

  if (view === "studio" && selected) {
    return <StudioShell project={selected} onBack={() => setView("home")} onRefresh={async () => { const project = await getProject(selected.id); setSelected(project); setProjects((current) => current.map((item) => item.id === project.id ? project : item)); }} />;
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const name = String(data.get("name") ?? "").trim();
    if (!name) return;
    try {
      const project = await createProject(name);
      setProjects((current) => [project, ...current]);
      setSelected(project);
      setView("studio");
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Could not create the project.");
    }
  }

  async function openProject(project: ProjectSummary) {
    try {
      setSelected(await getProject(project.id));
      setView("studio");
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Could not open the local project.");
    }
  }

  return (
    <main className="project-home" aria-label="OpenDub projects">
      <header className="home-topbar"><div className="home-brand"><span>OD</span> OpenDub <small>Local Studio</small></div><span>Video-aware dubbing workspace</span></header>
      <section className="project-home-content">
        <div className="home-heading"><div><p>PROJECTS</p><h1>OpenDub Studio</h1></div><button className="refresh-button" onClick={() => void refresh()} title="Refresh local projects"><RefreshCw size={16} /> Refresh</button></div>
        <div className="project-layout">
          <form className="new-project" onSubmit={submit}><h2><Plus size={18} /> New project</h2><label htmlFor="project-name">Project name</label><input id="project-name" name="name" placeholder="Authorized demo" maxLength={200} required /><button type="submit"><Plus size={16} /> Create local project</button><p>Project data stays in your local OpenDub workspace.</p></form>
          <section className="project-list" aria-live="polite"><div className="list-heading"><h2>Recent projects</h2><span>{loading ? "Loading" : `${projects.length} projects`}</span></div>{error ? <div className="connection-error"><ServerCrash size={18} /><div><strong>Local API unavailable</strong><p>{error}</p><button onClick={() => void refresh()}>Try again</button></div></div> : null}{!loading && !error && projects.length === 0 ? <div className="empty-projects"><FolderOpen size={24} /><p>No project yet. Create one to begin a local dubbing workspace.</p></div> : null}{projects.map((project) => <button className="project-row" key={project.id} onClick={() => void openProject(project)}><span className="project-thumbnail" /><span><strong>{project.name}</strong><small>Revision {project.revision} · Local project</small></span><span className="open-label">Open</span></button>)}</section>
        </div>
      </section>
    </main>
  );
}
