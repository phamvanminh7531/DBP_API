from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import TWO_IMG2IMG_WITH_PROMTSerializers, MASKSerializers
import uuid
from celery.result import AsyncResult
from django.http import JsonResponse
from .tasks import process_img2img_task, process_mask_img_task
from .utils import get_mask_result

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
                   
            
#             result = get_IMG2IMG_result(img_3d_input_url=img_3d_input_url, 
#                                         img_style_input_url=img_style_input_url, 
#                                         client_id=client_id,
#                                          promt_text=promt_text)
            
            
#             # Convert the image to base64
#             img_base64 = image_base64_encode(result)
#             return Response({
#                 "image_data": img_base64
#                 }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MASK(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request):
        serializer = MASKSerializers(data=request.data)
        if serializer.is_valid():
            client_id = str(uuid.uuid4())
            image_instance = serializer.save()
            img_mask_input_url = request.build_absolute_uri(image_instance.img_mask_input.url)
            img_material_input_url = request.build_absolute_uri(image_instance.img_material_input.url)
            ipadapter_weight = image_instance.ipadapter_weight
            print(ipadapter_weight)
         
            task = process_mask_img_task.delay(img_mask_url=img_mask_input_url,
                                     img_material_url=img_material_input_url,
                                     client_id=client_id,
                                     ipadapter_weight=ipadapter_weight,                                     
                                     )
            return Response({
                "task_id": task.id
            }, status=status.HTTP_202_ACCEPTED)
            # result = get_mask_result(   img_mask_url=img_mask_input_url, 
            #                             img_material_url=img_material_input_url, 
            #                             client_id=client_id,
            #                             ipadapter_weight=ipadapter_weight,
            #                             server_address = '192.168.1.49:8188' )
            
            
            # # Convert the image to base64
            # return Response({
            #     "image_data": result
            #     }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            task = process_img2img_task.delay(img_3d_input_url, img_style_input_url, client_id, promt_text)

            return Response({
                "task_id": task.id
            }, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def get_task_status(request, task_id):
    result = AsyncResult(task_id)  # Lấy thông tin task qua ID

    # Kiểm tra trạng thái
    if result.state == 'PENDING':
        return JsonResponse({'status': 'PENDING'})  # Task đang chờ xử lý
    elif result.state == 'STARTED':
        return JsonResponse({'status': 'STARTED'})  # Task đang chạy
    elif result.state == 'SUCCESS':
        return JsonResponse({'status': 'SUCCESS', 'result': result.result})  # Task hoàn thành
    elif result.state == 'FAILURE':
        return JsonResponse({'status': 'FAILURE', 'error': str(result.info)})  # Task thất bại
    else:
        return JsonResponse({'status': result.state})  # Các trạng thái khác