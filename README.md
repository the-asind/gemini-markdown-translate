# Documentation Translation

## Prerequisites

- Python 3.x (or you can use release executables) 
- Google Gemini API key (get FREE key from https://aistudio.google.com/app/apikey)

## Install 

### > for PROs

**Clone the repository:**
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   pip install google-generativeai
   ```

### > a simpler one

**Download last executable release**: https://github.com/the-asind/gemini-markdown-translate/releases

## Setup

2. **Create directories:**
   - Create a folder named `original` in the root directory and place the Markdown files (and/or folders with files) to be translated in it.
   - The translated files will be saved in a folder named `translated`.

3. **Change `promt.md`:**
   - Add the system instructions for translation in a file named `promt.md` in the root directory.

## Usage

1. **Run the script (or open .exe)**
   ```sh
   python main.py
   ```

2. **follow the instructions in the terminal**

## Notes

- The script reads the system instructions from `promt.md`.
- The script translates all `.md` files in the `original` directory and saves the translated files in the `translated` directory.
- If a translated file already exists (e.g. you interrupted the translation), you will be prompted to overwrite, ignore, or ignore always.

## Error Handling

- If the `original` folder is empty.
- If the `promt.md` file is missing.
- If the translation is blocked due to safety ratings, a message will be printed.

## License

This project is licensed under the MIT License.
