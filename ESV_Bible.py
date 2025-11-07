import os
import re
import time
import json
import requests
import random
import urllib3
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Configuration ---
# It's better to get API_KEY from environment variables for security
API_KEY = os.getenv("ESV_API_KEY", "?API KEY?")
if API_KEY == "?API KEY?":
    print("Warning: ESV_API_KEY environment variable not set. Using default/placeholder API key.")
    print("Please set the ESV_API_KEY environment variable for production use.")

BASE_FOLDER = "?C:/Users/USER/Documents/Bible?"
DEBUG_FOLDER = Path(BASE_FOLDER) / "Debug"
HEADERS = {"Authorization": f"Token {API_KEY}"}
OBSIDIAN_NOTES = "?C:/Users/USER/Documents/SecondBrain/Atlas/Sources/Bible/Study Notes?" # If you have notes you link to a verse "Study Notes"


BOOK_NAME_MAP = {
  "Gen": "Genesis", "Gen.": "Genesis", "Ex": "Exodus", "Ex.": "Exodus", "Lev": "Leviticus", "Lev.": "Leviticus",
  "Num": "Numbers", "Num.": "Numbers", "Deut": "Deuteronomy", "Deut.": "Deuteronomy", "Josh": "Joshua", "Josh.": "Joshua",
  "Judg": "Judges", "Judg.": "Judges", "Ruth": "Ruth", "1 Sam": "1 Samuel", "1 Sam.": "1 Samuel", "2 Sam": "2 Samuel",
  "2 Sam.": "2 Samuel", "1 Kgs": "1 Kings", "1 Kings": "1 Kings", "2 Kgs": "2 Kings", "2 Kings": "2 Kings",
  "1 Chr": "1 Chronicles", "1 Chron.": "1 Chronicles", "2 Chr": "2 Chronicles", "2 Chron.": "2 Chronicles",
  "Ezra": "Ezra", "Neh": "Nehemiah", "Neh.": "Nehemiah", "Esth": "Esther", "Esth.": "Esther", "Job": "Job",
  "Ps": "Psalm", "Ps.": "Psalm", "Prov": "Proverbs", "Prov.": "Proverbs", "Eccl": "Ecclesiastes", "Eccles.": "Ecclesiastes",
  "Song": "Song of Solomon", "Isa": "Isaiah", "Isa.": "Isaiah", "Jer": "Jeremiah", "Jer.": "Jeremiah",
  "Lam": "Lamentations", "Lam.": "Lamentations", "Ezek": "Ezekiel", "Ezek.": "Ezekiel", "Dan": "Daniel", "Dan.": "Daniel",
  "Hos": "Hosea", "Hos.": "Hosea", "Joel": "Joel", "Amos": "Amos", "Obad": "Obadiah", "Obad.": "Obadiah",
  "Jonah": "Jonah", "Mic": "Micah", "Mic.": "Micah", "Nah": "Nahum", "Nah.": "Nahum", "Hab": "Habakkuk",
  "Hab.": "Habakkuk", "Zeph": "Zephaniah", "Zeph.": "Zephaniah", "Hag": "Haggai", "Hag.": "Haggai", "Zech": "Zechariah",
  "Zech.": "Zechariah", "Mal": "Malachi", "Mal.": "Malachi", "Matt": "Matthew", "Matt.": "Matthew", "Mark": "Mark",
  "Luke": "Luke", "John": "John", "Acts": "Acts", "Rom": "Romans", "Rom.": "Romans", "1 Cor": "1 Corinthians",
  "1 Cor.": "1 Corinthians", "2 Cor": "2 Corinthians", "2 Cor.": "2 Corinthians", "Gal": "Galatians", "Gal.": "Galatians",
  "Eph": "Ephesians", "Eph.": "Ephesians", "Phil": "Philippians", "Phil.": "Philippians", "Col": "Colossians",
  "Col.": "Colossians", "1 Thess": "1 Thessalonians", "1 Thess.": "1 Thessalonians", "2 Thess": "2 Thessalonians",
  "2 Thess.": "2 Thessalonians", "1 Tim": "1 Timothy", "1 Tim.": "1 Timothy", "2 Tim": "2 Timothy", "2 Tim.": "2 Timothy",
  "Titus": "Titus", "Philem": "Philemon", "Philem.": "Philemon", "Heb": "Hebrews", "Heb.": "Hebrews", "James": "James",
  "Jas.": "James", "1 Pet": "1 Peter", "1 Pet.": "1 Peter", "2 Pet": "2 Peter", "2 Pet.": "2 Peter", "1 John": "1 John",
  "2 John": "2 John", "3 John": "3 John", "Jude": "Jude", "Rev": "Revelation", "Rev.": "Revelation"
}

