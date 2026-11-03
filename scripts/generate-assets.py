"""Generate high-contrast, clean 1200x675 hero images for FloatBoard blog articles.
Aesthetic inspired by Figma Real Estate showcase: Warm ivory canvas, rich olive green, warm sand accents.
Strict Rule: 100% generic mockups, ZERO personal data, ZERO private paths/usernames.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'blog' / 'assets'
ASSETS.mkdir(parents=True, exist_ok=True)

FONT_BOLD = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
FONT_REG = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
FONT_MONO = '/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf'
FONT_MONO_BOLD = '/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf'

def get_font(path, size):
    return ImageFont.truetype(path, size)

def draw_window_frame(draw, x, y, w, h, title="FloatBoard", bg="#ffffff", border="#2e4723"):
    # Window container with rounded corners and subtle shadow
    draw.rounded_rectangle([x+6, y+6, x+w+6, y+h+6], radius=16, fill="#e8e4da")
    draw.rounded_rectangle([x, y, x+w, y+h], radius=16, fill=bg, outline=border, width=2)
    # Titlebar
    draw.rounded_rectangle([x, y, x+w, y+48], radius=16, fill="#2e4723")
    draw.rectangle([x, y+32, x+w, y+48], fill="#2e4723")
    # Window dots
    draw.ellipse([x+18, y+18, x+30, y+30], fill="#f87171")
    draw.ellipse([x+38, y+18, x+50, y+30], fill="#fbbf24")
    draw.ellipse([x+58, y+18, x+70, y+30], fill="#34d399")
    # Title text
    f_title = get_font(FONT_BOLD, 16)
    draw.text((x+86, y+16), title, font=f_title, fill="#ffffff")

def generate_sticky_notes_image():
    W, H = 1200, 675
    img = Image.new("RGB", (W, H), "#faf8f3")
    draw = ImageDraw.Draw(img)

    # Subtle background pattern
    for gx in range(0, W, 40):
        draw.line([gx, 0, gx, H], fill="#f0ece1", width=1)
    for gy in range(0, H, 40):
        draw.line([0, gy, W, gy], fill="#f0ece1", width=1)

    # Main FloatBoard Floating Window
    draw_window_frame(draw, 140, 70, 920, 535, title="FloatBoard · Always-on-Top Floating Scratchpad")

    # Top Tag inside window
    draw.rounded_rectangle([175, 135, 420, 168], radius=9999, fill="#eef3eb", outline="#2e4723", width=1)
    draw.text((190, 142), "PINNED ABOVE WINDOWS 11", font=get_font(FONT_BOLD, 13), fill="#2e4723")

    draw.rounded_rectangle([435, 135, 680, 168], radius=9999, fill="#eadbb6", outline="#1e3117", width=1)
    draw.text((450, 142), "100% OFFLINE LOCAL MEMORY", font=get_font(FONT_BOLD, 13), fill="#1e3117")

    # Code / Scratchpad Area
    draw.rounded_rectangle([175, 185, 730, 565], radius=12, fill="#181e16")
    draw.text((200, 205), "// Temporary API Endpoints & Auth Keys (Stays Pinned)", font=get_font(FONT_MONO_BOLD, 15), fill="#eadbb6")
    lines = [
        ('const ', '#f472b6', 'CONFIG = {', '#ffffff'),
        ('  endpoint: ', '#94a3b8', '"https://api.internal/v1/health",', '#38bdf8'),
        ('  rateLimit: ', '#94a3b8', '120, // req / min', '#34d399'),
        ('  headers: {', '#ffffff', '', ''),
        ('    "Authorization": ', '#94a3b8', '"Bearer dev_staging_token_77a9",', '#fbbf24'),
        ('    "X-Request-Scope": ', '#94a3b8', '"offline-local-sandbox"', '#38bdf8'),
        ('  }', '#ffffff', '', ''),
        ('};', '#ffffff', '', ''),
        ('', '', '', ''),
        ('// FloatBoard stays floating while you code in VS Code', '#64748b', '', '')
    ]
    cur_y = 238
    for prefix, p_color, suffix, s_color in lines:
        if prefix:
            draw.text((200, cur_y), prefix, font=get_font(FONT_MONO, 14), fill=p_color)
        if suffix:
            draw.text((200 + draw.textlength(prefix, font=get_font(FONT_MONO, 14)), cur_y), suffix, font=get_font(FONT_MONO, 14), fill=s_color)
        cur_y += 28

    # Right Side Helper Card
    draw.rounded_rectangle([755, 185, 1025, 565], radius=12, fill="#fdfbf7", outline="#e2ddd2", width=1)
    draw.rounded_rectangle([755, 185, 1025, 235], radius=12, fill="#2e4723")
    draw.rectangle([755, 215, 1025, 235], fill="#2e4723")
    draw.text((775, 200), "Quick Checklist", font=get_font(FONT_BOLD, 15), fill="#ffffff")

    tasks = [
        ("✓  Zero OneNote Sync Bloat", "#2e4723"),
        ("✓  No Microsoft Account Required", "#2e4723"),
        ("✓  Stays Above Maximized Apps", "#2e4723"),
        ("✓  One-Click Always-on-Top", "#2e4723"),
        ("✓  Instant Clipboard Capture", "#2e4723"),
        ("✓  Zero Cloud Telemetry", "#2e4723"),
    ]
    ty = 260
    for task, tcol in tasks:
        draw.text((775, ty), task, font=get_font(FONT_BOLD, 13), fill=tcol)
        ty += 44

    dest = ASSETS / 'pin-sticky-notes-windows-11.jpg'
    img.save(dest, format='JPEG', quality=95)
    print('Generated', dest)

def generate_pureref_image():
    W, H = 1200, 675
    img = Image.new("RGB", (W, H), "#faf8f3")
    draw = ImageDraw.Draw(img)

    for gx in range(0, W, 40):
        draw.line([gx, 0, gx, H], fill="#f0ece1", width=1)
    for gy in range(0, H, 40):
        draw.line([0, gy, W, gy], fill="#f0ece1", width=1)

    draw_window_frame(draw, 140, 70, 920, 535, title="FloatBoard · Lightweight Visual Reference Board")

    # Badges
    draw.rounded_rectangle([175, 135, 410, 168], radius=9999, fill="#eef3eb", outline="#2e4723", width=1)
    draw.text((190, 142), "PURE-REF ALTERNATIVE", font=get_font(FONT_BOLD, 13), fill="#2e4723")

    draw.rounded_rectangle([425, 135, 660, 168], radius=9999, fill="#eadbb6", outline="#1e3117", width=1)
    draw.text((440, 142), "FAST · COMPACT · PINNED", font=get_font(FONT_BOLD, 13), fill="#1e3117")

    # Reference Image 1: Architectural minimalist building layout (Figma style)
    draw.rounded_rectangle([175, 185, 580, 420], radius=12, fill="#2e4723")
    # Draw geometric building silhouettes inside
    draw.polygon([(200, 420), (280, 240), (360, 240), (360, 420)], fill="#3e5d31")
    draw.polygon([(360, 420), (360, 210), (460, 210), (460, 420)], fill="#1e3117")
    draw.polygon([(460, 420), (460, 270), (555, 270), (555, 420)], fill="#4e723f")
    draw.text((195, 205), "Architecture & Contrast Study", font=get_font(FONT_BOLD, 13), fill="#ffffff")

    # Color Palette Swatches below
    draw.rounded_rectangle([175, 435, 580, 565], radius=12, fill="#ffffff", outline="#e2ddd2", width=1)
    draw.text((195, 448), "Extracted Palette Tokens", font=get_font(FONT_BOLD, 13), fill="#181e16")
    swatches = [
        ("#2e4723", "#2e4723", "Olive Dark"),
        ("#4a6b38", "#4a6b38", "Olive Light"),
        ("#eadbb6", "#eadbb6", "Warm Sand"),
        ("#181e16", "#181e16", "Charcoal"),
    ]
    sx = 195
    for hexcode, col, label in swatches:
        draw.rounded_rectangle([sx, 480, sx+85, 520], radius=8, fill=col)
        draw.text((sx+2, 532), label, font=get_font(FONT_BOLD, 11), fill="#556350")
        sx += 96

    # Right side: Design Notes & Dimensions
    draw.rounded_rectangle([600, 185, 1025, 565], radius=12, fill="#fdfbf7", outline="#e2ddd2", width=1)
    draw.rounded_rectangle([600, 185, 1025, 235], radius=12, fill="#2e4723")
    draw.rectangle([600, 215, 1025, 235], fill="#2e4723")
    draw.text((620, 200), "Project Constraints Note", font=get_font(FONT_BOLD, 15), fill="#ffffff")

    specs = [
        ("Target Canvas:", "1200px Grid / 16:9 Hero"),
        ("Contrast Ratio:", "14.5:1 (WCAG AAA Pass)"),
        ("Primary Color:", "Deep Forest Olive #2E4723"),
        ("Secondary Sand:", "Warm Sand #EADBB6"),
        ("Window Pinning:", "Always on Top (No Alt-Tab)"),
        ("Memory Footprint:", "< 25MB RAM Offline"),
    ]
    sy = 260
    for k, v in specs:
        draw.text((620, sy), k, font=get_font(FONT_BOLD, 13), fill="#181e16")
        draw.text((770, sy), v, font=get_font(FONT_REG, 13), fill="#4a5646")
        sy += 44

    dest = ASSETS / 'lightweight-pureref-alternative.jpg'
    img.save(dest, format='JPEG', quality=95)
    print('Generated', dest)

def generate_clipboard_manager_image():
    W, H = 1200, 675
    img = Image.new("RGB", (W, H), "#faf8f3")
    draw = ImageDraw.Draw(img)

    for gx in range(0, W, 40):
        draw.line([gx, 0, gx, H], fill="#f0ece1", width=1)
    for gy in range(0, H, 40):
        draw.line([0, gy, W, gy], fill="#f0ece1", width=1)

    draw_window_frame(draw, 140, 70, 920, 535, title="FloatBoard · Visual Offline Clipboard Manager")

    # Badges
    draw.rounded_rectangle([175, 135, 410, 168], radius=9999, fill="#eef3eb", outline="#2e4723", width=1)
    draw.text((190, 142), "VISUAL CLIPBOARD (WIN 11)", font=get_font(FONT_BOLD, 13), fill="#2e4723")

    draw.rounded_rectangle([425, 135, 680, 168], radius=9999, fill="#eadbb6", outline="#1e3117", width=1)
    draw.text((440, 142), "PINNED CLIPS & IMAGE PREVIEW", font=get_font(FONT_BOLD, 13), fill="#1e3117")

    # Clips Stack
    clips = [
        ("📌 [PINNED CODE]", "curl -s https://api.local/status -H 'X-Test: dev'", "#eef3eb", "#2e4723"),
        ("📌 [PINNED REF]", "Figma Token: --bg-page: #FAF8F5; --accent: #2E4723;", "#eadbb6", "#1e3117"),
        ("📌 [PINNED SQL]", "SELECT id, title, created_at FROM articles WHERE published = true;", "#f4f4f5", "#181e16"),
        ("📌 [IMAGE CLIP]", "Screenshot 1200x675 (Architecture Hero Reference) · Pinned", "#fdfbf7", "#2e4723"),
    ]
    cy = 185
    for tag, content, bgcol, bordercol in clips:
        draw.rounded_rectangle([175, cy, 1025, cy+75], radius=10, fill=bgcol, outline=bordercol, width=1)
        draw.text((195, cy+14), tag, font=get_font(FONT_BOLD, 12), fill=bordercol)
        draw.text((195, cy+38), content, font=get_font(FONT_MONO, 14), fill="#181e16")
        # Visual pin icon box
        draw.rounded_rectangle([960, cy+20, 1005, cy+55], radius=6, fill="#2e4723")
        draw.text((975, cy+27), "PIN", font=get_font(FONT_BOLD, 11), fill="#ffffff")
        cy += 88

    # Bottom status bar
    draw.rounded_rectangle([175, 545, 1025, 575], radius=6, fill="#181e16")
    draw.text((195, 552), "STATUS: 100% OFFLINE LOCAL MEMORY · ZERO NETWORK PERMISSIONS · INSTANT HOTKEY", font=get_font(FONT_MONO_BOLD, 11), fill="#34d399")

    dest = ASSETS / 'offline-clipboard-manager-windows-11.jpg'
    img.save(dest, format='JPEG', quality=95)
    print('Generated', dest)

if __name__ == '__main__':
    generate_sticky_notes_image()
    generate_pureref_image()
    generate_clipboard_manager_image()
