"""Passar termos para o outro lado da igualdade — o atalho vs. o que o justifica.

Resolve  3x + 5 = 20  duas vezes, lado a lado:

    ATALHO                          O QUE REALMENTE ACONTECE
    3x + 5 = 20                     3x + 5 = 20            equação dada
    3x = 20 - 5                     (3x+5) + (-5) = 20 + (-5)   princípio aditivo
                                    3x + (5 + (-5)) = 15        associatividade
                                    3x + 0 = 15                 elemento inverso
    3x = 15                         3x = 15                     elemento neutro
    x = 15/3                        (1/3)(3x) = (1/3)(15)       princípio multiplicativo
                                    ((1/3)·3) x = 5             associatividade
                                    1 · x = 5                   elemento inverso
    x = 5                           x = 5                       elemento neutro

Moral: nada "atravessa" o sinal de igual. Aplica-se a operação INVERSA aos dois
lados; associatividade reagrupa, o inverso produz o neutro, o neutro desaparece.

Render:
    manim -pqh scenes/transposicao.py Transposicao
"""

from manim import *

COR_ATALHO = YELLOW     # coluna da esquerda (a regra prática)
COR_PASSO = BLUE_B      # coluna da direita (a justificativa)
COR_PROP = GREY_B       # nomes das propriedades
COR_OK = GREEN          # resposta final
COR_ALERTA = RED_B      # a pergunta que o atalho esconde

LX = -5.05              # centro da coluna do atalho
DIV_X = -2.95           # divisória entre as colunas
RX = -2.40              # borda esquerda das equações da direita
LBL_X = 2.45            # borda esquerda dos rótulos de propriedade

Y0 = 2.10               # altura da primeira linha
DY = 0.60               # espaçamento entre linhas

# (LaTeX, nome da propriedade) — uma entrada por linha da coluna da direita
PASSOS = [
    (r"3x + 5 = 20",                          "equação dada"),
    (r"(3x + 5) + (-5) = 20 + (-5)",          "princípio aditivo"),
    (r"3x + \bigl(5 + (-5)\bigr) = 15",       "associatividade"),
    (r"3x + 0 = 15",                          "elemento inverso (oposto)"),
    (r"3x = 15",                              "elemento neutro (0)"),
    (r"\tfrac{1}{3}\cdot(3x) = \tfrac{1}{3}\cdot 15", "princípio multiplicativo"),
    (r"\bigl(\tfrac{1}{3}\cdot 3\bigr)\,x = 5",       "associatividade"),
    (r"1 \cdot x = 5",                        "elemento inverso (recíproco)"),
    (r"x = 5",                                "elemento neutro (1)"),
]


def linha_y(i):
    """Altura da i-ésima linha das colunas."""
    return Y0 - i * DY


