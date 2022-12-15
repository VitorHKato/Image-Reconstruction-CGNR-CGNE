import datetime
import numpy as np
import cv2

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Request
from .serializer import RequestSerializer, RequestSerializer2

MAX_ERROR = 10 ** -4
FLIP_HORIZONTALLY = 1

# Create your views here.
class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


class ReturnRequests(generics.GenericAPIView, APIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer2

    def get(self, *args, **kwargs):
        user_id = self.kwargs['user_id'] if self.kwargs else None

        if user_id:
            all_requests = Request.objects.filter(pk=user_id)
        else:
            all_requests = Request.objects.all()

        serializer = RequestSerializer2(all_requests, many=True)

        return Response(serializer.data)

"""
    Retorna a imagem do registro com o id passado por parÃ¢metro
"""
class ReturnImage(APIView):
    def get(self, request, pk=None):

        image = ''

        if pk:
            image = RequestViewSet.queryset.get(pk=pk)

        try:
            image = image.image.url
        except:
            image = ''

        dict_response = {
            'image': str(image)[1:]
        }

        img = mpimg.imread(str(image)[1:])
        plt.imshow(img)
        plt.show()

        return Response(dict_response)


class GenerateImages(APIView):
    def post(self, request):

        try:
            data = request.data

            for i in data:
                new_request = Request()
                new_request.user_id = i['user_id']
                new_request.user_name = i['user_name']

                if i['algorithm'] == 'cgnr':
                    generate_time, image, algorithm_name, pixel_size, iterations = conjugate_gradient_normal_residual(
                        user_id=i['user_id'], user_name=i['user_name'], signal_name=i['signal_name']
                    )
                else:
                    generate_time, image, algorithm_name, pixel_size, iterations = conjugate_gradient_method_normal_error(
                        user_id=i['user_id'], user_name=i['user_name'], signal_name=i['signal_name']
                    )

                new_request.generation_time = generate_time
                new_request.image = image
                new_request.algorithm_name = algorithm_name
                new_request.image_pixel_size = pixel_size
                new_request.iterations = iterations
                new_request.save()

            response = 'Done!'
        except Exception as e:
            response = 'Error, ' + str(e)

        a = {
            'response': response
        }

        return Response(a)


def conjugate_gradient_normal_residual(user_id=None, user_name=None, signal_name=None):

    # H = np.loadtxt('data/H-2.csv', delimiter=',')
    # np.save('data/' + 'h2-raw', H)                     #Salva o modelo em um arquivo .npy para ser carregado mais rÃ¡pido

    if signal_name == "30x30-1" or signal_name == "30x30-2":
        H = np.load("data/h2-raw.npy")
    else:
        H = np.load("data/h1-raw.npy")
    Ht = np.transpose(H)
    # g = np.loadtxt("data/g-30x30-2.csv", usecols=0)           #Salva o sinal em um arquivo .npy para ser carregado mais rÃ¡pido
    # np.save("data/g-30x30-2-raw", g)
    if signal_name == "30x30-1":
        g = np.load("data/g-30x30-1-raw.npy")
    elif signal_name == "30x30-2":
        g = np.load("data/g-30x30-2-raw.npy")
    elif signal_name ==  "60x60-1":
        g = np.load("data/g2-raw.npy")
    else:
        g = np.load("data/g1-raw.npy")

    f = np.zeros(H.shape[1], dtype=np.float32)  # Cria um vetor
    r = g.copy()  # r = g - Hf
    z = np.matmul(np.transpose(H), r)  # z=H(t)r
    p = z.copy()  # p=z
    r_ant = r.copy()
    z_ant = z.copy()
    out = f.copy()

    err = 1
    iter = 0
    while (err > MAX_ERROR):
        iter += 1
        w = np.matmul(H, p)
        a = (np.linalg.norm(z) ** 2) / (np.linalg.norm(w) ** 2)
        f += a * p
        r -= a * w
        new_err = np.linalg.norm(r) - np.linalg.norm(r_ant)

        if (new_err < err):
            err = new_err
            out = f

        if (new_err < MAX_ERROR):
            break

        z = np.matmul(Ht, r)
        b = (np.linalg.norm(z) ** 2 / np.linalg.norm(z_ant) ** 2)
        p = z + b * p
        r_ant = np.linalg.norm(r)

    image_path = create_image(out=out, user_id=user_id, user_name=user_name, signal_name=signal_name, algorithm='cgnr')

    #calcular aqui o tamanho em pixels da imagem gerada

    # tempo de execuÃ§Ã£o, imagem, algoritmo, pixel size, iteraÃ§Ãµes
    return datetime.datetime.today(), image_path, 'cgnr' + '_' + str(signal_name), 50087, iter


def conjugate_gradient_method_normal_error(user_id=None, user_name=None, signal_name=None):

    return datetime.datetime.today(), 'media/image2.png', 'cgne 30x30', 50087, 14

def create_image(out=None, user_id=None, user_name=None, signal_name=None, algorithm=None):
    if signal_name == "30x30-1" or signal_name == "30x30-2":
        img = out.reshape((30, 30))
    else:
        img = out.reshape((60, 60))
    cols, rows = img.shape[0], img.shape[1]
    # m = cv2.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0),90,1)
    # img = cv2.warpAffine(img,m,(cols,rows))
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img = cv2.flip(img, FLIP_HORIZONTALLY)
    img = cv2.resize(img, None, fx=20, fy=20)
    cv2.normalize(img, img, float(0), float(1), cv2.NORM_MINMAX)

    img = np.float32(img)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.imshow(str(algorithm) + '_' + str(signal_name) + '_' + str(user_name) + '_' + str(user_id), img)
    cv2.imwrite('media/' + str(algorithm) + '_' + str(signal_name) + '_' + str(user_name) + '_' + str(user_id) + '.bmp', img * 255)

    cv2.waitKey()
    cv2.destroyAllWindows()

    return str(algorithm) + '_' + str(signal_name) + '_' + str(user_name) + '_' + str(user_id) + '.bmp'


