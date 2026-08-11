"""UNESP — Trabalho realizado por duas máquinas (solução animada).

Máquina M1: eleva m1 = 1,0 kg até h = 20,0 m em movimento uniforme.
Máquina M2: acelera m2 = 3,0 kg do repouso até v = 10,0 m/s, sem atrito.

Solução (g = 10 m/s²):
    W1 = m1 · g · h  = 1,0 · 10 · 20,0 = 200 J
    W2 = ½ · m2 · v² = ½ · 3,0 · 10²   = 150 J

Render:
    manim -pqh scenes/unesp_trabalho.py UnespTrabalho
"""

from manim import *


def corpo(massa_tex, cor):
    """Uma caixinha colorida com o rótulo de massa no centro."""
    caixa = Square(side_length=0.8, color=cor, fill_color=cor, fill_opacity=0.55)
    rotulo = MathTex(massa_tex).scale(0.42).move_to(caixa)
    return VGroup(caixa, rotulo)


class UnespTrabalho(Scene):
    def construct(self):
        self.titulo = Text("UNESP — Trabalho de duas máquinas", weight=BOLD).scale(0.6)
        self.titulo.to_edge(UP)
        self.g_nota = MathTex(r"g = 10\ \text{m/s}^2").scale(0.55)
        self.g_nota.next_to(self.titulo, DOWN, buff=0.12)

        self.play(Write(self.titulo))
        self.play(FadeIn(self.g_nota))
        self.wait(0.4)

        self.maquina_1()
        self.maquina_2()
        self.resumo()

    # ------------------------------------------------------------------ #
    def maquina_1(self):
        sub = Text("M1: eleva um corpo na vertical (velocidade constante)").scale(0.4)
        sub.next_to(self.g_nota, DOWN, buff=0.18)
        self.play(FadeIn(sub))

        # --- diagrama (esquerda) ---
        y_base, y_topo, x0 = -2.6, 1.7, -3.6
        chao = Line([-6.3, -3.0, 0], [-1.5, -3.0, 0], color=GREY_B)
        c = corpo(r"m_1", BLUE).move_to([x0, y_base, 0])
        m_lbl = MathTex(r"m_1 = 1{,}0\ \text{kg}").scale(0.45).next_to(c, RIGHT, buff=0.25)

        seta_h = DoubleArrow([-5.4, y_base, 0], [-5.4, y_topo, 0], buff=0.0,
                             color=YELLOW, stroke_width=3, tip_length=0.22)
        h_lbl = MathTex(r"h = 20{,}0\ \text{m}").scale(0.45).next_to(seta_h, LEFT, buff=0.12)

        self.play(Create(chao), GrowFromCenter(seta_h), FadeIn(h_lbl))
        self.play(FadeIn(c), Write(m_lbl))
        self.wait(0.2)

        # subida uniforme: linear = velocidade constante
        d = y_topo - y_base
        self.play(c.animate.shift(UP * d), m_lbl.animate.shift(UP * d),
                  run_time=3.0, rate_func=linear)
        self.wait(0.2)

        # --- cálculo (direita) ---
        f1 = MathTex(r"W_1 = m_1 \cdot g \cdot h").scale(0.7)
        f2 = MathTex(r"W_1 = 1{,}0 \cdot 10 \cdot 20{,}0").scale(0.7)
        f3 = MathTex(r"W_1 = 200\ \text{J}").scale(0.85).set_color(GREEN)
        col = VGroup(f1, f2, f3).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        col.move_to([3.0, -0.1, 0])
        nota = Text("v constante ⇒ F = P = m1·g", slant=ITALIC).scale(0.36)
        nota.next_to(col, UP, buff=0.45).align_to(col, LEFT)

        self.play(FadeIn(nota))
        self.play(Write(f1))
        self.wait(0.2)
        self.play(Write(f2))
        self.wait(0.2)
        self.play(Write(f3))
        cx = SurroundingRectangle(f3, color=GREEN, buff=0.15)
        self.play(Create(cx))
        self.wait(1.0)

        self.play(FadeOut(VGroup(sub, chao, c, m_lbl, seta_h, h_lbl, col, nota, cx)))

    # ------------------------------------------------------------------ #
    def maquina_2(self):
        sub = Text("M2: acelera um corpo na horizontal (sem atrito)").scale(0.4)
        sub.next_to(self.g_nota, DOWN, buff=0.18)
        self.play(FadeIn(sub))

        # --- pista horizontal (parte de baixo) ---
        y_box = -2.2
        x_ini, x_fim = -5.5, 3.3
        pista = Line([-6.5, -2.6, 0], [6.5, -2.6, 0], color=GREY_B)
        atrito = Text("sem atrito", slant=ITALIC).scale(0.35).next_to(pista, DOWN, buff=0.12)

        c = corpo(r"m_2", ORANGE).move_to([x_ini, y_box, 0])
        m_lbl = MathTex(r"m_2 = 3{,}0\ \text{kg}").scale(0.45)
        m_lbl.add_updater(lambda t: t.next_to(c, DOWN, buff=0.15))

        self.play(Create(pista), FadeIn(atrito))
        self.play(FadeIn(c), FadeIn(m_lbl))

        # prog 0->1 linear no tempo; posição ~ prog^2 (aceleração constante),
        # velocidade ~ prog (linear no tempo, de 0 a 10 m/s).
        prog = ValueTracker(0.0)

        def px():
            p = prog.get_value()
            return x_ini + (x_fim - x_ini) * p * p

        c.add_updater(lambda m: m.move_to([px(), y_box, 0]))

        seta_v = always_redraw(lambda: Arrow(
            [px(), y_box + 0.85, 0],
            [px() + 0.25 + 2.2 * prog.get_value(), y_box + 0.85, 0],
            buff=0, color=YELLOW, stroke_width=5,
            max_tip_length_to_length_ratio=0.25,
        ))
        v_dec = DecimalNumber(0.0, num_decimal_places=1).scale(0.55).set_color(YELLOW)
        v_dec.add_updater(lambda d: d.set_value(10.0 * prog.get_value()))
        v_lbl = VGroup(MathTex(r"v = ").scale(0.55), v_dec,
                       MathTex(r"\ \text{m/s}").scale(0.55)).arrange(RIGHT, buff=0.08)
        v_lbl.add_updater(lambda g: g.arrange(RIGHT, buff=0.08).next_to(seta_v, UP, buff=0.12))

        self.add(seta_v, v_lbl)
        self.play(prog.animate.set_value(1.0), run_time=3.0, rate_func=linear)
        c.clear_updaters()
        v_dec.clear_updaters()
        v_lbl.clear_updaters()
        self.wait(0.3)

        # --- cálculo (centro-superior) ---
        g1 = MathTex(r"W_2 = \tfrac{1}{2}\, m_2\, v^2").scale(0.7)
        g2 = MathTex(r"W_2 = \tfrac{1}{2} \cdot 3{,}0 \cdot (10{,}0)^2").scale(0.7)
        g3 = MathTex(r"W_2 = 150\ \text{J}").scale(0.85).set_color(GREEN)
        col = VGroup(g1, g2, g3).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        col.move_to([0.0, 0.2, 0])
        nota = Text("Teorema trabalho–energia: W = ΔEc", slant=ITALIC).scale(0.36)
        nota.next_to(col, UP, buff=0.3).align_to(col, LEFT)

        self.play(FadeIn(nota))
        self.play(Write(g1))
        self.wait(0.2)
        self.play(Write(g2))
        self.wait(0.2)
        self.play(Write(g3))
        cx = SurroundingRectangle(g3, color=GREEN, buff=0.15)
        self.play(Create(cx))
        self.wait(1.0)

        self.play(FadeOut(VGroup(sub, pista, atrito, c, m_lbl, seta_v, v_lbl,
                                 col, nota, cx)))

    # ------------------------------------------------------------------ #
    def resumo(self):
        sub = Text("Resposta (a)", weight=BOLD).scale(0.5)
        sub.next_to(self.g_nota, DOWN, buff=0.25)

        r1 = MathTex(r"W_1 = 200\ \text{J}").scale(1.0).set_color(BLUE)
        r2 = MathTex(r"W_2 = 150\ \text{J}").scale(1.0).set_color(ORANGE)
        linha = VGroup(r1, r2).arrange(RIGHT, buff=1.5).move_to([0, 0.4, 0])
        b1 = SurroundingRectangle(r1, color=BLUE, buff=0.2)
        b2 = SurroundingRectangle(r2, color=ORANGE, buff=0.2)

        conc = Text("M1 realizou mais trabalho que M2 (200 J > 150 J).").scale(0.42)
        conc.next_to(linha, DOWN, buff=0.9)

        self.play(FadeIn(sub))
        self.play(Write(r1), Write(r2))
        self.play(Create(b1), Create(b2))
        self.play(FadeIn(conc, shift=0.3 * UP))
        self.wait(2.0)
