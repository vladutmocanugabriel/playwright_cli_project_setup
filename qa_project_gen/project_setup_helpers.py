import sys
import subprocess
import os
from pathlib import Path
import shutil

npm_cmd = None
npx_cmd = None

def read_cli_args(args):
    if not args:
        print("❌ Project name is missing. Usage: qa-gen <project-name> [--force] [--dry-run] [--path <destination>]")
        sys.exit(2)

    project_name = args[0]
    force = False
    dry = False
    path = "."

    i = 1
    while i < len(args):
        if args[i] == "--force":
            force = True
        elif args[i] == "--dry-run":
            dry = True
        elif args[i] == "--path" and i + 1 < len(args):
            path = args[i + 1]
            i += 1
        i += 1

    print(f"Project: {project_name} | Force: {force} | Dry-run: {dry} | Path: {path}")
    return project_name, force, dry, path


def resolve_cmd(cmd_name):
    path = shutil.which(cmd_name)
    if path is None:
        print(f"❌ '{cmd_name}' is not found in your PATH.")
        print(f"🔍 Current PATH: {os.environ.get('PATH')}")
        sys.exit(1)
    return path

def check_prerequisites():
    global npm_cmd, npx_cmd
    node_cmd = resolve_cmd("node")
    npm_cmd = resolve_cmd("npm")
    npx_cmd = shutil.which("npx")
    if npx_cmd is None:
        print("❌ 'npx' not found.")
        sys.exit(1)

    try:
        print("Running command:", [node_cmd, "--version"])
        node_check = subprocess.run(
            [node_cmd, "--version"],
            capture_output=True,
            text=True,
            check=True,
            env=os.environ.copy(),
        )
        node_check_result = node_check.stdout.strip()
        major = int(node_check_result.lstrip("v").split(".")[0])
        if major < 18:
            print("❌ Node.js 18+ required.")
            sys.exit(1)
        print(f"✅ Checked Node.js: {node_check_result}")

    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print("❌ Failed to run Node.js command.")
        print(str(e))
        sys.exit(1)

    try:
        print("Running command:", [npm_cmd, "--version"])
        npm_check = subprocess.run(
            [npm_cmd, "--version"],
            capture_output=True,
            text=True,
            check=True,
            env=os.environ.copy(),
        )
        print(f"✅ Checked npm: {npm_check.stdout.strip()}")

    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print("❌ Failed to run npm command.")
        print(str(e))
        sys.exit(1)

def create_folders(project_name, dry_run=False):
    base = Path(project_name)
    relative_paths = [
        "tests/e2e",
        "tests/front_end/feature_one",
        "tests/back_end/feature_one",
        "tests/support/POMs/feature_one",
        "tests/support/utils",
    ]

    for path in relative_paths:
        folder_path = base / path
        if dry_run:
            print(f"⚙️ [DRY RUN] would create: < {folder_path} >")
        else:
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"📥 Created: < {folder_path} >")

def ensure_root(project_name, dry_run=False):
    base = Path(project_name)
    if dry_run:
        print("⚙️ [DRY RUN] Would create root folder if missing:", base)
    else:
        if not base.exists():
            base.mkdir(parents=True)
            print("📥 Created:", base)
        else:
            print("✅ Exists:", base)
    return base


def init_node_project(project_root, dry_run=False):
    global npm_cmd, npx_cmd
    project_root = Path(project_root)
    if dry_run:
        print("⚙️ [DRY RUN] Would run: npm init -y")
        print("⚙️ [DRY RUN] Would run: npm install -D playwright @playwright/test typescript ts-node")
        if sys.platform.startswith("linux"):
            print("⚙️ [DRY RUN] Would run: npx playwright install --with-deps")
        else:
            print("⚙️ [DRY RUN] Would run: npx playwright install")
        return

    try:
        subprocess.run([npm_cmd, "init", "-y"], cwd=project_root, check=True)
        print("✅ Node.js project initialized.")
    except Exception as e:
        print(f"❌ Error initializing node project: {e}")
        sys.exit(1)

    try:
        subprocess.run([npm_cmd, "install", "-D", "@faker-js/faker"], cwd=project_root, check=True)
        print("✅ Faker.JS installed and ready to use.")
    except Exception as e:
        print(f"❌ Error installing faker: {e}")
        sys.exit(1)

    try:
        subprocess.run([npm_cmd, "install", "dotenv"], cwd=project_root, check=True)
        print("✅ DOTENV installed and ready to use.")
    except Exception as e:
        print(f"❌ Error installing dotenv: {e}")
        sys.exit(1)

    try:
        subprocess.run([npm_cmd, "install", "-D", "playwright", "@playwright/test", "typescript", "ts-node"], cwd=project_root, check=True)
        print("✅ Playwright is now installed.")
    except Exception as e:
        print(f"❌ Error installing Playwright: {e}")
        sys.exit(1)

    try:
        if sys.platform.startswith("linux"):
            subprocess.run([npx_cmd, "playwright", "install", "--with-deps"], cwd=project_root, check=True)
        else:
            subprocess.run([npx_cmd, "playwright", "install"], cwd=project_root, check=True)
        print("✅ Playwright browsers installed.")
    except Exception as e:
        print(f"❌ Error installing Playwright browsers: {e}")
        sys.exit(1)

def remove_node_project(project_root, dry_run=False):
    project_root = Path(project_root)

    targets = [
        project_root / "node_modules",
        project_root / "package.json",
        project_root / "package-lock.json",
        project_root / "tsconfig.json",
        project_root / "playwright.config.ts",
        project_root / "tests",
        project_root / ".gitignore",
        project_root / "README.md"
    ]

    for target in targets:
        if dry_run:
            print(f"⚙️ [DRY RUN] Would remove: {target}")
        else:
            if target.is_dir():
                shutil.rmtree(target, ignore_errors=True)
                print(f"🗑️ Removed directory: {target}")
            elif target.is_file():
                target.unlink(missing_ok=True)
                print(f"🗑️ Removed file: {target}")
            else:
                print(f"ℹ️ Nothing to remove at: {target}")
