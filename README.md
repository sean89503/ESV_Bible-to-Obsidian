ESV to Obsidian Markdown ConverterThis Python script fetches the entire English Standard Version (ESV) Bible, chapter by chapter, from the official ESV API. It parses the complex HTML responses and converts them into a set of clean, highly-interlinked Markdown files, perfectly formatted for use in an Obsidian.md vault.The final output is a complete, local, and navigable copy of the Bible, where cross-references are embedded, footnotes are linked, and navigation is seamless.FeaturesFull Bible Download: Iterates through every book and chapter to build a complete local copy.Obsidian-Native: Generates Markdown using Obsidian-specific features:[[Wikilink]] navigation for previous/next chapters and book indices.![[Embedded Links]] for all cross-references, allowing you to see context without leaving the page.> [!tip] callout blocks for cleanly grouped cross-references.[[Link|With Alias]] formatting for footnotes, linking to the exact note with the preceding word as the link text.Structured Output: Creates a clean folder structure, separating chapter files from footnote files.Smart Parsing:Correctly handles single-chapter books (Jude, 2 John, etc.).Parses complex cross-reference notation (e.g., "ch. 1:2-5", "ver. 6, 8").Links to external "Study Notes" if they exist in your vault (based on OBSIDIAN_NOTES path).Debug & Caching: Saves raw API responses as JSON files in a Debug folder. This caches your downloads, saving you from re-fetching data and respecting API rate limits.Example OutputThe script converts the API's HTML into clean, readable Markdown.Genesis 1.md (Partial Example)###### Navigation
>[!info ] **[[Bible]] | [[OUTLINE OF GENESIS|Outline]] | [[Genesis - Info|Info]] | ⏪ (Start of Bible) | [[Genesis|Chapters]] | [[Genesis 1|First (1)]] | [[Genesis 50|Last (50)]] | [[Genesis 2|Genesis 2 ⏩]]**

# Genesis 1

## The Creation of the World
###### 1
In the beginning, God created the heavens and the earth.
> [!tip]- Cross References
> 1 **Job 38:4-7**
> > ![[Job 38#4]]
> > ![[Job 38#5]]
> > ![[Job 38#6]]
> > ![[Job 38#7]]
> 1 **Psalm 33:6**
> > ![[Psalm 33#6]]
> 1 **John 1:1-3**
> > ![[John 1#1]]
> > ![[John 1#2]]
> > ![[John 1#3]]

###### 2
The earth was <sup>1</sup>without form and void, and darkness was over the face of the deep. And the Spirit of God was hovering over the face of the [[Footnotes for Genesis 1#f1-1|waters]].
> [!tip]- Cross References
> 1 **Jeremiah 4:23**
> > ![[Jeremiah 4#23]]

...
Footnotes/01 Genesis/Footnotes for Genesis 1.md# Footnotes for Genesis 1

>[!info] [[Bible]] | [[Genesis]] | **[[Genesis 1]]**

###### f1-1
Or *[f]luttering*
— Verse [[Genesis 1#2|1:2]]
RequirementsPython 3.xThe requests and beautifulsoup4 Python libraries.An ESV API Key.Installation & SetupClone the Repositorygit clone [https://github.com/your-username/esv-obsidian.git](https://github.com/your-username/esv-obsidian.git)
cd esv-obsidian
Install Dependenciespip install -r requirements.txt
(If no requirements.txt exists, install manually):pip install requests beautifulsoup4
Get Your ESV API KeyGo to https://api.esv.org/.Create a free account.Register a new "Application."You will be given an API token (a long string).Set the Environment VariableThe script reads the API key from an environment variable named ESV_API_KEY.Windows (PowerShell):$env:ESV_API_KEY = "YOUR_API_KEY_HERE"
(To set it permanently, search for "Edit the system environment variables").macOS / Linux:export ESV_API_KEY="YOUR_API_KEY_HERE"
(Add this line to your ~/.bashrc or ~/.zshrc file to make it permanent).ConfigurationBefore running, open test.py and edit the configuration constants at the top:BASE_FOLDER: The root folder where your Bible Markdown files will be saved.Example: "C:/Users/YourName/Documents/MyVault/Bible"OBSIDIAN_NOTES: The path to your existing study notes folder within your vault. The script will link to these if they follow the naming convention STUDY NOTES FOR [Book] [Chapter]_[Verse].md.Example: "C:/Users/YourName/Documents/MyVault/Study Notes"DEBUG_FOLDER: The subfolder for caching API responses. The default (Path(BASE_FOLDER) / "Debug") is usually fine.UsageOnce configured, simply run the script from your terminal:python test.py
The script will begin processing all books and chapters. It will print its progress to the console.👍 Skipping Book...: If the script finds the first chapter of a book (e.g., Genesis 1.md), it will skip the entire book, assuming it has already been processed.📄 Using cached HTML JSON...: If a raw JSON file is found in Debug, the script will use it instead of calling the API.To re-process a book, delete that book's folder from BASE_FOLDER and its corresponding JSON files from DEBUG_FOLDER.Output File StructureThe script will generate the following structure inside your BASE_FOLDER:C:/Users/YourName/Documents/MyVault/Bible/
├── 01 Genesis/
│   ├── Genesis 1.md
│   ├── Genesis 2.md
│   └── ...
├── 02 Exodus/
│   ├── Exodus 1.md
│   └── ...
├── Footnotes/
│   ├── 01 Genesis/
│   │   ├── Footnotes for Genesis 1.md
│   │   └── ...
│   └── 02 Exodus/
│       ├── Footnotes for Exodus 1.md
│       └── ...
└── Debug/
    ├── 01_Genesis_1_raw.json
    ├── 01_Genesis_1_cleaned.html
    ├── 01_Genesis_2_raw.json
    └── ...
LicenseThis project is licensed under the MIT License. See the LICENSE file for details.Note: The ESV Bible text is copyrighted by Crossway. The ESV API's terms of service apply. This script is intended for personal and non-commercial use.
