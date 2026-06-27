"""
Tool implementations for the Research Brief Agent.
All network tools are mocked with realistic sample data.
"""

import json
import os
from datetime import datetime


MOCK_SEARCH_RESULTS = {
    "artificial intelligence in healthcare": [
        {
            "title": "AI Diagnostics: FDA Approvals Surge in 2024",
            "url": "https://www.healthtech-review.com/ai-fda-approvals-2024",
            "snippet": "The FDA approved over 170 AI-enabled medical devices in 2024, a 40% increase from 2023. Key areas include radiology, pathology, and cardiology.",
        },
        {
            "title": "Google DeepMind AlphaFold3 Revolutionises Drug Discovery",
            "url": "https://www.nature.com/articles/alphafold3-drug-discovery",
            "snippet": "AlphaFold3 can now predict interactions between proteins, DNA, RNA, and small molecules, cutting early-stage drug discovery timelines by up to 60%.",
        },
        {
            "title": "AI in Clinical Decision Support: A 2025 Overview",
            "url": "https://www.nejm.org/ai-clinical-decision-support-2025",
            "snippet": "Machine learning models are outperforming junior doctors in triage accuracy across 12 major hospital systems in the US and UK.",
        },
        {
            "title": "Ethical Concerns Around Bias in Medical AI",
            "url": "https://www.bmj.com/content/ai-bias-medical-systems",
            "snippet": "Studies show AI models trained predominantly on Western patient data perform 23% worse on under-represented ethnic groups, raising equity concerns.",
        },
    ],
    "remote work productivity": [
        {
            "title": "Stanford Study: Remote Workers 13% More Productive",
            "url": "https://siepr.stanford.edu/research/remote-work-productivity",
            "snippet": "Nicholas Bloom's landmark study found remote workers completed 13.5% more calls than office counterparts, with lower attrition rates.",
        },
        {
            "title": "The Hybrid Work Model: Best of Both Worlds?",
            "url": "https://hbr.org/2024/hybrid-work-model-outcomes",
            "snippet": "Companies adopting 2-3 day office schedules report 18% higher employee satisfaction compared to fully remote or fully in-office arrangements.",
        },
        {
            "title": "Remote Work Technology Stack in 2025",
            "url": "https://techcrunch.com/2025/remote-work-tech-stack",
            "snippet": "Async-first tools like Notion, Loom, and Linear have displaced synchronous video calls as the primary collaboration medium for distributed teams.",
        },
    ],
    "default": [
        {
            "title": "Overview and Recent Developments",
            "url": "https://www.example-research.com/overview",
            "snippet": "A comprehensive overview of the latest trends, challenges, and opportunities in this field based on 2024-2025 research.",
        },
        {
            "title": "Industry Analysis Report 2025",
            "url": "https://www.industry-analysis.com/report-2025",
            "snippet": "Market experts highlight three macro trends shaping the landscape: automation, decentralisation, and sustainability pressures.",
        },
        {
            "title": "Expert Roundtable: Key Predictions",
            "url": "https://www.expert-forum.com/predictions",
            "snippet": "Leading practitioners predict significant disruption within the next two years, driven by regulatory changes and technological breakthroughs.",
        },
    ],
}

