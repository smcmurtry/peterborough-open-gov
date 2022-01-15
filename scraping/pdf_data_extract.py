import textract
from typing import List
import os

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


def save_output_file(text: str, html_fname="sample_minutes.html", format="html") -> None:
    lines = text.split("\n")
    header_index = get_header_index(lines)
    header_lines = lines[:header_index]
    body_lines = lines[header_index:]

    header_p_list = get_list_of_ps_from_header_lines(header_lines)
    body_p_list = get_list_of_ps_from_body_lines(body_lines)
    p_list = header_p_list + body_p_list

    output_lines = []
    if format == "html":
        output_lines = [html_format(line) for line in p_list]
    elif format == "text":
        output_lines = [line for line in p_list]

    output_file = "\n".join(output_lines)

    with open(html_fname, "w") as f:
        if format == "html":
            f.write("<!doctype html>")
            f.write("<div>")
            f.write(output_file)
            f.write("</div>")
        elif format == "text":
            f.write(output_file)


def convert_to_html(pdf_fname = "sample_minutes.pdf") -> None:
    binary_text = textract.process(pdf_fname)
    html_fname = pdf_fname.split(".")[0] + ".html"
    text = binary_text.decode("utf-8")
    save_output_file(text, html_fname, format)


def convert_to_text(pdf_fname="sample_minutes.txt") -> None:
    binary_text = textract.process(pdf_fname)
    txt_fname = pdf_fname.split(".")[0] + ".txt"
    text = binary_text.decode("utf-8")
    save_output_file(text, txt_fname, format="text")


def get_output_path(output_dir: str, pdf_fname: str, extension="html") -> str:
    output_fname = pdf_fname.split(".")[0] + "." + extension
    return output_dir + output_fname


if __name__ == "__main__":
    pdf_dir = "minutes/pdf/"
    pdf_files = [x for x in os.listdir(pdf_dir) if ".pdf" in x]

    output_dir = "minutes/txt/"
    for n, pdf_fname in enumerate(pdf_files):
        print(n, end=", ")
        pdf_path = pdf_dir + pdf_fname
        output_path = get_output_path(output_dir, pdf_fname, "txt")
        convert_to_text(pdf_path, output_path)