# Cord 19 version used

2021-03-01

This project can serve as a starting point for using CORD-19 within a project. It includes methods to parse its data into an SQL database.

## Setup

Download cord 19 from <https://www.semanticscholar.org/cord19/download>

Extract the files in this directory

Install python dependencies

`./update_pip_deps.sh`

or:

`pip3 install -r dependencies.txt`

## Scripts

To load data into the database:

`python load_csv_into_db.py`

Only run this to populate the sqlite/metadata.db file. Running it multiple times will duplicate the data. This is to avoid having to parse the entire CSV file every time.

## `metadata.csv` overview

This section comes from the cord 19 repo: <https://github.com/allenai/cord19> - it includes some details about the fields present inside the csv file.

- `cord_uid`: A `str`-valued field that assigns a unique identifier to each CORD-19 paper. This is not necessariy unique per row, which is explained in the FAQs.
- `sha`: A `List[str]`-valued field that is the SHA1 of all PDFs associated with the CORD-19 paper. Most papers will have either zero or one value here (since we either have a PDF or we don't), but some papers will have multiple. For example, the main paper might have supplemental information saved in a separate PDF. Or we might have two separate PDF copies of the same paper. If multiple PDFs exist, their SHA1 will be semicolon-separated (e.g. `'4eb6e165ee705e2ae2a24ed2d4e67da42831ff4a; d4f0247db5e916c20eae3f6d772e8572eb828236'`)
- `source_x`: A `List[str]`-valued field that is the names of sources from which we received this paper. Also semicolon-separated. For example, `'ArXiv; Elsevier; PMC; WHO'`. There should always be at least one source listed.
- `title`: A `str`-valued field for the paper title
- `doi`: A `str`-valued field for the paper DOI
- `pmcid`: A `str`-valued field for the paper's ID on PubMed Central. Should begin with `PMC` followed by an integer.
- `pubmed_id`: An `int`-valued field for the paper's ID on PubMed.
- `license`: A `str`-valued field with the most permissive license we've found associated with this paper. Possible values include: `'cc0', 'hybrid-oa', 'els-covid', 'no-cc', 'cc-by-nc-sa', 'cc-by', 'gold-oa', 'biorxiv', 'green-oa', 'bronze-oa', 'cc-by-nc', 'medrxiv', 'cc-by-nd', 'arxiv', 'unk', 'cc-by-sa', 'cc-by-nc-nd'`
- `abstract`: A `str`-valued field for the paper's abstract
- `publish_time`: A `str`-valued field for the published date of the paper. This is in `yyyy-mm-dd` format. Not always accurate as some publishers will denote unknown dates with future dates like `yyyy-12-31`
- `authors`: A `List[str]`-valued field for the authors of the paper. Each author name is in `Last, First Middle` format and semicolon-separated.
- `journal`: A `str`-valued field for the paper journal. Strings are not normalized (e.g. `BMJ` and `British Medical Journal` can both exist). Empty string if unknown.
- `mag_id`: Deprecated, but originally an `int`-valued field for the paper as represented in the Microsoft Academic Graph.
- `who_covidence_id`: A `str`-valued field for the ID assigned by the WHO for this paper. Format looks like `#72306`.
- `arxiv_id`: A `str`-valued field for the arXiv ID of this paper.
- `pdf_json_files`: A `List[str]`-valued field containing paths from the root of the current data dump version to the parses of the paper PDFs into JSON format. Multiple paths are semicolon-separated. Example: `document_parses/pdf_json/4eb6e165ee705e2ae2a24ed2d4e67da42831ff4a.json; document_parses/pdf_json/d4f0247db5e916c20eae3f6d772e8572eb828236.json`
- `pmc_json_files`: A `List[str]`-valued field. Same as above, but corresponding to the full text XML files downloaded from PMC, parsed into the same JSON format as above.
- `url`: A `List[str]`-valued field containing all URLs associated with this paper. Semicolon-separated.
- `s2_id`: A `str`-valued field containing the Semantic Scholar ID for this paper. Can be used with the Semantic Scholar API (e.g. `s2_id=9445722` corresponds to `http://api.semanticscholar.org/corpusid:9445722`)