BOOKS = {
     "01 Genesis": 50,
    "02 Exodus": 40,
    "03 Leviticus": 27,
    "04 Numbers": 36,
    "05 Deuteronomy": 34,
    "06 Joshua": 24,
    "07 Judges": 21,
    "08 Ruth": 4,
    "09 1 Samuel": 31,
    "10 2 Samuel": 24,
    "11 1 Kings": 22,
    "12 2 Kings": 25,
    "13 1 Chronicles": 29,
    "14 2 Chronicles": 36,
    "15 Ezra": 10,
    "16 Nehemiah": 13,
    "17 Esther": 10,
     "18 Job": 42,
     "19 Psalm": 150,
     "20 Proverbs": 31,
    "21 Ecclesiastes": 12,
    "22 Song of Solomon": 8,
    "23 Isaiah": 66,
    "24 Jeremiah": 52,
    "25 Lamentations": 5,
    "26 Ezekiel": 48,
    "27 Daniel": 12,
    "28 Hosea": 14,
    "29 Joel": 3,
    "30 Amos": 9,
    "31 Obadiah": 1,
    "32 Jonah": 4,
    "33 Micah": 7,
    "34 Nahum": 3,
    "35 Habakkuk": 3,
    "36 Zephaniah": 3,
    "37 Haggai": 2,
    "38 Zechariah": 14,
    "39 Malachi": 4,
    "40 Matthew": 28,
    "41 Mark": 16,
    "42 Luke": 24,
    "43 John": 21,
    "44 Acts": 28,
    "45 Romans": 16,
    "46 1 Corinthians": 16,
    "47 2 Corinthians": 13,
    "48 Galatians": 6,
    "49 Ephesians": 6,
    "50 Philippians": 4,
    "51 Colossians": 4,
    "52 1 Thessalonians": 5,
    "53 2 Thessalonians": 3,
    "54 1 Timothy": 6,
    "55 2 Timothy": 4,
    "56 Titus": 3,
    "57 Philemon": 1,
    "58 Hebrews": 13,
    "59 James": 5,
    "60 1 Peter": 5,
    "61 2 Peter": 3,
    "62 1 John": 5,
    "63 2 John": 1,
    "64 3 John": 1,
    "65 Jude": 1,
     "66 Revelation": 22,
}

SINGLE_CHAPTER_BOOKS = {"Obadiah", "Philemon", "2 John", "3 John", "Jude"}

# --- API Fetching ---
def fetch_html_content(book_key, chapter_num):
    """
    Fetches HTML content for a given Bible chapter from the ESV API.
    If a raw JSON debug file already exists in DEBUG_FOLDER, it is used instead.
    Otherwise, the API is called and the result is saved.
    Removes blank lines and stray \n from the 'passages' content before parsing.
    """
    
    # Use safer split logic from our previous conversation
    parts = book_key.split(" ", 1)
    book_name_short = parts[1] if len(parts) > 1 else parts[0]
    
    filename = f"{book_key.replace(' ', '_')}_{chapter_num}_raw.json"
    debug_path = DEBUG_FOLDER / filename

    # Check for existing file first
    if debug_path.exists():
        print(f"📄 Using cached HTML JSON: {filename}")
        with open(debug_path, "r", encoding="utf-8") as f:
            try:
                raw_json = json.load(f)
            except json.JSONDecodeError as e:
                print(f"❌ Error decoding cached JSON for {book_key} {chapter_num}: {e}")
                return None
    else:
        url = "https://api.esv.org/v3/passage/html/"
        
        # --- MODIFIED SECTION ---
        # For single-chapter books, query only the book name.
        # Otherwise, query "Book Chapter".
        if book_name_short in SINGLE_CHAPTER_BOOKS:
            query_text = book_name_short
        else:
            query_text = f"{book_name_short} {chapter_num}"
        # --- END MODIFIED SECTION ---

        params = {
            "q": query_text,  # <-- Use the new query_text variable
            "include-headings": "true",
            "include-verse-numbers": "true",
            "include-passage-references": "false",
            "include-first-verse-numbers": "true",
            "include-footnotes": "true",
            "include-footnote-body": "true",
            "include-crossrefs": "true",
        }
        try:
            time.sleep(random.uniform(2.0, 5.0))
            response = requests.get(url, headers=HEADERS, params=params)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            raw_json = response.json()

            DEBUG_FOLDER.mkdir(parents=True, exist_ok=True)
            with open(debug_path, "w", encoding="utf-8") as f:
                json.dump(raw_json, f, indent=2, ensure_ascii=False)
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP Error fetching content for {book_key} {chapter_num}: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Network or Request Error fetching content for {book_key} {chapter_num}: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ JSON Decode Error from API response for {book_key} {chapter_num}: {e}")
            return None

    passages = raw_json.get("passages")
    if passages and isinstance(passages, list) and len(passages) > 0:
        # Clean passage to remove literal \n and empty lines
        raw_html = passages[0]
        cleaned_html = "\n".join(line for line in raw_html.splitlines() if line.strip())
        # cleaned_html = raw_html
        return BeautifulSoup(cleaned_html, "html.parser")
    else:
        # Check if the query was for a chapter that doesn't exist (e.g., Jude 2)
        if book_name_short in SINGLE_CHAPTER_BOOKS and str(chapter_num) != "1":
             print(f"ℹ️ Info: Skipped {book_key} {chapter_num} (single-chapter book).")
             return None # Not an error, just no content.
        
        print(f"⚠️ Warning: No valid 'passages' content found for {book_key} {chapter_num}. Raw JSON: {raw_json}")
        return None

# --- Helper for extracting word before footnote and modifying DOM ---
def extract_word_before_footnote(sup_tag):
    """
    Attempts to find the last word of text immediately preceding the given <sup> tag.
    It traverses backwards through siblings to find the last NavigableString.
    If found, it extracts the last word and modifies the NavigableString in place
    to remove that word, preventing duplication.
    Returns the extracted word, or "Footnote" as a fallback.
    """
    word_before = "□" # Default fallback

    # Start searching from the immediate previous sibling
    current_element = sup_tag.previous_sibling

    while current_element:
        if isinstance(current_element, NavigableString):
            text_content = str(current_element)
            # Find the last word in the text, optionally followed by punctuation/whitespace
            match = re.search(r'([\w\'-]+)([^\w\s]*)\s*$', text_content)
            if match:
                word_before = match.group(1)
                trailing_chars = match.group(2)
                # Modify the NavigableString in place
                current_element.replace_with(NavigableString(text_content[:match.start(1)] + trailing_chars))
                return word_before
            # If no word found in this NavigableString, continue to the previous sibling
        elif isinstance(current_element, Tag):
            # If it's a tag, get its text content and try to extract the last word.
            text_content = current_element.get_text(" ", strip=True)
            if text_content:
                words = text_content.split()
                if words:
                    return words[-1]
        current_element = current_element.previous_sibling

    return word_before # Return default if no word was found or handled

