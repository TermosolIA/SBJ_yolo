
import cv2
import os


def buscar_videos_figuras(ruta):

    lista_videos = []

    directorio = os.path.abspath(ruta)

    for root, dirs, files in os.walk(directorio):

        for archivo in files:
            
            _, extension = os.path.splitext(archivo)

            if extension == ".MP4":

                ruta_archivo = os.path.join(root,archivo)
                lista_videos.append(ruta_archivo)

    return lista_videos


def hconcat_resize(img_list, interpolation= cv2.INTER_CUBIC):

	h_min = min(img.shape[0] for img in img_list)
	im_list_resize = [cv2.resize(img,(int(img.shape[1] * h_min / img.shape[0]),	h_min), interpolation= interpolation) for img in img_list]
	return cv2.hconcat(im_list_resize)
