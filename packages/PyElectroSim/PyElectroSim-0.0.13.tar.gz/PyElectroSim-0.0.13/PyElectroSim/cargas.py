from .conf import *
import math
import pygame as py


class Carga:
    """
    Classe que representa uma carga elétrica.

    Uma carga elétrica é representada por um círculo de raio R e cor C. A carga
    pode ser positiva ou negativa, e isso é representado pela cor do círculo.
    A carga também possui um valor, que é a quantidade de carga elétrica que ela
    possui. O valor é representado pela cor do círculo, sendo que a cor azul
    representa valores positivos e a cor vermelha representa valores negativos.

    A carga também possui um identificador, que é um texto que aparece ao lado
    da carga. O identificador é opcional, e é utilizado para identificar a carga
    em um sistema com várias cargas.

    A carga também possui uma massa, que é utilizada para calcular a força
    elétrica entre duas cargas. A massa é representada por um círculo preto
    dentro do círculo da carga.

    A carga também possui uma velocidade inicial, que é utilizada para calcular
    a posição da carga em um determinado instante de tempo. A velocidade inicial
    é representada por uma seta que sai do centro da carga.

    A carga também possui uma posição inicial, que é utilizada para calcular a
    posição da carga em um determinado instante de tempo. A posição inicial é
    representada por um ponto preto no centro da carga.

    A carga também possui uma posição, que é utilizada para calcular a posição
    da carga em um determinado instante de tempo. A posição é representada por
    um ponto preto no centro da carga.

    A carga também possui uma velocidade, que é utilizada para calcular a
    posição da carga em um determinado instante de tempo. A velocidade é
    representada por uma seta que sai do centro da carga.

    A carga também possui um sinal, que é utilizado para calcular a força
    elétrica entre duas cargas. O sinal é representado por um sinal de menos
    (-) ou um sinal de mais (+) no centro da carga.

    A carga também possui um valor, que é utilizado para calcular a força
    elétrica entre duas cargas. O valor é representado por um número no centro
    da carga.

    A carga também possui um raio, que é utilizado para calcular a força
    elétrica entre duas cargas. O raio é representado por um círculo preto
    dentro do círculo da carga.

    Attributes
    ----------
    rect : pygame.Rect
        Um retângulo que representa a carga.
    x_inicial : int
        A posição inicial da carga no eixo x.
    y_inicial : int
        A posição inicial da carga no eixo y.
    x : int
        A posição da carga no eixo x.
    y : int
        A posição da carga no eixo y.
    raio : int
        O raio da carga.
    valor : float
        O valor da carga.
    identificador : str
        O identificador da carga.
    sinal : int
        O sinal da carga.
    cor : tuple
        A cor da carga.
    massa : float
        A massa da carga.
    velocidade_x : float
        A velocidade da carga no eixo x.
    velocidade_y : float
        A velocidade da carga no eixo y.
    mover : bool
        Indica se a carga deve se mover ou não.
    """
    def __init__(self, x: int, y: int, raio: int, num_eletrons: int, identificador: str = None):
        """
        Construtor da classe Carga.

        Parameters
        ----------
        x : int
            A posição inicial da carga no eixo x.
        y : int
            A posição inicial da carga no eixo y.
        raio : int
            O raio da carga.
        num_eletrons : int
            O número de elétrons da carga.
        identificador : str, optional
            O identificador da carga, por padrão None.
        """
        super().__init__()
        self.rect = py.Rect(x, y, raio * 2, raio * 2)
        self.x_inicial = x
        self.y_inicial = y
        self.x = self.x_inicial
        self.y = self.y_inicial
        self.raio = raio
        self.valor = num_eletrons * e
        self.identificador = identificador
        self.sinal, self.cor = self.get_sinal_cor()
        self.massa = MASSA
        self.velocidade_x = VELOCIDADE_INICIAL
        self.velocidade_y = VELOCIDADE_INICIAL
        self.mover = True

    def get_sinal_cor(self):
        """
        Retorna o sinal e a cor da carga.
        """
        sinal = 0
        cor = CINZA
        if self.valor < 0:
            sinal = -1
            cor = VERMELHO
        elif self.valor > 0:
            sinal = 1
            cor = AZUL
        return sinal, cor
    
    def desenhar(self, tela: py.Surface):
        """
        Desenha a carga na tela.

        Parameters
        ----------
        tela : pygame.Surface
            A tela do simulador.
        """
        py.draw.circle(tela, self.cor, (self.x, self.y), self.raio)
        if self.identificador:
            fonte = py.font.SysFont('Arial', 15)
            texto = fonte.render(self.identificador, True, TEXT_COLOR)
            tela.blit(texto, (self.x + self.raio, self.y + self.raio))

    def distancia(self, carga: 'Carga') -> float:
        """
        Calcula a distância entre duas cargas.

        Parameters
        ----------
        carga : Carga
            A carga com a qual a distância será calculada.

        Returns
        -------
        float
            A distância entre duas cargas.
        """
        return math.sqrt((carga.x - self.x) ** 2 + (carga.y - self.y) ** 2)

    def calcular_forca_eletrica(self, carga: 'Carga') -> tuple:
        """
        Calcula a força elétrica entre duas cargas.

        Parameters
        ----------
        carga : Carga
            A carga com a qual a força elétrica será calculada.

        Returns
        -------
        tuple
            A força elétrica entre duas cargas.
        """
        forca_x = forca_y = 0
        dx = carga.x - self.x
        dy = carga.y - self.y
        quadrado_distancia = dx ** 2 + dy ** 2
        if quadrado_distancia > (self.raio * 2) ** 2:
            forca_eletrica = k * self.sinal * carga.sinal * -1 / quadrado_distancia
            angulo = math.atan2(dy, dx)
            forca_x += forca_eletrica * math.cos(angulo)
            forca_y += forca_eletrica * math.sin(angulo)
        return forca_x, forca_y

    def atualizar_posicao(self, cargas: list):
        """
        Atualiza a posição da carga.

        Parameters
        ----------
        cargas : list
            A lista de cargas que estão no sistema.
        """
        if self.mover:
            for carga in cargas:
                if carga != self:
                    forca_x, forca_y = self.calcular_forca_eletrica(carga)
                    self.x += forca_x / self.massa * ESCALA
                    self.y += forca_y / self.massa * ESCALA
                    if self.distancia(carga) <= self.raio + carga.raio:
                        carga.mover = False
                        self.mover = False

    def resetar(self):
        """
        Reseta a posição da carga.

        A posição da carga é resetada para a posição inicial, e a velocidade da
        carga é resetada para a velocidade inicial.
        """
        self.x = self.x_inicial
        self.y = self.y_inicial
        self.velocidade_x = self.velocidade_y = VELOCIDADE_INICIAL
        self.mover = True


if __name__ == '__main__':
    pass