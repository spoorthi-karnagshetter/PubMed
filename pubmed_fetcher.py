import requests
import csv
import xml.etree.ElementTree as ET

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def fetch_papers(query, debug=False):
    try:
        # Step 1: Search PubMed for articles matching the query
        search_url = f"{BASE_URL}esearch.fcgi?db=pubmed&term={query}&retmax=10&usehistory=y"
        search_response = requests.get(search_url)
        search_response.raise_for_status()

        search_root = ET.fromstring(search_response.text)
        ids = [id_elem.text for id_elem in search_root.findall(".//Id")]

        if not ids:
            return []

        # Step 2: Fetch detailed information about the articles
        ids_str = ",".join(ids)
        fetch_url = f"{BASE_URL}efetch.fcgi?db=pubmed&id={ids_str}&retmode=xml"
        fetch_response = requests.get(fetch_url)
        fetch_response.raise_for_status()

        fetch_root = ET.fromstring(fetch_response.text)
        papers = []

        for article in fetch_root.findall(".//PubmedArticle"):
            pubmed_id = article.find(".//PMID").text
            title_elem = article.find(".//ArticleTitle")
            title = title_elem.text if title_elem is not None else "N/A"

            date_elem = article.find(".//PubDate")
            pub_date = date_elem.find("Year").text if date_elem is not None else "Unknown"

            authors_elem = article.findall(".//Author")
            non_academic_authors = []
            company_affiliations = []
            corresponding_email = "N/A"

            for author in authors_elem:
                affiliation = author.find(".//Affiliation")
                if affiliation is not None:
                    affiliation_text = affiliation.text.lower()
                    if any(company in affiliation_text for company in ["inc", "ltd", "gmbh", "corp", "biotech", "pharma"]):
                        company_affiliations.append(author.find("LastName").text)
                    else:
                        non_academic_authors.append(author.find("LastName").text)

                email_elem = author.find(".//ElectronicAddress")
                if email_elem is not None:
                    corresponding_email = email_elem.text

            papers.append([
                pubmed_id,
                title,
                pub_date,
                "; ".join(non_academic_authors) if non_academic_authors else "N/A",
                "; ".join(company_affiliations) if company_affiliations else "N/A",
                corresponding_email
            ])

        return papers

    except requests.RequestException as e:
        print(f"Error fetching data from PubMed API: {e}")
        return []

def save_to_csv(data, filename="result.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["PubmedID", "Title", "Publication Date", "Non-Academic Authors", "Company Affiliations", "Corresponding Author Email"])
        writer.writerows(data)