# --- HTML Cleaning Function ---
def remove_specific_html_elements(html_soup):
    """
    Removes specific classes and tags from the BeautifulSoup object.
    - Removes 'block-indent' class from any tag.
    - Unwraps all <span> tags (removes the tag but keeps its contents).
    - Unwraps <p> tags that do not have any class attributes.
    - Unwraps <body> tags (removes the tag but keeps its contents).
    """
    #print("DEBUG: Applying HTML structure cleaning...")

    # Remove 'block-indent' class from any tag that has it
    for tag in html_soup.find_all(class_="block-indent"):
        if 'block-indent' in tag.get('class', []):
            tag['class'].remove('block-indent')
            # print(f"DEBUG: Removed 'block-indent' class from tag: <{tag.name}>")

  
    for br_tag in html_soup.find_all("br"):
        br_tag.extract() # .extract() removes the tag and its contents

    # Remove <h3> tags that have no text content
    for h3_tag in list(html_soup.find_all("h3")):
        if not h3_tag.get_text(strip=True):
            h3_tag.extract()
            # print(f"DEBUG: Removed empty <h3> tag.")
    for p_tag in list(html_soup.find_all("p")):
        # Get the classes of the current p_tag
        p_classes = p_tag.get('class', [])

        # Condition 1: Keep <p class="starts-chapter"> as it's a significant structural marker.
        if 'starts-chapter' in p_classes:
            continue
        # Condition 2: Keep <p class="block-indent"> if it contains verse lines (<span>s).
        if p_tag.find('span', class_='line'):
            continue
        if 'block-indent' in p_classes and p_tag.find('span', class_='line'):
            continue
        # Condition 3: Keep <p> tags that contain a direct verse number (e.g., Genesis, Job).
        if p_tag.find('b', class_='verse-num'):
            continue

        # Condition 4: Unwrap <p> tags that are empty or contain only whitespace.
        if not p_tag.get_text(strip=True) and not p_tag.find(recursive=False):
            p_tag.unwrap()
            continue
        if p_tag.find('a', class_='copyright') and not p_tag.get_text(strip=True).replace('(','').replace(')','').strip():
            p_tag.unwrap()
            continue
            
        # print(f"DEBUG: Unwrapped <body> tag. Content moved to parent.")
    # else:
        # print("DEBUG: No <body> tag found to unwrap.")

    return html_soup

# --- Function to save cleaned HTML to a file ---
def save_cleaned_html_to_file(book_key, chapter_num, html_soup_obj):
    """
    Saves the cleaned HTML content to a file within the specified DEBUG_FOLDER.
    It attempts to save only the content within the <body> (or what was within it),
    without the <html>, <head>, or <body> wrappers.
    """
    book_title = book_key.split(" ", 1)[1]
    file_path = DEBUG_FOLDER / f"{book_title}_{chapter_num}_cleaned.html"
    
    try:
        # Find the <html> tag, or use the soup object itself if it's the root.
        # After unwrapping <body>, its contents will be direct children of <html>.
        html_tag = html_soup_obj.find("html") or html_soup_obj

        # Get the string representation of the children of the <html> tag.
        # This will include everything that was inside <body>, but without the <body> tag itself.
        cleaned_html_string = html_tag.decode_contents()

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(cleaned_html_string)
        # print(f"✔️ Successfully saved cleaned HTML: {file_path}")
    except IOError as e:
        print(f"❌ Error saving cleaned HTML file {file_path}: {e}")
    except Exception as e:
        print(f"❌ Unexpected error during saving cleaned HTML for {book_key} {chapter_num}: {e}")

