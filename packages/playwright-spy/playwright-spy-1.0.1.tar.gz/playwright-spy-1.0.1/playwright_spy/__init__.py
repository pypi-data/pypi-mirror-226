import importlib.resources

from playwright.async_api import Page as AsyncPage, BrowserContext as AsyncContext
from playwright.sync_api import Page as SyncPage, BrowserContext as SyncContext


__all__ = ['load_sync', 'load_async']

SCRIPT = importlib.resources.read_text(package=__package__, resource="spy.min.js")


def load_sync(pw):
    """teaches synchronous playwright Page to be stealthy like a ninja!

    pw: type must between Page or Context
    """
    if not isinstance(pw, (SyncPage, SyncContext)):
        raise TypeError("Unknown Type! Type must between Page or Context")
    pw.add_init_script(SCRIPT)


async def load_async(pw):
    """teaches asynchronous playwright Page to be stealthy like a ninja!

    pw: type must between Page or Context
    """
    if not isinstance(pw, (AsyncPage, AsyncContext)):
        raise TypeError("Unknown Type! Type must between Page or Context")
    await pw.add_init_script(SCRIPT)


def pass_aliyun_sync(page: SyncPage):
    page.wait_for_load_state("networkidle")
    while page.title() == "滑动验证页面" or page.query_selector("#nc_1_nocaptcha", strict=True):
        if page.query_selector("#nc_1_n1z", strict=True):
            s = page.wait_for_selector("#nc_1_n1z", strict=True)
            s.click()
            box = s.bounding_box()
            page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.mouse.down()
            x = box["x"] + box["width"] / 2 + 260
            page.mouse.move(x, box["y"] + box["height"] / 2)
            page.mouse.up()
        else:
            s = page.wait_for_selector("#nc_1_nocaptcha", strict=True)
            s.click()
        page.wait_for_timeout(1000)
