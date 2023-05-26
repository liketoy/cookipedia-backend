from django.core.mail import send_mail

def slug_to_name(value):
    return value.replace("-", " ")


def custom_send_mail():
    try:
        send_mail(
                "테스트메일",
                "",
                "ksakdt@naver.com",
                ["byby8992@naver.com"],
                fail_silently=False,
            )
    except Exception as e:
        print("에러 발생 : ", e)