#!/usr/bin/env python3
import os
import sys
import time
import subprocess

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
inkscape_bin = "/Applications/Inkscape.app/Contents/MacOS/inkscape"
DEFAULT_DPI = 300

def convert_svgs(dpi=DEFAULT_DPI, batch_size=40):
    if not os.path.exists(inkscape_bin):
        print(f"Error: Inkscape binary not found at {inkscape_bin}", file=sys.stderr)
        return False

    svgs = []
    for root, dirs, files in os.walk(repo_root):
        if '.git' in root or 'node_modules' in root or 'scratch' in root or 'brain' in root:
            continue
        for f in sorted(files):
            if f.lower().endswith('.svg'):
                svg_path = os.path.join(root, f)
                png_path = os.path.splitext(svg_path)[0] + '.png'
                svgs.append((svg_path, png_path))

    print(f"Found {len(svgs)} SVGs to convert to PNG at {dpi} DPI (distortion-free, proportional).")
    if not svgs:
        return True

    profile_dir = "/tmp/inkscape-profile"
    os.makedirs(profile_dir, exist_ok=True)
    env = dict(os.environ, INKSCAPE_PROFILE_DIR=profile_dir)

    success_count = 0
    fail_count = 0

    # Process in batches using Inkscape shell mode
    # Using ONLY export-dpi ensures perfect aspect ratio preservation on both axes
    for i in range(0, len(svgs), batch_size):
        batch = svgs[i:i + batch_size]
        commands = []
        for src, dst in batch:
            commands.append(f"file-open:{src}")
            commands.append(f"export-dpi:{dpi}")
            commands.append(f"export-filename:{dst}")
            commands.append("export-do")
        commands.append("quit")

        shell_input = "\n".join(commands) + "\n"
        t0 = time.time()
        proc = subprocess.Popen(
            [inkscape_bin, "--shell"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        proc.communicate(input=shell_input)
        elapsed = time.time() - t0

        batch_ok = sum(1 for _, dst in batch if os.path.exists(dst) and os.path.getsize(dst) > 0)
        success_count += batch_ok
        fail_count += (len(batch) - batch_ok)
        print(f"  Batch {i // batch_size + 1}/{(len(svgs) + batch_size - 1) // batch_size}: {batch_ok}/{len(batch)} converted in {elapsed:.2f}s ({success_count}/{len(svgs)} total)")

    print(f"SVG Conversion complete: {success_count} succeeded, {fail_count} failed.")
    return fail_count == 0

def convert_jpgs():
    jpgs = []
    for root, dirs, files in os.walk(repo_root):
        if '.git' in root or 'node_modules' in root or 'scratch' in root or 'brain' in root:
            continue
        for f in sorted(files):
            if f.lower().endswith(('.jpg', '.jpeg')):
                jpg_path = os.path.join(root, f)
                png_path = os.path.splitext(jpg_path)[0] + '.png'
                if not os.path.exists(png_path) or os.path.getsize(png_path) == 0:
                    jpgs.append((jpg_path, png_path))

    if not jpgs:
        return True

    print(f"Found {len(jpgs)} JPGs without a PNG version.")
    success_count = 0
    for src, dst in jpgs:
        try:
            res = subprocess.run(
                ["sips", "-s", "format", "png", src, "--out", dst],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            if res.returncode == 0 and os.path.exists(dst) and os.path.getsize(dst) > 0:
                success_count += 1
        except Exception:
            pass

    print(f"JPG Conversion complete: {success_count}/{len(jpgs)} converted to PNG.")
    return True

if __name__ == "__main__":
    dpi = DEFAULT_DPI
    for arg in sys.argv:
        if arg.startswith("--dpi="):
            dpi = int(arg.split("=")[1])

    print(f"=== Generating Proportional PNG Assets ({dpi} DPI) ===")
    t_start = time.time()
    convert_svgs(dpi=dpi)
    convert_jpgs()
    print(f"All conversions finished in {time.time() - t_start:.2f}s.")
