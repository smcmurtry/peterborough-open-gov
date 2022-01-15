import argparse
import textract
from typing import List
import os

parser = argparse.ArgumentParser()
parser.add_argument('--pdf_dir', '-pdf', help="pdf directory", type= str)
parser.add_argument('--txt_dir', '-txt', help="txt directory", type= str)

# if we are in the 1st 80ish lines, or until we see a line containing "roll call" or "called to order" (whichever comes first)
# we consider "\n" a line break, after that we consider "\n\n" a line break
# let's try just with "\n\n" and see what that looks like

def get_header_index(_lines: List[str]) -> int:
    max_header_index = 100
    # find the index where we shoulc change how we break paragraphs
    for n, line in enumerate(_lines):
        if n > max_header_index:
            return max_header_index
        lower_line = line.lower()
        if "roll call" in lower_line or "called to order" in lower_line:
            return n


def get_list_of_ps_from_header_lines(_lines: List[str]) -> List[str]:
    lines = [x.strip() for x in _lines]
    return lines


def get_list_of_ps_from_body_lines(_lines: List[str]) -> List[str]:
    # I need to remove the page numbers
    _lines_to_remove = [str(x) for x in range(100)] + ["\x0c"]
    lines_to_remove = set(_lines_to_remove)
    lines = [x.strip() for x in _lines if x.strip() not in lines_to_remove]
    new_lines = "\n".join(lines).split("\n\n")
    _new_lines = [line.replace("\n", " ").strip() for line in new_lines]
    return _new_lines


def html_format(line: str) -> str:
    if line:
        return f"<p>{line}</p>"
    return "<br>"


def save_output_file(text: str, output_fname="sample_minutes.html", file_format="html") -> None:
    lines = text.split("\n")
    header_index = get_header_index(lines)
    header_lines = lines[:header_index]
    body_lines = lines[header_index:]

    header_p_list = get_list_of_ps_from_header_lines(header_lines)
    body_p_list = get_list_of_ps_from_body_lines(body_lines)
    p_list = header_p_list + body_p_list

    output_lines = []
    if file_format == "html":
        output_lines = [html_format(line) for line in p_list]
    elif file_format == "text":
        output_lines = [line for line in p_list]

    output_file = "\n".join(output_lines)

    with open(output_fname, "w") as f:
        if file_format == "html":
            f.write("<!doctype html>")
            f.write("<div>")
            f.write(output_file)
            f.write("</div>")
        elif file_format == "text":
            f.write(output_file)


def convert_to_html(pdf_fname: str, html_fname: str) -> None:
    binary_text = textract.process(pdf_fname)
    text = binary_text.decode("utf-8")
    save_output_file(text, html_fname, file_format="html")


def convert_to_text(pdf_fname: str, txt_fname: str) -> None:
    binary_text = textract.process(pdf_fname)
    text = binary_text.decode("utf-8")
    save_output_file(text, txt_fname, file_format="text")


if __name__ == "__main__":
    args = parser.parse_args()

    pdf_dir = args.pdf_dir
    txt_dir = args.txt_dir

    pdf_files = [x for x in os.listdir(pdf_dir) if ".pdf" in x]

    for n, pdf_fname in enumerate(pdf_files):
        print(n, end=", ")
        pdf_path = f"{pdf_dir}/{pdf_fname}"
        txt_fname = pdf_fname.split(".")[0] + ".txt"
        # html_fname = pdf_fname.split(".")[0] + ".html"
        txt_path = f"{txt_dir}/{txt_fname}"
        convert_to_text(pdf_path, txt_path)