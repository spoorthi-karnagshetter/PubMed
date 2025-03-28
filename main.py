import argparse
from pubmed_fetcher import fetch_papers, save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed based on a search query.")
    parser.add_argument("query", type=str, help="Search query for PubMed (e.g., 'heart disease')")
    parser.add_argument("-f", "--file", type=str, default="result.csv", help="Output CSV filename (default: result.csv)")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()

    try:
        papers = fetch_papers(args.query, args.debug)
        if papers:
            save_to_csv(papers, args.file)
            print(f"Results saved to {args.file}")
        else:
            print("No results found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
