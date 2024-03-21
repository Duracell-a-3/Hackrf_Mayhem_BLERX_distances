import re


def extract_ouis(file_path):
    """
    Extracts OUIs from the given file and prints them.

    Args:
        file_path (str): The path to the input file.
    """
    ouiList = []
    oui_pattern = re.compile(r"([0-9A-F]{2}:?){6}")  # Regular expression for OUI format

    with open(file_path, "r") as file:
        for line in file:
            identifier = line.split(",")[1]  # Get the Identifier field
            match = oui_pattern.search(identifier)

            if match:
                ouiList.append(match.group(0))
        return ouiList


def main():
    file_path = "distances.csv"
    outPath = "extract_ouis.csv"
    x = extract_ouis(file_path)
    with open(outPath, "w") as file:
        for item in x:
            file.write(str(item) + "\n")


main()
