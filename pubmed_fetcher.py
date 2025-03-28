import requests
import xml.etree.ElementTree as ET
import csv
from typing import List, Dict

# PubMed API URLs
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
PUBMED_DB = "pubmed"

# Keywords to identify company affiliations
COMPANY_KEYWORDS = ["Inc", "Ltd", "LLC", "GmbH", "Biotech", "Pharma", "Corporation"]

def fetch_papers(query: str) -> List[Dict]:
    """Fetch papers from PubMed based on a query."""
    
    # Step 1: Get PubMed IDs for the query
    search_params = {
        "db": PUBMED_DB,
        "term": query,
        "retmax": 10,  # Number of results to return
        "retmode": "json"
    }
    
    search_response = requests.get(PUBMED_SEARCH_URL, params=search_params)
    if search_response.status_code != 200:
        raise Exception("Failed to search PubMed API.")
    
    search_data = search_response.json()
    pubmed_ids = search_data.get("esearchresult", {}).get("idlist", [])
    if not pubmed_ids:
        raise Exception("No results found for this query.")

    # Step 2: Fetch detailed article information using EFetch
    fetch_params = {
        "db": PUBMED_DB,
        "id": ",".join(pubmed_ids),
        "retmode": "xml"
    }
    
    fetch_response = requests.get(PUBMED_FETCH_URL, params=fetch_params)
    if fetch_response.status_code != 200:
        raise Exception("Failed to fetch article details from PubMed API.")
    
    root = ET.fromstring(fetch_response.text)
    papers = []

    for article in root.findall(".//PubmedArticle"):
        pmid = article.find(".//PMID").text
        title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "N/A"
        pub_date = article.find(".//PubDate/Year")
        pub_date = pub_date.text if pub_date is not None else "N/A"

        # Extract authors and affiliations
        non_academic_authors = []
        company_affiliations = []
        corresponding_author_email = "N/A"

        for author in article.findall(".//Author"):
            lastname = author.find("LastName")
            firstname = author.find("ForeName")
            author_name = f"{firstname.text} {lastname.text}" if firstname is not None and lastname is not None else "N/A"

            affiliation = author.find(".//Affiliation")
            if affiliation is not None:
                affiliation_text = affiliation.text

                # Identify company affiliations
                if any(keyword in affiliation_text for keyword in COMPANY_KEYWORDS):
                    company_affiliations.append(affiliation_text)

                # Identify non-academic authors
                elif not any(term in affiliation_text.lower() for term in ["university", "college", "institute", "school"]):
                    non_academic_authors.append(author_name)

            # Extract corresponding author email (if available)
            email = author.find(".//Email")
            if email is not None:
                corresponding_author_email = email.text

        papers.append({
            "PubmedID": pmid,
            "Title": title,
            "Publication Date": pub_date,
            "Non-Academic Authors": ", ".join(non_academic_authors) if non_academic_authors else "N/A",
            "Company Affiliations": ", ".join(company_affiliations) if company_affiliations else "N/A",
            "Corresponding Author Email": corresponding_author_email
        })

    return papers

def save_to_csv(papers: List[Dict], filename: str = "result.csv") -> None:
    """Save results to a CSV file."""
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["PubmedID", "Title", "Publication Date", "Non-Academic Authors", "Company Affiliations", "Corresponding Author Email"])
        
        for paper in papers:
            writer.writerow([
                paper.get("PubmedID", "N/A"),
                paper.get("Title", "N/A"),
                paper.get("Publication Date", "N/A"),
                paper.get("Non-Academic Authors", "N/A"),
                paper.get("Company Affiliations", "N/A"),
                paper.get("Corresponding Author Email", "N/A")
            ])
