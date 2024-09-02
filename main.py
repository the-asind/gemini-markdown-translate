import os
import google.generativeai as genai

# Get the directory path of the current file
dir_path = os.path.dirname(os.path.realpath(__file__))

# Define the paths for the input and output directories
input_dir = dir_path + '/original/'
output_dir = dir_path + '/translated/'

# Read the system instructions from promt.md
with open('promt.md', 'r', encoding='utf-8') as file:
    system_instructions = file.read()


def translate_file(file_path, output_path):
    """
    Translates the content of a file using the Google Gemini API and writes the translated content to an output file.

    Args:
        file_path (str): The path to the input file to be translated.
        output_path (str): The path to the output file where the translated content will be saved.
    """
    response = None
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Create the model with system instructions
    model = genai.GenerativeModel(
        "models/gemini-1.5-flash",
        system_instruction=system_instructions
    )

    try:
        # Call the Google Gemini API to translate the content
        response = model.generate_content(f"{content}")

        # Check if the response contains valid Part
        if not response.text:
            raise ValueError("Invalid operation: The `response.text` quick accessor requires the response to contain "
                             "a valid `Part`, but none were returned.")

        translated_content = response.text.strip()

        # Write the translated content to the output file
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(translated_content)

    except ValueError as e:
        # Check the candidate.safety_ratings to determine if the response was blocked
        if hasattr(response, 'candidate') and hasattr(response.candidate, 'safety_ratings'):
            safety_ratings = response.candidate.safety_ratings
            print(f"Translation blocked due to safety ratings: {safety_ratings}")
        else:
            print(f"Error: {e}")
        print(f"\033[91mFailed to translate: {file_path[len(dir_path):]}\033[0m")


def translate_directory(input_dir, output_dir):
    """
    Translates all .md files in the input directory and saves the translated files in the output directory.

    Args:
        input_dir (str): The path to the input directory containing files to be translated.
        output_dir (str): The path to the output directory where the translated files will be saved.
    """
    # Count the total number of files to be translated
    files_count = sum(len(files) for _, _, files in os.walk(input_dir) if any(file.endswith('.md') for file in files))

    if files_count == 0:
        print("Error: The original folder is empty. Please add some files to translate.")
        return

    completed_files_count = 0
    ignore_always = False

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.md'):
                input_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_file_path, input_dir)
                output_file_path = os.path.join(output_dir, relative_path)

                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

                if os.path.exists(output_file_path):
                    if ignore_always:
                        completed_files_count += 1
                        print(f"Ignoring: {input_file_path[len(dir_path):]}")
                        continue

                    user_input = input(f"File {output_file_path} already exists. Do you want to (1) overwrite, "
                                       f"(2) ignore, or (3) ignore always?\n")
                    if user_input == '2':
                        print(f"Ignoring: {input_file_path[len(dir_path):]}")
                        continue
                    elif user_input == '3':
                        ignore_always = True
                        completed_files_count += 1
                        print(f"Ignoring: {input_file_path[len(dir_path):]}")
                        continue

                # Print the progress
                completed_files_count += 1
                print(f"{completed_files_count/files_count*100:.2f}% Translating: {input_file_path[len(dir_path):]}")

                translate_file(input_file_path, output_file_path)


if __name__ == '__main__':
    """Main entry point of the script."""
    print('Create in the root directory a folder named "original" and put the files to be translated in it.')
    print('The translated files will be saved in the "translated" folder.')
    if not os.path.exists('promt.md'):
        print('Error: The "promt.md" file is missing. Please create it and add the system instructions. See the '
              'README for more information.')
        exit()
    # Set up your Google Gemini API key
    genai.configure(api_key=input('Enter your Google Gemini API key: '))  # you may just paste your key here

    # Translate all files in the input directory
    translate_directory(input_dir, output_dir)