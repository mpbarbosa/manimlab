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
    ValueTracker,
    rotate_vector,
    linear,
    BLUE,
    GREEN,
    YELLOW,
    PI,
    TAU,
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
        self.wait(0.5)

        # Rotate every B circle independently, each about its own center (so the
        # labels and dots spin in place). Played together, but each is its own
        # rotation; alternating directions makes the independence clear.
        group_b1 = VGroup(circle_b1, label_b1, dots_b1)
        group_b2 = VGroup(circle_b2, label_b2, dots_b2)
        group_b3 = VGroup(circle_b3, label_b3, dots_b3)
        group_b4 = VGroup(circle_b4, label_b4, dots_b4)
        self.play(
            Rotate(group_b1, angle=360 * DEGREES),
            Rotate(group_b2, angle=-360 * DEGREES),
            Rotate(group_b3, angle=360 * DEGREES),
            Rotate(group_b4, angle=-360 * DEGREES),
            run_time=3.0,
        )
        self.wait(0.5)

        # Attach every B circle to Circle A: each B keeps a fixed offset from A's
        # center via an updater, so moving A drags the B circles along.
        a_group = VGroup(circle_a, label_a, dots)
        b_groups = [group_b1, group_b2, group_b3, group_b4]
        a_center = circle_a.get_center()
        for gb in b_groups:
            offset = gb.get_center() - a_center
            gb.add_updater(lambda m, o=offset: m.move_to(circle_a.get_center() + o))

        # Run A back and forth; the attached B circles follow.
        self.play(a_group.animate.shift(RIGHT * 2.5), run_time=1.5)
        self.play(a_group.animate.shift(LEFT * 5.0), run_time=2.5)
        self.play(a_group.animate.shift(RIGHT * 2.5), run_time=1.5)

        for gb in b_groups:
            gb.clear_updaters()
        self.wait(0.5)

        # Rotate A with the B circles attached: the whole rigid assembly turns
        # about Circle A's center, so each attached B orbits A.
        assembly = VGroup(a_group, *b_groups)
        self.play(
            Rotate(assembly, angle=360 * DEGREES, about_point=circle_a.get_center()),
            run_time=3.0,
        )
        self.wait(0.5)

        # Rotate A about its own center. B stays attached to A -- each B's center
        # revolves around A as A turns (driven by phi) -- while ALSO spinning
        # independently about its own center at its own rate.
        a_center = circle_a.get_center()
        phi = ValueTracker(0.0)               # A's angle; also orbits the Bs
        spin_rates = {                        # each B's own spin (rad/s), independent
            group_b1: 2.0,
            group_b2: -3.0,
            group_b3: 2.5,
            group_b4: -1.5,
        }
        base_offsets = {gb: gb.get_center() - a_center for gb in spin_rates}

        def attach(rate, offset):
            def updater(m, dt):
                m.rotate(rate * dt, about_point=m.get_center())               # own spin
                m.move_to(a_center + rotate_vector(offset, phi.get_value()))  # orbit
            return updater

        for gb, rate in spin_rates.items():
            gb.add_updater(attach(rate, base_offsets[gb]))

        self.play(
            Rotate(a_group, angle=360 * DEGREES, about_point=a_center),
            phi.animate.set_value(TAU),
            run_time=4.0,
            rate_func=linear,
        )
        for gb in spin_rates:
            gb.clear_updaters()
        self.wait(1.0)
