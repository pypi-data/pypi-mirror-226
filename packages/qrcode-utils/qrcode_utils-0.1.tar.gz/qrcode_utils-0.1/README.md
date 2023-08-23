qrcode_utils
............

"""Este pacote permite gerar um código do tipo imagem .png, QR CODE a partir de uma string fornecida pelo usuário, como também decodificar o codigo gerado através do arquivo de imagem fornecido.
""" 

""" Instalação:
pip install qrcode_utils

""" Instruções de uso:
Primeiramente precisa importa a classe Qr do módulo QrUtilitario.Qr
Em seguida, definir uma palavra (string de até 4296 caracteres) como entrada, que será transformada em QR CODE.
Para a decodificação, a entrada será um arquivo de imagem do tipo QR CODE, que será lida e decodificada em string.

"""

from QrUtilitario.Qr import Qr

palavra = "Suco de cevadiss, é um leite divinis, qui tem lupuliz, matis, aguis e fermentis"

dado = Qr.gerar_qr(palavra)

Qr.ler_imagem("meu_qr_code.png")