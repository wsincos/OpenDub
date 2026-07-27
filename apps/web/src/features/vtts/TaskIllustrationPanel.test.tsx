import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";

import { TaskIllustrationPanel } from "./TaskIllustrationPanel";

describe("TaskIllustrationPanel", () => {
  it("labels the female scene as task illustration rather than a historical case", () => {
    render(<TaskIllustrationPanel />);

    expect(screen.getByText(/task illustration · concept scene/i)).toBeVisible();
    expect(screen.getByText(/task illustration · no case audio or transcript/i)).toBeVisible();
    expect(screen.queryByText(/human-0\s*\/\s*gt audio/i)).not.toBeInTheDocument();
  });

  it("keeps English IPA and illustrated signal tracks on one controllable playhead", async () => {
    const user = userEvent.setup();
    render(<TaskIllustrationPanel />);

    expect(screen.getByText("ðə")).toBeVisible();
    expect(screen.getByText("ˈtʃeɪn.dʒɪz")).toBeVisible();
    expect(screen.getByText(/illustrated pitch \+ energy/i)).toBeVisible();
    expect(screen.getByText(/illustrated target speech/i)).toBeVisible();

    await user.click(screen.getByRole("button", { name: /hide face overlay/i }));

    expect(screen.queryByText(/face affect/i)).not.toBeInTheDocument();
  });
});
