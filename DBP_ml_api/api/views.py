from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import TWO_IMG2IMGSerializers
from .utils import get_IMG2IMG_result
from io import BytesIO
import io
from PIL import Image
import base64
from django.conf import settings
import uuid

class IMG2IMG(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request):
        serializer = TWO_IMG2IMGSerializers(data=request.data)
        if serializer.is_valid():
            client_id = str(uuid.uuid4())
            image_instance = serializer.save()
            img_3d_input_path = image_instance.img_3d_input.url
            img_style_input_path = image_instance.img_style_input.url
            
            result = get_IMG2IMG_result(img_3d_input_path=f'{settings.BASE_DIR}/{img_3d_input_path}', 
                                        img_style_input_path=f'{settings.BASE_DIR}/{img_style_input_path}', 
                                        client_id=client_id)
            # print(result)
            image = Image.open(io.BytesIO(result))
            img_io = BytesIO()
            image.save(img_io, 'PNG')  # You can save in another format if needed
            img_io.seek(0)

            # Convert the image to base64
            img_base64 = base64.b64encode(img_io.read()).decode('utf-8')
            return Response({"image_data": img_base64}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

