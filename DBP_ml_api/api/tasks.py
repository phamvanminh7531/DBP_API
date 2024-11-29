from celery import shared_task
from celery.exceptions import Retry
from .utils import test_IMG2IMG, image_base64_encode

@shared_task(bind=True, max_retries=3, default_retry_delay=15)  # Thử lại tối đa 3 lần, cách nhau 60 giây
def process_image_task(self, img_3d_input_url, img_style_input_url, client_id, promt_text):
    try:
        # Gọi hàm xử lý
        result = test_IMG2IMG(img_3d_input_url=img_3d_input_url, 
                              img_style_input_url=img_style_input_url, 
                              client_id=client_id, 
                              promt_text=promt_text)

        # Mã hóa ảnh thành Base64
        img_base64 = image_base64_encode(result)
        print(img_base64)
        print("-" * 10)
        return img_base64

    except Exception as e:
        # Log lỗi trước khi retry
        self.retry(exc=e)
