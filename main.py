import cv2
import numpy as np

# Carregar a imagem
image = cv2.imread('2.bmp')
image = image.astype(np.float32) / 255.0

canal_azul, canal_verde, canal_vermelho = cv2.split(image)

# Criar uma máscara para os tons de verde na imagem
green_mask = canal_verde - np.maximum(canal_vermelho, canal_azul)
green_mask[green_mask > 1] = 1
green_mask[green_mask < 0] = 0
green_mask = cv2.normalize(green_mask, None, 0, 1, cv2.NORM_MINMAX)

green_mask -= 0.5
green_mask *= 1.5
green_mask += 0.5

green_mask[green_mask > 1] = 1
green_mask[green_mask < 0] = 0

green_mask[green_mask > 0.95] = 1

cv2.imshow('Resultado', green_mask)
cv2.waitKey(0)

# Carregar o novo fundo
background = cv2.imread('dw.jpg')

background = cv2.resize(background, (image.shape[1], image.shape[0]))

background = background.astype(np.float32) / 255

img_saida = background.copy()

height = green_mask.shape[0]
width = green_mask.shape[1]
for y in range(0, height):
    for x in range(0, width):
        if green_mask[y][x] == 0:
            img_saida[y][x] = image[y][x]
        else:
            if green_mask[y][x] >= 1:
                img_saida[y][x] = background[y][x]
            else:
                print(green_mask[y][x])
                img_saida[y][x] = background[y][x] * (1 - green_mask[y][x])

# Converter a máscara para 3 canais (escala de cinza para BGR) - Deixado para mostrar outras tentativas de alpha blending
mascara_rgb = cv2.merge([green_mask, green_mask, green_mask])
# Foi tentado usar esse blend, que funcionou bem para as imagens, porém sempre deixou as bordas verdes (e as sombras também)
blended = background * (1 - mascara_rgb) + image * (mascara_rgb)

# Converter a imagem resultante de volta para escala de 0 a 255
blended = (blended * 255).astype(np.uint8)

cv2.imshow('Imagem Mesclada', img_saida)
cv2.waitKey(0)
cv2.destroyAllWindows()
