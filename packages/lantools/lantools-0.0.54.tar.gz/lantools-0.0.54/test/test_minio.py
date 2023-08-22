import unittest
import base64
import datetime
from lantools import minio 

class TestCase(unittest.TestCase):
    def setUp(self):
        self.bucket = "mybucket"
        self.minio = minio.PyMinio(
            '10.10.9.31',
            9000,
            'minioadmin',
            'minioadmin',
        )
        self.minio.set_bucket(self.bucket)

    def tearDown(self):
        pass

    def test_upload_1(self):
        with open("/app/test/file/1.jpeg", "rb") as f:
            content = f.read()

        image_base64=str(base64.b64encode(content),encoding='utf8')

        filename = self.minio.upload_image(image_base64, object_name="test/1.jpeg")

        self.assertEqual(self.minio.exists(filename, trim=True), True)

        self.minio.remove_file(filename, trim=True)

    def test_upload_2(self):
        with open("/app/test/file/1.jpeg", "rb") as f:
            content = f.read()

        image_base64=str(base64.b64encode(content),encoding='utf8')

        filename = self.minio.upload_image(image_base64)

        self.assertEqual(self.minio.exists(filename, trim=True), True)

        self.minio.remove_file(filename, trim=True)

    # 自定义名称
    def test_upload_3(self):
        with open("/app/test/file/1.jpeg", "rb") as f:
            content = f.read()

        image_base64=str(base64.b64encode(content),encoding='utf8')

        filename = self.minio.upload_image(image_base64, object_name="default/01.jpeg")

        assert filename=='mybucket/default/01.jpeg'
        self.assertEqual(self.minio.exists(filename, trim=True), True)

        self.minio.remove_file(filename, trim=True)

    # 自定义名称:无扩展名
    def test_upload_4(self):
        with open("/app/test/file/noface.webp", "rb") as f:
            content = f.read()

        image_base64=str(base64.b64encode(content),encoding='utf8')

        filename = self.minio.upload_image(image_base64, object_name="default/01")

        assert filename=='mybucket/default/01.webp'
        self.assertEqual(self.minio.exists(filename, trim=True), True)

        self.minio.remove_file(filename, trim=True)

    # 自定义名称
    def test_upload_5(self):
        with open("/app/test/file/1.jpeg", "rb") as f:
            content = f.read()

        image_base64=str(base64.b64encode(content),encoding='utf8')

        filename = self.minio.upload_image(image_base64, object_name="default/01", filetype='jpg')

        assert filename=='mybucket/default/01.jpg'
        self.assertEqual(self.minio.exists(filename, trim=True), True)

        self.minio.remove_file(filename, trim=True)

    