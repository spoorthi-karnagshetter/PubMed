# PubMed Paper Fetcher

This project allows users to fetch research papers from **PubMed** using a search query and save the results in a CSV file.

## Features
- Fetch research papers from **PubMed** based on user queries.
- Extract relevant details, including **title, publication date, non-academic authors, company affiliations, and corresponding author emails**.
- Save the results to a **CSV file**.
- Command-line interface using **Poetry** for dependency management.
- Debug mode available for troubleshooting.
- **Utilizes Large Language Model (LLM):** OpenAI's ChatGPT for generating responses and documentation.

## Installation and Setup

### Step 1: Install Poetry
Poetry is used for dependency management. Run the following command in your terminal:
```sh
curl -sSL https://install.python-poetry.org | python3 -
```
If you are on **Windows** and encounter issues, install Poetry using:
```sh
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

### **Step 2: Clone the Repository**
```sh
git clone <repository-url>
cd test
```

### **Step 3: Install Dependencies**
```sh
poetry install
```

## Running the Project

### **Fetch Papers and Save to CSV**
To fetch research papers based on a query and save the results to a CSV file, use:
```sh
poetry run python main.py "cancer treatment" -f result.csv
```
### **Enable Debug Mode**
To troubleshoot errors, use the `-d` flag:
```sh
poetry run python main.py "cancer treatment" -d
```

## Project Structure
```
test/
│── main.py            # Main execution script
│── pubmed_fetcher.py  # Fetches and processes data from PubMed
│── result.csv         # Output file for fetched papers
│── poetry.toml        # Poetry configuration file
│── pyproject.toml     # Dependencies and project details
│── README.md          # Documentation
```

## Output Format
The CSV file (`result.csv`) will have the following columns:
- **PubmedID**: Unique identifier for the paper.
- **Title**: Title of the paper.
- **Publication Date**: Date the paper was published.
- **Non-Academic Authors**: Names of authors affiliated with non-academic institutions.
- **Company Affiliations**: Names of pharmaceutical/biotech companies.
- **Corresponding Author Email**: Email address of the corresponding author.

## LLM Used
- This project leverages **OpenAI’s ChatGPT** for generating parts of the documentation, explanations, and structuring the implementation.

## License
This project is licensed under the **MIT License**.


