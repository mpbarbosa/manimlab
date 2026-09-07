"""Onde o atalho quebra — quatro casos em que "passar para o outro lado" falha.

A cena companheira de `transposicao.py`. Lá o atalho funciona porque a operação
aplicada aos dois lados é inversível; aqui, quatro situações em que ela não é:

    1. Cancelar por uma expressão que pode ser zero  ->  perde raiz
       x² = x  =>  x = 1        (sumiu x = 0)

    2. Elevar ao quadrado                            ->  cria raiz falsa
       V(x+6) = x  =>  x = 3 ou x = -2   (x = -2 não serve)

    3. Matrizes: a multiplicação não é comutativa    ->  o lado importa
       AX = B  exige  A^-1 pela ESQUERDA nos dois lados

    4. Desigualdades: multiplicar por negativo       ->  inverte o sentido
       -2x < 6  =>  x > -3

Fio condutor: o princípio de equivalência só vale para operações inversíveis.
Quando a operação perde informação (x0) ou ganha soluções (elevar ao quadrado),
a equivalência vira mera implicação e a verificação passa a ser obrigatória.

Render:
    manim -pqh scenes/atalho_quebra.py AtalhoQuebra
"""

from manim import *

COR_ERRO = RED_B        # o caminho que parece certo e não é
COR_CERTO = GREEN       # o caminho válido
COR_NEUTRO = BLUE_B     # equações neutras / curvas
COR_NOTA = GREY_A       # comentários


