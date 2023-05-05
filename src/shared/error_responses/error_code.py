# ------------------------------ General code ----------------------------------- #
APP_CODE = [
    {
        "code": "0400",
        "message": "Invalid data",
        "vi_message": "Dữ liệu không hợp lệ"
    },
    {
        "code": "0401",
        "message": "The authentication token is invalid",
        "vi_message": "Token đăng nhập không hợp lệ, gộp chung các trường hợp như token hết hạn, không decode được...v"
    },
    {
        "code": "0403",
        "message": "The account does not have enough permission to execute this operation",
        "vi_message": "Không đủ quyền để thực hiện chức năng này"
    },
    {
        "code": "0404",
        "message": "The requested resource does not exist",
        "vi_message": "Tài nguyên không tồn tại"
    },
    {
        "code": "0405",
        "message": "This method is not allowed",
        "vi_message": "Phương thức truy cập không hợp lệ"
    },
    {
        "code": "0500",
        "message": "Unknown Error",
        "vi_message": "Khong biet loi"
    }
]


def get_app_code_content(code: str):
    try:
        return [content for content in APP_CODE if content["code"] == code][0]['message']
    except:
        raise Exception("Does not have this app_code {}".format(code))
