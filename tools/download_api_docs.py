#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "playwright>=1.40.0",
#     "python-dotenv>=1.0.0",
# ]
# ///
"""
Download API documentation from VoIP.ms using Playwright browser automation.
"""

import os
import time

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Load environment variables from .env file
load_dotenv()


def login_with_redirect():
    """Login using redirect URL to go straight to API docs"""

    email = os.getenv("VOIPMS_USERNAME")
    password = os.getenv("VOIPMS_PASSWORD")

    if not email or not password:
        print("❌ Missing credentials!")
        print("\nPlease set environment variables:")
        print("  export VOIPMS_USERNAME='your-email@example.com'")
        print("  export VOIPMS_PASSWORD='your-website-password'")
        print("\nNote: This is your website password, NOT your API password")
        return False

    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Navigate to login WITH redirect parameter
            print("Opening VoIP.ms login with API redirect...")
            page.goto(
                "https://voip.ms/signin/index.php?redirect=/m/apidocs.php",
                wait_until="domcontentloaded",
            )
            page.wait_for_timeout(3000)

            # Handle cookie popup
            print("Handling popups...")
            if page.is_visible('button:has-text("Accept All")'):
                page.click('button:has-text("Accept All")')
                print("✓ Clicked Accept All")
            page.keyboard.press("Escape")
            page.wait_for_timeout(1000)

            # Fill login form
            print("\nFilling login form...")
            page.fill("#col_email", email)
            print(f"✓ Email: {email}")

            page.fill("#col_password", password)
            print("✓ Password: ********")

            # Screenshot before login
            page.screenshot(path="before_redirect_login.png")

            # Click login button
            print("\nClicking login...")
            page.click("#login-btn")
            print("✓ Clicked LOG IN")

            # Wait for redirect to API page
            print("\nWaiting for redirect to API page...")
            page.wait_for_timeout(7000)

            # Check where we ended up
            current_url = page.url
            print(f"\nCurrent URL: {current_url}")

            # Capture whatever page we're on
            content = page.content()

            # Save the content
            if "api" in current_url.lower():
                print("✓ We're on an API page!")

                if "api_username" in content or "getBalance" in content:
                    with open("api_docs_redirected.html", "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"✅ API documentation saved! ({len(content):,} bytes)")

                    print("\n" + "=" * 60)
                    print("✨ SUCCESS! API documentation captured!")
                    print("\nFile saved: api_docs_redirected.html")
                    print("\nNext steps:")
                    print("1. cp api_docs_redirected.html ../resources/")
                    print("2. cd ..")
                    print("3. uv run python3 enhanced_json_generator.py")
                    print("=" * 60)

                    return True
                else:
                    # Save it anyway
                    with open("api_page_content.html", "w", encoding="utf-8") as f:
                        f.write(content)
                    print("⚠️  On API page but no familiar content. Saved to api_page_content.html")
                    print("Check if this file contains the API documentation")

                    # Take screenshot
                    page.screenshot(path="api_page.png")
                    print("Screenshot saved: api_page.png")
            else:
                print(f"⚠️  Not on API page. Current URL: {current_url}")
                with open("redirect_result.html", "w", encoding="utf-8") as f:
                    f.write(content)
                page.screenshot(path="redirect_result.png")
                print("Saved redirect_result.html and .png")

            # Keep browser open
            print("\nBrowser stays open. You can manually navigate if needed.")
            print("Close browser when done.")

            while True:
                try:
                    page.title()
                    time.sleep(1)
                except:
                    break

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback

            traceback.print_exc()
        finally:
            try:
                browser.close()
            except:
                pass

    return False


def main():
    print("VoIP.ms Login with API Redirect")
    print("=" * 32)
    print("\nUsing redirect URL: ?redirect=/m/apidocs.php")
    print("This should take us directly to API docs after login!\n")

    success = login_with_redirect()

    if not success:
        print("\nIf the redirect didn't work, you can:")
        print("1. Manually navigate to the API page in the open browser")
        print("2. Check the saved HTML files")


if __name__ == "__main__":
    main()