class AtalhoQuebra(Scene):
    def construct(self):
        self.titulo = Text("Onde o atalho quebra", weight=BOLD).scale(0.58)
        self.titulo.to_edge(UP, buff=0.28)
        self.play(Write(self.titulo))

        self.caso_cancelamento()
        self.caso_quadrado()
        self.caso_matrizes()
        self.caso_desigualdade()
        self.fecho()

    # ------------------------------------------------------------------ #
    # utilitários de cartão
    # ------------------------------------------------------------------ #
    def cabecalho(self, n, texto):
        """Numeração + título do caso, com régua embaixo."""
        cab = VGroup(
            Text(f"{n}", weight=BOLD).scale(0.62).set_color(COR_ERRO),
            Text(texto, weight=BOLD).scale(0.46),
        ).arrange(RIGHT, buff=0.3).move_to([0, 2.68, 0])
        regua = Line(cab.get_left(), cab.get_right(), color=GREY_D, stroke_width=2)
        regua.next_to(cab, DOWN, buff=0.13)
        self.play(FadeIn(cab, shift=0.2 * DOWN), Create(regua), run_time=0.8)
        return VGroup(cab, regua)

    def rotulo(self, texto, cor, ref, buff=0.30):
        """Etiqueta 'ATALHO' / 'CORRETO' acima de um bloco."""
        t = Text(texto, weight=BOLD).scale(0.34).set_color(cor)
        return t.next_to(ref, UP, buff=buff)

    def veredito(self, texto, cor, ref):
        """Palavra final ('falso' / 'verdadeiro') ao lado de um teste."""
        t = Text(texto, weight=BOLD, slant=ITALIC).scale(0.32).set_color(cor)
        return t.next_to(ref, RIGHT, buff=0.25)

    def nota(self, texto, y=-3.30, cor=COR_NOTA, escala=0.40):
        """Comentário de rodapé do cartão."""
        t = Text(texto, slant=ITALIC).scale(escala).set_color(cor).move_to([0, y, 0])
        self.play(FadeIn(t, shift=0.2 * UP))
        return t

    def fechar(self, *mobs):
        self.wait(1.6)
        self.play(FadeOut(VGroup(*mobs)), run_time=0.8)

    # ------------------------------------------------------------------ #
    # 1. cancelar por algo que pode ser zero
    # ------------------------------------------------------------------ #
    def caso_cancelamento(self):
        cab = self.cabecalho(1, "Cancelar por algo que pode ser zero")

        # o atalho: "corta o x dos dois lados"
        errado = VGroup(
            MathTex(r"x^2 = x").scale(0.85),
            MathTex(r"\Downarrow").scale(0.75).set_color(COR_ERRO),
            MathTex(r"x = 1").scale(0.85).set_color(COR_ERRO),
        ).arrange(DOWN, buff=0.20).move_to([-3.75, 1.02, 0])
        lbl_e = self.rotulo("ATALHO:  corta o x dos dois lados", COR_ERRO, errado)

        self.play(FadeIn(lbl_e), Write(errado[0]), run_time=0.9)
        self.play(FadeIn(errado[1]), Write(errado[2]), run_time=0.9)
        self.wait(0.5)

        # a raiz que o atalho perdeu
        perdida = Text("perdeu a raiz  x = 0", weight=BOLD).scale(0.34)
        perdida.set_color(COR_ERRO).next_to(errado, DOWN, buff=0.28)
        self.play(FadeIn(perdida), run_time=0.7)

        # o caminho válido: fatorar em vez de cancelar
        certo = VGroup(
            MathTex(r"x^2 - x = 0").scale(0.8),
            MathTex(r"x\,(x - 1) = 0").scale(0.8),
            MathTex(r"x = 0 \quad \text{ou} \quad x = 1").scale(0.8).set_color(COR_CERTO),
        ).arrange(DOWN, buff=0.20).move_to([-3.75, -1.72, 0])
        lbl_c = self.rotulo("CORRETO:  fatorar", COR_CERTO, certo, buff=0.34)

        self.play(FadeIn(lbl_c), Write(certo[0]), run_time=0.9)
        self.play(Write(certo[1]), run_time=0.8)
        self.play(Write(certo[2]), run_time=0.9)
        self.wait(0.4)

        # as duas curvas se cruzam exatamente nas duas raízes
        eixos = Axes(
            x_range=[-0.5, 1.7, 0.5], y_range=[-0.4, 2.0, 0.5],
            x_length=4.0, y_length=3.4,
            axis_config={"include_ticks": False, "stroke_width": 2,
                         "color": GREY_B, "tip_width": 0.16, "tip_height": 0.16},
        ).move_to([3.55, -0.20, 0])
        par = eixos.plot(lambda t: t ** 2, x_range=[-0.5, 1.45], color=COR_NEUTRO)
        ret = eixos.plot(lambda t: t, x_range=[-0.4, 1.7], color=YELLOW)
        l_par = MathTex("y = x^2").scale(0.5).set_color(COR_NEUTRO)
        l_par.next_to(par.get_end(), RIGHT, buff=0.08)
        l_ret = MathTex("y = x").scale(0.5).set_color(YELLOW)
        l_ret.next_to(ret.get_end(), RIGHT, buff=0.08)

        self.play(Create(eixos), run_time=0.9)
        self.play(Create(par), FadeIn(l_par), Create(ret), FadeIn(l_ret), run_time=1.3)

        d0 = Dot(eixos.c2p(0, 0), color=COR_ERRO, radius=0.09)
        d1 = Dot(eixos.c2p(1, 1), color=COR_CERTO, radius=0.09)
        t0 = MathTex("x = 0").scale(0.5).set_color(COR_ERRO)
        t0.next_to(d0, DOWN, buff=0.30).shift(0.42 * RIGHT)
        t1 = MathTex("x = 1").scale(0.5).set_color(COR_CERTO)
        t1.next_to(d1, UL, buff=0.10)
        self.play(FadeIn(d1), FadeIn(t1), run_time=0.6)
        self.play(FadeIn(d0), FadeIn(t0),
                  Flash(d0, color=COR_ERRO, line_length=0.16, num_lines=12,
                        flash_radius=0.34), run_time=1.0)

        nota = self.nota("Cortar o x supõe x diferente de 0 — e a raiz perdida é justamente esse caso")
        self.fechar(cab, errado, lbl_e, certo, lbl_c, perdida,
                    eixos, par, ret, l_par, l_ret, d0, d1, t0, t1, nota)

    # ------------------------------------------------------------------ #
    # 2. elevar ao quadrado
    # ------------------------------------------------------------------ #
    def caso_quadrado(self):
        cab = self.cabecalho(2, "Elevar ao quadrado")

        cadeia = VGroup(
            MathTex(r"\sqrt{x + 6} = x").scale(0.85),
            MathTex(r"x + 6 = x^2").scale(0.85),
            MathTex(r"x^2 - x - 6 = 0").scale(0.85),
            MathTex(r"(x - 3)(x + 2) = 0").scale(0.85),
            MathTex(r"x = 3 \quad \text{ou} \quad x = -2").scale(0.85),
        ).arrange(DOWN, buff=0.36)
        cadeia[0].shift(0.42 * UP)          # abre espaço para anotar o passo crítico
        cadeia.move_to([-3.70, -0.35, 0])

        self.play(Write(cadeia[0]), run_time=0.8)

        # o passo crítico: elevar ao quadrado só garante a ida
        ida = MathTex(r"\Downarrow").scale(0.75)
        ida.move_to(midpoint(cadeia[0].get_bottom(), cadeia[1].get_top()))
        volta = MathTex(r"\Longleftarrow").scale(0.68).set_color(COR_ERRO)
        risco = Cross(volta, stroke_color=COR_ERRO, stroke_width=4, scale_factor=0.6)
        anot = VGroup(
            Text("( )²  nos dois lados", slant=ITALIC).scale(0.30).set_color(COR_NOTA),
            VGroup(
                VGroup(volta, risco),
                Text("não é reversível", slant=ITALIC).scale(0.30).set_color(COR_ERRO),
            ).arrange(RIGHT, buff=0.16),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(ida, RIGHT, buff=0.40)

        self.play(FadeIn(ida), FadeIn(anot[0]), Write(cadeia[1]), run_time=1.2)
        self.play(FadeIn(anot[1]), run_time=0.8)
        self.wait(0.6)

        for k in (2, 3, 4):
            self.play(Write(cadeia[k]), run_time=0.7)
        self.wait(0.4)

        # verificar na equação ORIGINAL é o que separa raiz de raiz falsa
        v_tit = Text("verificar na equação original", weight=BOLD).scale(0.36)
        v_tit.set_color(COR_NOTA).move_to([3.55, 1.35, 0])
        v_ok = MathTex(r"x = 3:", r"\ \sqrt{9} = 3", r"\ \checkmark").scale(0.62)
        v_ok.set_color(COR_CERTO).move_to([3.55, 0.35, 0])
        v_no = MathTex(r"x = -2:", r"\ \sqrt{4} = 2 \neq -2").scale(0.62)
        v_no.set_color(COR_ERRO).move_to([3.55, -0.70, 0])

        self.play(FadeIn(v_tit), run_time=0.6)
        self.play(TransformFromCopy(cadeia[4], v_ok), run_time=1.0)
        self.play(TransformFromCopy(cadeia[4], v_no), run_time=1.0)
        falsa = Text("raiz falsa: a raiz quadrada nunca é negativa",
                     slant=ITALIC).scale(0.32).set_color(COR_ERRO)
        falsa.next_to(v_no, DOWN, buff=0.30)
        self.play(Indicate(v_no, color=COR_ERRO, scale_factor=1.12),
                  FadeIn(falsa), run_time=1.0)

        nota = self.nota("Operação não inversível dá implicação, não equivalência — por isso verificar")
        self.fechar(cab, cadeia, ida, anot, v_tit, v_ok, v_no, falsa, nota)

    # ------------------------------------------------------------------ #
    # 3. matrizes: o lado importa
    # ------------------------------------------------------------------ #
    def caso_matrizes(self):
        cab = self.cabecalho(3, "Matrizes: o lado importa")

        eq = MathTex(r"A\,X = B").scale(1.0)
        pede = Text("resolver para X", slant=ITALIC).scale(0.36).set_color(COR_NOTA)
        topo = VGroup(eq, pede).arrange(RIGHT, buff=0.50).move_to([0, 1.75, 0])
        self.play(Write(eq), FadeIn(pede))
        self.wait(0.5)

        certo = VGroup(
            MathTex(r"A^{-1}(A\,X) = A^{-1}B").scale(0.68),
            MathTex(r"(A^{-1}A)\,X = A^{-1}B").scale(0.68),
            MathTex(r"I\,X = A^{-1}B").scale(0.68),
            MathTex(r"X = A^{-1}B").scale(0.68).set_color(COR_CERTO),
        ).arrange(DOWN, buff=0.26).move_to([-3.55, -0.55, 0])
        lbl_c = self.rotulo("PELA ESQUERDA nos dois lados", COR_CERTO, certo)

        errado = VGroup(
            MathTex(r"(A\,X)A^{-1} = B\,A^{-1}").scale(0.68),
            MathTex(r"A\,X\,A^{-1} = B\,A^{-1}").scale(0.68),
            MathTex(r"?").scale(0.9).set_color(COR_ERRO),
        ).arrange(DOWN, buff=0.26).move_to([3.55, -0.30, 0])
        lbl_e = self.rotulo("PELA DIREITA nos dois lados", COR_ERRO, errado)

        self.play(FadeIn(lbl_c), FadeIn(lbl_e), run_time=0.6)
        self.play(TransformFromCopy(eq, certo[0]), TransformFromCopy(eq, errado[0]),
                  run_time=1.2)
        self.play(Write(certo[1]), Write(errado[1]), run_time=0.9)

        # à esquerda A^-1 A colapsa em I; à direita o X fica preso no meio
        self.play(Write(certo[2]), run_time=0.7)
        preso = Text("X preso no meio: nada cancela", slant=ITALIC).scale(0.32)
        preso.set_color(COR_ERRO).next_to(errado[2], DOWN, buff=0.22)
        self.play(Indicate(errado[1], color=COR_ERRO, scale_factor=1.15),
                  FadeIn(errado[2]), FadeIn(preso), run_time=1.1)
        self.play(Write(certo[3]), run_time=0.8)
        caixa = SurroundingRectangle(certo[3], color=COR_CERTO, buff=0.14)
        self.play(Create(caixa), run_time=0.6)

        det = Text("e a inversa só existe se det A não for zero — o 'não dividir por zero' das matrizes",
                   slant=ITALIC).scale(0.36).set_color(COR_NOTA).move_to([0, -2.85, 0])
        self.play(FadeIn(det))

        nota = self.nota("Em geral AB e BA diferem: aplicar a mesma operação exige aplicar do mesmo lado",
                         y=-3.45)
        self.fechar(cab, topo, certo, errado, lbl_c, lbl_e, preso, caixa, det, nota)

    # ------------------------------------------------------------------ #
    # 4. desigualdades
    # ------------------------------------------------------------------ #
    def caso_desigualdade(self):
        cab = self.cabecalho(4, "Desigualdades: multiplicar por negativo")

        eq = MathTex(r"-2x < 6").scale(1.0).move_to([0, 1.85, 0])
        self.play(Write(eq))
        self.wait(0.4)

        errado = VGroup(
            MathTex(r"x < -3").scale(0.78).set_color(COR_ERRO),
            MathTex(r"x = -4: \quad -2(-4) = 8 \;\not< \;6").scale(0.55).set_color(COR_ERRO),
        ).arrange(DOWN, buff=0.30).move_to([-3.55, 0.62, 0])
        lbl_e = self.rotulo("ATALHO:  divide por -2 e mantém o sinal", COR_ERRO, errado)

        certo = VGroup(
            MathTex(r"x > -3").scale(0.78).set_color(COR_CERTO),
            MathTex(r"x = 0: \quad -2(0) = 0 < 6").scale(0.55).set_color(COR_CERTO),
        ).arrange(DOWN, buff=0.30).move_to([3.55, 0.62, 0])
        lbl_c = self.rotulo("CORRETO:  inverte o sentido", COR_CERTO, certo)

        self.play(FadeIn(lbl_e), TransformFromCopy(eq, errado[0]), run_time=1.0)
        self.play(Write(errado[1]), run_time=0.9)
        v_err = self.veredito("falso", COR_ERRO, errado[1])
        self.play(FadeIn(v_err), Indicate(errado[0], color=COR_ERRO), run_time=0.9)
        self.wait(0.3)

        self.play(FadeIn(lbl_c), TransformFromCopy(eq, certo[0]), run_time=1.0)
        self.play(Write(certo[1]), run_time=0.9)
        v_ok = self.veredito("verdadeiro", COR_CERTO, certo[1])
        self.play(FadeIn(v_ok), run_time=0.6)

        # a reta mostra os dois conjuntos-solução em disputa
        reta = NumberLine(x_range=[-7, 3, 1], length=9.5, include_numbers=True,
                          font_size=22, color=GREY_B).move_to([0, -1.55, 0])
        self.play(Create(reta), run_time=1.0)

        p = reta.n2p(-3)
        raio_e = Line(reta.n2p(-7), p, color=COR_ERRO, stroke_width=7).shift(0.30 * UP)
        raio_c = Line(p, reta.n2p(3), color=COR_CERTO, stroke_width=7).shift(0.30 * UP)
        bola = Circle(radius=0.10, color=WHITE, stroke_width=3).move_to(p + 0.30 * UP)
        self.play(Create(raio_e), run_time=0.7)
        self.play(Create(raio_c), FadeIn(bola), run_time=0.8)
        self.play(FadeOut(raio_e), run_time=0.8)

        nota = self.nota("A ordem de ℝ só é preservada por positivos — o negativo espelha a reta",
                         y=-2.95)
        self.fechar(cab, eq, errado, certo, lbl_e, lbl_c, v_err, v_ok,
                    reta, raio_c, bola, nota)

    # ------------------------------------------------------------------ #
    def fecho(self):
        regra = Text("O princípio de equivalência só vale para operações INVERSÍVEIS",
                     weight=BOLD).scale(0.50).move_to([0, 0.95, 0])

        linhas = VGroup(
            Text("perde informação  (× 0)   →   some uma solução", slant=ITALIC).scale(0.42),
            Text("ganha soluções  ( )²   →   aparece uma raiz falsa", slant=ITALIC).scale(0.42),
            Text("não comuta  (matrizes)   →   o lado importa", slant=ITALIC).scale(0.42),
            Text("inverte a ordem  (× negativo)   →   o sinal vira", slant=ITALIC).scale(0.42),
        ).arrange(DOWN, buff=0.30, aligned_edge=LEFT).move_to([0, -1.05, 0])
        linhas.set_color(COR_NOTA)

        self.play(FadeIn(regra, shift=0.3 * UP))
        for lin in linhas:
            self.play(FadeIn(lin, shift=0.15 * RIGHT), run_time=0.5)
        self.wait(3.0)
