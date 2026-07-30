import { Crosshair, MousePointer2 } from "lucide-react";
import { useState } from "react";

import type { MethodDefinition } from "../../content/methods";
import { getPaperFigure } from "./paper-figures";
import "./paper-architecture-figure.css";

export function PaperArchitectureFigure({ method }: { method: MethodDefinition }) {
  const figure = getPaperFigure(method);
  const [selectedRegionId, setSelectedRegionId] = useState(figure.regions[0].id);
  const selectedRegion = figure.regions.find((region) => region.id === selectedRegionId) ?? figure.regions[0];

  return (
    <section aria-label={`${method.title} original method architecture figure`} className="paper-architecture" style={{ "--method-color": method.color } as React.CSSProperties}>
      <div className="paper-architecture-figure-column">
        <div className="paper-architecture-heading"><span><Crosshair size={14} /> ORIGINAL METHOD EVIDENCE</span><span>PUBLISHED SOURCE FIGURE</span></div>
        <figure className="paper-figure-sheet">
          <div className="paper-figure-image-wrap">
            <img alt={`${method.title} original method architecture`} src={figure.imagePath} />
            {figure.regions.map((region, index) => (
              <button
                aria-label={`Inspect ${region.label} in original method figure`}
                aria-pressed={selectedRegion.id === region.id}
                className={selectedRegion.id === region.id ? "paper-figure-hotspot is-selected" : "paper-figure-hotspot"}
                key={region.id}
                onClick={() => setSelectedRegionId(region.id)}
                style={{ left: `${region.x}%`, top: `${region.y}%`, width: `${region.width}%`, height: `${region.height}%` }}
                type="button"
              >
                <span>{String(index + 1).padStart(2, "0")}</span>
                {selectedRegion.id === region.id ? <strong>{region.label}</strong> : null}
              </button>
            ))}
          </div>
          <figcaption>{figure.caption}</figcaption>
        </figure>
      </div>
      <aside className="paper-reading-rail">
        <p><MousePointer2 size={13} /> COMPONENT READING</p>
        <span>0{figure.regions.findIndex((region) => region.id === selectedRegion.id) + 1} / 0{figure.regions.length}</span>
        <h2>{selectedRegion.label}</h2>
        <p>{selectedRegion.detail}</p>
        <div className="paper-region-list" aria-label="Original method figure regions">
          {figure.regions.map((region, index) => <button aria-pressed={selectedRegion.id === region.id} key={region.id} onClick={() => setSelectedRegionId(region.id)} type="button"><i>{String(index + 1).padStart(2, "0")}</i>{region.label}</button>)}
        </div>
      </aside>
    </section>
  );
}
