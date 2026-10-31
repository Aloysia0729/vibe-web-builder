# Studio demonstration — fictional user, actual execution

Northstar Design Studio and its projects are fictional. No customer endorsement, real client data, or production deployment is implied.

## Recorded sequence

1. User starts with an unclear studio website idea. Independent agent loads the actual Skill and asks three new questions (audience/services, contact action, visual direction).
2. A separate test driver supplies a clearly fictional studio, small-business audience, five single-page sections, email only, and cream/black/green style. The agent records requirements revision 2 and requests approval.
3. Driver explicitly confirms requirements r2. The agent records it, presents wireframe r1 and recommends static HTML/CSS, then asks for an independent sketch approval. Still no application.
4. Driver explicitly confirms wireframe r1 and asks to switch from planning to development. The agent builds the actual local page and verifies it in Chromium.

[Complete transcript](recorded-run/transcript.md) · [Untouched raw transcript](recorded-run/transcript.txt) · [Requirements](recorded-run/docs/web-builder/requirements.md) · [Design](recorded-run/docs/web-builder/design.md) · [Progress](recorded-run/docs/web-builder/progress.md) · [Actual browser checks](recorded-run/verification/browser-results.json).

## Media provenance

- walkthrough.gif: paced **transcript-excerpt replay**, generated from real recorded messages, followed by an actual browser capture. It is not a live screen recording of Codex. Wait time is omitted; no response or confirmation is fabricated.
- studio-desktop.png / studio-mobile.png: full-page captures of the actual site snapshot at 1280px / 390px. No visual retouching or post-capture collage.
- before-after.png: a labeled comparison graphic quoting the real initial input and actual resulting requirements. It is a document illustration, not a screenshot of a product UI.
- The terminal-style hero and social cover are separate brand concept artwork, not demonstration evidence.

All key information is readable without playing the animation via the transcript, documents, and static images. The demo tests do not prove universal host discovery or a production-ready service. Mail delivery is untested; .example is a placeholder. Original checks cover five nav targets, Work/back-to-top links, keyboard skip, local images, and no overflow/page errors at 1280×900 and 390×844. The initial browser attempt lacked sandbox permissions; the supported escalation allowed the unchanged browser checks to run. State checking also caught generic phase/status labels; the demo documents were corrected to the existing schema, without changing Skill code.

## Replay locally

From repository root, serve the snapshot with Python 3:

```bash
python3 -m http.server 8000 --bind 127.0.0.1 --directory assets/demo/recorded-run/site
```

Stop your own server with Ctrl+C. This is a demonstration fixture, not a separate product website.

For evidence capture, run `python3 assets/demo/capture.py` with environment-provided Python Playwright, Pillow, and /usr/bin/chromium. It serves only an ephemeral loopback port and closes it on completion; sandbox environments may require permission to bind. The copied original verify_browser.py expects its original source layout and port 4187, so read/adapt paths before replaying; it is retained as execution evidence, not part of the project's CI.
