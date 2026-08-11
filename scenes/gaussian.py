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
    DecimalNumber,
    VGroup,
    Create,
    Write,
    FadeIn,
    Indicate,
    ValueTracker,
    linear,
    BLUE,
    YELLOW,
    GREY_B,
    UP,
    RIGHT,
    UL,
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
        # Drive the dot with a ValueTracker; an updater keeps it on the curve.
        t = ValueTracker(-3.0)

        def gaussian(x: float) -> float:
            return float(np.exp(-x * x))

        marker = Dot(axes.c2p(-3.0, gaussian(-3.0)), color=YELLOW)

        # --- live (x, y) readout of the marker's position ---
        # DecimalNumber updates glyphs cheaply per frame; a MathTex rebuilt each
        # frame would recompile LaTeX and make the render crawl.
        x_dec = DecimalNumber(-3.0, num_decimal_places=2, include_sign=True)
        y_dec = DecimalNumber(gaussian(-3.0), num_decimal_places=2)
        x_dec.set_color(YELLOW)
        y_dec.set_color(YELLOW)
        readout = VGroup(
            MathTex(r"(x,\,y) = ("), x_dec, MathTex(","), y_dec, MathTex(")")
        )
        readout.arrange(RIGHT, buff=0.12).scale(0.8).to_corner(UL)

        # ================= SCRIPT =================
        self.play(Create(axes), run_time=1.0)
        self.play(Write(label), run_time=0.6)
        self.play(Create(curve), run_time=1.6)

        # Reveal the dot first, THEN attach the updater — a live updater would
        # otherwise overwrite the FadeIn's opacity/scale every frame.
        self.play(FadeIn(marker, scale=0.5), run_time=0.3)
        self.play(FadeIn(readout, shift=0.2 * UP), run_time=0.3)

        marker.add_updater(
            lambda m: m.move_to(axes.c2p(t.get_value(), gaussian(t.get_value())))
        )
        x_dec.add_updater(lambda d: d.set_value(t.get_value()))
        y_dec.add_updater(lambda d: d.set_value(gaussian(t.get_value())))

        # Slow, steady sweep across the curve (linear = constant speed).
        self.play(t.animate.set_value(3.0), run_time=7.0, rate_func=linear)

        marker.clear_updaters()
        x_dec.clear_updaters()
        y_dec.clear_updaters()

        self.play(Indicate(marker))
        self.wait(0.8)
