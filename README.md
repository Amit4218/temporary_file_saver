# Temporary File Saver

Lightweight Python app for uploading, temporarily storing, previewing, and auto-removing files after a short lifetime. Useful for sharing quick files or previews without a long-term storage cost.

**Features**
- Upload files via a web UI and get preview links.
- Automatic cleanup of expired files.
- Simple file size and lifetime checks.
- Small, dependency-light codebase for easy hosting.

**Quick Start**

Prerequisites: Python 3.10+ (or the version in `pyproject.toml`).

1. Create a virtual environment and install dependencies:

```bash
# if using python3 and pip

python3 -m venv .venv 
source .venv/bin/activate
pip install -r requirements.txt

# using uv
uv sync
```


2. Configure (optional): edit configuration in `config/` or provide env vars as needed. See `config/database.py` for DB settings and `utils/constants.py` for defaults.

3. Run the app:

```bash
python main.py

# or 

uv run main.py
```

4. Open http://localhost:5000/ (or the address printed by the server) to upload and preview files.

**Project Layout**
- `main.py` — application entrypoint.
- `core/` — core application logic (file saving, models, helpers).
- `utils/` — utility scripts (size checks, scheduled cleanup, path helpers).
- `templates/` and `static/` — frontend HTML, CSS, and JS for the upload/preview UI.
- `config/` — configuration and database helpers.

**Important modules**
- `core/save_file.py` — handles receiving and saving files.
- `utils/task_scheduler.py` — schedules periodic cleanup of expired files.
- `utils/check_expired_file.py` — logic to remove expired files from disk and DB.

**Running background cleanup**
The app includes a scheduler for cleaning expired files. Ensure the scheduler is started alongside the web server (it may be integrated in `main.py`), or run it as a separate process/cron job depending on deployment.

**Deployment notes**
- Serve the app behind a WSGI server (Gunicorn/uvicorn) for production.
- Ensure file storage directory (e.g., `temp/`) is writable and has sufficient disk space.
- Secure uploads via HTTPS and consider limits and virus scanning for public deployments.

**Contributing**
Pull requests welcome. Suggested workflow:
1. Fork the repo.
2. Create a branch for your feature/fix.
3. Run and test application locally.
4. Open a PR with a short description.

**License**

This project includes a license file in the repository. See [LICENSE](LICENSE) for the full terms.


