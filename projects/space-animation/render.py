from pathlib import Path
import subprocess
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parent
frames = root / "frames"
frames.mkdir(exist_ok=True)

print("Rendering the new 10-second galaxy animation...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        viewport={"width": 1280, "height": 720},
        device_scale_factor=1
    )
    page.goto((root / "animation.html").as_uri())

    for i in range(300):
        page.evaluate("(t) => window.renderAt(t)", i / 30)
        page.screenshot(
            path=str(frames / f"galaxy_{i:04d}.png")
        )
        if i % 30 == 0:
            print(f"Rendered {i // 30} of 10 seconds")

    browser.close()

output = root / "beyond_the_void_galaxy_style_test.mp4"

subprocess.run([
    "ffmpeg", "-y",
    "-framerate", "30",
    "-i", str(frames / "galaxy_%04d.png"),
    "-c:v", "libx264",
    "-preset", "ultrafast",
    "-crf", "18",
    "-pix_fmt", "yuv420p",
    "-an",
    str(output)
], check=True)

print("SUCCESS! VIDEO CREATED:", output)
