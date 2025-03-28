import argparse
from pubmed_fetcher import fetch_papers, save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="PubMed search query.")
    parser.add_argument("-f", "--file", type=str, help="Filename to save the results (CSV).", default="result.csv")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    args = parser.parse_args()
    
    try:
        papers = fetch_papers(args.query)
        save_to_csv(papers, args.file)
        print(f"Results saved to {args.file}")
    except Exception as e:
        if args.debug:
            print(f"Error: {e}")
        else:
            print("An error occurred. Use -d for debug mode.")

if __name__ == "__main__":
    main()
