import cv2
import numpy as np

# Carregar a imagem
image = cv2.imread('2.bmp')

# Converter de RGB para HSL
hsl_image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)

# Definir a faixa de tons de verde na imagem HSL
lower_green = np.array([35, 40, 40])  # Valores mínimos de H, S e L para verde
upper_green = np.array([85, 255, 255])  # Valores máximos de H, S e L para verde

# Criar uma máscara para os tons de verde na imagem HSL
green_mask = cv2.inRange(hsl_image, lower_green, upper_green)

# Carregar o novo fundo
background = cv2.imread('dw.jpg')

# Redimensionar o novo fundo para as dimensões da imagem original
background = cv2.resize(background, (image.shape[1], image.shape[0]))

# Criar uma máscara invertida para o fundo verde
inverse_green_mask = cv2.bitwise_not(green_mask)

# Extrair o objeto (não verde) da imagem original
object_only = cv2.bitwise_and(image, image, mask=inverse_green_mask)

# Extrair o fundo verde da imagem de fundo usando a máscara verde
green_background = cv2.bitwise_and(background, background, mask=green_mask)

# Combinar o objeto extraído com o fundo de sua escolha
final_result = cv2.add(object_only, green_background)

# Mostrar o resultado
cv2.imshow('Resultado', final_result)
cv2.waitKey(0)
cv2.destroyAllWindows()
