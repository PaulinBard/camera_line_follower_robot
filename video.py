import numpy as np
import cv2 as cv2
import time

def transfo(frame):
    dim_x=320
    dim_y=240
    range_bande=4
    img='ruban-rouge-d'
   
    image = frame
    #reduire
    image = cv2.resize(image, (dim_x, dim_y ))
    # Convertir l'image en espace de couleur HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # rgb_color=np.array([0,118,231]) #bleu RGB
    # bgr_color = rgb_color.reshape(1, 1, 3).astype(np.uint8)

    # # Convertir la couleur de BGR à HSV
    # target_color = cv2.cvtColor(bgr_color, cv2.COLOR_BGR2HSV)
    # print(target_color)
    # tolérance = 40
    # lower_red = np.array([target_color[0][0][0]+tolérance, target_color[0][0][1]+tolérance, target_color[0][0][2]+tolérance])  # Limite inférieure du rouge dans l'espace HSV
    # upper_red = np.array([target_color[0][0][0]-tolérance, target_color[0][0][1]-tolérance, target_color[0][0][2]-tolérance])  # Limite supérieure du rouge dans l'espace HSV
    # print(lower_red)
    lower_red = np.array([0, 100, 100])  # Limite inférieure du rouge dans l'espace HSV
    upper_red = np.array([10, 255, 255])  # Limite supérieure du rouge dans l'espace HSV
#      ([100, 0, 0], [140, 255, 255]),  # Bleu #0076e7 rgb (0,118,231) hsv (209,100,90)(teinte,saturation,luminosité)
#      ([35, 50, 50], [85, 255, 255]),   # Vert 
#      ([0, 120, 70], [10, 255, 255])    # Rouge[0, 100, 100][10, 255, 255]

    # Créer un masque en utilisant les seuils de teinte pour détecter le rouge
    red_mask = cv2.inRange(hsv_image, lower_red, upper_red)
    
    # Trouver les contours des objets rouges dans l'image
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dessiner les contours sur l'image originale
    image_with_contours = cv2.drawContours(image.copy(), contours, -1, (0, 0, 255), 2)

    
    mask = np.zeros_like(image)

    # Dessiner les contours sur le masque
    cv2.drawContours(mask, contours, -1, (255), thickness=cv2.FILLED) 
    
    #recup BNW
    blue_channel = mask[:, :, 0]
    non_zero_points = cv2.findNonZero(blue_channel)
    if non_zero_points is not None:
        if non_zero_points.size!=0 :
            centre = np.mean(non_zero_points, axis=0).astype(int)
            print(centre)
            y=centre[0][1]
            x=centre[0][0]
            print(x,y)
            mask[y][x][1]=255
            return mask
    
    return mask
    


cap = cv2.VideoCapture(-1)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, image = cap.read()

    # Récupérer les dimensions de l'image
    hauteur, largeur = image.shape[:2]

    # Calculer la largeur de la partie droite à remplacer (1/3 de la largeur)
    largeur_a_remplacer = int(largeur / 3)

    # Créer une image noire de la même taille que l'image d'origine
    partie_noire = np.zeros_like(image)

    # Remplacer la partie droite par l'image noire
    image[:, -largeur_a_remplacer:] = partie_noire[:, -largeur_a_remplacer:]



    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
   # gray = transfo(frame)#cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv2.imshow('frame', image)
    time.sleep(0.1)
    if cv2.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
