"""Build the integrated Phase 2 PDF from the reviewed Markdown sections."""

from pathlib import Path
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import CondPageBreak, PageBreak, Paragraph, SimpleDocTemplate, Spacer

import build_phase1_pdf as common


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "reports" / "phase2"
OUTPUT = ROOT / "reports" / "phase2.pdf"


def phase2_inline(value: str) -> str:
    # Local Markdown links are useful in source files; their readable labels
    # are sufficient in the printed PDF. Keep web links active.
    value = re.sub(r"\[([^\]]+)\]\((?!https?://)[^)]+\)", r"\1", value)
    value = escape(value)
    value = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", value)
    value = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)",
                   r"<link href='\2' color='#1a5e96'>\1</link>", value)
    return value


def footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Arial", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(0.7 * inch, 0.45 * inch,
                      "NHANES Sleep and Supplement Project - Phase 2")
    canvas.drawRightString(7.8 * inch, 0.45 * inch, str(doc.page))
    canvas.restoreState()


def main() -> None:
    sections = sorted(SOURCE.glob("*.md"), key=lambda p: (p.name.startswith("A"), p.name))
    if len(sections) != 13:
        raise ValueError(f"Expected nine common and four Path A sections, found {len(sections)}")
    common.inline = phase2_inline
    for heading in ("TitleA", "H1A", "H2A", "H3A"):
        common.styles[heading].keepWithNext = True
    story = [
        Spacer(1, 1.2 * inch),
        Paragraph("Phase 2: Probability and Probability Distributions", common.styles["TitleA"]),
        Paragraph("Dietary supplement use and sleep in NHANES, August 2021-August 2023",
                  common.styles["CaptionA"]),
        Spacer(1, 0.35 * inch),
        Paragraph("Common tasks 2.1-2.9 and NHANES Path A requirements A1-A4",
                  common.styles["H2A"]),
        Paragraph("Analysis, tables, figures, and reproducibility details are provided in the following sections. The principal empirical probability sample contains 4,741 adults. Numeric sleep summaries and weighted comparisons use the documented outcome-specific subsets.",
                  common.styles["BodyA"]),
        PageBreak(),
    ]
    for index, path in enumerate(sections):
        if index:
            story.extend([Spacer(1, 0.18 * inch), CondPageBreak(1.6 * inch)])
        common.render_md(path, story)
    document = SimpleDocTemplate(
        str(OUTPUT), pagesize=letter, leftMargin=0.68 * inch,
        rightMargin=0.68 * inch, topMargin=0.65 * inch, bottomMargin=0.7 * inch,
        title="NHANES Phase 2 Report", author="Statistics Course Project",
    )
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Created {OUTPUT} ({OUTPUT.stat().st_size:,} bytes) from {len(sections)} sections")


if __name__ == "__main__":
    main()
