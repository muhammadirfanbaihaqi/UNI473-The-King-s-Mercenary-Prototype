import time
from collections import deque

# Menyimpan posisi ikan dari beberapa frame terakhir
history = deque(maxlen=60 * 3)  # 3 menit dengan 1 sample per 3 detik

def update_and_check_frozen(boxes):
    timestamp = time.time()
    history.append((timestamp, boxes))

    if len(history) < history.maxlen:
        return False  # Belum cukup data

    # Cek apakah posisi ikan tidak berubah signifikan selama 3 menit
    first_boxes = history[0][1]
    for _, current_boxes in history:
        if len(current_boxes) != len(first_boxes):
            return False  # Jumlah berubah

        for i in range(len(first_boxes)):
            fx1, fy1, fx2, fy2 = first_boxes[i]
            cx1, cy1, cx2, cy2 = current_boxes[i]

            if abs(cx1 - fx1) > 15 or abs(cy1 - fy1) > 15:
                return False  # Ada pergerakan signifikan

    return True
