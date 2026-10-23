"""Build the integrated Phase 1 PDF from its Markdown source files."""
from pathlib import Path
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports" / "phase1"
OUTPUT = ROOT / "reports" / "phase1.pdf"
FONT = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
pdfmetrics.registerFont(TTFont("Arial", str(FONT)))
pdfmetrics.registerFont(TTFont("Arial-Bold", str(BOLD)))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="BodyA", parent=styles["BodyText"], fontName="Arial", fontSize=9, leading=12, spaceAfter=6))
styles.add(ParagraphStyle(name="H1A", parent=styles["Heading1"], fontName="Arial-Bold", fontSize=18, leading=22, spaceBefore=12, spaceAfter=10, textColor=colors.HexColor("#17365D")))
styles.add(ParagraphStyle(name="H2A", parent=styles["Heading2"], fontName="Arial-Bold", fontSize=13, leading=16, spaceBefore=10, spaceAfter=6, textColor=colors.HexColor("#24527A")))
styles.add(ParagraphStyle(name="H3A", parent=styles["Heading3"], fontName="Arial-Bold", fontSize=10, leading=13, spaceBefore=8, spaceAfter=4))
styles.add(ParagraphStyle(name="CaptionA", parent=styles["BodyText"], fontName="Arial", fontSize=8, leading=10, alignment=TA_CENTER, textColor=colors.HexColor("#555555"), spaceAfter=9))
styles.add(ParagraphStyle(name="TitleA", parent=styles["Title"], fontName="Arial-Bold", fontSize=22, leading=27, alignment=TA_CENTER, textColor=colors.HexColor("#17365D"), spaceAfter=14))


def inline(text):
    text = escape(text)
    text = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r"<link href='\2' color='#1a5e96'>\1</link>", text)
    return text


def table_from(lines):
    parsed = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c or "-") for c in cells):
            continue
        parsed.append([Paragraph(inline(c), styles["BodyA"]) for c in cells])
    if not parsed:
        return None
    n = max(map(len, parsed))
    for row in parsed:
        row.extend([Paragraph("", styles["BodyA"])] * (n - len(row)))
    widths = [7.15 * inch / n] * n
    t = Table(parsed, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCE6F1")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#17365D")),
        ("FONTNAME", (0, 0), (-1, 0), "Arial-Bold"),
        ("GRID", (0, 0), (-1, -1), .35, colors.HexColor("#AAB7C4")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def render_md(path, story):
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    first_title = True
    while i < len(lines):
        raw = lines[i].strip()
        if not raw:
            i += 1; continue
        if raw.startswith("|"):
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(lines[i]); i += 1
            table = table_from(block)
            if table: story.extend([Spacer(1, 3), table, Spacer(1, 7)])
            continue
        img = re.match(r"!\[(.*?)\]\((.*?)\)", raw)
        if img:
            image_path = (path.parent / img.group(2)).resolve()
            if image_path.exists():
                im = Image(str(image_path), width=6.9*inch, height=4.2*inch, kind="proportional", hAlign="CENTER")
                story.extend([im, Paragraph(inline(img.group(1)), styles["CaptionA"])])
            i += 1; continue
        if raw.startswith("#"):
            level = len(raw) - len(raw.lstrip("#")); title = raw[level:].strip()
            style = styles["TitleA"] if first_title else styles["H1A"] if level <= 2 else styles["H2A"] if level == 3 else styles["H3A"]
            story.append(Paragraph(inline(title), style)); first_title = False
            i += 1; continue
        if raw.startswith("- ") or re.match(r"\d+\. ", raw):
            bullet = "• " if raw.startswith("- ") else "• "
            txt = raw[2:] if raw.startswith("- ") else re.sub(r"^\d+\. ", "", raw)
            story.append(Paragraph(bullet + inline(txt), styles["BodyA"]))
            i += 1; continue
        if raw.startswith("```"):
            block=[]; i+=1
            while i < len(lines) and not lines[i].startswith("```"):
                block.append(lines[i]); i+=1
            story.append(Paragraph("<br/>".join(escape(x) for x in block), styles["BodyA"]))
            i+=1; continue
        para=[raw]; i+=1
        while i < len(lines) and lines[i].strip() and not lines[i].lstrip().startswith(("#", "|", "- ", "![")) and not re.match(r"\d+\. ", lines[i].strip()):
            para.append(lines[i].strip()); i+=1
        story.append(Paragraph(inline(" ".join(para)), styles["BodyA"]))


def page_num(canvas, doc):
    canvas.saveState()
    canvas.setFont("Arial", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(.7*inch, .45*inch, "NHANES Sleep and Supplement Project — Phase 1")
    canvas.drawRightString(7.8*inch, .45*inch, str(doc.page))
    canvas.restoreState()

files = sorted(REPORT_DIR.glob("*.md"), key=lambda p: (p.name.startswith("A"), p.name))
story = [Paragraph("Phase 1: Study, Data, and Descriptive Statistics", styles["TitleA"]),
         Paragraph("Sleep duration and dietary supplement use in NHANES, August 2021–August 2023", styles["CaptionA"]),
         Spacer(1, 16)]
for idx, path in enumerate(files):
    if idx:
        story.append(PageBreak())
    render_md(path, story)

doc = SimpleDocTemplate(str(OUTPUT), pagesize=letter, rightMargin=.68*inch, leftMargin=.68*inch,
                        topMargin=.65*inch, bottomMargin=.7*inch, title="NHANES Phase 1 Report",
                        author="Statistics Course Project")
doc.build(story, onFirstPage=page_num, onLaterPages=page_num)
print(f"Created {OUTPUT} ({OUTPUT.stat().st_size:,} bytes) from {len(files)} Markdown sections.")
