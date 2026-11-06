"""
GitHub Automation Script for LIFELINE Phase 1
Creates private repo '24I-0104-A_24I-0020-A', invites staff, and pushes.
"""

import sys
import subprocess
import urllib.request
import json

STAFF_ACCOUNTS = [
    "Rida-Zubair",
    "aymanirshad",
    "mariamshaiq"
]

REPO_NAME = "24I-0104-A_24I-0020-A"

def setup(token, username):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "LIFELINE-Automator"
    }

    print(f"Creating private repository '{REPO_NAME}' for user '{username}'...")
    repo_url = "https://api.github.com/user/repos"
    payload = json.dumps({
        "name": REPO_NAME,
        "private": True,
        "description": "LIFELINE Algorithmic Relief-Command Engine - Phase 1 (Group 66)"
    }).encode('utf-8')

    req = urllib.request.Request(repo_url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f"Repository created successfully: {data.get('html_url')}")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        if e.code == 422 and "already exists" in err_body:
            print(f"Repository '{REPO_NAME}' already exists. Proceeding...")
        else:
            print(f"Error creating repo: {e.code} - {err_body}")
            return False

    # Add collaborators
    print("\nAdding staff collaborators...")
    for staff in STAFF_ACCOUNTS:
        collab_url = f"https://api.github.com/repos/{username}/{REPO_NAME}/collaborators/{staff}"
        collab_req = urllib.request.Request(collab_url, data=b"", headers=headers, method="PUT")
        try:
            with urllib.request.urlopen(collab_req) as resp:
                print(f"  + Invited collaborator: {staff}")
        except urllib.error.HTTPError as e:
            print(f"  - Failed to invite {staff}: {e.code} - {e.read().decode()}")

    # Git Remote & Push
    print("\nConfiguring git remote and pushing...")
    auth_remote = f"https://{username}:{token}@github.com/{username}/{REPO_NAME}.git"
    
    # Check if origin exists
    try:
        subprocess.run(["git", "remote", "remove", "origin"], check=False, capture_output=True)
    except Exception:
        pass

    subprocess.run(["git", "remote", "add", "origin", auth_remote], check=True)
    subprocess.run(["git", "branch", "-M", "main"], check=True)
    res = subprocess.run(["git", "push", "-u", "origin", "main"], capture_output=True, text=True)
    
    if res.returncode == 0:
        print("Successfully pushed all 8 commits to GitHub!")
        # Clean remote URL to not expose token locally
        clean_remote = f"https://github.com/{username}/{REPO_NAME}.git"
        subprocess.run(["git", "remote", "set-url", "origin", clean_remote], check=True)
        print(f"Remote URL cleaned to: {clean_remote}")
        
        # Update repository.txt
        with open("repository.txt", "w", encoding="utf-8") as f:
            f.write(f"https://github.com/{username}/{REPO_NAME}\n")
        print("Updated repository.txt with your GitHub URL.")
        
        # Repackage submission ZIP
        import create_submission_zip
        create_submission_zip.create_zip()
        print("Repackaged 24I-0104-A_24I-0020-A.zip with updated repository.txt!")
        return True
    else:
        print(f"Push error: {res.stderr}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python setup_github_and_collaborators.py <GITHUB_USERNAME> <GITHUB_TOKEN>")
        sys.exit(1)
    setup(sys.argv[2], sys.argv[1])

