# ESV Bible to Obsidian Markdown

This Python script fetches Bible chapters from the ESV API, parses the complex HTML response, and generates feature-rich Markdown files perfectly formatted for an Obsidian vault.

It intelligently handles verses, section headings, footnotes, and cross-references, turning them into a deeply interlinked, navigable digital Bible.

## Key Features

  * **Full API Integration**: Fetches chapter data directly from the official ESV API.
  * **Smart Caching**: Saves the raw JSON response for each chapter, so you can re-run the script without hitting the API every time.
  * **Advanced HTML Parsing**: Uses BeautifulSoup to meticulously parse verses, headings, footnotes, and cross-reference markers.
  * **Obsidian-Native Output**: Generates files using Obsidian-friendly Markdown, including:
      * `[[Wikilinks]]` for all navigation.
      * `![[Embeds]]` for cross-references.
      * Callouts (`[!info]`, `[!tip]`) for navigation and metadata.
  * **Automatic Navigation**: Creates a navigation header and footer for every chapter, linking to the previous/next chapter, book, and Bible index.
  * **Structured Output**:
      * Creates one Markdown file per chapter (e.g., `Genesis 1.md`).
      * Generates separate, dedicated files for footnotes (e.g., `Footnotes for Genesis 1.md`).
  * **Cross-Reference Engine**: Parses the ESV's complex cross-reference notation (e.g., "ch. 6:4-8; ver. 12") and converts each reference into an individual `![[Embed]]` link.
  * **Study Note Integration**: Automatically checks for and embeds your personal study notes from a separate folder in your vault.

-----

## Example File Output

The script generates clean, highly functional Markdown files. Here is a sample of the output for `Jude 1.md`:

```md
###### Navigation
>[!info ] **[[Bible|Bible]] | [[OUTLINE OF JUDE|Outline]] | [[Jude - Info|Info]] | [[3 John 1|⏪ 3 John 1]] | [[Jude|Chapters]] | [[Jude 1|First (1)]] | [[Jude 1|Last (1)]] | [[Revelation 1|Revelation 1 ⏩]]**

# Jude 1

## Greeting

###### 1
Jude, a [[Footnotes for Jude 1#f1-1|servant]] of Jesus Christ and brother of James, <sup>1</sup>To those who are called, <sup>2</sup>beloved in God the Father and <sup>3</sup>kept [[Footnotes for Jude 1#f2-1|for]] Jesus Christ:

> [!summary]- Study Notes
> ![[STUDY NOTES FOR Jude 1_1|Study Notes]]
***

> [!tip]- Cross References
> 1 **Romans 1:7**
> ![[Romans 1#7]]
> 1 **1 Corinthians 1:24**
> ![[1 Corinthians 1#24]]
> ---
> 2 **1 Thessalonians 1:4**
> ![[1 Thessalonians 1#4]]
> 2 **2 Thessalonians 2:13**
> ![[2 Thessalonians 2#13]]
> ---
> 3 **John 17:11, 15**
> ![[John 17#11]]
> ![[John 17#15]]
>

###### Navigation
>[!info ] **[[Bible|Bible]] | [[OUTLINE OF JUDE|Outline]] | [[Jude - Info|Info]] | [[3 John 1|⏪ 3 John 1]] | [[Jude|Chapters]] | [[Jude 1|First (1)]] | [[Jude 1|Last (1)]] | [[Revelation 1|Revelation 1 ⏩]]**
```

-----

## Setup & Configuration

Before you can run the script, you must complete these four steps.

### 1\. Get an ESV API Key

You need a free API key from Crossway.

1.  Go to [api.esv.org](https://api.esv.org/)
2.  Create an account and register a new "application."
3.  This will give you an API token (key).

### 2\. Set Your Environment Variable

The script reads your API key from an environment variable for security.

Set an environment variable named `ESV_API_KEY` to the value of the token you just received.

### 3\. Install Dependencies

This script relies on `requests` for API calls and `BeautifulSoup` for parsing.

```bash
pip install requests beautifulsoup4
```

### 4\. Configure Paths in `test.py`

You **must** edit the script to set the correct folder paths for your system.

Open `test.py` and modify these variables at the top of the file:

```python
# The root folder where your Bible files will be generated
BASE_FOLDER = "C:/Users/seans/Documents/Bible" 

# The folder for storing cached API (JSON) responses
DEBUG_FOLDER = Path(BASE_FOLDER) / "Debug" 

# The path to your *existing* Obsidian vault folder containing study notes
# This must match the format the script expects, e.g., 
# "C:/Vault/Notes/STUDY NOTES FOR Genesis 1_1.md"
OBSIDIAN_NOTES = "C:/Users/user/Documents/SecondBrain/Atlas/Sources/Bible/Study Notes"
```

-----

## How to Run

Once you have configured your paths and API key, simply run the script from your terminal:

```bash
python test.py
```

The script will process every book and chapter listed in the `BOOKS` dictionary.

**Note:** The script is designed to be run incrementally. It checks if the first chapter of a book (e.g., `Genesis 1.md`) already exists. If it does, it will skip that entire book, assuming it has already been processed. To re-process a book, you must delete its folder from your `BASE_FOLDER`.

## Output File Structure

The script will create the following directory structure inside your `BASE_FOLDER`:

```
/Your-Base-Folder/
├── /01 Genesis/
│   ├── Genesis 1.md
│   ├── Genesis 2.md
│   └── ...
├── /02 Exodus/
│   ├── Exodus 1.md
│   └── ...
├── /65 Jude/
│   ├── Jude 1.md
│   └── ...
├── /Debug/
│   ├── 01_Genesis_1_raw.json
│   ├── 01_Genesis_2_raw.json
│   ├── 65_Jude_1_raw.json
│   └── ...
└── /Footnotes/
    ├── /01 Genesis/
    │   ├── Footnotes for Genesis 1.md
    │   └── ...
    └── /65 Jude/
        ├── Footnotes for Jude 1.md
        └── ...
```

-----

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