MOCK_PAGE_CONTENT = {
    "https://www.healthtech-review.com/ai-fda-approvals-2024": """
AI Diagnostics: FDA Approvals Surge in 2024
============================================
Published: March 2025 | Source: HealthTech Review

The U.S. Food and Drug Administration (FDA) approved 172 AI-enabled medical devices in 2024,
marking a 40% year-on-year increase. This acceleration reflects growing clinical confidence
in algorithm-assisted diagnostics.

Key Approval Categories:
- Radiology (CT, MRI interpretation): 68 devices
- Pathology (digital slide analysis): 31 devices
- Cardiology (ECG and echo interpretation): 29 devices
- Ophthalmology (retinal screening): 22 devices
- Other specialties: 22 devices

Notable approvals include:
- Aidoc's BriefCase platform for multi-condition radiology triage
- PathAI's breast cancer grading system, shown to reduce pathologist review time by 47%
- Apple Watch's AFib detection algorithm, now cleared for clinical decision support

Regulatory Outlook:
The FDA's proposed "predetermined change control plan" framework allows AI devices to adapt
to new data without full re-review, expected to further accelerate innovation in 2025-2026.
""",
    "https://www.nature.com/articles/alphafold3-drug-discovery": """
AlphaFold3 and the New Era of Drug Discovery
=============================================
Published: Nature, January 2025

Google DeepMind's AlphaFold3 extends beyond its predecessor's protein-structure prediction
to model interactions across the full range of biological molecules.

Core Capabilities:
- Protein-protein interaction prediction (PPI): 89% accuracy on benchmark datasets
- Protein-ligand docking: outperforms traditional docking software by 26%
- Nucleic acid structure: first model to accurately predict RNA tertiary structures

Impact on Drug Discovery Timelines:
Traditional hit identification: 18-24 months -> With AlphaFold3: 6-9 months
Lead optimisation: 12-18 months -> With AlphaFold3: 4-6 months

Early Adopters:
- Isomorphic Labs (DeepMind spinout): 3 novel targets in clinical trial within 18 months
- AstraZeneca: integrated into oncology pipeline, reducing screening costs by 40M GBP annually
- Novartis: using for GPCR drug discovery, historically one of the hardest protein families
""",
    "default": """
Article Content
===============
Published: 2024-2025

This source provides detailed analysis of recent developments in the field.
Key findings include significant growth trends, adoption challenges, and
opportunities for innovation. Experts highlight the importance of responsible
implementation and stakeholder alignment.

Main Points:
1. Market adoption is accelerating faster than regulatory frameworks
2. Early movers are capturing disproportionate competitive advantage
3. Workforce upskilling remains the primary implementation bottleneck
4. Return on investment is strongest in automation-heavy use cases
""",
}


def search_web(query: str, num_results: int = 3) -> dict:
    """Search the web for information on a query."""
    query_lower = query.lower()
    results = None
    for key in MOCK_SEARCH_RESULTS:
        if key == "default":
            continue
        if any(word in query_lower for word in key.split()):
            results = MOCK_SEARCH_RESULTS[key]
            break
    if results is None:
        results = MOCK_SEARCH_RESULTS["default"]
    return {
        "query": query,
        "results": results[:num_results],
        "total_found": len(results),
    }


def read_url(url: str) -> dict:
    """Fetch and return the main text content of a URL."""
    content = MOCK_PAGE_CONTENT.get(url, MOCK_PAGE_CONTENT["default"])
    return {
        "url": url,
        "content": content.strip(),
        "word_count": len(content.split()),
        "fetched_at": datetime.now().isoformat(),
    }


def write_report(filename: str, content: str) -> dict:
    """Save a research brief to a file."""
    os.makedirs("reports", exist_ok=True)
    path = os.path.join("reports", filename)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return {"path": path, "bytes_written": len(content.encode("utf-8")), "success": True}
    except Exception as e:
        return {"path": path, "bytes_written": 0, "success": False, "error": str(e)}


TOOLS = [
    {
        "name": "search_web",
        "description": (
            "Search the web for information on a topic. Returns a list of results "
            "with title, URL, and snippet. Use this to find relevant sources."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query to run"},
                "num_results": {"type": "integer", "description": "Number of results to return (default 3)", "default": 3},
            },
            "required": ["query"],
        },
    },
    {
        "name": "read_url",
        "description": "Fetch and read the main text content of a URL.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The URL to fetch and read"}
            },
            "required": ["url"],
        },
    },
    {
        "name": "write_report",
        "description": "Save the finished research brief to a file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Filename for the report (e.g. 'ai-healthcare-brief.md')"},
                "content": {"type": "string", "description": "The full markdown content of the research brief"},
            },
            "required": ["filename", "content"],
        },
    },
]

TOOL_FUNCTIONS = {
    "search_web": search_web,
    "read_url": read_url,
    "write_report": write_report,
}
