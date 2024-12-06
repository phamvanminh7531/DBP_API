from celery import shared_task
from celery.exceptions import Retry
from .utils import get_mask_result, get_IMG2IMG_result
import os

@shared_task(bind=True)
def process_img2img_task(self, img_3d_input_url, img_style_input_url, client_id, promt_text):
    # Xác định server dựa vào tên worker (Run without docker compose)
    # worker_name = process_image_task.request.hostname
    # if 'worker1' in worker_name:
    #     server_address = '192.168.1.49:8188'
    # elif 'worker2' in worker_name:
    #     server_address = '192.168.1.50:8188'
    # else:
    #     raise ValueError(f"Worker không xác định: {worker_name}")
    
    # RUN ON DOCKER COMPOSE
    server_address = os.getenv('WORKER_SERVER_ADDRESS')
    # try:
    #     # Gọi hàm xử lý
    #     result = get_IMG2IMG_result(img_3d_input_url=img_3d_input_url, 
    #                           img_style_input_url=img_style_input_url, 
    #                           client_id=client_id, 
    #                           promt_text=promt_text)

    #     # Mã hóa ảnh thành Base64
    #     img_base64 = image_base64_encode(result)
    #     print(img_base64)
    #     print("-" * 10)
    #     return img_base64

    # except Exception as e:
    #     # Log lỗi trước khi retry
    #     # self.retry(exc=e)
    #     pass
    result = get_IMG2IMG_result(img_3d_input_url=img_3d_input_url, 
                            img_style_input_url=img_style_input_url, 
                            client_id=client_id,
                            server_address=server_address, 
                            promt_text=promt_text)

    
    return result

@shared_task(bind=True)
def process_mask_img_task(img_mask_url, img_material_url, client_id, ipadapter_weight):
    
    server_address = os.getenv('WORKER_SERVER_ADDRESS')
    
    result = get_mask_result(img_mask_url=img_mask_url,
                                     img_material_url=img_material_url,
                                     ipadapter_weight=ipadapter_weight,
                                     client_id=client_id,
                                     server_address=server_address
                                     )
    
    return result
