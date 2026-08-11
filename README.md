# manimlab

A lab for math-driven graphics and animations built with [Manim](https://www.manim.community/)
(the Community Edition of 3Blue1Brown's animation engine).

## Setup

Manim needs Python 3.9+, plus a few system dependencies (FFmpeg, and a LaTeX
distribution for typeset equations).

```bash
# 1. System deps (Debian/Ubuntu)
sudo apt update && sudo apt install -y ffmpeg build-essential python3-dev pkg-config \
  libcairo2-dev libpango1.0-dev texlive texlive-latex-extra

# 2. Python venv + manim
python3 -m venv .venv
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
