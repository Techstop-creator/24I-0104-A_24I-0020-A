"""
LIFELINE Submission Packager
Creates the final compliant ZIP archive: 24I-0104-A_24I-0020-A.zip
"""

import os
import zipfile

ZIP_NAME = "24I-0104-A_24I-0020-A.zip"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def create_zip():
    print(f"Packaging {ZIP_NAME}...")
    with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as z:
        # 1. cases.xlsx
        z.write(os.path.join(BASE_DIR, "cases.xlsx"), arcname="cases.xlsx")
        
        # 2. generator/
        for root, dirs, files in os.walk(os.path.join(BASE_DIR, "generator")):
            for f in files:
                if f.endswith(('.py', '.md', '.txt')):
                    full_path = os.path.join(root, f)
                    rel_path = os.path.relpath(full_path, BASE_DIR)
                    z.write(full_path, arcname=rel_path)

        # 3. validator/
        for root, dirs, files in os.walk(os.path.join(BASE_DIR, "validator")):
            for f in files:
                if f.endswith(('.py', '.md', '.txt', '.xlsx')):
                    full_path = os.path.join(root, f)
                    rel_path = os.path.relpath(full_path, BASE_DIR)
                    z.write(full_path, arcname=rel_path)

        # 4. validation_report.txt
        z.write(os.path.join(BASE_DIR, "validation_report.txt"), arcname="validation_report.txt")

        # 5. approach_note.pdf
        z.write(os.path.join(BASE_DIR, "approach_note.pdf"), arcname="approach_note.pdf")

        # 6. proposal.pdf
        z.write(os.path.join(BASE_DIR, "proposal.pdf"), arcname="proposal.pdf")

        # 7. repository.txt
        z.write(os.path.join(BASE_DIR, "repository.txt"), arcname="repository.txt")

        # 8. members.txt
        z.write(os.path.join(BASE_DIR, "members.txt"), arcname="members.txt")

    print(f"Archive {ZIP_NAME} successfully created!")

    # Verify contents
    with zipfile.ZipFile(ZIP_NAME, "r") as z:
        print("\nZIP Contents:")
        for info in z.infolist():
            print(f"  {info.filename} ({info.file_size:,} bytes)")

if __name__ == "__main__":
    create_zip()