class Transposicao(Scene):
    def construct(self):
        titulo = Text("Passar para o outro lado: o atalho e o que ele esconde",
                      weight=BOLD).scale(0.52)
        titulo.to_edge(UP, buff=0.3)
        self.play(Write(titulo))

        self.abertura()
        self.bloco_aditivo()
        self.bloco_multiplicativo()
        self.conclusao()

    # ------------------------------------------------------------------ #
    def passo_direita(self, i, cor=COR_PASSO):
        """Escreve a i-ésima linha da coluna da direita com sua propriedade."""
        tex, prop = PASSOS[i]
        eq = MathTex(tex).scale(0.50).set_color(cor)
        eq.move_to([RX, linha_y(i), 0], aligned_edge=LEFT)
        lbl = Text(prop, slant=ITALIC).scale(0.30).set_color(COR_PROP)
        lbl.move_to([LBL_X, linha_y(i), 0], aligned_edge=LEFT)

        self.play(FadeIn(eq, shift=0.15 * RIGHT), run_time=0.7)
        self.play(FadeIn(lbl), run_time=0.4)
        self.direita.add(eq, lbl)
        return eq

    def passo_esquerda(self, mob, i):
        """Posiciona uma linha do atalho na altura da i-ésima linha da direita."""
        mob.scale(0.60).move_to([LX, linha_y(i), 0])
        self.esquerda.add(mob)
        return mob

    def encontro(self, esq, dir_):
        """Marca que atalho e justificativa chegaram ao mesmo lugar."""
        self.play(Indicate(esq, color=COR_OK, scale_factor=1.25),
                  Indicate(dir_, color=COR_OK, scale_factor=1.25), run_time=1.0)

    # ------------------------------------------------------------------ #
    def abertura(self):
        """A equação a resolver, e a montagem das duas colunas."""
        self.esquerda = VGroup()
        self.direita = VGroup()

        eq = MathTex("3x + 5 = 20").scale(1.4).move_to([0, 0.6, 0])
        alvo = Text("isolar o x", slant=ITALIC).scale(0.5).set_color(GREY_A)
        alvo.next_to(eq, DOWN, buff=0.45)
        self.play(Write(eq))
        self.play(FadeIn(alvo))
        self.wait(1.0)
        self.play(FadeOut(alvo))

        # divisória e cabeçalhos das duas colunas
        divisoria = DashedLine([DIV_X, 2.95, 0], [DIV_X, -2.95, 0],
                               color=GREY_D, stroke_width=2)
        h_esq = Text("O ATALHO", weight=BOLD).scale(0.42).set_color(COR_ATALHO)
        h_esq.move_to([LX, 2.72, 0])
        h_dir = Text("O QUE REALMENTE ACONTECE", weight=BOLD).scale(0.42)
        h_dir.set_color(COR_PASSO).move_to([RX, 2.72, 0], aligned_edge=LEFT)
        self.play(Create(divisoria), FadeIn(h_esq), FadeIn(h_dir), run_time=1.0)
        self.cabecalho = VGroup(divisoria, h_esq, h_dir)

        # a mesma equação inicia as duas colunas
        self.e1 = MathTex("3x", "+", "5", "=", "20").set_color(COR_ATALHO)
        self.passo_esquerda(self.e1, 0)
        d1 = MathTex(PASSOS[0][0]).scale(0.50).set_color(COR_PASSO)
        d1.move_to([RX, linha_y(0), 0], aligned_edge=LEFT)
        lbl = Text(PASSOS[0][1], slant=ITALIC).scale(0.30).set_color(COR_PROP)
        lbl.move_to([LBL_X, linha_y(0), 0], aligned_edge=LEFT)

        self.play(ReplacementTransform(eq, self.e1),
                  TransformFromCopy(eq, d1), run_time=1.3)
        self.play(FadeIn(lbl), run_time=0.4)
        self.direita.add(d1, lbl)
        self.wait(0.4)

    # ------------------------------------------------------------------ #
    def bloco_aditivo(self):
        """O +5 'atravessa' virando -5 — e os quatro passos que fazem isso."""
        # ATALHO: o termo voa por cima do sinal de igual e troca de sinal
        e2 = MathTex("3x", "=", "20", "-", "5").set_color(COR_ATALHO)
        self.passo_esquerda(e2, 1)
        self.play(TransformFromCopy(self.e1[0], e2[0]),
                  TransformFromCopy(self.e1[3], e2[1]),
                  TransformFromCopy(self.e1[4], e2[2]), run_time=0.8)
        self.play(TransformFromCopy(self.e1[1], e2[3], path_arc=-0.85 * PI),
                  TransformFromCopy(self.e1[2], e2[4], path_arc=-0.85 * PI),
                  run_time=1.4)

        duvida = Text("o sinal trocou — por quê?", slant=ITALIC).scale(0.36)
        duvida.set_color(COR_ALERTA).move_to([LX, linha_y(2.6), 0])
        self.play(FadeIn(duvida), Flash(e2[3], color=COR_ALERTA,
                                        line_length=0.12, num_lines=10,
                                        flash_radius=0.32))
        self.wait(1.2)

        # JUSTIFICATIVA: somar -5 aos dois lados, reagrupar, anular, sumir
        for i in (1, 2, 3):
            self.passo_direita(i)
            if i == 1:
                self.play(FadeOut(duvida), run_time=0.4)
            self.wait(0.3)

        d5 = self.passo_direita(4)
        e3 = MathTex("3x", "=", "15").set_color(COR_ATALHO)
        self.passo_esquerda(e3, 4)
        self.play(TransformFromCopy(VGroup(e2[2], e2[3], e2[4]), e3[2]),
                  TransformFromCopy(e2[0], e3[0]),
                  TransformFromCopy(e2[1], e3[1]), run_time=1.0)
        self.encontro(e3, d5)
        self.e3 = e3
        self.wait(0.3)

    # ------------------------------------------------------------------ #
    def bloco_multiplicativo(self):
        """O coeficiente 3 'passa dividindo' — e o que o autoriza."""
        # ATALHO: o 3 desce para o denominador
        e4 = MathTex("x", "=", r"\frac{15}{3}").set_color(COR_ATALHO)
        self.passo_esquerda(e4, 5)
        self.play(TransformFromCopy(self.e3[0], e4[0]),
                  TransformFromCopy(self.e3[1], e4[1]), run_time=0.8)
        self.play(TransformFromCopy(VGroup(self.e3[2], self.e3[0]), e4[2],
                                    path_arc=-0.6 * PI), run_time=1.2)
        self.wait(0.6)

        # JUSTIFICATIVA: multiplicar pelo inverso, reagrupar, anular, sumir
        for i in (5, 6, 7):
            self.passo_direita(i)
            self.wait(0.3)

        d9 = self.passo_direita(8, cor=COR_OK)
        e5 = MathTex("x", "=", "5").set_color(COR_OK)
        self.passo_esquerda(e5, 8)
        self.play(TransformFromCopy(e4[0], e5[0]),
                  TransformFromCopy(e4[1], e5[1]),
                  TransformFromCopy(e4[2], e5[2]), run_time=1.0)
        self.encontro(e5, d9)

        caixa = SurroundingRectangle(VGroup(e5, d9), color=COR_OK, buff=0.18)
        self.play(Create(caixa), run_time=0.8)
        self.caixa = caixa
        self.wait(0.8)

    # ------------------------------------------------------------------ #
    def conclusao(self):
        """A moral: o atalho é a operação inversa aplicada aos dois lados."""
        moral = Text(
            "Nada atravessa a igualdade: aplica-se a operação INVERSA aos dois lados",
            weight=BOLD).scale(0.44)
        moral.move_to([0, -3.32, 0])
        ferramentas = Text(
            "associatividade  ·  elemento inverso  ·  elemento neutro",
            slant=ITALIC).scale(0.38).set_color(COR_PROP)
        ferramentas.move_to([0, -3.72, 0])

        self.play(FadeIn(moral, shift=0.25 * UP))
        self.play(FadeIn(ferramentas))
        self.wait(3.0)
