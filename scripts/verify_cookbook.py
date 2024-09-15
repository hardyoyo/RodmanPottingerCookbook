#!/usr/bin/env python3

import os
import subprocess
from pdfreader import SimplePDFViewer

def extract_recipe_titles(markdown_file):
    cmd = f"recipemd {markdown_file} -t"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error extracting title from {markdown_file}")
        return []
    return [line.strip() for line in result.stdout.splitlines()]

def extract_text_from_pdf(pdf_file):
    fd = open(pdf_file, "rb")
    viewer = SimplePDFViewer(fd)

    text = ""
    try:
        while True:
            viewer.render()
            text += "".join(viewer.canvas.strings)
            viewer.next()
    except:
        pass

    fd.close()
    return text

def verify_titles_in_pdf(markdown_file, pdf_file):
    titles = extract_recipe_titles(markdown_file)
    pdf_text = extract_text_from_pdf(pdf_file)

    for title in titles:
        if title.lower() not in pdf_text.lower():
            return False

    return True

def main():
    source_dir = "recipes"
    output_dir = "build"

    sources = os.listdir(source_dir)
    total_tests = len(sources)
    passed_tests = 0

    for filename in sources:
        if filename.endswith(".md"):
            input_md = os.path.join(source_dir, filename)
            # TODO: use the correct cookbook filename here
            output_pdf = os.path.join(output_dir, f"{filename.replace('.md', '.pdf')}")

            print(f"Processing {filename}...")

            # NOT NECESSARY, the Makefile builds things, this script tests
            # Generate PDF using pandoc
            # cmd = f"pandoc {input_md} -o {output_pdf}"
            # subprocess.run(cmd, shell=True, check=True)

            # Verify titles
            if verify_titles_in_pdf(input_md, output_pdf):
                print(f"Test passed for {filename}")
                passed_tests += 1
            else:
                print(f"Test failed for {filename}")

    print(f"\nTotal tests: {total_tests}")
    print(f"Passed tests: {passed_tests}")
    print(f"Failed tests: {total_tests - passed_tests}")

if __name__ == "__main__":
    main()

