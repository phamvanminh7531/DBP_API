from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import TWO_IMG2IMGSerializers, TWO_IMG2IMG_WITH_PROMTSerializers
from .utils import get_IMG2IMG_result, test_IMG2IMG
from django.conf import settings
import uuid
from .utils import image_base64_encode

# class IMG2IMG(APIView):
#     parser_classes = (MultiPartParser, FormParser)
#     def post(self, request):
#         serializer = TWO_IMG2IMG_WITH_PROMTSerializers(data=request.data)
#         if serializer.is_valid():
#             client_id = str(uuid.uuid4())
#             image_instance = serializer.save()
#             img_3d_input_url = request.build_absolute_uri(image_instance.img_3d_input.url)
#             img_style_input_url = request.build_absolute_uri(image_instance.img_style_input.url)
#             promt_text = image_instance.promt_text
                   
            
#             result = test_IMG2IMG(img_3d_input_url=img_3d_input_url, 
#                                         img_style_input_url=img_style_input_url, 
#                                         client_id=client_id,
#                                          promt_text=promt_text)
            
            
#             # Convert the image to base64
#             img_base64 = image_base64_encode(result)
#             return Response({
#                 "image_data": img_base64
#                 }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from .tasks import process_image_task

class IMG2IMG(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        serializer = TWO_IMG2IMG_WITH_PROMTSerializers(data=request.data)
        if serializer.is_valid():
            client_id = str(uuid.uuid4())
            image_instance = serializer.save()
            img_3d_input_url = request.build_absolute_uri(image_instance.img_3d_input.url)
            img_style_input_url = request.build_absolute_uri(image_instance.img_style_input.url)
            promt_text = image_instance.promt_text

            # Gửi task đến Celery
            task = process_image_task.delay(img_3d_input_url, img_style_input_url, client_id, promt_text)

            return Response({
                "task_id": task.id,
                "status": "Processing"
            }, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)