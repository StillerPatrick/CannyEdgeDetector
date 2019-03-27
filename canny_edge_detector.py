import numpy as np 
import cv2 as cv

def canny_edge(input_path, output_path, threshold_low, treshold_high)
    img = np.array(load_image('praha.jpg'))
    blurred = cv.GaussianBlur(img,(5,5),0)
    dx = np.array(cv.Sobel(blurred,-1,1,0))
    dy = np.array(cv.Sobel(blurred,-1,0,1))
    d_img = dx + dy
    shape = dx.shape
    orientations = np.zeros(shape)
    for x in range(shape[0]):
    for y in range(shape[1]):
        if dx[x][y]:
            #calculate orientation in degree 
            orientations[x][y] = (np.arctan(dy[x,y]/dx[x,y])*180) / np.pi

    angle_array= np.array([0,45,90,135])

    sampled_orientations = np.zeros(shape)
    for x in range(shape[0]):
        for y in range(shape[1]):
            if orientations[x][y] % 180 <= 45 / 2:
                sampled_orientations[x][y] = 0

            if orientations[x][y] % 180 > 45 / 2 and orientations[x][y] % 180 <= 45 + 45/2:
                sampled_orientations[x][y] = 45
            
            if orientations[x][y] % 180 > 45 + 45/2 and orientations[x][y] % 180 <= 90 + 45/2:
                sampled_orientations[x][y] = 90
            
            if orientations[x][y] % 180 >  90 + 45/2 and orientations[x][y] % 180 <= 135 + 45/2:
                sampled_orientations[x][y] = 90
    magnitude = np.sqrt(dx**2 + dy**2)
    holded = 0
    deleted = 0
    for x in range (1,shape[0]-1):
        for y in range(1,shape[1]-1):
            hold=False
            current_magnitude = magnitude[x,y]
            current_orientation = sampled_orientations[x,y]

            neighborhood_magnitude_orientation = np.array([[magnitude[x-1][y-1],sampled_orientations[x-1][y-1]],
                                                            [magnitude[x][y-1],sampled_orientations[x][y-1]],
                                                            [magnitude[x+1][y-1],sampled_orientations[x+1][y-1]],
                                                            [magnitude[x-1][y],sampled_orientations[x-1][y]],
                                                            [magnitude[x+1][y],sampled_orientations[x+1][y]],
                                                            [magnitude[x-1][y+1],sampled_orientations[x-1][y+1]],
                                                            [magnitude[x][y+1],sampled_orientations[x][y+1]],
                                                            [magnitude[x+1][y+1],sampled_orientations[x+1][y+1]]])

            if current_magnitude == np.max(neighborhood_magnitude_orientation[:,0]):
                                     continue
            for n in neighborhood_magnitude_orientation:
                if n[0] > current_magnitude and n[1] == current_orientation:
                    hold = True 
            
            if not hold:
                d_img[x][y] = 0
    for x in range(shape[0]):
        for y in range(shape[1]):
            if magnitude[x][y] > treshold_high:
                continue
            if magnitude[x][y] > treshold_low:
                continue
            if magnitude[x][y] <= treshold_low:
                d_img[x][y] = 0
    return d_img
    
      
    
