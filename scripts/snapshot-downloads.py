"""Save a dated snapshot of FloatBoard's GitHub release asset download counts.

Run with: python3 scripts/snapshot-downloads.py
The public GitHub API needs no token for these public releases. Counts are
cumulative asset downloads, not unique people or confirmed installations.
"""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import tempfile
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
RELEASES = (
    (
        "nazihyazan/floating_board",
        "v1.0.15",
        (
            "FloatBoard.Setup.1.0.15.exe",
            "FloatBoard.Setup.1.0.15.appx",
            "FloatBoard-1.0.15-mac.zip",
        ),
    ),
    (
        "nazihyazan/mac_test",
        "v1.0.17",
        (
            "FloatBoard-1.0.17-linux.deb",
            "FloatBoard-1.0.17-linux.rpm",
            "FloatBoard-1.0.17-linux.AppImage",
            "FloatBoard-1.0.17-linux.snap",
        ),
    ),
)


def fetch_release(repo, tag):
    request = Request(
        f"https://api.github.com/repos/{repo}/releases/tags/{tag}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "FloatBoard-download-snapshot",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urlopen(request, timeout=15) as response:
            return json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"GitHub API returned HTTP {exc.code} for {repo} {tag}") from exc
    except URLError as exc:
        raise RuntimeError(f"Could not reach GitHub API for {repo} {tag}: {exc.reason}") from exc
    except (ValueError, OSError) as exc:
        raise RuntimeError(f"Could not read GitHub release data for {repo} {tag}: {exc}") from exc


def build_snapshot(now=None):
    now = now or datetime.now(timezone.utc)
    assets = []
    for repo, tag, expected_names in RELEASES:
        release = fetch_release(repo, tag)
        if not isinstance(release, dict) or release.get("tag_name") != tag or not isinstance(release.get("assets"), list):
            raise RuntimeError(f"Unexpected GitHub release data for {repo} {tag}")

        if not all(isinstance(asset, dict) for asset in release["assets"]):
            raise RuntimeError(f"Unexpected GitHub assets for {repo} {tag}")
        by_name = {asset.get("name"): asset for asset in release["assets"]}
        for name in expected_names:
            asset = by_name.get(name)
            if asset is None:
                raise RuntimeError(f"Missing expected asset {name} in {repo} {tag}")
            count = asset.get("download_count")
            if type(count) is not int or count < 0:
                raise RuntimeError(f"Invalid download_count for {repo} {tag} {name}")
            assets.append(
                {
                    "repo": repo,
                    "tag": tag,
                    "name": name,
                    "asset_id": asset.get("id"),
                    "download_count": count,
                }
            )

    return {
        "recorded_at_utc": now.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "metric": "github_release_asset_download_count",
        "note": "Cumulative requests for the listed GitHub assets; not unique users or confirmed installations. Snap Store installs are excluded.",
        "assets": assets,
        "tracked_asset_total": sum(asset["download_count"] for asset in assets),
    }


def save_snapshot(snapshot, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = snapshot["recorded_at_utc"].replace(":", "-")
    destination = output_dir / f"github-downloads-{timestamp}.json"
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=output_dir, prefix=".github-downloads-", delete=False
        ) as temporary:
            temporary_path = Path(temporary.name)
            json.dump(snapshot, temporary, indent=2)
            temporary.write("\n")
        # The hard link creates the final file atomically without replacing an older snapshot.
        os.link(temporary_path, destination)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    return destination


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "metrics",
        help="directory for dated JSON snapshots (default: metrics/)",
    )
    args = parser.parse_args(argv)

    try:
        snapshot = build_snapshot()
        destination = save_snapshot(snapshot, args.output_dir)
    except (RuntimeError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    for asset in snapshot["assets"]:
        print(f"{asset['repo']} {asset['tag']} {asset['name']}: {asset['download_count']}")
    print(f"Tracked asset total: {snapshot['tracked_asset_total']}")
    print(f"Saved: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
