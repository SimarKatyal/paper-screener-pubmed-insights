# paper-screener-pubmed-insights
A Python-based tool that searches PubMed and screens research papers with at least one author from a pharmaceutical or biotech company.

## Table of Contents
- About the Project (#about-the-project)
- Features (#features)
- How It Works(#how-it-works)
- Installations (#installations)
- Usage (#usage)
- Sample Output (#sample-output)
- Heuristics Used (#heuristics-used)
- Tech Stack (#tech-stack)
- Limitations & Future Improvements (#limitations--future-improvements)
- License(#license)

## About the Project

This project is a backend-focused Python tool that fetches research papers from the PubMed API based on a user-defined query, identifies those with non-academic (e.g., pharmaceutical/biotech) authors, and exports the results in CSV format.

It’s designed to assist research professionals, pharma analysts, and academic-industry collaboration studies in quickly narrowing down relevant literature beyond purely academic contributions.

## Features
- Search PubMed using full query syntax
- Filter out academic-only papers using affiliation heuristics
- Extract paper metadata: PubMed ID, Title, Date, Author, Company, Email
- Output results to CSV or print to console
- Built using typed, modular, and maintainable Python
- Debug flag to inspect filtering logic (e.g., excluded academic-only papers)

## How It Works
1. Accepts a search query as input (e.g., `"cancer AND therapy"`).
2. Uses PubMed's API (`esearch`, `efetch`) to retrieve articles and metadata.
3. Parses author affiliations and filters out academic-only papers using keyword heuristics (like `"inc"`, `"biotech"`, `"pharma"`).
4. Extracts key information and presents it in a structured format.

## Installations

## Usage

## Sample Output

## Heuristics Used

## Tech Stack

## Limitations & Future Improvements

## License

## Created by:
- Simar Katyal
- +91 9311450011
- simarkatyal17@gmail.com
