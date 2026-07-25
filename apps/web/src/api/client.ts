export type ProjectSummary = {
  id: string;
  name: string;
  revision: number;
  updated_at: string;
};

const apiBase = import.meta.env.VITE_OPENDUB_API_BASE ?? "http://127.0.0.1:8000";

export async function listProjects(): Promise<ProjectSummary[]> {
  const response = await fetch(`${apiBase}/api/v1/projects`);
  if (!response.ok) throw new Error(`Local API returned ${response.status}`);
  return response.json() as Promise<ProjectSummary[]>;
}

export async function createProject(name: string): Promise<ProjectSummary> {
  const response = await fetch(`${apiBase}/api/v1/projects`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
  if (!response.ok) throw new Error(`Local API returned ${response.status}`);
  return response.json() as Promise<ProjectSummary>;
}
