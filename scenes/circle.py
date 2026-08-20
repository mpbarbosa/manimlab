"""Draw Circle A with dots on its edge at 0°, 90°, 180° and 270°.

Render:
    manim -pql scenes/circle.py DrawCircle
"""

from manim import (
    Scene,
    Circle,
    Dot,
    Text,
    Create,
    FadeIn,
    Rotate,
    VGroup,
    BLUE,
    GREEN,
    YELLOW,
    PI,
    DEGREES,
    RIGHT,
    UP,
    LEFT,
    DOWN,
    ORIGIN,
)


def cardinal_dots(circle, color=YELLOW, radius=0.08):
    """Dots on a circle's edge at 0, 90, 180 and 270 degrees."""
    angles = [0, PI / 2, PI, 3 * PI / 2]
    return VGroup(
        *[Dot(circle.point_at_angle(a), color=color, radius=radius) for a in angles]
    )


class DrawCircle(Scene):
    def construct(self):
        # Circle A
        circle_a = Circle(radius=2.0, color=BLUE)
        label_a = Text("A", color=BLUE).scale(0.8).move_to(circle_a.get_center())
        self.play(Create(circle_a))
        self.play(FadeIn(label_a))

        # Dots on Circle A's line at 0, 90, 180 and 270 degrees.
        # point_at_angle takes radians: 0, PI/2, PI, 3*PI/2.
        angles = [0, PI / 2, PI, 3 * PI / 2]
        dots = VGroup(
            *[Dot(circle_a.point_at_angle(a), color=YELLOW) for a in angles]
        )
        self.play(FadeIn(dots, scale=0.5))
        self.wait(0.5)

        # Rotate Circle A (with its label and dots) two full turns, then stop.
        circle_group = VGroup(circle_a, label_a, dots)
        self.play(Rotate(circle_group, angle=720 * DEGREES), run_time=3.0)
        self.wait(0.5)

        # Circle B1: external to Circle A, tangent at Circle A's 0 degree point.
        # For external tangency, B1's center sits one B1-radius beyond the touch
        # point, along the outward (+x) normal.
        touch = circle_a.point_at_angle(0)          # (2, 0, 0)
        r_b1 = 1.0
        circle_b1 = Circle(radius=r_b1, color=GREEN).move_to(touch + RIGHT * r_b1)
        label_b1 = Text("B1", color=GREEN).scale(0.5).move_to(circle_b1.get_center())
        self.play(Create(circle_b1), FadeIn(label_b1))
        self.wait(0.5)

        # Circle B2: external to Circle A, tangent at Circle A's 90 degree point.
        # Center sits one B2-radius beyond the touch point along the outward
        # (+y) normal.
        touch_90 = circle_a.point_at_angle(PI / 2)   # (0, 2, 0)
        r_b2 = 1.0
        circle_b2 = Circle(radius=r_b2, color=GREEN).move_to(touch_90 + UP * r_b2)
        label_b2 = Text("B2", color=GREEN).scale(0.5).move_to(circle_b2.get_center())
        self.play(Create(circle_b2), FadeIn(label_b2))
        self.wait(0.5)

        # Circle B3: external to Circle A, tangent at Circle A's 180 degree point.
        # Center sits one B3-radius beyond the touch point along the outward
        # (-x) normal.
        touch_180 = circle_a.point_at_angle(PI)      # (-2, 0, 0)
        r_b3 = 1.0
        circle_b3 = Circle(radius=r_b3, color=GREEN).move_to(touch_180 + LEFT * r_b3)
        label_b3 = Text("B3", color=GREEN).scale(0.5).move_to(circle_b3.get_center())
        self.play(Create(circle_b3), FadeIn(label_b3))
        self.wait(0.5)

        # Circle B4: external to Circle A, tangent at Circle A's 270 degree point.
        # Center sits one B4-radius beyond the touch point along the outward
        # (-y) normal.
        touch_270 = circle_a.point_at_angle(3 * PI / 2)   # (0, -2, 0)
        r_b4 = 1.0
        circle_b4 = Circle(radius=r_b4, color=GREEN).move_to(touch_270 + DOWN * r_b4)
        label_b4 = Text("B4", color=GREEN).scale(0.5).move_to(circle_b4.get_center())
        self.play(Create(circle_b4), FadeIn(label_b4))
        self.wait(0.5)

        # Dots at 0, 90, 180 and 270 degrees on every B circle (smaller, to suit
        # the smaller radius).
        dots_b1 = cardinal_dots(circle_b1, radius=0.06)
        dots_b2 = cardinal_dots(circle_b2, radius=0.06)
        dots_b3 = cardinal_dots(circle_b3, radius=0.06)
        dots_b4 = cardinal_dots(circle_b4, radius=0.06)
        self.play(FadeIn(VGroup(dots_b1, dots_b2, dots_b3, dots_b4), scale=0.5))
        self.wait(0.5)

        # Rotate every circle together, as one rigid group, one full turn about
        # Circle A's center (the origin).
        everything = VGroup(
            circle_a, label_a, dots,
            circle_b1, label_b1, dots_b1,
            circle_b2, label_b2, dots_b2,
            circle_b3, label_b3, dots_b3,
            circle_b4, label_b4, dots_b4,
        )
        self.play(Rotate(everything, angle=360 * DEGREES, about_point=ORIGIN),
                  run_time=3.0)
        self.wait(1.0)
