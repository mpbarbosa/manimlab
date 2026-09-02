"""Multiplicação de matrizes — M · I₂ (solução animada, passo a passo).

    M = [3  4]        I₂ = [1  0]
        [5  1]             [0  1]

Regra: o elemento c_ij do produto é o "produto escalar" da LINHA i da primeira
matriz pela COLUNA j da segunda.

    c11 = 3·1 + 4·0 = 3        c12 = 3·0 + 4·1 = 4
    c21 = 5·1 + 1·0 = 5        c22 = 5·0 + 1·1 = 1

    M · I₂ = [3  4] = M   →  I₂ é o elemento neutro da multiplicação de matrizes
             [5  1]          (assim como 7 · 1 = 7 nos números reais).

Render:
    manim -pqh scenes/matriz_identidade.py MatrizIdentidade
"""

from manim import *

COR_M = BLUE_B      # entradas de M (vêm das LINHAS)
COR_I = YELLOW      # entradas de I₂ (vêm das COLUNAS)
COR_R = GREEN       # entradas do resultado

M_VALS = [[3, 4], [5, 1]]
I_VALS = [[1, 0], [0, 1]]


class MatrizIdentidade(Scene):
    def construct(self):
        self.titulo = Text("Multiplicação de matrizes: M · I₂", weight=BOLD).scale(0.6)
        self.titulo.to_edge(UP, buff=0.35)
        self.play(Write(self.titulo))

        self.apresentar()
        self.regra()
        for i, j in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            self.calcular(i, j, primeira=(i == 0 and j == 0))
        self.conclusao()

    # ------------------------------------------------------------------ #
    def apresentar(self):
        """Mostra as duas matrizes e monta a equação M · I₂ = [ ]."""
        self.M = Matrix(M_VALS)
        self.M.get_entries().set_color(COR_M)
        self.I = Matrix(I_VALS)
        self.I.get_entries().set_color(COR_I)
        self.R = Matrix(M_VALS)  # resultado: entra em cena uma casa por vez
        self.R.get_entries().set_color(COR_R)

        ponto = MathTex(r"\cdot").scale(1.3)
        igual = MathTex("=").scale(1.3)
        eq = VGroup(self.M, ponto, self.I, igual, self.R)
        eq.arrange(RIGHT, buff=0.45).scale(0.85).move_to([0, 1.45, 0])

        lbl_m = MathTex("M").scale(0.7).set_color(COR_M).next_to(self.M, DOWN, buff=0.22)
        lbl_i = MathTex("I_2").scale(0.7).set_color(COR_I).next_to(self.I, DOWN, buff=0.22)
        self.rotulos = VGroup(lbl_m, lbl_i)

        # 1) as matrizes dadas
        self.play(FadeIn(self.M), FadeIn(lbl_m))
        self.play(FadeIn(self.I), FadeIn(lbl_i))
        self.wait(0.3)

        # 2) a identidade tem 1 na diagonal e 0 fora dela
        diag = VGroup(*[self.I.get_entries()[k] for k in (0, 3)])
        nota_i = Text("I₂: 1 na diagonal, 0 fora dela", slant=ITALIC).scale(0.38)
        nota_i.next_to(lbl_i, DOWN, buff=0.3)
        self.play(Indicate(diag, color=COR_I, scale_factor=1.4), FadeIn(nota_i))
        self.wait(0.8)
        self.play(FadeOut(nota_i))

        # 3) a equação a resolver, com o resultado ainda vazio
        self.play(FadeIn(ponto), FadeIn(igual), FadeIn(self.R.get_brackets()))
        self.molde = VGroup(*[
            Square(side_length=0.42, color=GREY_B, stroke_width=2,
                   stroke_opacity=0.6).move_to(e)
            for e in self.R.get_entries()
        ])
        self.play(*[Create(q) for q in self.molde], run_time=0.9)
        self.wait(0.4)

    # ------------------------------------------------------------------ #
    def regra(self):
        """Enuncia a regra linha × coluna e mostra o que ela significa."""
        texto = Text("Cada casa do resultado = linha de M  ×  coluna de I₂",
                     slant=ITALIC).scale(0.44)
        texto.move_to([0, -0.25, 0])
        self.play(FadeIn(texto, shift=0.2 * UP))

        # demonstração: linha 1 de M e coluna 1 de I₂ produzem a casa (1,1)
        linha = SurroundingRectangle(self.M.get_rows()[0], color=COR_M, buff=0.12)
        coluna = SurroundingRectangle(self.I.get_columns()[0], color=COR_I, buff=0.12)
        alvo = SurroundingRectangle(self.molde[0], color=COR_R, buff=0.06)

        self.play(Create(linha))
        self.play(Create(coluna))
        self.play(Create(alvo))

        # linha e coluna "se encontram" exatamente nessa casa
        eco_l, eco_c = linha.copy(), coluna.copy()
        self.play(Transform(eco_l, alvo.copy()), Transform(eco_c, alvo.copy()),
                  run_time=1.2)
        self.play(Flash(alvo, color=COR_R, line_length=0.15, num_lines=12,
                        flash_radius=0.45), FadeOut(VGroup(eco_l, eco_c)))
        self.wait(0.8)
        self.play(FadeOut(VGroup(linha, coluna, alvo)))

        self.regra_txt = texto

    # ------------------------------------------------------------------ #
    def calcular(self, i, j, primeira=False):
        """Anima o cálculo de c_ij: linha i de M vezes coluna j de I₂."""
        a1, a2 = M_VALS[i][0], M_VALS[i][1]   # linha i de M
        b1, b2 = I_VALS[0][j], I_VALS[1][j]   # coluna j de I₂
        res = a1 * b1 + a2 * b2

        linha = SurroundingRectangle(self.M.get_rows()[i], color=COR_M, buff=0.12)
        coluna = SurroundingRectangle(self.I.get_columns()[j], color=COR_I, buff=0.12)
        alvo = SurroundingRectangle(self.molde[2 * i + j], color=COR_R, buff=0.06)
        self.play(Create(linha), Create(coluna), Create(alvo), run_time=0.7)

        conta = MathTex(
            f"c_{{{i + 1}{j + 1}}}", "=",
            str(a1), r"\cdot", str(b1), "+", str(a2), r"\cdot", str(b2),
            "=", str(res),
        ).scale(0.95).move_to([0, -1.55, 0])
        conta[2].set_color(COR_M)
        conta[6].set_color(COR_M)
        conta[4].set_color(COR_I)
        conta[8].set_color(COR_I)
        conta[10].set_color(COR_R)

        # os números "descem" das matrizes para a conta
        m_ent = self.M.get_entries()
        i_ent = self.I.get_entries()
        self.play(Write(conta[0]), Write(conta[1]), run_time=0.6)
        self.play(TransformFromCopy(m_ent[2 * i + 0], conta[2]),
                  TransformFromCopy(i_ent[0 * 2 + j], conta[4]),
                  FadeIn(conta[3]), run_time=1.0)
        self.play(FadeIn(conta[5]), run_time=0.25)
        self.play(TransformFromCopy(m_ent[2 * i + 1], conta[6]),
                  TransformFromCopy(i_ent[1 * 2 + j], conta[8]),
                  FadeIn(conta[7]), run_time=1.0)
        self.wait(0.3)

        # um dos termos sempre morre: é o que está multiplicado por 0
        k = 2 if b1 == 0 else 6           # índice do primeiro fator do termo nulo
        termo = VGroup(conta[k], conta[k + 1], conta[k + 2])
        risco = Line(termo.get_left() + 0.05 * LEFT, termo.get_right() + 0.05 * RIGHT,
                     color=RED, stroke_width=5)
        self.play(Create(risco), run_time=0.5)
        if primeira:
            nota = Text("×0 anula o termo · ×1 preserva o termo",
                        slant=ITALIC).scale(0.36).set_color(GREY_A)
            nota.next_to(conta, DOWN, buff=0.4)
            self.play(FadeIn(nota))
            self.wait(1.0)
            self.play(FadeOut(nota))

        # sobra apenas o termo multiplicado por 1
        self.play(Write(conta[9]), Write(conta[10]), run_time=0.7)
        self.wait(0.4)

        # o valor sobe para a casa correspondente do resultado
        casa = self.R.get_entries()[2 * i + j]
        self.play(TransformFromCopy(conta[10], casa),
                  FadeOut(self.molde[2 * i + j]), run_time=1.0)
        self.wait(0.3)

        self.play(FadeOut(VGroup(linha, coluna, alvo, risco, conta)), run_time=0.5)

    # ------------------------------------------------------------------ #
    def conclusao(self):
        self.play(FadeOut(self.regra_txt))

        caixa = SurroundingRectangle(self.R, color=COR_R, buff=0.12)
        self.play(Create(caixa))
        self.wait(0.5)

        # o resultado é a própria matriz M
        comp = MathTex(r"M \cdot I_2", "=", r"\begin{bmatrix} 3 & 4 \\ 5 & 1 \end{bmatrix}",
                       "=", "M").scale(0.9)
        comp[2].set_color(COR_R)
        comp[4].set_color(COR_M)
        comp.move_to([0, -0.9, 0])
        self.play(TransformFromCopy(VGroup(self.R, caixa), comp[2]),
                  FadeIn(comp[0]), FadeIn(comp[1]), run_time=1.2)
        self.play(FadeIn(comp[3]), TransformFromCopy(self.M, comp[4]), run_time=1.0)
        self.wait(0.8)

        moral = VGroup(
            Text("A identidade não muda a matriz:  M · I₂ = I₂ · M = M",
                 weight=BOLD).scale(0.46),
            Text("É o mesmo papel que o número 1 faz nos reais:  7 · 1 = 7",
                 slant=ITALIC).scale(0.42).set_color(GREY_A),
        ).arrange(DOWN, buff=0.28).move_to([0, -2.6, 0])

        self.play(FadeIn(moral[0], shift=0.25 * UP))
        self.play(FadeIn(moral[1]))
        self.wait(2.5)
