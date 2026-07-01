"""
This file holds a base test case to launch a webpage and assert content.
"""

import logging

import pytest
from playwright.sync_api import expect

from conftest import save_screenshot

log = logging.getLogger(__name__)


@pytest.mark.Plv
class TestExamplePage:
    """
    Base example: launch a page and assert something on it.
    """

    def test_launch_and_assert(self, portal):
        """
        *****Launch webpage and assert*****
        1. Navigate to the target URL.
        2. Wait for the page to finish loading.
        3. Assert the title, a visible element, and text content.
        """
        page = portal.page

        log.info("Navigating to the target webpage")
        page.goto(portal.base_url)
        page.wait_for_load_state("domcontentloaded")

        log.info("Asserting page title")
        expect(page).to_have_title(
            "Fast and reliable end-to-end testing for modern web apps | Playwright"
        )

        log.info("Asserting an element is visible")
        expect(page.get_by_role("link", name="Get started")).to_be_visible()

        log.info("Asserting text content")
        expect(page.locator("h1")).to_contain_text("Playwright")

        save_screenshot(portal)