# --- HTML Parsing and Data Extraction (Consolidated) ---
def parse_chapter_html(html_soup, book_name_short, chapter_num):
    """
    Parses the cleaned BeautifulSoup object to extract verses, section headings,
    and footnotes, returning them in a structured dictionary.
    """
    verses_data = {}
    section_headings = {}
    all_footnotes = {}
    current_verse_num = None
    section_heading_counter = 0

    # Dictionaries to store data for placeholders
    crossref_placeholders = {} # Key: unique_id, Value: raw_title
    footnote_placeholders = {} # Key: unique_id, Value: {'fn_id': 'f1-1', 'word_before': 'servants'}

    # --- Pass 1: Extract Footnotes and Cross-references, replace with placeholders ---
    # This part needs to operate on the original soup before cleaning, or be adapted
    # to find elements in the modified soup.
    # The `extract_word_before_footnote` function modifies the soup, so it's fine.

    footnotes_div = html_soup.find("div", class_="footnotes")
    if footnotes_div:
        container_p = footnotes_div.find("p")
        if container_p:
            children = list(container_p.children)
            current_id = None
            current_verse = None
            for child in children:
                if isinstance(child, Tag):
                    a_tag = child.find("a", id=True)
                    if a_tag:
                        current_id = a_tag["id"].replace("fb", "f")
                    elif child.name == "span" and "footnote-ref" in child.get("class", []):
                        current_verse = child.get_text(strip=True)
                    elif child.name == "note" and current_id:
                        note_text = child.get_text(" ", strip=True)
                        all_footnotes[current_id] = {
                            "verse": current_verse if current_verse else "?",
                            "text": note_text
                        }
                        current_id = None
                        current_verse = None
        footnotes_div.extract() # Remove the footnotes div from the main soup after processing

    passage_container = html_soup.find("div", class_="passage") or html_soup.body or html_soup # Use body or soup if no specific passage div

    for tag in passage_container.find_all(['a', 'span', 'sup'], class_=['cf', 'crossref-letter', 'footnote']):
        if tag.name == 'sup' and 'footnote' in tag.get('class', []):
            fn_tag = tag.find('a', class_='fn')
            if fn_tag:
                fn_id_from_href = fn_tag.get('href', '').replace('#', '')
                word_before_footnote = extract_word_before_footnote(tag)
                placeholder_id = f"FN_PLACEHOLDER_{len(footnote_placeholders)}"
                footnote_placeholders[placeholder_id] = {
                    'fn_id': fn_id_from_href,
                    'word_before': word_before_footnote
                }
                tag.replace_with(f"__{placeholder_id}__")
        elif tag.name in ['a', 'span'] and ('cf' in tag.get('class', []) or 'crossref-letter' in tag.get('class', [])):
            title = tag.get('title', '')
            if title:
                placeholder_id = f"CR_PLACEHOLDER_{len(crossref_placeholders)}"
                crossref_placeholders[placeholder_id] = title
                tag.replace_with(f"__{placeholder_id}__")

    # --- Pass 2: Extract main text content (verses and headings) ---
    # Iterate through all children of the main content container, now that <br> and some <p> are handled
    # and placeholders are in place.
    for top_level_element in list(passage_container.children): # Use list() for safe iteration during modification
        if not top_level_element.parent: # Skip if element has already been extracted
            continue

        if top_level_element.name == 'h3':
            section_heading_counter += 1
            section_id = f"s{section_heading_counter}"
            # Check for psalm-book class on h3 (though psalm-title is on h4)
            if 'psalm-book' in top_level_element.get('class', []):
                section_headings[section_id] = f"### {top_level_element.get_text(strip=True)}"
            else:
                section_headings[section_id] = top_level_element.get_text(strip=True)
            top_level_element.extract() # Remove heading after processing
            continue

        # If the element is a <p> tag or a <span> that might contain verse content
        if top_level_element.name in ['p', 'span']:
            # Find all verse number tags within this element
            verse_number_tags = top_level_element.find_all('b', class_=['verse-num', 'chapter-num'])

            # If no verse numbers are found in this element, and it's not a NavigableString,
            # just get its full text content and append to the current verse.
            if not verse_number_tags:
                text_content = top_level_element.get_text(" ", strip=True) # Use space as separator for nested tags
                if text_content and current_verse_num is not None:
                    verses_data[current_verse_num]["text"] += text_content + " "
                elif text_content and current_verse_num is None: # Text before first verse
                     verses_data.setdefault(1, {"text": "", "footnotes": [], "crossrefs_raw_titles": {}, "section_heading_id": None})
                     verses_data[1]["text"] += text_content + " "
                top_level_element.extract()
                continue

            # Process content around each verse number within this top_level_element
            # Create a temporary soup for the content to easily split by verse tags
            temp_soup = BeautifulSoup(str(top_level_element), 'html.parser')
            
            # Replace verse number tags with a unique delimiter for splitting
            for tag_to_replace in temp_soup.find_all('b', class_=['verse-num', 'chapter-num']):
                verse_text_raw = tag_to_replace.get_text(strip=True)
                # Use a specific delimiter that includes the verse number for later parsing
                tag_to_replace.replace_with(f"__VERSE_DELIMITER__{verse_text_raw}__")

            # Get the text of the modified temp_soup
            full_text_with_delimiters = temp_soup.get_text(separator=" ", strip=False)

            # Split the text by the delimiter
            segments = re.split(r'__VERSE_DELIMITER__(\d+):?(\d*)__', full_text_with_delimiters)

            # The first segment is content before the first verse number (if any)
            # Subsequent segments alternate: verse_num_raw, verse_content
            
            # Handle text before the first verse number in this element
            initial_text = segments[0].strip()
            if initial_text and current_verse_num is not None:
                verses_data[current_verse_num]["text"] += initial_text + " "
            elif initial_text and current_verse_num is None:
                verses_data.setdefault(1, {"text": "", "footnotes": [], "crossrefs_raw_titles": {}, "section_heading_id": None})
                verses_data[1]["text"] += initial_text + " "

            # Process the remaining segments (verse number and content)
            for i in range(1, len(segments), 3): # Iterate by 3s: skip initial text, then verse_num_part1, verse_num_part2, content
                if i + 1 < len(segments): # Ensure there's a verse number and content
                    verse_num_part1 = segments[i]
                    verse_num_part2 = segments[i+1] # This might be empty for single-digit verse numbers
                    verse_content_segment = segments[i+2].strip()

                    new_verse_num = None
                    if verse_num_part2: # It's a chapter:verse format
                        new_verse_num = int(verse_num_part2)
                    else: # It's just a verse number
                        new_verse_num = int(verse_num_part1)
                    
                    if new_verse_num is not None:
                        # Finalize previous verse's text before starting a new one
                        if current_verse_num is not None and verses_data[current_verse_num]["text"].strip():
                            verses_data[current_verse_num]["text"] = re.sub(r'\s+', ' ', verses_data[current_verse_num]["text"]).strip()
                        
                        current_verse_num = new_verse_num
                        verses_data.setdefault(current_verse_num, {"text": "", "footnotes": [], "crossrefs_raw_titles": {}, "section_heading_id": None})

                        if section_heading_counter > 0 and verses_data[current_verse_num]["section_heading_id"] is None:
                            verses_data[current_verse_num]["section_heading_id"] = f"s{section_heading_counter}"
                    
                    if verse_content_segment:
                        verses_data[current_verse_num]["text"] += verse_content_segment + " "

            top_level_element.extract() # Remove the processed element from soup

        elif isinstance(top_level_element, NavigableString):
            text_content = str(top_level_element).strip()
            if text_content:
                if current_verse_num is not None:
                    verses_data[current_verse_num]["text"] += text_content + " "
                else:
                    # If text appears before any verse number, assign to verse 1
                    verses_data.setdefault(1, {"text": "", "footnotes": [], "crossrefs_raw_titles": {}, "section_heading_id": None})
                    verses_data[1]["text"] += text_content + " "
        
        # Remove the processed top_level_element from soup to avoid re-processing
        top_level_element.extract()

    # Final pass to replace placeholders and clean up whitespace for all verse texts
    for verse_num in verses_data:
        text = verses_data[verse_num]["text"]
        # Replace footnote placeholders
        for ph_id, fn_data in footnote_placeholders.items():
            if f"__{ph_id}__" in text:
                replacement = f"[[Footnotes for {book_name_short} {chapter_num}#{fn_data['fn_id']}|{fn_data['word_before']}]]"
                text = text.replace(f"__{ph_id}__", replacement)

        # Replace cross-reference placeholders
        for ph_id, cr_title in crossref_placeholders.items():
            if f"__{ph_id}__" in text:
                reph_id = ph_id.replace("CR_PLACEHOLDER_", "")
                text = text.replace(f"__{ph_id}__", f"<sup>{reph_id}</sup>")
                # Ensure crossref is associated with a verse
                if verse_num is not None: # Already ensured by loop, but good for safety
                    verses_data[verse_num]["crossrefs_raw_titles"][reph_id] = cr_title
                else:
                    verses_data.setdefault(1, {"text": "", "footnotes": [], "crossrefs_raw_titles": {}, "section_heading_id": None})
                    verses_data[1]["crossrefs_raw_titles"][reph_id] = cr_title
        
        verses_data[verse_num]["text"] = re.sub(r'\s+', ' ', text).strip()


    return {
        "verses": verses_data,
        "section_headings": section_headings,
        "footnotes": all_footnotes
    }

