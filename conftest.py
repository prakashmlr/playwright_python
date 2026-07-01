from playwright.sync_api import Browser, BrowserContext, Page
import logging
import pytest
from dataclasses import dataclass

log = logging.getLogger(__name__)

base_url = ""

@dataclass
class EnvClass:
    context: BrowserContext
    page: Page
    url: str

def portal(browser: Browser, request: pytest.FixtureRequest);
    env = test_setup(browser, request)
    yield env
    test_teardown(env)
    
    
def test_setup(browser:Browser, request: pytest.FixtureRequest):
    context = browser.new_context()
    page = context.new_page()
    return EnvClass(
        context= context,
        page= page,
        url = base_url
    )

def test_teardown(env: EnvClass):
    env.page.close()
    env.context.close()

    
