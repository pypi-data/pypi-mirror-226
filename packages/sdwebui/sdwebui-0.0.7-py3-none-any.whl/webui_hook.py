import os
import random
import string


def get_webui_root_path():
    return os.path.dirname(os.path.abspath(__file__))

def get_webui_models_path():
    return os.path.join(get_webui_root_path(), "models")

def get_stable_diffusion_models_path():
    return os.path.join(get_webui_models_path(), "Stable-diffusion")

def create_file_with_random_content(file_path: str) -> bool:
    """
    创建指定路径的文件，并在其中写入一个长度为10的随机字符串。

    :param file_path: 要写入的文件的路径。
    :return: 是否成功创建并写入文件。
    """
    try:
        # 获得文件目录
        dir_path = os.path.dirname(file_path)
        print(f"dir_path: {dir_path}")

        # 如果目录不存在，则创建
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # 生成随机字符串，长度为10
        random_string = "".join(
            random.choices(string.ascii_letters + string.digits, k=10)
        )

        # 写入文件
        with open(file_path, "w") as f:
            f.write(random_string)

        print(f"Created {file_path} with content: {random_string}")
        return True
    except Exception as e:
        print(f"Failed to create {file_path}. Reason: {e}")
        return False


def simple_test():
    print(f"get_webui_root_path: {get_webui_root_path()}")
    file_path = os.path.join(
        get_stable_diffusion_models_path(), "simple.txt"
    )
    create_file_with_random_content(file_path)

# 测试函数
if __name__ == "__main__":
    simple_test()
