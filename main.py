import cv2
import numpy as np

# Carregar a imagem
image = cv2.imread('4.bmp')
image = image.astype(np.float32) / 255

canal_azul, canal_verde, canal_vermelho = cv2.split(image)

# Criar uma máscara para os tons de verde na imagem
green_mask = canal_verde - np.maximum(canal_vermelho, canal_azul)
green_mask[green_mask > 1] = 1
green_mask[green_mask < 0] = 0
green_mask = cv2.normalize(green_mask, None, 0, 1, cv2.NORM_MINMAX)

green_mask = green_mask * 255

_, mascara_binaria = cv2.threshold(green_mask, 1, 255, cv2.THRESH_BINARY)


cv2.imshow('Resultado', green_mask)
cv2.waitKey(0)

# Carregar o novo fundo
background = cv2.imread('dw.jpg')

# Redimensionar o novo fundo para as dimensões da imagem original
background = cv2.resize(background, (image.shape[1], image.shape[0]))
img_8u = cv2.convertScaleAbs(mascara_binaria)
# Criar uma máscara invertida para o fundo verde
inverse_green_mask = cv2.bitwise_not(img_8u)

cv2.imshow('Resultado', inverse_green_mask)
cv2.waitKey(0)
# Extrair o objeto (não verde) da imagem original
object_only = cv2.bitwise_and(image, image, mask=inverse_green_mask)

# Extrair o fundo verde da imagem de fundo usando a máscara verde
green_background = cv2.bitwise_and(background, background, mask=img_8u)

# Combinar o objeto extraído com o fundo de sua escolha
#final_result = cv2.add(object_only, green_background)

# Mostrar o resultado
cv2.imshow('Resultado', green_background + object_only)
cv2.waitKey(0)
cv2.destroyAllWindows()
