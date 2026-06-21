"""Render ResearchDoc.md as HTML for the How it works page."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

SECTION_H2 = frozenset(
    {
        "Physiological Mechanisms and Neurovascular Hemodynamics",
        "Clinical Trial Evidence and Therapeutic Timelines",
        "Diagnostic Scoring and Etiology Mapping",
        "Clinical Triage and Referral Algorithms",
        "Standardized Male Pelvic Floor Muscle Training Protocols",
        "Conclusions and Clinical Summary",
    }
)

SECTION_H3 = frozenset(
    {
        "Physical Therapy / PFMT Alone",
        "Cognitive Behavioral Therapy (CBT) or Sex Therapy",
        "Specialist Referrals",
        "Muscle Isolation and Verification",
        "Progressive Positional Protocol",
        "Dynamic Exercise Modalities",
        "Parameter Control and Dosing",
    }
)

REF_START_MARKERS = ("weillcornell.org",)

_CITE_RE = re.compile(r"\[cite:\s*([^\]]+)\]")
_FLOW_BLOCK_START = frozenset({"[erection-flow]", "[research-flow]"})
_FLOW_BLOCK_END = frozenset({"[/erection-flow]", "[/research-flow]"})
_LIST_BLOCK_START = frozenset({"[numbered-list]"})
_LIST_BLOCK_END = frozenset({"[/numbered-list]"})
_FLOW_STEP_RE = re.compile(r"^\d+\.\s+(.+)$")
VERTICAL_TABLES: dict[str, tuple[int, tuple[str, ...]]] = {
    "Clinical Trial / Study Reference": (
        6,
        (
            "Dorey et al., 2004/2005",
            "Filocamo et al., 2005",
            "Lavoisier et al., 2014",
            "Pastore et al., 2014/2018",
            "Post-Prostatectomy Meta-Analysis, 2022",
        ),
    ),
    "Diagnostic Parameter": (
        4,
        (
            "Onset of Dysfunction",
            "Morning / Nocturnal Erections",
            "Situational Consistency",
            "Rigidity during Masturbation",
            "Associated Clinical Comorbidities",
            "Modified IIEF Classification",
            "Objective Diagnostic Validation",
        ),
    ),
    "Clinical Presentation": (
        6,
        (
            "Isolated Pelvic Floor Weakness",
            "Situational Performance Anxiety",
            "Penile Pain, Plaque, or Curvature",
            "Sustained Erection >4 Hours",
            "ED with Known High-Risk CVD",
            "Suspected Endocrine Deficiency",
        ),
    ),
    "Protocol Phase": (
        6,
        (
            "Phase I: Base Neural Mobilization",
            "Phase II: Progressive Loading",
            "Phase III: Functional Integration",
            "Phase IV: Somatic Automation",
        ),
    ),
}


@dataclass(frozen=True)
class Reference:
    index: int
    domain: str
    title: str

    @property
    def url(self) -> str:
        return self.domain if self.domain.startswith("http") else f"https://{self.domain}"

    @property
    def ieee_title(self) -> str:
        title = self.title.strip()
        if " - " in title:
            title = title.rsplit(" - ", 1)[0].strip()
        if " | " in title:
            title = title.split(" | ")[0].strip()
        return title

    @property
    def publisher(self) -> str:
        if " - " in self.title:
            return self.title.rsplit(" - ", 1)[-1].strip()
        if " | " in self.title:
            tail = self.title.split(" | ")[-1].strip()
            if " - " in tail:
                return tail.rsplit(" - ", 1)[-1].strip()
            return tail
        host = self.domain.removeprefix("www.")
        label = host.rsplit(".", 1)[0]
        return label.replace("-", " ").replace(".", " ").title()


def _esc(text: str) -> str:
    return html.escape(text.strip(), quote=True)


def _ieee_access_date() -> str:
    today = date.today()
    return f"{today.strftime('%b')}. {today.day}, {today.year}"


def _parse_cite_numbers(raw: str) -> list[int]:
    return [int(part.strip()) for part in raw.split(",") if part.strip().isdigit()]


def _format_cite_links(raw: str) -> str:
    numbers = _parse_cite_numbers(raw)
    if not numbers:
        return ""
    return ", ".join(
        f'<a href="#ref-{num}" class="research-cite">[{num}]</a>' for num in numbers
    )


def _format_markdown_inline(text: str) -> str:
    """Render simple **bold**, *italic*, and [cite: …] markers."""
    parts: list[str] = []
    last = 0
    for match in _CITE_RE.finditer(text):
        if match.start() > last:
            parts.append(_format_md_only(text[last : match.start()]))
        cite_html = _format_cite_links(match.group(1))
        if cite_html:
            parts.append(cite_html)
        last = match.end()
    if last < len(text):
        parts.append(_format_md_only(text[last:]))
    return "".join(parts).strip()


def _format_md_only(text: str) -> str:
    out: list[str] = []
    i = 0
    while i < len(text):
        if text.startswith("**", i):
            end = text.find("**", i + 2)
            if end != -1:
                out.append(f"<strong>{_esc(text[i + 2 : end])}</strong>")
                i = end + 2
                continue
        if text[i] == "*" and (i + 1 >= len(text) or text[i + 1] != "*"):
            end = text.find("*", i + 1)
            if end != -1:
                out.append(f"<em>{_esc(text[i + 1 : end])}</em>")
                i = end + 1
                continue
        start = i
        i += 1
        while i < len(text) and not text.startswith("**", i) and text[i] != "*":
            i += 1
        out.append(_esc(text[start:i]))
    return "".join(out)


def _format_inline(text: str) -> str:
    parts: list[str] = []
    last = 0
    for match in _CITE_RE.finditer(text):
        if match.start() > last:
            parts.append(_esc(text[last : match.start()]))
        cite_html = _format_cite_links(match.group(1))
        if cite_html:
            parts.append(cite_html)
        last = match.end()
    if last < len(text):
        parts.append(_esc(text[last:]))
    return "".join(parts).strip()


def _format_cell(text: str) -> str:
    cleaned = text.strip()
    if not cleaned:
        return ""
    parts: list[str] = []
    for chunk in cleaned.split("\n\n"):
        chunk = chunk.strip()
        if not chunk:
            continue
        formatted = _format_inline(chunk)
        if formatted:
            parts.append(formatted)
    return "<br><br>".join(parts)


def _parse_references(ref_lines: list[str]) -> list[Reference]:
    items: list[Reference] = []
    i = 0
    while i < len(ref_lines):
        domain = ref_lines[i]
        if domain == "Opens in a new window":
            i += 1
            continue
        if i + 1 >= len(ref_lines):
            break
        title = ref_lines[i + 1]
        i += 2
        if i < len(ref_lines) and ref_lines[i] == "Opens in a new window":
            i += 1
        if title == "Opens in a new window":
            continue
        items.append(Reference(index=len(items) + 1, domain=domain, title=title))
    return items


def _format_ieee_reference(ref: Reference) -> str:
    access_date = _ieee_access_date()
    return (
        f'<span class="research-ref-num">[{ref.index}]</span> '
        f'"{_esc(ref.ieee_title)}," '
        f"<em>{_esc(ref.publisher)}</em>. "
        f"[Online]. Available: "
        f'<a href="{_esc(ref.url)}" rel="noopener noreferrer" target="_blank">{_esc(ref.url)}</a>. '
        f"Accessed: {access_date}."
    )


def _render_numbered_flow(lines: list[str]) -> str:
    steps: list[str] = []
    for line in lines:
        match = _FLOW_STEP_RE.match(line.strip())
        if not match:
            continue
        steps.append(
            f'<li class="research-flow__step">{_format_markdown_inline(match.group(1))}</li>'
        )
    if not steps:
        return ""
    return (
        '<ol class="research-flow">'
        f'{"".join(steps)}'
        "</ol>"
    )


def _render_simple_numbered_list(lines: list[str]) -> str:
    items: list[str] = []
    for line in lines:
        match = _FLOW_STEP_RE.match(line.strip())
        if not match:
            continue
        items.append(f"<li>{_format_markdown_inline(match.group(1))}</li>")
    if not items:
        return ""
    return f'<ol class="research-numbered-list">{"".join(items)}</ol>'


def _render_table(headers: list[str], rows: list[list[str]]) -> str:
    if not headers:
        return ""
    parts = ['<table class="research-table"><thead><tr>']
    parts.extend(f"<th>{_format_cell(cell)}</th>" for cell in headers)
    parts.append("</tr></thead><tbody>")
    for row in rows:
        parts.append("<tr>")
        parts.extend(f"<td>{_format_cell(cell)}</td>" for cell in row)
        parts.append("</tr>")
    parts.append("</tbody></table>")
    return "".join(parts)


def _render_tab_table(lines: list[str]) -> str:
    rows = [[cell.strip() for cell in line.split("\t")] for line in lines if line.strip()]
    if not rows:
        return ""
    head, *body = rows
    return _render_table(head, body)


def _table_row_lines(raw_lines: list[str], row_starters: tuple[str, ...]) -> list[list[str]]:
    starters = set(row_starters)
    rows: list[list[str]] = []
    current: list[str] = []
    pending_cite: str | None = None

    for line in raw_lines:
        stripped = line.strip()
        if not stripped:
            continue
        if _CITE_RE.fullmatch(stripped):
            pending_cite = stripped
            continue
        if stripped in starters:
            if current:
                rows.append(current)
            current = [stripped]
            pending_cite = None
        else:
            if pending_cite:
                stripped = f"{stripped} {pending_cite}"
                pending_cite = None
            current.append(stripped)

    if current:
        rows.append(current)
    return rows


def _pack_table_row(lines: list[str], num_columns: int) -> list[str]:
    if not lines:
        return [""] * num_columns
    if len(lines) <= num_columns:
        return lines + [""] * (num_columns - len(lines))

    cells = [""] * num_columns
    cells[-1] = lines[-1]
    remaining = lines[:-1]
    split_at = num_columns - 2
    cells[:split_at] = remaining[:split_at]
    cells[split_at] = "\n\n".join(remaining[split_at:])
    return cells


def _render_vertical_table(marker: str, lines: list[str], num_columns: int) -> str:
    headers = [lines[0]] + lines[1:num_columns]
    row_starters = VERTICAL_TABLES[marker][1]
    raw_rows = _table_row_lines(lines[num_columns:], row_starters)
    rows = [_pack_table_row(row_lines, num_columns) for row_lines in raw_rows]
    return _render_table(headers, rows)


def _split_body_and_references(text: str) -> tuple[list[str], list[str]]:
    lines = text.splitlines()
    ref_start = None
    for idx, line in enumerate(lines):
        if line.strip() in REF_START_MARKERS and idx > 200:
            ref_start = idx
            break
    if ref_start is None:
        return lines, []
    body_lines = lines[:ref_start]
    ref_lines = [line.strip() for line in lines[ref_start:] if line.strip()]
    return body_lines, ref_lines


def _flush_paragraph(buffer: list[str], parts: list[str]) -> None:
    if not buffer:
        return
    if len(buffer) == 1:
        line = buffer[0].strip()
        if line in SECTION_H2:
            parts.append(f"<h2>{_format_inline(line)}</h2>")
            return
        if line in SECTION_H3:
            parts.append(f"<h3>{_format_inline(line)}</h3>")
            return
        if line.endswith(":") and len(line) < 80 and line[0].isupper():
            parts.append(f"<h4>{_format_inline(line)}</h4>")
            return
    parts.extend(f"<p>{_format_inline(line)}</p>" for line in buffer if line.strip())


def _render_body_lines(lines: list[str]) -> str:
    if not lines:
        return ""

    parts: list[str] = []
    parts.append(f'<h1 class="research-doc__title">{_format_inline(lines[0])}</h1>')

    i = 1
    paragraph_buffer: list[str] = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            _flush_paragraph(paragraph_buffer, parts)
            paragraph_buffer = []
            i += 1
            continue

        if stripped in SECTION_H2:
            _flush_paragraph(paragraph_buffer, parts)
            paragraph_buffer = []
            parts.append(f"<h2>{_format_inline(stripped)}</h2>")
            i += 1
            continue

        if stripped in SECTION_H3:
            _flush_paragraph(paragraph_buffer, parts)
            paragraph_buffer = []
            parts.append(f"<h3>{_format_inline(stripped)}</h3>")
            i += 1
            continue

        if stripped in _LIST_BLOCK_START:
            _flush_paragraph(paragraph_buffer, parts)
            paragraph_buffer = []
            i += 1
            list_lines: list[str] = []
            while i < len(lines):
                row = lines[i].strip()
                if row in _LIST_BLOCK_END:
                    i += 1
                    break
                if row:
                    list_lines.append(row)
                i += 1
            parts.append(_render_simple_numbered_list(list_lines))
            continue

        if stripped in _FLOW_BLOCK_START:
            _flush_paragraph(paragraph_buffer, parts)
            paragraph_buffer = []
            i += 1
            flow_lines: list[str] = []
            while i < len(lines):
                row = lines[i].strip()
                if row in _FLOW_BLOCK_END:
                    i += 1
                    break
                if row:
                    flow_lines.append(row)
                i += 1
            parts.append(_render_numbered_flow(flow_lines))
            continue

        if stripped.startswith("[Supraspinal"):
            _flush_paragraph(paragraph_buffer, parts)
            paragraph_buffer = []
            diagram: list[str] = []
            while i < len(lines) and lines[i].strip() and "\t" not in lines[i]:
                diagram.append(lines[i].rstrip())
                i += 1
                if i < len(lines) and lines[i].strip() in SECTION_H2:
                    break
            parts.append(f'<pre class="research-diagram">{_esc(chr(10).join(diagram))}</pre>')
            continue

        if stripped in VERTICAL_TABLES:
            _flush_paragraph(paragraph_buffer, parts)
            paragraph_buffer = []
            num_columns, _ = VERTICAL_TABLES[stripped]
            table_lines: list[str] = []
            while i < len(lines):
                row_stripped = lines[i].strip()
                if row_stripped in SECTION_H2:
                    break
                if row_stripped:
                    table_lines.append(row_stripped)
                i += 1
            parts.append(_render_vertical_table(stripped, table_lines, num_columns))
            continue

        if "\t" in line:
            _flush_paragraph(paragraph_buffer, parts)
            paragraph_buffer = []
            tab_lines: list[str] = []
            while i < len(lines) and lines[i].strip() and "\t" in lines[i]:
                tab_lines.append(lines[i])
                i += 1
            parts.append(_render_tab_table(tab_lines))
            continue

        if (
            stripped.endswith(":")
            and len(stripped) < 80
            and stripped[0].isupper()
            and not stripped.startswith("http")
        ):
            _flush_paragraph(paragraph_buffer, parts)
            paragraph_buffer = []
            parts.append(f"<h4>{_format_inline(stripped)}</h4>")
            i += 1
            continue

        paragraph_buffer.append(stripped)
        i += 1

    _flush_paragraph(paragraph_buffer, parts)
    return "\n".join(parts)


def _render_references(refs: list[Reference]) -> str:
    if not refs:
        return ""

    items = "".join(
        f'<li id="ref-{ref.index}" class="research-ref-item">{_format_ieee_reference(ref)}</li>'
        for ref in refs
    )
    return (
        '<h2 id="references">References</h2>'
        f'<ol class="research-references ieee-references">{items}</ol>'
    )


def research_doc_html(base_dir: Path | None = None) -> str:
    """Return sanitized HTML for the full research document."""
    if base_dir is None:
        from application.config import Config

        base_dir = Config.BASE_DIR

    path = base_dir / "ResearchDoc.md"
    if not path.is_file():
        return (
            '<p class="research-doc__missing">'
            "Research documentation is unavailable in this build."
            "</p>"
        )

    text = path.read_text(encoding="utf-8")
    body_lines, ref_lines = _split_body_and_references(text)
    refs = _parse_references(ref_lines)
    return "\n".join(
        part
        for part in (_render_body_lines(body_lines), _render_references(refs))
        if part
    )
