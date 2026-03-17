# tests/e2e/conftest.py

import pytest
import subprocess
import time
import sys
import os
import requests


@pytest.fixture(scope="session")
def fastapi_server():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    env = os.environ.copy()
    for key in ("COVERAGE_PROCESS_START", "COV_CORE_SOURCE", "COV_CORE_CONFIG", "COV_CORE_DATAFILE"):
        env.pop(key, None)

    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=project_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )

    for _ in range(20):
        try:
            response = requests.get("http://localhost:8000")
            if response.status_code == 200:
                break
        except requests.ConnectionError:
            time.sleep(0.5)

    yield

    process.terminate()
    process.wait()


@pytest.fixture
def page(page):
    original_click = page.click

    def click_and_wait(*args, **kwargs):
        original_click(*args, **kwargs)
        page.wait_for_load_state("networkidle")

    page.click = click_and_wait
    return page
