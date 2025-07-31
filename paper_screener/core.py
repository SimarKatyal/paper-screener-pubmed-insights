import requests
import pandas as pd
import xml.etree.ElementTree as ET
import re
from typing import List, Dict, Optional

# Keywords used to detect non-academic affiliations
NON_ACADEMIC_KEYWORDS = [
    'pharma', 'biotech', 'inc', 'ltd', 'gmbh', 'corp',
    'therapeutics', 'labs', 'llc', 'co.', 'plc'
]

def search_pubmed(query: str, retmax: int = 20) -> List[str]:
    """Search PubMed using a query and return list of PubMed IDs."""
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax
    }
    response.raise_for_status()
    return response.json()["esearchresult"]["idlist"]

def fetch_articles(pubmed_ids: List[str]) -> List[ET.Element]:
    """Fetch article metadata from PubMed using ID list."""
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml"
    }
    response.raise_for_status()
    root = ET.fromstring(response.text)
    return root.findall(".//PubmedArticle")

def is_non_academic(affiliation: str) -> bool:
    """Check if an affiliation is non-academic using keyword heuristics."""
    return any(keyword in affiliation.lower() for keyword in NON_ACADEMIC_KEYWORDS)

def extract_email(text: str) -> Optional[str]:
    """Extract email from text using regex."""
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match.group(0) if match else None

def parse_article(article: ET.Element, debug: bool = False) -> Optional[Dict[str, str]]:
    """Parse one article, extract fields only if it has non-academic authors."""
    pmid = article.findtext(".//PMID")
    title = article.findtext(".//ArticleTitle")
    pub_date = article.findtext(".//PubDate/Year") or "Unknown"

    non_acad_authors = []
    affiliations = []
    email = ""

    for author in article.findall(".//Author"):
        name = f"{author.findtext('ForeName') or ''} {author.findtext('LastName') or ''}".strip()
        affiliation_node = author.find(".//AffiliationInfo")

        if affiliation_node is not None:
            affiliation = affiliation_node.findtext("Affiliation")
            if affiliation:
                if is_non_academic(affiliation):
                    non_acad_authors.append(name)
                    affiliations.append(affiliation)
                if not email:
                    email = extract_email(affiliation) or email

    if not non_acad_authors:
        if debug:
            print(f"🔍 Excluded PMID {pmid} — Academic only.")
        return None

    return {
        "PubmedID": pmid,
        "Title": title,
        "Publication Date": pub_date,
        "Non-academic Author(s)": "; ".join(non_acad_authors),
        "Company Affiliation(s)": "; ".join(affiliations),
        "Corresponding Author Email": email
    }

def run_pipeline(query: str, retmax: int = 20, debug: bool = False) -> pd.DataFrame:
    """End-to-end process: search, fetch, parse, filter, return DataFrame."""
    pubmed_ids = search_pubmed(query, retmax)
    if debug:
        print(f"🔎 Found {len(pubmed_ids)} articles for query: '{query}'")

    articles = fetch_articles(pubmed_ids)
    results = []

    for article in articles:
        data = parse_article(article, debug=debug)
        if data:
            results.append(data)

    df = pd.DataFrame(results)
    return df