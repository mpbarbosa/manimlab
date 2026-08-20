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
    YELLOW,
    PI,
    DEGREES,
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
        self.wait(1.0)
