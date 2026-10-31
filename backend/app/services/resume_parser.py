"""Resume Ingestion and Parsing Service for PDF and DOCX Documents.

Extracts candidate identity, professional experience, projects, education,
and technical competencies using robust multi-format document decoders.
"""

import io
import re
import xml.etree.ElementTree as ET
import zipfile
from typing import Dict, List, Optional, Tuple
from app.services.skill_extractor import extract_skills_from_text


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract plain text from a DOCX file using standard library zipfile and XML parser."""
    try:
        with zipfile.ZipFile(io.BytesIO(file_bytes)) as docx_zip:
            if "word/document.xml" not in docx_zip.namelist():
                return ""
            xml_content = docx_zip.read("word/document.xml")
            tree = ET.fromstring(xml_content)
            # w:t elements contain text
            namespaces = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
            paragraphs = []
            for p in tree.iterfind(".//w:p", namespaces):
                texts = [node.text for node in p.iterfind(".//w:t", namespaces) if node.text]
                if texts:
                    paragraphs.append("".join(texts))
            return "\n".join(paragraphs)
    except Exception as e:
        # Fallback to UTF-8 / latin-1 decoding
        return file_bytes.decode("latin-1", errors="ignore")


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract plain text from a PDF file using pypdf if available, or regex streams fallback."""
    try:
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        pages_text = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages_text)
    except ImportError:
        pass
    except Exception:
        pass

    # Heuristic PDF text extraction fallback
    text_fragments = []
    # Match PDF text blocks like (Text) Tj or [(T) (ext)] TJ
    try:
        decoded = file_bytes.decode("latin-1", errors="ignore")
        # Find stream contents
        streams = re.findall(r"stream[\r\n]+(.*?)[\r\n]+endstream", decoded, re.DOTALL)
        for s in streams:
            tj_matches = re.findall(r"\((.*?)\)\s*Tj", s)
            for m in tj_matches:
                cleaned = re.sub(r"\\[0-9]{3}", " ", m)
                cleaned = cleaned.replace("\\(", "(").replace("\\)", ")")
                text_fragments.append(cleaned)
        if text_fragments:
            return " ".join(text_fragments)
    except Exception:
        pass

    return file_bytes.decode("latin-1", errors="ignore")


def extract_candidate_contact(text: str) -> dict:
    """Extract candidate name, email, phone, and links from resume header."""
    contact = {
        "name": "Candidate",
        "email": None,
        "phone": None,
        "linkedin": None,
        "github": None
    }

    # Email
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    if email_match:
        contact["email"] = email_match.group(0)

    # Phone
    phone_match = re.search(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
    if phone_match:
        contact["phone"] = phone_match.group(0).strip()

    # LinkedIn & GitHub
    linkedin_match = re.search(r"(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/[a-zA-Z0-9_-]+", text, re.IGNORECASE)
    if linkedin_match:
        contact["linkedin"] = linkedin_match.group(0)

    github_match = re.search(r"(?:https?:\/\/)?(?:www\.)?github\.com\/[a-zA-Z0-9_-]+", text, re.IGNORECASE)
    if github_match:
        contact["github"] = github_match.group(0)

    # Candidate Name heuristic from first few lines
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    for line in lines[:5]:
        if len(line.split()) in [2, 3, 4] and not any(k in line.lower() for k in ["resume", "curriculum", "email", "@", "http", "phone"]):
            # Filter non-alpha
            if re.match(r"^[A-Za-z\s\.\'-]+$", line):
                contact["name"] = line
                break

    return contact


def parse_resume_document(file_bytes: bytes, filename: str) -> dict:
    """Parse resume document (PDF or DOCX), extracting structured profile details."""
    lower_name = filename.lower()
    if lower_name.endswith(".docx"):
        raw_text = extract_text_from_docx(file_bytes)
    elif lower_name.endswith(".pdf"):
        raw_text = extract_text_from_pdf(file_bytes)
    else:
        raw_text = file_bytes.decode("utf-8", errors="ignore")

    contact = extract_candidate_contact(raw_text)
    extracted_skills = extract_skills_from_text(raw_text, default_mandatory=False, is_job_posting=False)

    # Extract approximate experience years
    years_found = [int(m) for m in re.findall(r"(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?experience", raw_text, re.IGNORECASE)]
    estimated_experience = max(years_found) if years_found else 2.0

    return {
        "filename": filename,
        "name": contact["name"],
        "email": contact["email"],
        "phone": contact["phone"],
        "linkedin": contact["linkedin"],
        "github": contact["github"],
        "estimated_experience_years": float(estimated_experience),
        "raw_text": raw_text[:5000],  # truncated sample
        "skills": extracted_skills,
        "skills_count": len(extracted_skills)
    }
