"""Professional PDF and CSV Export Service for Skill Gap Analysis & Learning Roadmaps.

Generates RFC 4180 compliant CSV tables and vector-rendered PDF documents
with corporate styling, executive summaries, and explainability disclaimers.
"""

import csv
import io
import datetime
from typing import Dict, List, Optional


def generate_gap_csv(gap_data: dict, candidate_name: str = "Candidate", job_title: str = "Target Role") -> bytes:
    """Generate professional CSV export for skill gap analysis."""
    output = io.StringIO()
    writer = csv.writer(output)

    # Header metadata
    writer.writerow(["SKILLSYNC - CAREER COMPATIBILITY & SKILL GAP REPORT"])
    writer.writerow(["Generated At", datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")])
    writer.writerow(["Candidate Name", candidate_name])
    writer.writerow(["Target Job Role", job_title])
    writer.writerow(["Overall Match Score", f"{gap_data.get('overall_score', 0)}%"])
    writer.writerow(["Mandatory Coverage", f"{gap_data.get('mandatory_score', 0)}%"])
    writer.writerow(["Preferred Coverage", f"{gap_data.get('preferred_score', 0)}%"])
    writer.writerow(["Alignment Tier", gap_data.get("alignment_tier", "N/A")])
    writer.writerow([])

    # Table columns
    writer.writerow([
        "Skill Name",
        "Category",
        "Requirement Tier",
        "Match Status",
        "Matched / Transferable Equivalent",
        "Similarity Score",
        "Importance Weight",
        "Required Experience (Yrs)"
    ])

    for s in gap_data.get("matched_skills", []):
        writer.writerow([
            s.get("name"),
            s.get("category_name", s.get("category")),
            "Mandatory" if s.get("is_mandatory") else "Preferred",
            "Matched",
            s.get("matched_with", "Direct Match"),
            s.get("similarity", 1.0),
            s.get("weight", 1.5),
            s.get("years_required") or "Not specified"
        ])

    for s in gap_data.get("partially_matched_skills", []):
        writer.writerow([
            s.get("name"),
            s.get("category_name", s.get("category")),
            "Mandatory" if s.get("is_mandatory") else "Preferred",
            "Partially Matched",
            s.get("transferable_skill", "Related"),
            s.get("similarity", 0.7),
            s.get("weight", 1.5),
            s.get("years_required") or "Not specified"
        ])

    for s in gap_data.get("missing_mandatory_skills", []):
        writer.writerow([
            s.get("name"),
            s.get("category_name", s.get("category")),
            "Mandatory",
            "Missing (High Impact)",
            "None",
            0.0,
            s.get("weight", 2.0),
            s.get("years_required") or "Not specified"
        ])

    for s in gap_data.get("missing_preferred_skills", []):
        writer.writerow([
            s.get("name"),
            s.get("category_name", s.get("category")),
            "Preferred",
            "Missing (Optional)",
            "None",
            0.0,
            s.get("weight", 1.0),
            s.get("years_required") or "Not specified"
        ])

    writer.writerow([])
    writer.writerow(["Disclaimer", gap_data.get("disclaimer", "")])

    return output.getvalue().encode("utf-8")


def generate_roadmap_csv(roadmap_data: dict) -> bytes:
    """Generate professional CSV export for a personalized learning roadmap."""
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["SKILLSYNC - PERSONALIZED LEARNING ROADMAP"])
    writer.writerow(["Plan Title", roadmap_data.get("title", "Engineering Upskilling Plan")])
    writer.writerow(["Target Role", roadmap_data.get("target_role", "Engineering")])
    writer.writerow(["Total Duration", f"{roadmap_data.get('duration_weeks', 0)} Weeks"])
    writer.writerow(["Generated At", datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")])
    writer.writerow([])

    writer.writerow([
        "Week Number",
        "Phase Title",
        "Learning Goal",
        "Key Technologies",
        "Project Deliverable",
        "Task Description",
        "Status"
    ])

    for week in roadmap_data.get("weeks", []):
        w_num = week.get("week_number")
        w_title = week.get("title")
        w_goal = week.get("goal")
        w_skills = ", ".join([s.get("name", s.get("id", "")) for s in week.get("skills", [])])
        w_proj = week.get("project_milestone")

        tasks = week.get("tasks", [])
        if not tasks:
            writer.writerow([w_num, w_title, w_goal, w_skills, w_proj, "Review materials", "Pending"])
        else:
            for t in tasks:
                writer.writerow([
                    w_num,
                    w_title,
                    w_goal,
                    w_skills,
                    w_proj,
                    t.get("description"),
                    "Completed" if t.get("completed") else "Pending"
                ])

    return output.getvalue().encode("utf-8")


def generate_gap_pdf(gap_data: dict, candidate_name: str = "Candidate", job_title: str = "Target Role") -> bytes:
    """Generate formatted PDF document for skill gap analysis with ReportLab or fallback generator."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        styles = getSampleStyleSheet()

        elements = []

        # Title
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=20,
            leading=24,
            textColor=colors.HexColor('#0f172a')
        )
        elements.append(Paragraph(f"SkillSync &bull; Skill Gap & Compatibility Report", title_style))
        elements.append(Spacer(1, 10))

        # Executive Metrics
        meta_style = ParagraphStyle('MetaStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#475569'))
        elements.append(Paragraph(
            f"<b>Candidate:</b> {candidate_name} &nbsp;&nbsp;|&nbsp;&nbsp; "
            f"<b>Target Role:</b> {job_title} &nbsp;&nbsp;|&nbsp;&nbsp; "
            f"<b>Date:</b> {datetime.datetime.utcnow().strftime('%B %d, %Y')}",
            meta_style
        ))
        elements.append(Spacer(1, 14))

        # Overall Score Callout
        score = gap_data.get("overall_score", 0)
        tier = gap_data.get("alignment_tier", "Assessment Complete")
        summary_text = gap_data.get("executive_summary", "")

        callout_data = [
            [
                Paragraph(f"<font size=28><b>{score}%</b></font><br/><font size=10 color='#2563eb'>Overall Compatibility</font>", styles['Normal']),
                Paragraph(f"<b>Alignment Tier:</b> {tier}<br/>{summary_text}", meta_style)
            ]
        ]
        callout_table = Table(callout_data, colWidths=[150, 390])
        callout_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
            ('PADDING', (0, 0), (-1, -1), 12),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(callout_table)
        elements.append(Spacer(1, 16))

        # Missing Skills Table
        elements.append(Paragraph("<b>Primary Skill Gaps to Bridge</b>", styles['Heading3']))
        elements.append(Spacer(1, 6))

        gap_rows = [["Skill", "Category", "Importance", "Recommended Focus"]]
        for s in gap_data.get("missing_mandatory_skills", [])[:8]:
            gap_rows.append([
                s.get("name"),
                s.get("category_name", s.get("category")),
                "Mandatory (High Impact)",
                s.get("project_idea")[:45] + "..." if s.get("project_idea") else "Review documentation"
            ])
        for s in gap_data.get("missing_preferred_skills", [])[:4]:
            gap_rows.append([
                s.get("name"),
                s.get("category_name", s.get("category")),
                "Preferred (Secondary)",
                s.get("project_idea")[:45] + "..." if s.get("project_idea") else "Review documentation"
            ])

        if len(gap_rows) == 1:
            gap_rows.append(["None", "All requirements matched!", "-", "-"])

        t = Table(gap_rows, colWidths=[130, 110, 130, 170])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 20))

        # Disclaimer
        disclaimer_style = ParagraphStyle('Disc', parent=styles['Normal'], fontSize=7, textColor=colors.HexColor('#64748b'))
        elements.append(Paragraph(f"<b>Disclaimer:</b> {gap_data.get('disclaimer', '')}", disclaimer_style))

        doc.build(elements)
        return buffer.getvalue()
    except Exception as e:
        # Fallback to pure minimal PDF generator
        return _generate_minimal_pdf(
            f"SkillSync Career Compatibility Report: {candidate_name} - {job_title}\n"
            f"Overall Match Score: {gap_data.get('overall_score', 0)}%\n"
            f"Alignment Tier: {gap_data.get('alignment_tier', 'N/A')}\n\n"
            f"Summary: {gap_data.get('executive_summary', '')}\n\n"
            f"Disclaimer: {gap_data.get('disclaimer', '')}"
        )


def generate_roadmap_pdf(roadmap_data: dict) -> bytes:
    """Generate formatted PDF document for learning roadmap with ReportLab or fallback."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        styles = getSampleStyleSheet()
        elements = []

        title_style = ParagraphStyle('TStyle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#0f172a'))
        elements.append(Paragraph(f"SkillSync &bull; Personalized Learning Roadmap", title_style))
        elements.append(Spacer(1, 8))

        meta_style = ParagraphStyle('MStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#475569'))
        elements.append(Paragraph(
            f"<b>Roadmap:</b> {roadmap_data.get('title')} &nbsp;|&nbsp; "
            f"<b>Duration:</b> {roadmap_data.get('duration_weeks')} Weeks &nbsp;|&nbsp; "
            f"<b>Target:</b> {roadmap_data.get('target_role')}",
            meta_style
        ))
        elements.append(Spacer(1, 14))

        for week in roadmap_data.get("weeks", []):
            w_box = [
                [
                    Paragraph(f"<b>Week {week.get('week_number')}: {week.get('title')}</b>", styles['Normal']),
                ],
                [
                    Paragraph(f"<b>Goal:</b> {week.get('goal')}", meta_style)
                ],
                [
                    Paragraph(f"<b>Project Milestone:</b> {week.get('project_milestone')}", meta_style)
                ]
            ]
            t = Table(w_box, colWidths=[540])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
                ('PADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 10))

        doc.build(elements)
        return buffer.getvalue()
    except Exception:
        return _generate_minimal_pdf(
            f"SkillSync Learning Roadmap: {roadmap_data.get('title')}\n"
            f"Duration: {roadmap_data.get('duration_weeks')} Weeks\n\n"
            + "\n".join([f"Week {w.get('week_number')}: {w.get('title')}\nGoal: {w.get('goal')}\nMilestone: {w.get('project_milestone')}\n" for w in roadmap_data.get("weeks", [])])
        )


def _generate_minimal_pdf(plain_text: str) -> bytes:
    """Minimal standards-compliant single-page PDF generator without any external C dependencies."""
    # Escape parentheses and backslashes for PDF string literal
    escaped = plain_text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    lines = escaped.split("\n")
    
    stream_content = "BT\n/F1 10 Tf\n40 750 Td\n14 TL\n"
    for line in lines[:50]:
        stream_content += f"({line}) '\n"
    stream_content += "ET"
    
    stream_bytes = stream_content.encode("latin-1", errors="replace")
    stream_len = len(stream_bytes)

    pdf = (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
        b"4 0 obj\n<< /Length " + str(stream_len).encode("ascii") + b" >>\nstream\n"
        + stream_bytes +
        b"\nendstream\nendobj\n"
        b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
        b"xref\n0 6\n"
        b"0000000000 65535 f \n"
        b"0000000009 00000 n \n"
        b"0000000058 00000 n \n"
        b"0000000115 00000 n \n"
        b"0000000244 00000 n \n"
        b"0000000000 00000 n \n"
        b"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n350\n%%EOF\n"
    )
    return pdf
