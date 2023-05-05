
# ------------------------------ General code ----------------------------------- #
APP_CODE = [
    {
        "code": "0000",
        "message": "The authentication token is invalid",
        "vi_message": "Token đăng nhập không hợp lệ, gộp chung các trường hợp như token hết hạn, không decode được...v"
    },
    {
        "code": "0001",
        "message": "The requested resource does not exist"
    },
    {
        "code": "0002",
        "message": "The account does not have enough permission to execute this operation",
        "vi_message": "Không đủ quyền để thực hiện chức năng này"
    },
    {
        "code": "0003",
        "message": "Data too large",
        "vi_message": "Dữ liệu quá lớn"
    },
    {
        "code": "0004",
        "message": "Invalid data",
        "vi_message": "Dữ liệu không hợp lệ"
    },
    {
        "code": "0005",
        "message": "Method Not Allowed",
        "vi_message": "Phương thức truy cập không hợp lệ"
    },
    {
        "code": "0008",
        "message": "Unknown Error",
        "vi_message": "Khong biet loi"
    },
    {
        "code": "0009",
        "message": "Service temporarily unavailable, try again later.",
        "vi_message": "Service temporarily unavailable, try again later."
    }
]


# ------------------------------ User error code ----------------------------------- #
APP_CODE += [

]


# ------------------------------ Device error code --------------------------------- #
APP_CODE += [
    {
        "code": "2000",
        "message": "You can not delete the master device",
        "vi_message": "Bạn không thể xóa thiết bị chính"
    }
]

# ------------------------------ Message error code --------------------------------- #
APP_CODE += [
    {
        "code": "3000",
        "message": "The device destination mismatched",
        "vi_message": "Không tìm thấy thiết bị đích"
    },
    {
        "code": "3001",
        "message": "The device destination is staled",
        "vi_message": "Thiết bị đích đã cũ"
    },
    {
        "code": "3002",
        "message": "The device destination is disabled or not found",
        "vi_message": "Thiết bị đích không tìm thấy"
    }
]

# --------------------------- Group chat error code --------------------------------- #
APP_CODE += [
    {
        "code": "4000",
        "message": "The attachments of the group chat can not be deleted",
        "vi_message": "Các tệp đính kèm của nhóm hội thoại không thể xóa"
    },
]


def get_app_code_content(code):
    try:
        return [content for content in APP_CODE if content["code"] == code][0]['message']
    except (IndexError, KeyError):
        raise Exception("Does not have this app_code")