def replace_placeholders_in_text(text, footnote_placeholders, crossref_placeholders, inline_crossref_markers, book_name_short, chapter_num):
    """Replaces placeholder strings with their formatted Obsidian links."""
    # Footnote placeholders: [[FN_PLACEHOLDER:fn_id:word_before]] -> [[Footnotes for Book Chapter#fn_id|word_before]]
    def replace_fn(match):
        fn_id = match.group(1)
        word_before = match.group(2)
        return f"[[Footnotes for {book_name_short} {chapter_num}#{fn_id}|{word_before}]]"

    text = re.sub(r'\[\[FN_PLACEHOLDER:([^:]+):([^\]]*)\]\]', replace_fn, text)

    # Cross-reference inline placeholders: [[CR_INLINE_PLACEHOLDER:unique_id]] -> <sup>inline_marker</sup>
    def replace_cr_inline(match):
        ph_id = match.group(1)
        inline_marker = inline_crossref_markers.get(ph_id, "")
        if inline_marker:
            return f"<sup>{inline_marker}</sup>"
        return "" # Fallback if marker not found

    text = re.sub(r'\[\[CR_INLINE_PLACEHOLDER:([^\]]+)\]\]', replace_cr_inline, text)

    # Cross-reference block placeholders (these are handled by build_crossref_block, so they shouldn't be in text)
    # This regex is for safety, if any [[CR_PLACEHOLDER:unique_id]] somehow remains in the text.
    text = re.sub(r'\[\[CR_PLACEHOLDER:([^\]]+)\]\]', '', text) # Remove any remaining block placeholders from inline text

    return text

# --- Navigation Logic ---
def get_chapter_navigation(book_key, chapter_num, total_chapters_in_book):
    """
    Generates the navigation block for a chapter, using short book names for links.
    """
    book_name_short = book_key.split(" ", 1)[1]
    book_keys_list = list(BOOKS.keys())
    current_book_index = book_keys_list.index(book_key)

    # Previous Chapter/Book
    prev_chapter_link = ""
    if chapter_num > 1:
        prev_chapter_link = f"[[{book_name_short} {chapter_num - 1}|⏪ {book_name_short} {chapter_num - 1}]]"
    elif current_book_index > 0:
        prev_book_key = book_keys_list[current_book_index - 1]
        prev_book_name_short = prev_book_key.split(" ", 1)[1]
        prev_book_total_chapters = BOOKS[prev_book_key]
        prev_chapter_link = f"[[{prev_book_name_short} {prev_book_total_chapters}|⏪ {prev_book_name_short} {prev_book_total_chapters}]]"
    else: # First chapter of the first book
        prev_chapter_link = "⏪ (Start of Bible)"

    # Next Chapter/Book
    next_chapter_link = ""
    if chapter_num < total_chapters_in_book:
        next_chapter_link = f"[[{book_name_short} {chapter_num + 1}|{book_name_short} {chapter_num + 1} ⏩]]"
    elif current_book_index < len(book_keys_list) - 1:
        next_book_key = book_keys_list[current_book_index + 1]
        next_book_name_short = next_book_key.split(" ", 1)[1]
        next_chapter_link = f"[[{next_book_name_short} 1|{next_book_name_short} 1 ⏩]]"
    else: # Last chapter of the last book
        next_chapter_link = "(End of Bible) ⏩"

    # Book-level navigation
    book_nav_links = f"[[{book_name_short}|Chapters]] | [[{book_name_short} 1|First (1)]] | [[{book_name_short} {total_chapters_in_book}|Last ({total_chapters_in_book})]]"
    
    outline = f"[[OUTLINE OF {book_name_short.upper()}|Outline]]"
    navinfo = f"[[{book_name_short} - Info|Info]]"
    return (
        f"###### Navigation\n"
        f">[!info ] **[[Bible|Bible]] | {outline} | {navinfo} | {prev_chapter_link} | {book_nav_links} | {next_chapter_link}**\n\n"
    )

