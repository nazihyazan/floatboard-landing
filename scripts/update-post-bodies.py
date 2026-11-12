#!/usr/bin/env python3
import json

def update_posts():
    with open('blog/posts.json', 'r', encoding='utf-8') as f:
        posts = json.load(f)

    post_map = {p['slug']: p for p in posts}

    # 1. start-two-image-reference-board (Blender 3D)
    if 'start-two-image-reference-board' in post_map:
        p = post_map['start-two-image-reference-board']
        p['intro'] = "When modeling hard-surface vehicles, characters, or props in Blender, splitting your 3D Viewport between front (NumPad 1) and right (NumPad 3) orthographic cameras takes away valuable screen real estate. FloatBoard pins your front and side blueprint references in an always-on-top floating card directly above Blender, letting you model vertices, adjust edge loops, and check subdivision topology without minimizing or wrestling with background image empties."
        p['sections'] = [
            {
                "id": "blender-orthographic-alignment",
                "title": "Set up Front and Side Blueprint Orthographics",
                "html": "<p>Hard-surface modeling in Blender requires constant alignment between front (NumPad 1) and right side (NumPad 3) orthographic projections. Traditionally, artists import reference images as Viewport Empties or Background Images. However, viewport empties can shift when you accidentally rotate your camera, clutter your outliner hierarchy, and slow down viewport playback on complex subdivision surfaces.</p><p>FloatBoard decouples your blueprints from the Blender scene. By pinning your front and side reference cards in a hardware-accelerated floating window locked in the upper corner of your monitor, you can freely orbit, pan, and zoom in your perspective viewport (NumPad 5) while keeping the exact silhouette proportions visible.</p>"
            },
            {
                "id": "eliminate-viewport-empties",
                "title": "Avoid Cluttering Blender with Viewport Background Empties",
                "html": "<p>When working on multi-part assets like mechanical props or automotive chassis, keeping image empties inside your Blender file causes several workflow bottlenecks:</p><ul><li>Empties get accidentally selected during box-select operations in Object Mode unless manually toggled as non-selectable in the Outliner.</li><li>Depth sorting issues in X-Ray mode (Alt + Z) can obscure mesh wireframes behind semi-transparent references.</li><li>Exporting FBX or glTF files for Unreal Engine or Unity risks bundling unnecessary reference empties into the game asset hierarchy.</li></ul><p>FloatBoard operates completely outside Blender's memory space, ensuring your .blend file remains 100% clean and export-ready.</p>"
            },
            {
                "id": "lock-subdivision-topology",
                "title": "Check Mesh Proportions and Subdivision Curvature",
                "html": "<p>Before applying a Subdivision Surface modifier, verifying edge loop flow against authentic vehicle or anatomy blueprints prevents tedious retopology later. Placing FloatBoard right above your 3D Viewport lets you align vertices along characteristic silhouette lines with sub-pixel precision.</p><p>With FloatBoard's spacebar QuickLook feature, you can instantly magnify fine mechanical details—such as door panel gaps or aero splitters—without leaving your active Blender edit session.</p>"
            },
            {
                "id": "pureref-alternative-workflow",
                "title": "Lightweight Alternative to PureRef for Single-Screen 3D Artists",
                "html": "<p>While PureRef is widely used in the 3D industry, its infinite canvas model often leads to sprawling boards that consume gigabytes of RAM and lack integrated text scratchpads for jotting down modifier stack notes or shortcut reminders.</p><p>FloatBoard is designed as a focused, lightweight companion that pairs dual reference slots with an active text scratchpad. For artists looking for a simpler reference setup without memory-heavy canvas navigation, check our full comparison of <a href=\"/blog/lightweight-pureref-alternative-reference-board/\">lightweight PureRef alternatives for desktop</a>.</p>"
            },
            {
                "id": "blender-reference-faq",
                "title": "Frequently Asked Questions About Blender Reference Setup",
                "html": "<h3>Does FloatBoard interfere with Blender keyboard shortcuts like G, R, and S?</h3><p>No. FloatBoard stays pinned on top visually without stealing keyboard focus, meaning your Blender transform shortcuts (G for Grab, R for Rotate, S for Scale) remain completely responsive in the 3D Viewport.</p><h3>Can I run FloatBoard on Linux with Blender?</h3><p>Yes. FloatBoard provides native support for Ubuntu, Fedora, and Arch Linux, integrating seamlessly with both X11 and Wayland desktop environments.</p>"
            }
        ]

    # 2. review-image-grid-and-large-preview (DaVinci Resolve & Premiere)
    if 'review-image-grid-and-large-preview' in post_map:
        p = post_map['review-image-grid-and-large-preview']
        p['intro'] = "Color grading in DaVinci Resolve or Premiere Pro requires constant comparison between your current timeline shot and client reference stills or LUT moodboards. Instead of cluttering your Color Page with gallery wipes or toggling split screens, FloatBoard pins a grid of graded stills and color palettes directly above your vectorscopes and waveform monitors."
        p['sections'] = [
            {
                "id": "davinci-resolve-color-matching",
                "title": "Keep Hero Reference Stills Anchored Over DaVinci's Color Page",
                "html": "<p>Matching skin tones, highlight roll-off, and shadow tint across scenes is one of the most demanding tasks in post-production. While DaVinci Resolve provides an internal Gallery Wipe feature, toggling split screens repeatedly interrupts the colorist's visual rhythm and temporarily hides timeline scopes.</p><p>FloatBoard allows colorists to float reference stills directly alongside the Vectorscope and Waveform monitor. This persistent reference window enables real-time color balancing on primary color wheels without constantly activating and deactivating wipe overlays.</p>"
            },
            {
                "id": "premiere-lumetri-workflow",
                "title": "Compare Moodboard Palettes in Premiere Pro Lumetri Color",
                "html": "<p>In Adobe Premiere Pro, applying creative Look Up Tables (LUTs) through the Lumetri Color panel frequently requires checking client visual guidelines. Toggling back to a PDF deck or browser moodboard introduces cognitive friction and breaks color perception.</p><p>By anchoring a curated 4-card reference grid in FloatBoard, video editors can evaluate Lumetri Curves, HSL Secondary selections, and Vignette settings against approved project art directions instantly.</p>"
            },
            {
                "id": "multitasking-single-monitor-colorist",
                "title": "Grade with Reference Grids on a Single Editing Display",
                "html": "<p>Many independent video editors and colorists work on high-color-accuracy laptops (such as Apple MacBook Pro Liquid Retina XDR displays or calibrated OLED workstations) where dual-monitor setups are unavailable during travel or set shoots.</p><p>When working on a single display, pairing your stills with an <a href=\"/blog/always-on-top-floating-notes-developers-multitasking/\">always-on-top floating notes scratchpad</a> keeps client hex codes, revision timestamps, and LUT names right beside your video scopes without blocking essential playback controls.</p>"
            },
            {
                "id": "color-grading-stills-faq",
                "title": "Frequently Asked Questions About Video Reference Stills",
                "html": "<h3>Does FloatBoard affect color calibration or apply ICC profile shifts?</h3><p>FloatBoard renders images using hardware-accelerated sRGB rendering, ensuring consistent luminance and saturation values that match your calibrated display.</p><h3>Can I store text notes alongside color reference images?</h3><p>Yes. FloatBoard features an integrated text scratchpad next to image tiles, allowing you to log client revision timestamps and camera ISO/shutter notes side by side with visual stills.</p>"
            }
        ]

    # 3. keep-web-image-reference-visible-while-browsing (Digital Artists)
    if 'keep-web-image-reference-visible-while-browsing' in post_map:
        p = post_map['keep-web-image-reference-visible-while-browsing']
        p['intro'] = "Digital painting in Photoshop, Krita, or Clip Studio Paint demands constant glance-back references for bone landmarks, dynamic poses, and subsurface scattering. On graphics tablets like Wacom Cintiq or Huion, resizing your painting canvas to fit references wastes drawing area. FloatBoard pins high-res anatomy and lighting crops right above your digital canvas."
        p['sections'] = [
            {
                "id": "tablet-anatomy-pinning",
                "title": "Lock Anatomy and Key Lighting Beside Your Painting Canvas",
                "html": "<p>Illustrators and concept artists often spend hours hunting for gesture, costuming, and facial expressions before starting a piece. When painting on a display tablet (Wacom, Huion, XP-Pen), having to continuously resize canvas windows or zoom out to inspect moodboard layers disrupts drawing flow.</p><p>FloatBoard hovers quietly in the corner of your screen as a dedicated floating art reference board. You can lock high-resolution anatomy turnarounds, muscle studies, and rim-light photos right where your eyes can track them while drawing brushstrokes.</p>"
            },
            {
                "id": "photoshop-krita-integration",
                "title": "Zero Canvas Resizing in Photoshop, Krita & Clip Studio Paint",
                "html": "<p>Instead of pasting reference images onto separate Photoshop layers—which bloats file sizes and creates layer clutter—FloatBoard holds your reference material completely outside the drawing document. In Krita and Clip Studio Paint, FloatBoard stays pinned above full-screen canvas modes without triggering unwanted window minimizes.</p><p>With keyboard shortcut QuickLook (Spacebar), artists can magnify fine skin textures or fabric weaves to 100% scale without disrupting their active brush tool.</p>"
            },
            {
                "id": "pureref-comparison-artists",
                "title": "Lightweight PureRef Alternative for Stylus and Tablet Work",
                "html": "<p>While PureRef is popular among illustrators, it can consume substantial RAM when handling large collections of high-res images and lacks integrated text scratchpads for client notes or color hex codes.</p><p>Artists who want a cleaner board that includes text scratchpads for client notes can explore why FloatBoard serves as a <a href=\"/blog/lightweight-pureref-alternative-reference-board/\">lightweight PureRef alternative for reference boards</a> on desktop.</p>"
            },
            {
                "id": "digital-artist-reference-faq",
                "title": "Frequently Asked Questions About Digital Art Reference Setup",
                "html": "<h3>Does drawing with a stylus tablet interfere with FloatBoard?</h3><p>No. FloatBoard only responds to direct clicks on its cards. When drawing in Photoshop or Krita with a pen tablet, stylus input passes seamlessly to your drawing canvas.</p><h3>Can I quickly hide FloatBoard during final artwork review?</h3><p>Yes. A single hotkey minimizes or hides FloatBoard instantly, letting you inspect your completed illustration unobstructed.</p>"
            }
        ]

    # 4. inspect-image-original-after-thumbnail (Linux Users)
    if 'inspect-image-original-after-thumbnail' in post_map:
        p = post_map['inspect-image-original-after-thumbnail']
        p['intro'] = "On Ubuntu, Fedora, and Arch Linux desktops, inspecting image crops or screenshot details from the clipboard usually involves launching bulky image viewers like GIMP, Eye of GNOME (eog), or Gwenview. FloatBoard provides Linux creators and developers with a native, lightweight Wayland/X11 floating scratchpad that renders full-resolution clipboard crops instantly without file saving or window management overhead."
        p['sections'] = [
            {
                "id": "linux-clipboard-image-flow",
                "title": "Instant 1:1 Pixel Inspection on Ubuntu, Fedora & Arch",
                "html": "<p>Linux power users frequently capture terminal outputs, UI bugs, or graphic assets with tools like Spectacle, Flameshot, or GNOME Screenshot. Opening an image viewer just to check text sharpness or hex colors introduces unnecessary system overhead and clutters your workspace with temporary files in /tmp/.</p><p>FloatBoard receives clipboard image data directly through native Linux clipboard APIs. Simply copy any screenshot or web image, and FloatBoard displays it immediately with crystal-clear 1:1 pixel rendering.</p>"
            },
            {
                "id": "wayland-x11-floating-pin",
                "title": "Native Always-on-Top Floating on Linux Desktops",
                "html": "<p>Under Wayland compositors (GNOME Mutter, KDE KWin, Sway) and X11 window managers (i3, bspwm, XFCE), managing always-on-top window rules often requires editing compositor configuration files or wrestling with window decoration menus.</p><p>FloatBoard handles window pinning internally with zero configuration, remaining consistently anchored over your active terminal emulators, IDEs, and browser windows.</p>"
            },
            {
                "id": "linux-clipboard-manager-efficiency",
                "title": "Offline Clipboard History for Linux Power Users",
                "html": "<p>Unlike cloud-dependent clipboard synchronization utilities that transmit sensitive server tokens or private screenshots to third-party endpoints, FloatBoard stores all reference data strictly on your local machine.</p><p>For developers who require full history privacy and offline security across distributions, see our comprehensive guide to the <a href=\"/blog/best-offline-clipboard-manager-windows-11/\">best offline clipboard managers</a>.</p>"
            },
            {
                "id": "linux-image-inspection-faq",
                "title": "Frequently Asked Questions About Linux Image Reference Tools",
                "html": "<h3>Does FloatBoard support Wayland natively on Linux?</h3><p>Yes. FloatBoard runs smoothly on both Wayland and X11 display servers across major Linux distributions including Ubuntu 24.04, Fedora 40, and Arch Linux.</p><h3>How does FloatBoard handle system memory on Linux?</h3><p>FloatBoard uses an efficient, hardware-accelerated rendering engine with minimal background memory usage, making it ideal for resource-conscious Linux workstations.</p>"
            }
        ]

    # 5. collect-visual-references-across-search-pages (Architects & Interior Designers)
    if 'collect-visual-references-across-search-pages' in post_map:
        p = post_map['collect-visual-references-across-search-pages']
        p['intro'] = "Architectural visualization and interior design require gathering dozens of disparate finishes: terrazzo flooring, brushed brass fixtures, acoustic felt baffles, and veneer grain samples. FloatBoard lets architects collect swatches, supplier specs, and material references directly from web searches into a unified floating board that hovers over Revit, SketchUp, and AutoCAD."
        p['sections'] = [
            {
                "id": "material-swatch-curation",
                "title": "Curate Finish Palettes Across Multiple Supplier Catalogs",
                "html": "<p>Sourcing architectural specifications requires visiting dozens of manufacturer websites for stone, wood, metal, and textile finishes. Keeping 40 browser tabs open while cross-referencing floor plans wastes time and increases mental fatigue.</p><p>FloatBoard allows designers to copy material swatches directly from online supplier catalogs into a consolidated visual board. Tiles auto-align into a clean grid that stays pinned over your screen while browsing.</p>"
            },
            {
                "id": "revit-sketchup-overlay",
                "title": "Keep Material Moodboards Pinned Over Revit and SketchUp",
                "html": "<p>When assigning realistic PBR materials, reflectance properties, and bump maps in Revit, SketchUp, or 3ds Max, having the client-approved moodboard floating beside your 3D model ensures visual consistency across all elevations.</p><p>Designers can check gloss levels, fabric textures, and timber stains directly without toggling away from the modeling viewport.</p>"
            },
            {
                "id": "spec-notes-alongside-swatches",
                "title": "Store Manufacturer SKU Numbers Beside Material Images",
                "html": "<p>A visual moodboard is only half the equation in architectural practice; every material must map to a specific manufacturer SKU, fire-rating code, and price per square meter.</p><p>Pairing visual swatches with text specs prevents specification errors; learn how an <a href=\"/blog/always-on-top-floating-notes-developers-multitasking/\">always-on-top floating scratchpad</a> streamlines technical drafting and client reviews.</p>"
            },
            {
                "id": "architecture-material-faq",
                "title": "Frequently Asked Questions About Architectural Material Boards",
                "html": "<h3>Can I export material moodboards from FloatBoard for client presentations?</h3><p>Yes. FloatBoard allows quick exporting of your active board or individual high-resolution swatch images for inclusion in client PDF presentations and spec sheets.</p><h3>Does FloatBoard work across multiple monitors in an architectural studio?</h3><p>Yes. You can position FloatBoard on your primary modeling screen or float it over your secondary drafting monitor according to your studio setup.</p>"
            }
        ]

    # 6. organize-image-references (7 Best PureRef Alternatives)
    if 'organize-image-references' in post_map:
        p = post_map['organize-image-references']
        p['intro'] = "PureRef has long been the gold standard for visual artists, but its lack of native rich-text note pads, heavy memory footprint with large canvases, and steep navigation curve have led many creators to look for modern alternatives. We compare the 7 best PureRef alternatives in 2026 for digital painters, 3D modelers, and UI designers."
        p['sections'] = [
            {
                "id": "pureref-limitations",
                "title": "Why Creators Look for Modern PureRef Alternatives",
                "html": "<p>While PureRef is remarkably versatile, many everyday creative workflows run into specific roadblocks with its infinite-canvas philosophy:</p><ul><li>Lack of integrated, structured text scratchpads alongside image cards.</li><li>Heavy RAM usage when large image collections remain loaded in memory.</li><li>Keyboard navigation and canvas zooming that can feel disconnected from standard desktop conventions.</li><li>No built-in clipboard text management for code, hex codes, or prompt notes.</li></ul>"
            },
            {
                "id": "top-alternatives-breakdown",
                "title": "Top 7 PureRef Alternatives Compared for 2026",
                "html": "<p>We evaluated the leading reference board tools available across Windows, macOS, and Linux:</p><ol><li><strong>FloatBoard:</strong> The premier lightweight hybrid tool combining image tiles with an always-on-top text scratchpad. 100% offline and sub-40ms latency.</li><li><strong>Kuadro:</strong> Lightweight per-image floating viewer, but lacks unified multi-card grid layouts and text notes.</li><li><strong>BeeRef:</strong> Open-source Python/Qt reference viewer, though interface customization is limited.</li><li><strong>Eagle:</strong> Powerful asset management library, but heavier footprint designed for long-term archiving rather than quick floating reference.</li><li><strong>VizRef:</strong> Solid iPad alternative for mobile illustrators.</li><li><strong>Pureref (Legacy):</strong> Still robust for massive 100+ image moodboards, though resource-heavy.</li><li><strong>Milanote:</strong> Cloud-based moodboard builder, but requires constant internet connectivity and monthly subscription fees.</li></ol>"
            },
            {
                "id": "floatboard-hybrid-advantage",
                "title": "Why FloatBoard is the Best Lightweight Choice for Multitaskers",
                "html": "<p>FloatBoard bridges the gap between dedicated reference viewers and daily productivity tools. Instead of managing unwieldy infinite canvases, FloatBoard offers an organized floating board that pairs reference imagery with quick note taking.</p><p>Read our in-depth analysis on why creators are switching to our <a href=\"/blog/lightweight-pureref-alternative-reference-board/\">lightweight PureRef alternative reference board</a>.</p>"
            },
            {
                "id": "pureref-alternatives-faq",
                "title": "Frequently Asked Questions About PureRef Alternatives",
                "html": "<h3>Is FloatBoard free to download?</h3><p>Yes. FloatBoard offers a fully functional free tier for Windows, Mac, and Linux, with optional lifetime licenses for power users.</p><h3>Does FloatBoard require an internet connection?</h3><p>No. FloatBoard is 100% offline and stores all your data locally on your device with zero cloud tracking.</p>"
            }
        ]

    # 7. copy-web-image-and-keep-source (Designers Source Attribution)
    if 'copy-web-image-and-keep-source' in post_map:
        p = post_map['copy-web-image-and-keep-source']
        p['intro'] = "Browsing design galleries like Mobbin, Dribbble, and Behance often leaves designers with a folder full of unlabeled PNGs and no way to trace the original prototype or creator. FloatBoard automatically preserves source URLs, dimensions, and timestamps alongside every copied image, keeping your visual inspiration organized and properly attributed."
        p['sections'] = [
            {
                "id": "attribution-friction",
                "title": "The Cost of Lost Source URLs in Design Research",
                "html": "<p>Every designer has experienced finding the perfect UI layout or typography sample on desktop, only to discover weeks later that the image file is named 'Screenshot_2026-04-12.png' with no indication of what app or design system it came from. Finding the live production URL or original designer becomes virtually impossible.</p><p>FloatBoard solves this by automatically attaching metadata—including origin URLs, resolution, and capture timestamps—to every image card in your board.</p>"
            },
            {
                "id": "automatic-origin-logging",
                "title": "Pin Web Images with Clickable Origin Metadata",
                "html": "<p>When copying UI patterns from platforms like Mobbin, Behance, or Awwwards, FloatBoard's integrated metadata inspector lets you click directly through to the original source page anytime during your design sprint. You never have to re-search or maintain separate spreadsheet link trackers.</p>"
            },
            {
                "id": "clipboard-source-pairing",
                "title": "Clipboard Ingestion Without Cloud Tracking",
                "html": "<p>Many modern bookmarking and design curation apps upload your research to cloud servers for AI indexing or team analytics. For internal enterprise projects and unreleased product audits, this creates significant security and NDA risks.</p><p>Ensure your design assets remain private with a secure, 100% local tool by exploring the <a href=\"/blog/best-offline-clipboard-manager-windows-11/\">best offline clipboard manager for Windows 11</a>.</p>"
            },
            {
                "id": "source-attribution-faq",
                "title": "Frequently Asked Questions About Saving Image Source URLs",
                "html": "<h3>How does FloatBoard capture web source URLs?</h3><p>When you copy an image from standard web browsers (Chrome, Edge, Firefox, Brave), FloatBoard extracts the clipboard HTML metadata to record the origin URL automatically.</p><h3>Can I export my curated image boards with links?</h3><p>Yes. You can export cards along with their source links into Markdown or CSV format for design documentation.</p>"
            }
        ]

    # 8. shortlist-landscape-photos-for-website-hero (Web Designers Staging)
    if 'shortlist-landscape-photos-for-website-hero' in post_map:
        p = post_map['shortlist-landscape-photos-for-website-hero']
        p['intro'] = "Choosing the right hero imagery for a SaaS landing page or e-commerce storefront cannot be done in a separate file viewer. You need to test typography legibility, button contrast, and focal point alignment directly against your live navigation bar and headlines. FloatBoard lets web designers float candidate images over active staging builds to test contrast instantly."
        p['sections'] = [
            {
                "id": "hero-contrast-testing",
                "title": "Test Headline Readability and CTA Contrast Live",
                "html": "<p>A landscape photo that looks stunning in an image viewer can completely fail as a website hero if high-frequency details (such as trees or snow peaks) clash with your white H1 typography or primary CTA buttons.</p><p>By floating candidate hero images directly over your local development server or Figma canvas, FloatBoard lets you test visual contrast and headline legibility in real time before writing a single line of CSS.</p>"
            },
            {
                "id": "responsive-aspect-ratio-check",
                "title": "Evaluate Focal Points Across Mobile and Desktop Viewports",
                "html": "<p>Modern responsive headers change aspect ratio dramatically from ultra-wide 21:9 monitors to vertical 9:16 mobile screens. FloatBoard allows you to quickly crop and inspect how subject elements behave under different viewport constraints.</p>"
            },
            {
                "id": "pureref-layout-comparison",
                "title": "Side-by-Side Candidate Evaluation Without Photoshop",
                "html": "<p>Instead of creating heavy Photoshop artboards with 10 different hero variations, FloatBoard lets you cycle through candidate images with spacebar previews directly over your live layout.</p><p>For comparing multiple marketing variations side by side without heavyweight software, see our guide on <a href=\"/blog/lightweight-pureref-alternative-reference-board/\">lightweight reference board alternatives</a>.</p>"
            },
            {
                "id": "hero-image-staging-faq",
                "title": "Frequently Asked Questions About Hero Image Testing",
                "html": "<h3>Can I adjust the opacity of FloatBoard while testing hero images?</h3><p>Yes. FloatBoard provides opacity slider controls so you can overlay semi-transparent candidates directly across your typography.</p><h3>Does FloatBoard support high-DPI retina screenshots?</h3><p>Yes. FloatBoard maintains full 2x and 3x retina resolution on macOS and Windows high-DPI displays.</p>"
            }
        ]

    # 9. capture-webpage-detail-screenshot-reference (UX Designers Rapid Moodboards)
    if 'capture-webpage-detail-screenshot-reference' in post_map:
        p = post_map['capture-webpage-detail-screenshot-reference']
        p['intro'] = "Competitive UX research requires capturing granular details: modal animations, microcopy variations, onboarding progress bars, and mobile checkout patterns. FloatBoard allows product designers to crop webpage components directly to an always-on-top scratchpad, assembling rich competitive audits in minutes without cluttering their Downloads directory."
        p['sections'] = [
            {
                "id": "ux-microinteraction-capture",
                "title": "Capture Micro-Interactions and Form Patterns at Speed",
                "html": "<p>Auditing competitor user journeys requires grabbing dozens of specific UI elements: tooltips, pricing toggle switches, input validation error banners, and sticky navigation headers. Using standard screenshot utilities creates a mess of disconnected files on your desktop.</p><p>With FloatBoard, every screen crop is instantly ingested into an organized floating moodboard that stays visible while you navigate competitor applications.</p>"
            },
            {
                "id": "zero-file-clutter-workflow",
                "title": "Build Audit Moodboards Without Hundreds of Temporary PNGs",
                "html": "<p>FloatBoard holds your active research set entirely in memory and lightweight local storage. You never have to spend 15 minutes deleting 'Screenshot (128).png' files from your Downloads folder after finishing an audit sprint.</p>"
            },
            {
                "id": "floating-designer-scratchpad",
                "title": "Synthesize UX Observations Alongside Screenshots",
                "html": "<p>A visual audit is only complete when paired with critical analysis of user friction and usability heuristics. FloatBoard's integrated text notes scratchpad lets you type feedback directly beside each UI screen crop.</p><p>Jot down heuristic notes and usability pros/cons alongside visual crops with an <a href=\"/blog/always-on-top-floating-notes-developers-multitasking/\">always-on-top floating scratchpad for multitasking designers</a>.</p>"
            },
            {
                "id": "ux-screenshot-moodboard-faq",
                "title": "Frequently Asked Questions About UX Screenshot Audits",
                "html": "<h3>What is the fastest shortcut to capture screen crops into FloatBoard?</h3><p>Press Win + Shift + S on Windows (or Cmd + Shift + 4 on macOS); FloatBoard automatically detects the new screenshot in your clipboard and docks it into your board.</p><h3>Can I reorder cards inside the UX moodboard?</h3><p>Yes. FloatBoard supports intuitive drag-and-drop reordering of both images and text notes.</p>"
            }
        ]

    # Update modified date for all posts
    for p in posts:
        p['modified'] = '2026-11-08'

    with open('blog/posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

    print("Successfully updated posts.json with rich software-specific body content and pillar links!")

if __name__ == '__main__':
    update_posts()

