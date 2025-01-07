import math


# 預計入場時間計算
def time_cal(ID: int) -> str:
    # 初始入場時間
    total_time = 12 * 60  # 12:00 以分鐘計算

    if ID > 300:
        additional = ID - 300
        additional_time = (math.ceil(additional / 80)) * 30

        total_time += additional_time

    h = total_time // 60
    m = total_time % 60

    return f"{h:02}:{m:02}"