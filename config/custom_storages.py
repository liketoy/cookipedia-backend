from storages.backends.s3boto3 import S3Boto3Storage


class SecurityTokenWorkaroundS3Boto3Storage(S3Boto3Storage):
    def _get_security_token(self):
        return None


class StaticStorage(SecurityTokenWorkaroundS3Boto3Storage):
    location = "static/"
    file_overwrite = False


class UploadStorage(SecurityTokenWorkaroundS3Boto3Storage):
    location = "uploads/"