def validate_and_clean_obsidian_link(link: str, book_name_map: dict) -> str:
    """
    Validates and cleans an Obsidian link string, ensuring it's in the correct format
    and uses full book names.
    """
    link = link.strip()
    link = link.replace("[[", "").replace("]]", "").replace("[", "").replace("]", "")
    link = re.sub(r"[^\w\s:#\-]", "", link)

    match = re.match(r"(?P<book>[1-3]?\s?[A-Za-z ]+)\s(?P<chapter>\d+)#(?P<verse>[\d\-]+)", link)
    if not match:
        return ""

    book = match.group("book").strip()
    chapter = match.group("chapter")
    verse = match.group("verse")

    book_clean = re.sub(r"[^A-Za-z0-9 ]", "", book)
    book_full = book_name_map.get(book_clean, book_clean)

    return f"![[{book_full} {chapter}#{verse}]]"

def parse_crossref(ref, last_book=None, current_book=None, current_chapter=None):
    """
    Parses a single cross-reference string and returns a pretty formatted string,
    a list of Obsidian embed links, and the book name used (for tracking last_book).
    Handles various formats including "See", "ver.", "ch", and standard "Book Chapter:Verse".
    """
    ref = ref.strip().replace("–", "-").strip("[]()")
    lower_ref = ref.lower()

    for prefix in ["see also", "see", "also"]:
        if lower_ref.startswith(prefix):
            clean_ref_part = ref[len(prefix):].strip()
            pretty = f"**{ref}**"
            links = []
            individual_refs = re.split(r'[;,]', clean_ref_part)
            for part in individual_refs:
                sub_pretty, sub_links, last_book = parse_crossref(part.strip(), last_book, current_book, current_chapter)
                links.extend(sub_links)
            return pretty, links, last_book

    if lower_ref.startswith("ver."):
        verse_part = ref[4:].strip()
        #print(f"DEBUG: Parsing 'ver.' reference: {verse_part}")
        if lower_ref.startswith("cited"):
            verse_part = verse_part[6:].strip()  # Remove "cited" prefix if present
        #print(f"DEBUG: Parsing 'cited.' reference: {verse_part}")
        verses = [v.strip() for v in verse_part.split(",")]
        pretty = f"**ver. {verse_part}**"
        links = []
        for v in verses:
            #print(f"DEBUG: Processing verse: {v}")
            if  v.startswith("cited "):
                clean = v[6:].strip()
                pretty = f"**cited {clean}**"
                links = []
                individual_refs = re.split(r'[;,]', clean)
                for part in individual_refs:
                    sub_pretty, sub_links, last_book = parse_crossref(part.strip(), last_book, current_book, current_chapter)
                    links.extend(sub_links)
                return pretty, links, last_book
                
                
            # Handle verse-chapter:verse ranges like "51-8:9"
            cross_chapter_verse_match = re.match(r'(\d+)-(\d+):(\d+)', v)
            if cross_chapter_verse_match:
                start_v = int(cross_chapter_verse_match.group(1))
                end_ch = int(cross_chapter_verse_match.group(2))
                end_v = int(cross_chapter_verse_match.group(3))
                links.append(f"![[{current_book} {current_chapter}#{start_v}]]")
                links.append(f"![[{current_book} {end_ch}#{end_v}]]")
            elif "-" in v:
                try:
                    start_v, end_v = map(int, v.split("-"))
                    links.extend([f"![[{current_book} {current_chapter}#{i}]]" for i in range(start_v, end_v + 1)])
                except ValueError:
                    print(f"Warning: Could not parse simple verse range '{v}' in 'ver.'. Adding as single link.")
                    links.append(f"![[{current_book} {current_chapter}#{v}]]")
            else:
                links.append(f"![[{current_book} {current_chapter}#{v}]]")
        return pretty, links, current_book
    
    
    # Handle "ch. X" or "ch. X:Y-Z" format
    if lower_ref.startswith("ch ") or lower_ref.startswith("ch. "):
        ch_part = ref.split(" ", 1)[1].strip()
        
        # Check for chapter-verse range (e.g., "37:2-39:8")
        range_match = re.match(r"(\d+):(\d+)-(\d+):(\d+)", ch_part)
        if range_match:
            start_ch, start_v, end_ch, end_v = map(int, range_match.groups())
            pretty = f"**ch. {start_ch}:{start_v}-{end_ch}:{end_v}**"
            links = []
            # For simplicity, we'll just link to the start and end of the range for now.
            links.append(f"![[{current_book} {start_ch}#{start_v}]]")
            links.append(f"![[{current_book} {end_ch}#{end_v}]]")
            return pretty, links, current_book

        # Handle single chapter or chapter:verse/range
        if ":" in ch_part:
            chapter, verses = ch_part.split(":", 1)
            chapter = chapter.strip()
            verses_list = [v.strip() for v in verses.split(",")]
        else:
            chapter = ch_part.strip()
            verses_list = []

        pretty = f"**ch {chapter}:{', '.join(verses_list)}**" if verses_list else f"**ch {chapter}**"
        links = []
        if verses_list:
            for v in verses_list:
                if "-" in v:
                    try:
                        start_v, end_v = map(int, v.split("-"))
                        links.extend([f"![[{current_book} {chapter}#{i}]]" for i in range(start_v, end_v + 1)])
                    except ValueError:
                        # Fallback for cases like "39:8" where it's not just a verse range
                        print(f"Warning: Could not parse verse range '{v}' in 'ch {chapter}'. Adding as single link.")
                        links.append(f"![[{current_book} {chapter}#{v}]]")
                else:
                    links.append(f"![[{current_book} {chapter}#{v}]]")
        else:
            links.append(f"![[{current_book} {chapter}]]")
        return pretty, links, current_book

    # Handle "Book Chapter:Verse" format
    match = re.match(r"([1-3]?\s?[A-Za-z. ]+)\s+(\d+):([\d,\- ]+)", ref)
    if match:
        book_raw = match.group(1).strip().replace(".", "")
        chapter = match.group(2).strip()
        verse_part = match.group(3).strip()
        book = BOOK_NAME_MAP.get(book_raw, book_raw)

        links = []
        for part in verse_part.split(","):
            part = part.strip()
            # Handle verse-chapter:verse ranges like "51-8:9"
            cross_chapter_verse_match = re.match(r'(\d+)-(\d+):(\d+)', part)
            if cross_chapter_verse_match:
                start_v = int(cross_chapter_verse_match.group(1))
                end_ch = int(cross_chapter_verse_match.group(2))
                end_v = int(cross_chapter_verse_match.group(3))
                links.append(f"![[{book} {chapter}#{start_v}]]") # Assuming start verse is in 'chapter'
                links.append(f"![[{book} {end_ch}#{end_v}]]")
            elif "-" in part:
                try:
                    start, end = map(int, part.split("-"))
                    links.extend([f"![[{book} {chapter}#{i}]]" for i in range(start, end + 1)])
                except ValueError:
                    print(f"Warning: Could not parse simple verse range '{part}' in '{book} {chapter}'. Adding as single link.")
                    links.append(f"![[{book} {chapter}#{part}]]")
            else:
                links.append(f"![[{book} {chapter}#{part}]]")

        pretty = f"**{book} {chapter}:{verse_part}**"
        return pretty, links, book

    # Handle "Chapter:Verse" format (assuming current book)
    if ":" in ref:
        chapter, verses = ref.split(":", 1)
        verses_list = [v.strip() for v in verses.split(",")]
        book = last_book or current_book or ""
        pretty = f"**{ref}**"
        links = []
        for v in verses_list:
            # Handle verse-chapter:verse ranges like "51-8:9"
            cross_chapter_verse_match = re.match(r'(\d+)-(\d+):(\d+)', v)
            if cross_chapter_verse_match:
                start_v = int(cross_chapter_verse_match.group(1))
                end_ch = int(cross_chapter_verse_match.group(2))
                end_v = int(cross_chapter_verse_match.group(3))
                links.append(f"![[{book} {chapter}#{start_v}]]") # Assuming start verse is in 'chapter'
                links.append(f"![[{book} {end_ch}#{end_v}]]")
            elif "-" in v:
                try:
                    start_v, end_v = map(int, v.split("-"))
                    links.extend([f"![[{book} {chapter}#{i}]]" for i in range(start_v, end_v + 1)])
                except ValueError:
                    print(f"Warning: Could not parse simple verse range '{v}' in '{book} {chapter}'. Adding as single link.")
                    links.append(f"![[{book} {chapter}#{v}]]")
            else:
                links.append(f"![[{book} {chapter}#{v}]]")
        return pretty, links, book

    # Handle single verse number (assuming current book and chapter)
    book = last_book or current_book or ""
    pretty = f"**{ref}**"
    if re.match(r'^\d+$', ref.strip()):
        link = f"![[{book} {current_chapter}#{ref.strip()}]]"
    else:
        # Fallback for any other unhandled format, just create a link with the raw ref
        link = f"![[{book} {current_chapter}#{ref.strip()}]]"

    return pretty, [link], book

