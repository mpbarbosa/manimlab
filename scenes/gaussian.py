"""Plot a formula and ride a dot along it.

Render:
    manim -pql scenes/gaussian.py Gaussian
"""

import numpy as np
from manim import (
    Scene,
    Axes,
    Dot,
    MathTex,
    Create,
    Write,
    FadeIn,
    Indicate,
    ValueTracker,
    always_redraw,
    BLUE,
    YELLOW,
    GREY_B,
    UP,
)


class Gaussian(Scene):
    def construct(self):
        # --- axes ---
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 1.1, 0.5],
            x_length=10,
            y_length=5,
            axis_config={"color": GREY_B, "include_tip": True},
        )

        # --- the curve: a Gaussian  y = e^(-x^2) ---
        curve = axes.plot(lambda x: np.exp(-x * x), x_range=[-3, 3], color=BLUE)

        # --- the formula, typeset in LaTeX ---
        label = MathTex(r"y = e^{-x^2}").scale(1.2).to_edge(UP)

        # --- a dot that rides along the curve ---
        t = ValueTracker(-3.0)
        marker = always_redraw(
            lambda: Dot(
                axes.c2p(t.get_value(), float(np.exp(-t.get_value() ** 2))),
                color=YELLOW,
            )
        )

        # ================= SCRIPT =================
        self.play(Create(axes), run_time=1.0)
        self.play(Write(label), run_time=0.6)
        self.play(Create(curve), run_time=1.6)
        self.add(marker)
        self.play(FadeIn(marker, scale=0.5), run_time=0.3)
        self.play(t.animate.set_value(3.0), run_time=3.0)
        self.play(Indicate(marker))
        self.wait(0.8)
