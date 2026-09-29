"""As propriedades do limite — por que o limite "entra" nas operações.

O roteiro vai da intuição à regra, e da regra ao seu limite de validade:

    1. INTUIÇÃO      f(x) = (x²-1)/(x-1) tem um buraco em x = 1, mas
                     lim f(x) = 2 quando x -> 1. O limite não pergunta
                     quanto vale f(1); pergunta para onde f(x) aponta.

    2. A REGRA       Com lim f = L e lim g = M, os dois pontos que viajam
       EM AÇÃO       sobre f e g arrastam o ponto de f+g: ele chega em
                     L + M sem que ninguém precise calcular nada.

    3. O CATÁLOGO    soma, diferença, múltiplo constante, produto,
                     quociente (M != 0), potência e raiz — todas erguidas
                     sobre dois tijolos: lim c = c e lim x = a.

    4. APLICAÇÃO     lim (3x² - 4x + 1)/(x + 3) quando x -> 2, um passo por
                     propriedade, com o nome de cada uma ao lado.

    5. O CUIDADO     A propriedade do quociente exige M != 0. Em
                     lim (x²-1)/(x-1) com x -> 1 ela simplesmente não se
                     aplica: 0/0 não é um número, é um aviso de que falta
                     álgebra antes do limite.

Moral: o limite respeita as operações aritméticas — desde que os limites
das partes existam e o denominador não vá a zero. Fora disso, primeiro se
reescreve a expressão, depois se toma o limite.

Render:
    manim -pqh scenes/limites_propriedades.py PropriedadesLimite
"""

from manim import *

COR_F = BLUE_B          # a função f
COR_G = YELLOW          # a função g
COR_SOMA = GREEN        # a combinação f + g / respostas
COR_PROP = GREY_B       # nomes das propriedades
COR_ALERTA = RED_B      # onde a regra não se aplica
COR_NOTA = GREY_A       # comentários


def f_demo(x):
    """f(x) = x/2 + 1  —  f(2) = 2."""
    return x / 2 + 1


def g_demo(x):
    """g(x) = 4 - x²/4  —  g(2) = 3."""
    return 4 - x * x / 4


def s_demo(x):
    """(f + g)(x)  —  (f+g)(2) = 5."""
    return f_demo(x) + g_demo(x)