def write_footnote_file(book_key, chapter_num, footnotes_data):
    """
    Writes the footnotes for a chapter to a dedicated Markdown file.
    Folder name uses book_key, file name and content use book_name_short.
    """
    if not footnotes_data:
        return

    book_name_short = book_key.split(" ", 1)[1]

    folder = Path(BASE_FOLDER) / "Footnotes" / book_key
    folder.mkdir(parents=True, exist_ok=True)
    file_path = folder / f"Footnotes for {book_name_short} {chapter_num}.md"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# Footnotes for {book_name_short} {chapter_num}\n\n")
        f.write(f">[!info] [[Bible]] | [[{book_name_short}]] | **[[{book_name_short} {chapter_num}]]**\n\n")
        for fn_id in sorted(footnotes_data.keys()):
            entry = footnotes_data[fn_id]
            verse = entry.get("verse", "?")
            text = entry.get("text", "")
            verse_only = verse.split(":")[-1]
            backlink = f"[[{book_name_short} {chapter_num}#{verse_only}"
            f.write(f"###### {fn_id}\n")
            f.write(f"{text}\n")
            f.write(f"— Verse {backlink}|{verse}]] \n")

def build_crossref_block(crossrefs_dict, book_name_short, chapter_num):
    """
    Builds the Markdown string for the cross-references callout block.
    """
    if not crossrefs_dict:
        return ""

    lines = ["> [!tip]- Cross References"]
    last_book_in_block = book_name_short  # Initialize with current book

    for reph_id, raw_title in sorted(crossrefs_dict.items(), key=lambda x: int(x[0])):
        individual_refs = [ref.strip() for ref in raw_title.split(';') if ref.strip()]
        for ref in individual_refs:
            pretty, links, book_used = parse_crossref(
                ref,
                last_book=last_book_in_block,
                current_book=book_name_short,
                current_chapter=chapter_num
            )
            lines.append(f"> {reph_id} {pretty}")
            for link in links:
                cleaned_link = validate_and_clean_obsidian_link(link, BOOK_NAME_MAP)
                if cleaned_link:
                    lines.append(f"> {cleaned_link}")
            last_book_in_block = book_used

    lines.append(">")  # Close the callout block

    return "\n".join(lines) + "\n"  # Add a final newline after the block

