"""
Tool implementations for the Lead Enrichment Agent.
Uses mock company data that realistically simulates a business lookup API.
"""

import csv
import json
import os
from datetime import datetime

MOCK_COMPANY_DATA = {
    "stripe": {
        "name": "Stripe",
        "industry": "Financial Technology",
        "size": "5,000-10,000 employees",
        "website": "https://stripe.com",
        "headquarters": "San Francisco, CA",
        "founded": 2010,
        "contact_name": "Patrick Collison",
        "contact_title": "CEO & Co-Founder",
        "contact_email": "info@stripe.com",
        "description": "Payment infrastructure for the internet",
    },
    "notion": {
        "name": "Notion",
        "industry": "Productivity Software",
        "size": "500-1,000 employees",
        "website": "https://notion.so",
        "headquarters": "San Francisco, CA",
        "founded": 2016,
        "contact_name": "Ivan Zhao",
        "contact_title": "CEO & Co-Founder",
        "contact_email": "contact@makenotion.com",
        "description": "All-in-one workspace for notes, docs, and projects",
    },
    "linear": {
        "name": "Linear",
        "industry": "Project Management Software",
        "size": "50-200 employees",
        "website": "https://linear.app",
        "headquarters": "San Francisco, CA",
        "founded": 2019,
        "contact_name": "Karri Saarinen",
        "contact_title": "CEO & Co-Founder",
        "contact_email": "hello@linear.app",
        "description": "Issue tracking built for modern software teams",
    },
    "vercel": {
        "name": "Vercel",
        "industry": "Cloud Infrastructure",
        "size": "500-1,000 employees",
        "website": "https://vercel.com",
        "headquarters": "San Francisco, CA",
        "founded": 2015,
        "contact_name": "Guillermo Rauch",
        "contact_title": "CEO & Founder",
        "contact_email": "support@vercel.com",
        "description": "Frontend cloud platform and deployment network",
    },
    "figma": {
        "name": "Figma",
        "industry": "Design Software",
        "size": "1,000-5,000 employees",
        "website": "https://figma.com",
        "headquarters": "San Francisco, CA",
        "founded": 2012,
        "contact_name": "Dylan Field",
        "contact_title": "CEO & Co-Founder",
        "contact_email": "hello@figma.com",
        "description": "Collaborative interface design tool",
    },
    "retool": {
        "name": "Retool",
        "industry": "Low-Code Development",
        "size": "200-500 employees",
        "website": "https://retool.com",
        "headquarters": "San Francisco, CA",
        "founded": 2017,
        "contact_name": "David Hsu",
        "contact_title": "CEO & Co-Founder",
        "contact_email": "hello@retool.com",
        "description": "Low-code platform for building internal tools",
    },
}

SAMPLE_COMPANIES_CSV = """company_name
Stripe
Notion
Linear
Vercel
Figma
Retool
"""


def read_companies_csv(filepath: str = "companies.csv") -> dict:
    """
    Read a list of company names from a CSV file.
    If the file does not exist, creates a sample file to work with.

    Args:
        filepath: Path to the CSV file with a 'company_name' column

    Returns:
        dict with 'companies' list and 'count'
    """
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(SAMPLE_COMPANIES_CSV)
        print(f"  [Created sample {filepath}]")

    companies = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("company_name", "").strip()
                if name:
                    companies.append(name)
    except Exception as e:
        return {"companies": [], "count": 0, "error": str(e)}

    return {"companies": companies, "count": len(companies), "filepath": filepath}


def lookup_company(company_name: str) -> dict:
    """
    Look up enrichment data for a company by name.
    Returns industry, size, website, and a contact name.

    Args:
        company_name: The company name to look up

    Returns:
        dict with company details or a 'not_found' flag
    """
    key = company_name.lower().strip()
    data = MOCK_COMPANY_DATA.get(key)
    if data:
        return {"found": True, **data}
    # Return partial data for unknown companies
    return {
        "found": True,
        "name": company_name,
        "industry": "Technology",
        "size": "Unknown",
        "website": f"https://www.{key.replace(' ', '')}.com",
        "headquarters": "Unknown",
        "founded": None,
        "contact_name": "General Enquiries",
        "contact_title": "N/A",
        "contact_email": f"info@{key.replace(' ', '')}.com",
        "description": "No description available",
    }


def save_results(filepath: str, row: dict) -> dict:
    """
    Append an enriched company row to a CSV output file.
    Creates the file with headers if it does not exist.

    Args:
        filepath: Path to the output CSV file
        row: Dict with enriched company data

    Returns:
        dict with success status and row count
    """
    fieldnames = [
        "name", "industry", "size", "website",
        "headquarters", "contact_name", "contact_title",
        "contact_email", "description",
    ]
    file_exists = os.path.exists(filepath)
    try:
        with open(filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)

        # Count rows
        with open(filepath, "r", encoding="utf-8") as f:
            row_count = sum(1 for _ in f) - 1  # subtract header

        return {"success": True, "filepath": filepath, "total_rows": row_count}
    except Exception as e:
        return {"success": False, "filepath": filepath, "error": str(e)}


TOOLS = [
    {
        "name": "read_companies_csv",
        "description": "Read a list of company names from the input CSV file. Call this first to get the list to enrich.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the CSV file (default: companies.csv)",
                    "default": "companies.csv",
                }
            },
            "required": [],
        },
    },
    {
        "name": "lookup_company",
        "description": "Look up enrichment data for a single company: industry, size, website, and contact name.",
        "input_schema": {
            "type": "object",
            "properties": {
                "company_name": {
                    "type": "string",
                    "description": "The company name to look up",
                }
            },
            "required": ["company_name"],
        },
    },
    {
        "name": "save_results",
        "description": "Append one enriched company row to the output CSV file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the output CSV file (default: enriched_leads.csv)",
                },
                "row": {
                    "type": "object",
                    "description": "Dict of enriched company data to save",
                },
            },
            "required": ["filepath", "row"],
        },
    },
]

TOOL_FUNCTIONS = {
    "read_companies_csv": read_companies_csv,
    "lookup_company": lookup_company,
    "save_results": save_results,
}