class PropriedadesLimite(Scene):
    def construct(self):
        self.titulo = Text("Propriedades do limite", weight=BOLD).scale(0.56)
        self.titulo.to_edge(UP, buff=0.26)
        self.secao_atual = None
        self.play(Write(self.titulo))

        self.intuicao()
        self.regra_em_acao()
        self.catalogo()
        self.aplicacao()
        self.cuidado()
        self.fecho()

    # ------------------------------------------------------------------ #
    # auxiliares
    # ------------------------------------------------------------------ #
    def secao(self, texto):
        """Troca o subtítulo que nomeia a etapa atual."""
        novo = Text(texto, slant=ITALIC).scale(0.40).set_color(COR_NOTA)
        novo.next_to(self.titulo, DOWN, buff=0.20)
        if self.secao_atual is None:
            self.play(FadeIn(novo, shift=0.15 * DOWN), run_time=0.6)
        else:
            self.play(ReplacementTransform(self.secao_atual, novo), run_time=0.7)
        self.secao_atual = novo

    def nota(self, texto, y=-3.35, cor=COR_NOTA, escala=0.40):
        """Um comentário curto no rodapé."""
        mob = Text(texto, slant=ITALIC).scale(escala).set_color(cor)
        mob.move_to([0, y, 0])
        self.play(FadeIn(mob), run_time=0.6)
        return mob

    def limpar(self, *mobs):
        """Apaga o que sobrou da etapa, preservando título e subtítulo."""
        alvos = [m for m in mobs if m is not None]
        if alvos:
            self.play(*[FadeOut(m) for m in alvos], run_time=0.7)

    # ------------------------------------------------------------------ #
    # 1. o limite não é o valor da função
    # ------------------------------------------------------------------ #
    def intuicao(self):
        self.secao("primeiro: o limite não pergunta quanto vale f(1)")

        eixos = Axes(x_range=[0, 3.2, 1], y_range=[0, 4.2, 1],
                     x_length=5.4, y_length=3.5,
                     axis_config={"include_numbers": True, "font_size": 20,
                                  "include_tip": False})
        eixos.move_to([-3.6, -0.35, 0])
        graf = eixos.plot(lambda x: x + 1, x_range=[0, 3.1], color=COR_F)

        defin = MathTex(r"f(x) = \frac{x^2 - 1}{x - 1}").scale(0.62)
        defin.set_color(COR_F).move_to([-3.6, 2.40, 0])
        self.play(Write(defin))
        self.play(Create(eixos), run_time=1.0)
        self.play(Create(graf), run_time=1.2)

        # o buraco: x = 1 está fora do domínio
        buraco = Circle(radius=0.075, color=COR_ALERTA, stroke_width=3,
                        fill_opacity=1, fill_color=BLACK)
        buraco.move_to(eixos.c2p(1, 2))
        aviso = MathTex(r"f(1)\ \text{não existe}").scale(0.46)
        aviso.set_color(COR_ALERTA).move_to(eixos.c2p(2.25, 0.85))
        indicador = Arrow(aviso.get_top(), buraco.get_center(),
                          buff=0.14, stroke_width=2.5, color=COR_ALERTA,
                          max_tip_length_to_length_ratio=0.12)
        self.play(Create(buraco), FadeIn(aviso, shift=0.1 * UP),
                  GrowArrow(indicador))
        self.wait(0.8)

        # os dois pontos que se aproximam do buraco, um de cada lado
        t = ValueTracker(0.25)
        p_esq = always_redraw(lambda: Dot(eixos.c2p(t.get_value(),
                                                    t.get_value() + 1),
                                          color=COR_SOMA, radius=0.065))
        u = ValueTracker(2.85)
        p_dir = always_redraw(lambda: Dot(eixos.c2p(u.get_value(),
                                                    u.get_value() + 1),
                                          color=COR_SOMA, radius=0.065))
        self.play(FadeIn(p_esq), FadeIn(p_dir))
        self.bring_to_front(buraco)  # o buraco continua visível sob os pontos

        # tabela de valores: os dois lados convergem para 2
        cab = VGroup(MathTex("x").set_color(COR_NOTA),
                     MathTex("f(x)").set_color(COR_NOTA)).scale(0.55)
        linhas = [(r"0{,}9", r"1{,}9"), (r"0{,}99", r"1{,}99"),
                  (r"1{,}01", r"2{,}01"), (r"1{,}1", r"2{,}1")]
        celulas = VGroup(*[MathTex(s).scale(0.55) for par in linhas for s in par])
        tabela = VGroup(cab[0], cab[1], *celulas)
        tabela.arrange_in_grid(rows=5, cols=2, buff=(0.75, 0.28))
        tabela.move_to([2.9, 0.35, 0])
        risco = Line(LEFT, RIGHT, color=GREY_D, stroke_width=2)
        risco.set_width(tabela.width + 0.35).next_to(cab, DOWN, buff=0.14)

        self.play(FadeIn(cab), Create(risco), run_time=0.7)
        # cada linha da tabela empurra um dos pontos mais perto de x = 1
        aproximacoes = [(t, 0.90), (t, 0.99), (u, 1.01), (u, 1.10)]
        for i, (tracker, destino) in enumerate(aproximacoes):
            par = VGroup(celulas[2 * i], celulas[2 * i + 1])
            self.play(FadeIn(par, shift=0.12 * RIGHT),
                      tracker.animate.set_value(destino), run_time=0.9)
        self.wait(0.5)

        seta = MathTex(r"\downarrow").scale(0.7).set_color(COR_SOMA)
        seta.next_to(tabela, DOWN, buff=0.18)
        resp = MathTex(r"\lim_{x \to 1} f(x) = 2").scale(0.70)
        resp.set_color(COR_SOMA).next_to(seta, DOWN, buff=0.18)
        self.play(FadeIn(seta), Write(resp), run_time=1.1)
        self.play(Flash(buraco, color=COR_SOMA, line_length=0.14,
                        num_lines=12, flash_radius=0.30))

        moral = self.nota("o limite descreve a viagem, não o destino ocupado")
        self.wait(1.4)
        self.limpar(defin, eixos, graf, buraco, aviso, indicador,
                    p_esq, p_dir, tabela, risco, seta, resp, moral)

    # ------------------------------------------------------------------ #
    # 2. duas funções viajam juntas: a soma chega na soma
    # ------------------------------------------------------------------ #
    def regra_em_acao(self):
        self.secao("a regra em ação: quem chega em L e em M leva f+g a L+M")

        eixos = Axes(x_range=[0, 4.4, 1], y_range=[0, 6.5, 1],
                     x_length=5.8, y_length=4.1,
                     axis_config={"include_numbers": True, "font_size": 20,
                                  "include_tip": False})
        eixos.move_to([-3.4, -0.55, 0])
        gf = eixos.plot(f_demo, x_range=[0, 4.2], color=COR_F)
        gg = eixos.plot(g_demo, x_range=[0, 4.0], color=COR_G)
        gs = eixos.plot(s_demo, x_range=[0, 4.0], color=COR_SOMA)

        # rotuladas à esquerda, onde as três curvas estão bem separadas
        rot_f = MathTex("f").scale(0.6).set_color(COR_F)
        rot_f.next_to(eixos.c2p(0.9, f_demo(0.9)), UP, buff=0.10)
        rot_g = MathTex("g").scale(0.6).set_color(COR_G)
        rot_g.next_to(eixos.c2p(0.9, g_demo(0.9)), UP, buff=0.10)
        rot_s = MathTex("f+g").scale(0.6).set_color(COR_SOMA)
        rot_s.next_to(eixos.c2p(0.9, s_demo(0.9)), UP, buff=0.10)

        self.play(Create(eixos), run_time=1.0)
        self.play(Create(gf), FadeIn(rot_f), run_time=0.9)
        self.play(Create(gg), FadeIn(rot_g), run_time=0.9)
        self.play(Create(gs), FadeIn(rot_s), run_time=0.9)

        # o x que caminha rumo a a = 2
        t = ValueTracker(4.0)
        reta_x = always_redraw(lambda: DashedLine(
            eixos.c2p(t.get_value(), 0),
            eixos.c2p(t.get_value(), s_demo(t.get_value())),
            color=GREY_D, stroke_width=2))

        def ponto(func, cor):
            return always_redraw(lambda: Dot(
                eixos.c2p(t.get_value(), func(t.get_value())),
                color=cor, radius=0.07))

        pf, pg, ps = ponto(f_demo, COR_F), ponto(g_demo, COR_G), ponto(s_demo, COR_SOMA)
        marca_a = VGroup(
            Line(eixos.c2p(2, 0), eixos.c2p(2, 5.6), color=GREY_D,
                 stroke_width=2).set_opacity(0.55),
            MathTex("a = 2").scale(0.45).set_color(COR_NOTA)
            .next_to(eixos.c2p(2, 5.6), UP, buff=0.10))
        self.play(FadeIn(reta_x), FadeIn(pf), FadeIn(pg), FadeIn(ps),
                  Create(marca_a[0]), FadeIn(marca_a[1]), run_time=1.0)

        # painel de leitura: três valores correndo para 2, 3 e 5
        def leitura(nome, func, cor, y):
            rot = MathTex(nome).scale(0.55).set_color(cor)
            rot.move_to([1.15, y, 0], aligned_edge=LEFT)
            val = DecimalNumber(func(t.get_value()), num_decimal_places=2)
            val.scale(0.55).set_color(cor)
            val.add_updater(lambda m, fn=func: m.set_value(fn(t.get_value())))
            val.move_to([3.60, y, 0], aligned_edge=LEFT)
            return rot, val

        rf, vf = leitura("f(x)", f_demo, COR_F, 1.55)
        rg, vg = leitura("g(x)", g_demo, COR_G, 0.85)
        rs, vs = leitura("(f+g)(x)", s_demo, COR_SOMA, 0.15)
        self.add(vf, vg, vs)
        self.play(FadeIn(rf), FadeIn(rg), FadeIn(rs), run_time=0.7)

        self.play(t.animate.set_value(2.02), run_time=3.2, rate_func=smooth)
        self.wait(0.5)
        self.play(t.animate.set_value(0.6), run_time=1.6)
        self.play(t.animate.set_value(1.98), run_time=2.4, rate_func=smooth)
        self.wait(0.6)

        # o que os três valores acabaram de mostrar
        for v in (vf, vg, vs):
            v.clear_updaters()
        conclusao = VGroup(
            MathTex(r"\lim_{x \to 2} f(x) = 2").set_color(COR_F),
            MathTex(r"\lim_{x \to 2} g(x) = 3").set_color(COR_G),
            MathTex(r"\lim_{x \to 2} \bigl[f(x) + g(x)\bigr] = 5")
            .set_color(COR_SOMA),
        ).scale(0.55).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
        conclusao.move_to([3.05, -1.35, 0])
        self.play(FadeIn(conclusao[0], shift=0.1 * UP),
                  FadeIn(conclusao[1], shift=0.1 * UP), run_time=0.9)
        self.play(TransformFromCopy(VGroup(conclusao[0], conclusao[1]),
                                    conclusao[2]), run_time=1.3)
        caixa = SurroundingRectangle(conclusao[2], color=COR_SOMA, buff=0.14)
        self.play(Create(caixa), run_time=0.7)

        moral = self.nota("2 + 3 = 5 — o limite passou por dentro da soma")
        self.wait(1.4)
        self.limpar(eixos, gf, gg, gs, rot_f, rot_g, rot_s, reta_x, pf, pg, ps,
                    marca_a, rf, rg, rs, vf, vg, vs, conclusao, caixa, moral)

    # ------------------------------------------------------------------ #
    # 3. o catálogo completo
    # ------------------------------------------------------------------ #
    def catalogo(self):
        self.secao("o catálogo: tudo o que o limite atravessa")

        hip = VGroup(
            MathTex(r"\lim_{x \to a} f(x) = L").set_color(COR_F),
            MathTex(r"\lim_{x \to a} g(x) = M").set_color(COR_G),
        ).scale(0.62).arrange(RIGHT, buff=1.20)
        hip.move_to([0, 2.10, 0])
        rot_hip = Text("supondo que os dois limites existam:",
                       slant=ITALIC).scale(0.36).set_color(COR_NOTA)
        rot_hip.next_to(hip, UP, buff=0.18)
        self.play(FadeIn(rot_hip), Write(hip), run_time=1.3)

        props = [
            (r"\lim_{x \to a}\bigl[f(x) + g(x)\bigr] = L + M", "soma"),
            (r"\lim_{x \to a}\bigl[f(x) - g(x)\bigr] = L - M", "diferença"),
            (r"\lim_{x \to a}\bigl[c \cdot f(x)\bigr] = c \cdot L",
             "múltiplo constante"),
            (r"\lim_{x \to a}\bigl[f(x) \cdot g(x)\bigr] = L \cdot M", "produto"),
            (r"\lim_{x \to a}\frac{f(x)}{g(x)} = \frac{L}{M}",
             "quociente  (só vale se M não for zero)"),
            (r"\lim_{x \to a}\bigl[f(x)\bigr]^{n} = L^{n}", "potência"),
            (r"\lim_{x \to a}\sqrt[n]{f(x)} = \sqrt[n]{L}", "raiz"),
        ]

        y0, dy = 1.42, 0.59
        grupo = VGroup()
        for i, (tex, nome) in enumerate(props):
            cor = COR_ALERTA if "quociente" in nome else WHITE
            eq = MathTex(tex).scale(0.50).set_color(cor)
            eq.move_to([-4.60, y0 - i * dy, 0], aligned_edge=LEFT)
            lbl = Text(nome, slant=ITALIC).scale(0.32).set_color(
                COR_ALERTA if "quociente" in nome else COR_PROP)
            lbl.move_to([1.20, y0 - i * dy, 0], aligned_edge=LEFT)
            self.play(FadeIn(eq, shift=0.12 * RIGHT), FadeIn(lbl), run_time=0.55)
            grupo.add(eq, lbl)

        self.wait(0.6)

        # os dois casos-base de onde tudo isso se apoia
        base = VGroup(MathTex(r"\lim_{x \to a} c = c"),
                      MathTex(r"\lim_{x \to a} x = a")).scale(0.55)
        base.arrange(RIGHT, buff=1.1).set_color(COR_SOMA)
        base.move_to([0, -3.40, 0])
        rot_base = Text("os dois tijolos de onde tudo isso sai",
                        slant=ITALIC).scale(0.34).set_color(COR_NOTA)
        rot_base.next_to(base, UP, buff=0.14)
        self.play(FadeIn(rot_base), Write(base), run_time=1.2)
        self.wait(1.6)
        self.limpar(rot_hip, hip, grupo, base, rot_base)

    # ------------------------------------------------------------------ #
    # 4. uma conta inteira, um passo por propriedade
    # ------------------------------------------------------------------ #
    def aplicacao(self):
        self.secao("aplicação: cada linha é uma propriedade sendo usada")

        passos = [
            (r"\lim_{x \to 2} \frac{3x^2 - 4x + 1}{x + 3}", "o limite pedido"),
            (r"= \frac{\displaystyle\lim_{x \to 2}\,(3x^2 - 4x + 1)}"
             r"{\displaystyle\lim_{x \to 2}\,(x + 3)}",
             "quociente — vale porque o de baixo dá 5"),
            (r"= \frac{\lim 3x^2 - \lim 4x + \lim 1}{\lim x + \lim 3}",
             "soma e diferença"),
            (r"= \frac{3\lim x^2 - 4\lim x + 1}{\lim x + 3}",
             "múltiplo constante e  lim c = c"),
            (r"= \frac{3 \cdot 2^2 - 4 \cdot 2 + 1}{2 + 3}",
             "potência e  lim x = a"),
            (r"= \frac{12 - 8 + 1}{5} = \frac{5}{5} = 1", "aritmética"),
        ]

        y0, dy = 2.05, 0.92
        grupo = VGroup()
        anterior = None
        for i, (tex, nome) in enumerate(passos):
            cor = COR_SOMA if i == len(passos) - 1 else WHITE
            eq = MathTex(tex).scale(0.55).set_color(cor)
            eq.move_to([-5.40, y0 - i * dy, 0], aligned_edge=LEFT)
            lbl = Text(nome, slant=ITALIC).scale(0.32).set_color(COR_PROP)
            lbl.move_to([0.70, y0 - i * dy, 0], aligned_edge=LEFT)
            if anterior is None:
                self.play(Write(eq), run_time=0.9)
            else:
                self.play(TransformFromCopy(anterior, eq), run_time=1.0)
            self.play(FadeIn(lbl, shift=0.12 * RIGHT), run_time=0.45)
            grupo.add(eq, lbl)
            anterior = eq
            self.wait(0.25)

        caixa = SurroundingRectangle(grupo[-2], color=COR_SOMA, buff=0.14)
        self.play(Create(caixa), run_time=0.8)
        moral = self.nota("nenhuma linha inventa nada: cada uma cita uma regra")
        self.wait(1.4)
        self.limpar(grupo, caixa, moral)

    # ------------------------------------------------------------------ #
    # 5. onde a regra do quociente não se aplica
    # ------------------------------------------------------------------ #
    def cuidado(self):
        self.secao("o cuidado: a regra do quociente exige denominador não nulo")

        eq = MathTex(r"\lim_{x \to 1} \frac{x^2 - 1}{x - 1}").scale(0.85)
        eq.move_to([0, 2.05, 0])
        self.play(Write(eq))
        self.wait(0.4)

        tentativa = MathTex(r"\frac{\lim_{x \to 1}(x^2 - 1)}"
                            r"{\lim_{x \to 1}(x - 1)}", r"=",
                            r"\frac{0}{0}").scale(0.70)
        tentativa.move_to([0, 0.70, 0])
        tentativa[2].set_color(COR_ALERTA)
        self.play(TransformFromCopy(eq, tentativa), run_time=1.2)
        self.play(Flash(tentativa[2], color=COR_ALERTA, line_length=0.16,
                        num_lines=12, flash_radius=0.42))

        veredito = Text("o de baixo vai a zero: a propriedade não se aplica"
                        " — 0/0 não é resposta, é um aviso",
                        slant=ITALIC).scale(0.38)
        veredito.set_color(COR_ALERTA).next_to(tentativa, DOWN, buff=0.40)
        self.play(FadeIn(veredito), run_time=0.7)
        self.wait(1.2)

        # o conserto: álgebra antes do limite
        conserto = VGroup(
            MathTex(r"\frac{x^2 - 1}{x - 1} = \frac{(x-1)(x+1)}{x-1} = x + 1",
                    r"\quad (x \neq 1)"),
            MathTex(r"\lim_{x \to 1} \frac{x^2 - 1}{x - 1}"
                    r" = \lim_{x \to 1} (x + 1) = 2"),
        ).scale(0.60).arrange(DOWN, buff=0.45)
        conserto.move_to([0, -1.25, 0])
        conserto[0][1].set_color(COR_NOTA)
        conserto[1].set_color(COR_SOMA)
        self.play(FadeOut(veredito), run_time=0.4)
        self.play(Write(conserto[0]), run_time=1.4)
        self.wait(0.5)
        self.play(Write(conserto[1]), run_time=1.4)
        caixa = SurroundingRectangle(conserto[1], color=COR_SOMA, buff=0.16)
        self.play(Create(caixa), run_time=0.7)

        moral = self.nota("primeiro reescreve-se a expressão; só depois o limite"
                          " é tomado")
        self.wait(1.5)
        self.limpar(eq, tentativa, conserto, caixa, moral)

    # ------------------------------------------------------------------ #
    def fecho(self):
        self.play(FadeOut(self.secao_atual), run_time=0.5)
        self.secao_atual = None

        frases = VGroup(
            Text("O limite atravessa soma, diferença, produto,",
                 weight=BOLD).scale(0.52),
            Text("quociente, potência e raiz —", weight=BOLD).scale(0.52),
            Text("desde que os limites das partes existam", slant=ITALIC)
            .scale(0.46).set_color(COR_SOMA),
            Text("e o denominador não vá a zero.", slant=ITALIC)
            .scale(0.46).set_color(COR_ALERTA),
        ).arrange(DOWN, buff=0.34)
        frases.move_to([0, 0.05, 0])

        for frase in frases:
            self.play(FadeIn(frase, shift=0.16 * UP), run_time=0.8)
        self.wait(2.0)
        self.play(FadeOut(frases), FadeOut(self.titulo), run_time=1.2)
        self.wait(0.4)