def generate_chapter_markdown(book_key, chapter_num, parsed_data, total_chapters_in_book):
    """
    Generates the main chapter Markdown file, including inline cross-references.
    Folder name uses book_key, file name and internal links use book_name_short.
    """
    book_name_short = book_key.split(" ", 1)[1]

    chapter_dir = Path(BASE_FOLDER) / book_key
    chapter_dir.mkdir(parents=True, exist_ok=True)
    chapter_file_path = chapter_dir / f"{book_name_short} {chapter_num}.md"
    
    markdown_lines = []

    # Navigation block
    markdown_lines.append(get_chapter_navigation(book_key, chapter_num, total_chapters_in_book))

    # Main chapter heading
    markdown_lines.append(f"# {book_name_short} {chapter_num}\n")

    printed_section_headings = set()

    sorted_verse_nums = sorted([int(v) for v in parsed_data["verses"].keys()])

    for verse_num_int in sorted_verse_nums:
        verse_num_str = str(verse_num_int)
        verse_data = parsed_data["verses"][verse_num_int]
        verse_content = verse_data["text"]

        # Add section heading if associated with this verse and not already added
        if verse_data["section_heading_id"] and \
           verse_data["section_heading_id"] in parsed_data["section_headings"] and \
           verse_data["section_heading_id"] not in printed_section_headings:

            heading_text = parsed_data["section_headings"][verse_data["section_heading_id"]]
            markdown_lines.append(f"## {heading_text}\n") # Add heading, followed by a single newline
            printed_section_headings.add(verse_data["section_heading_id"])

        # Add verse number and content
        markdown_lines.append(f"###### {verse_num_str}\n")
        markdown_lines.append(verse_content.strip() + "\n") # Ensure content is stripped and followed by single newline

        # Add study notes placeholder
        study_note_path = Path(OBSIDIAN_NOTES) / f"Study Notes For {book_name_short}" / f"STUDY NOTES FOR {book_name_short} {chapter_num}_{verse_num_str}.md"
        if study_note_path.exists():
            markdown_lines.append("> [!summary]- Study Notes\n") # Single newline after callout start
            markdown_lines.append(f"> ![[STUDY NOTES FOR {book_name_short} {chapter_num}_{verse_num_str}|Study Notes]]\n")
            markdown_lines.append("***\n") # Separator, followed by single newline

        # Add cross-reference block
        crossref_block_markdown = build_crossref_block(
            verse_data["crossrefs_raw_titles"],
            book_name_short,
            chapter_num
        )
        if crossref_block_markdown:
            markdown_lines.append(crossref_block_markdown) # build_crossref_block already adds trailing newline

    # Final navigation block
    markdown_lines.append(get_chapter_navigation(book_key, chapter_num, total_chapters_in_book))
    # Join all lines, removing any redundant blank lines that might occur from multiple appends
    final_markdown_content = []
    for line in markdown_lines:
        stripped_line = line.strip()
        if stripped_line or (final_markdown_content and final_markdown_content[-1].strip() != ""): # Check if previous line was not blank
            final_markdown_content.append(line)
            if stripped_line and not line.endswith('\n'): # Ensure a newline if it's a content line without one
                 final_markdown_content.append('\n')
    
    # A final pass to ensure no more than one blank line between blocks
    cleaned_final_markdown = []
    prev_line_was_blank = False
    for line in final_markdown_content:
        if line.strip() == "":
            if not prev_line_was_blank:
                cleaned_final_markdown.append("\n")
            prev_line_was_blank = True
        else:
            cleaned_final_markdown.append(line)
            prev_line_was_blank = False

    with open(chapter_file_path, "w", encoding="utf-8") as f:
        f.write("".join(cleaned_final_markdown).strip()) # Final strip to remove leading/trailing blanks
    print(f"Generated: ✅ {chapter_file_path}")

# --- Main Orchestration ---
def build_chapter(book_key, chapter_num):
    """Orchestrates the fetching, parsing, and writing for a single chapter."""
    book_name_short = book_key.split(" ", 1)[1]
    total_chapters_in_book = BOOKS[book_key]

    #print(f"  Fetching and processing {book_name_short} chapter {chapter_num}...")
    html_soup = fetch_html_content(book_key, chapter_num)
    
    if html_soup:
        save_cleaned_html_to_file(book_key, f"{chapter_num}_raw", html_soup)
        html_soup = remove_specific_html_elements(html_soup)# Clean the HTML structure
        save_cleaned_html_to_file(book_key, chapter_num, html_soup)
        parsed_data = parse_chapter_html(html_soup, book_name_short, chapter_num)
        
        # Generate main chapter file (now includes cross-references)
        generate_chapter_markdown(book_key, chapter_num, parsed_data, total_chapters_in_book)
        
        # Generate separate footnote files
        write_footnote_file(book_key, chapter_num, parsed_data["footnotes"])
    else:
        print(f" ❌ Skipping {book_key} {chapter_num} due to fetch error.")
    
    # Be polite to the API
    # time.sleep(random.uniform(2.0, 5.0))

def main():
    """Main function to iterate through all books and chapters."""
    DEBUG_FOLDER.mkdir(parents=True, exist_ok=True) # Ensure debug folder exists for the log
    error_log_path = DEBUG_FOLDER / "processing_failures.log"

    with open(error_log_path, "a", encoding="utf-8") as error_log:
        for book_key, ch_count in BOOKS.items():
            book_title = book_key.split(" ", 1)[1]
            book_name_short = book_key.split(" ", 1)[1]
            
            # Define expected output file path for the main chapter file
            chapter_file = Path(BASE_FOLDER) / book_key / f"{book_name_short} {1}.md" # Check for chapter 1 existence

            # Only skip if the first chapter of the book exists, assuming full book was processed
            # For more robust skipping, you might check all chapter files or use a manifest
            if chapter_file.exists():
                print(f"👍 Skipping Book {book_name_short} (first chapter already exists)")
                continue

            print(f"\nProcessing Book: 📘 {book_title} with {ch_count} Chapters")
            for chapter_num in range(1, ch_count + 1):
                try:
                    build_chapter(book_key, chapter_num)
                except Exception as e:
                    error_message = f"❌ Failed to process {book_key} {chapter_num}: {e}"
                    print(error_message)
                    error_log.write(f"{error_message}\n")

if __name__ == "__main__":
    main()
