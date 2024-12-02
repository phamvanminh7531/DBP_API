from celery import shared_task
from celery.exceptions import Retry
from .utils import test_IMG2IMG, image_base64_encode, get_IMG2IMG_result

@shared_task(bind=True)  # Thử lại tối đa 3 lần, cách nhau 60 giây
def process_image_task(self, img_3d_input_url, img_style_input_url, client_id, promt_text):

    
    worker_name = process_image_task.request.hostname

    # Xác định server dựa vào tên worker
    if 'worker1' in worker_name:
        server_address = '192.168.1.49:8188'
    elif 'worker2' in worker_name:
        server_address = '192.168.1.50:8188'
    else:
        raise ValueError(f"Worker không xác định: {worker_name}")
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
    result = test_IMG2IMG(img_3d_input_url=img_3d_input_url, 
                            img_style_input_url=img_style_input_url, 
                            client_id=client_id,
                            server_address=server_address, 
                            promt_text=promt_text)

    # Mã hóa ảnh thành Base64
    img_base64 = image_base64_encode(result)
    print(img_base64)
    print("-" * 10)
    return img_base64
