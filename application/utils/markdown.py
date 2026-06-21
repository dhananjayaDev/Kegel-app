"""Minimal markdown-to-HTML for plan rendering."""

from __future__ import annotations

import html
import re


def render_markdown(text: str) -> str:
    if not text:
        return ""
    lines = text.split("\n")
    output: list[str] = []
    in_list = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_list:
                output.append("</ul>")
                in_list = False
            continue

        if stripped.startswith("### "):
            if in_list:
                output.append("</ul>")
                in_list = False
            output.append(f"<h3>{html.escape(stripped[4:])}</h3>")
        elif stripped.startswith("## "):
            if in_list:
                output.append("</ul>")
                in_list = False
            output.append(f"<h2>{html.escape(stripped[3:])}</h2>")
        elif stripped.startswith("# "):
            if in_list:
                output.append("</ul>")
                in_list = False
            output.append(f"<h1>{html.escape(stripped[2:])}</h1>")
        elif stripped.startswith("- "):
            if not in_list:
                output.append("<ul>")
                in_list = True
            content = stripped[2:]
            content = re.sub(
                r"\*\*(.+?)\*\*",
                lambda m: f"<strong>{html.escape(m.group(1))}</strong>",
                content,
            )
            if "**" not in stripped:
                content = html.escape(stripped[2:])
            output.append(f"<li>{content}</li>")
        else:
            if in_list:
                output.append("</ul>")
                in_list = False
            escaped = html.escape(stripped)
            escaped = re.sub(
                r"\*\*(.+?)\*\*",
                lambda m: f"<strong>{m.group(1)}</strong>",
                escaped,
            )
            if stripped.startswith("*") and stripped.endswith("*"):
                output.append(f"<p><em>{html.escape(stripped.strip('*'))}</em></p>")
            else:
                output.append(f"<p>{escaped}</p>")

    if in_list:
        output.append("</ul>")
    return "\n".join(output)
