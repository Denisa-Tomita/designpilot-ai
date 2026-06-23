import os

OUTPUT_DIR = "project_output"


def save_file(filename: str, content: str):

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Saved file: {path}")

    return path
