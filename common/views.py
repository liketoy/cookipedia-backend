import boto3
import os
from uuid import uuid4
from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class QuillEditorUploader(APIView):
    def post(self, request):
        try:
            files = request.FILES.getlist("image")
            s3 = boto3.resource(
                "s3",
                aws_access_key_id=os.environ.get("AWS_S3_ACCESS_KEY_ID"),
                aws_secret_access_key=os.environ.get("AWS_S3_SECRET_ACCESS_KEY"),
            )
            ymd_path = datetime.now().strftime("%Y/%m/%d")
            for file in files:
                ext = file._name.split(".")[-1]
                filename = uuid4().hex
                file._set_name(str(f"{filename}.{ext}"))
                result = s3.Bucket(
                    os.environ.get("AWS_STORAGE_BUCKET_NAME")
                ).put_object(
                    Key=f"uploads/description/{ymd_path}/{file.name}",
                    Body=file,
                    ContentType="image/jpg",
                )
                return Response(
                    {
                        "ok": True,
                        "imageUrl": f"https://{result.bucket_name}.s3.ap-northeast-2.amazonaws.com/{result.key}",
                    }
                )
        except Exception as e:
            return Response(
                {"ok": False, "detail": e}, status=status.HTTP_400_BAD_REQUEST
            )
