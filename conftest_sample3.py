"""
This file holds fixtures for UI test cases (self-contained version).
"""

import logging
import os
from dataclasses import dataclass
from uuid import uuid4

import pytest
from playwright.sync_api import Browser, BrowserContext, Page

log = logging.getLogger(__name__)

# Base URL the tests launch against. Override with: BASE_URL=https://example.com pytest
BASE_URL = os.getenv("BASE_URL", "https://playwright.dev/")

# Directory where traces/videos/screenshots are written.
ARTIFACTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "artifacts")


@dataclass
class EnvironmentSettings:
    """Bundles together everything a test needs: context, page and config."""

    context: BrowserContext
    page: Page
    base_url: str
    trace: bool = False
    video: bool = False


def test_env_setup(browser: Browser, request: pytest.FixtureRequest) -> EnvironmentSettings:
    """Creates a fresh browser context + page, optionally with trace/video."""
    tracing_option = request.config.getoption("--tracing")
    capture_trace = tracing_option in ["on", "retain-on-failure"]
    video_option = request.config.getoption("--video")
    capture_video = video_option in ["on", "retain-on-failure"]

    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    context_params = {"ignore_https_errors": True}
    if capture_video:
        context_params["record_video_dir"] = os.path.join(ARTIFACTS_DIR, "videos")

    context = browser.new_context(**context_params)
    if capture_trace:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

    context.set_default_navigation_timeout(60000)
    context.set_default_timeout(60000)

    page = context.new_page()
    return EnvironmentSettings(
        context=context,
        page=page,
        base_url=BASE_URL,
        trace=capture_trace,
        video=capture_video,
    )


def test_env_teardown(env: EnvironmentSettings):
    """Stops trace/video and closes the page + context."""
    if env.trace:
        trace_path = os.path.join(ARTIFACTS_DIR, "{}.zip".format(uuid4()))
        env.context.tracing.stop(path=trace_path)
        log.info("Saved trace to %s", trace_path)
    env.page.close()
    env.context.close()
    if env.video:
        log.info("Saved video to %s", env.page.video.path())


def save_screenshot(portal: EnvironmentSettings):
    """Save a full-page screenshot of the current page into the artifacts dir."""
    path = os.path.join(ARTIFACTS_DIR, "{}.png".format(uuid4()))
    portal.page.screenshot(path=path, full_page=True)
    log.info("Saved screenshot to %s", path)


@pytest.fixture
def portal(browser: Browser, request: pytest.FixtureRequest):
    """Function-scoped portal: new browser context per test."""
    env = test_env_setup(browser, request)
    yield env
    test_env_teardown(env)


@pytest.fixture(scope="module")
def portal_module_scope(browser: Browser, request: pytest.FixtureRequest):
    """Module-scoped portal: one browser context shared across a module."""
    env = test_env_setup(browser, request)
    yield env
    test_env_teardown(env)
