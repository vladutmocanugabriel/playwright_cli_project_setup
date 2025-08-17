from project_setup_helpers import *
from files_setup_helpers import *
from pathlib import Path
import sys

def main():
    project_name, force, dry_run = read_cli_args(sys.argv[1:])
    project_root = Path(project_name)

    if "--clean" in sys.argv[1:]:
        remove_node_project(project_root, dry_run)
        return

    check_prerequisites()
    project_root = ensure_root(project_name, dry_run)
    init_node_project(project_root, dry_run)
    create_folders(project_root, dry_run)
    create_files(project_root, dry_run, force)

    print("\n🚀 Done! Your Playwright testing project is ready.")
    if dry_run:
        print("🧪 This was a dry run. No actual files were written.")
    else:
        print(f"📁 Navigate to: {project_name}")
        print("💡 Run tests with: `npx playwright test`")

if __name__ == "__main__":
    main()
