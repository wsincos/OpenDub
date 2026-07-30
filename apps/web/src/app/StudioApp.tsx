import { FormEvent, useEffect, useState } from "react";
import { FolderOpen, Plus, RefreshCw, ServerCrash } from "lucide-react";
import { useSearchParams } from "react-router-dom";

import {
  createProject,
  getProject,
  listProjects,
  Project,
  ProjectSummary,
  selectProjectMethod,
} from "../api/client";
import { createMethodSelectionDraft, getMethod } from "../content/methods";
import { StudioShell } from "./shell/StudioShell";
import "./studio-app.css";

type ViewState = "home" | "studio";

export function StudioApp() {
  const [searchParams] = useSearchParams();
  const [projects, setProjects] = useState<ProjectSummary[]>([]);
  const [selected, setSelected] = useState<Project | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [view, setView] = useState<ViewState>("home");
  const preselectedMethod = getMethod(searchParams.get("method") ?? undefined);

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
      const createdProject = await createProject(name);
      let project = createdProject;
      if (preselectedMethod) {
        try {
          project = await savePreselectedMethod(createdProject);
        } catch (selectionError) {
          setProjects((current) => [createdProject, ...current]);
          setError(selectionError instanceof Error
            ? `Project created, but the selected method was not recorded: ${selectionError.message}`
            : "Project created, but the selected method was not recorded. Open the project and try again.");
          return;
        }
      }
      setProjects((current) => [project, ...current]);
      setSelected(project);
      setView("studio");
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Could not create the project.");
    }
  }

  async function openProject(project: ProjectSummary) {
    try {
      const loadedProject = await getProject(project.id);
      const selectedProject = preselectedMethod
        ? await savePreselectedMethod(loadedProject)
        : loadedProject;
      setSelected(selectedProject);
      setView("studio");
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Could not open the local project.");
    }
  }

  async function savePreselectedMethod(project: Project): Promise<Project> {
    if (!preselectedMethod || project.method_selection?.method_id === preselectedMethod.id) return project;
    return selectProjectMethod(
      project.id,
      createMethodSelectionDraft(preselectedMethod),
      project.revision,
    );
  }

  return (
    <main className="project-home" aria-label="OpenDub projects">
      <header className="home-topbar"><div className="home-brand"><span>OD</span> OpenDub <small>LOCAL STUDIO</small></div><span>LOCAL-ONLY PROJECT WORKSPACE</span></header>
      <section className="project-home-content">
        <div className="home-heading"><div><p>OPEN DUB / LOCAL PROJECT DESK</p><h1>Prepare an authorized video-dubbing project.</h1><span>Local files, source permissions, selected complete method, and preparation export remain explicit at every step.</span></div><button className="refresh-button" onClick={() => void refresh()} title="Refresh local projects"><RefreshCw size={16} /> Refresh</button></div>
        <div className="project-layout">
          <form className="new-project" onSubmit={submit}><p className="local-command">NEW LOCAL PROJECT</p><h2><Plus size={18} /> Project identity</h2>{preselectedMethod ? <div className="method-intent"><span>METHOD PRESELECTED</span><strong>Preparing a project for {preselectedMethod.title}</strong><p>{preselectedMethod.status} content · runtime {preselectedMethod.runtimeStatus}</p></div> : null}<label htmlFor="project-name">Project name</label><input id="project-name" name="name" placeholder="Authorized demo" maxLength={200} required /><button type="submit"><Plus size={16} /> Create local project</button><p>Project data stays in your local OpenDub workspace.</p></form>
          <section className="project-list" aria-live="polite"><div className="list-heading"><div><p>LOCAL PROJECT INDEX</p><h2>Recent projects</h2></div><span>{loading ? "Loading" : `${projects.length} projects`}</span></div>{error ? <div className="connection-error"><ServerCrash size={18} /><div><strong>Local API unavailable</strong><p>{error}</p><button onClick={() => void refresh()}>Try again</button></div></div> : null}{!loading && !error && projects.length === 0 ? <div className="empty-projects"><FolderOpen size={24} /><p>No project yet. Create one to begin a local dubbing workspace.</p></div> : null}{projects.map((project, index) => <button className="project-row" key={project.id} onClick={() => void openProject(project)}><span className="project-index">{String(index + 1).padStart(2, "0")}</span><span><strong>{project.name}</strong><small>Revision {project.revision} · Local project</small></span><span className="open-label">Open</span></button>)}</section>
        </div>
      </section>
    </main>
  );
}
