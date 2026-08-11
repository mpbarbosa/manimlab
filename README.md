# manimlab

A lab for math-driven graphics and animations built with [Manim](https://www.manim.community/)
(the Community Edition of 3Blue1Brown's animation engine).

## Setup

Manim 0.21 supports **Python 3.9–3.14**, plus a few system dependencies (FFmpeg,
and a LaTeX distribution for typeset equations). Verified working on Ubuntu 26.04
with Python 3.14.

> **Dev headers must match your interpreter.** `pycairo` compiles from source (no
> Linux wheels), so it needs the `pythonX.Y-dev` package matching the exact Python
> you build the venv with — e.g. `python3.14-dev` for a 3.14 venv. A mismatched
> `python3-dev` will fail with `Python dependency not found`. If you use the
> `--copies` venv flag below, use whichever `pythonX.Y` your system provides
> headers for.

```bash
# 1. System deps (Debian/Ubuntu). Match the -dev package to your Python version.
sudo apt update && sudo apt install -y ffmpeg build-essential python3-dev pkg-config \
  libcairo2-dev libpango1.0-dev texlive texlive-latex-extra

# 2. Python venv + manim
#    Use --copies to avoid a venv symlink quirk seen on some Ubuntu builds where
#    `python`/`python3` resolve to the system default instead of the venv Python.
python3 -m venv --copies .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Verify:

```bash
manim --version
```

## Render a scene

```bash
# Preview quality, opens the result when done
manim -pql scenes/gaussian.py Gaussian

# High quality (1080p60)
manim -qh scenes/gaussian.py Gaussian
```

Common flags: `-p` preview when done · `-ql/-qm/-qh/-qk` quality (480p/720p/1080p/4k)
· `--format gif` · `-s` save last frame as PNG.

Rendered output lands in `media/` (git-ignored).

## Layout

```
manimlab/
├── scenes/          # one file per animation; each class is a Scene
│   └── gaussian.py  # plot y = e^(-x^2) with a dot riding the curve
├── requirements.txt
├── manim.cfg        # project-wide render defaults
└── media/           # generated videos/images (ignored)
```

## Add a scene

Create `scenes/my_scene.py` with a class that subclasses `Scene` and implements
`construct(self)`, then render it by class name:

```bash
manim -pql scenes/my_scene.py MyScene
```
