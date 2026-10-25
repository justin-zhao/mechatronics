import os
import shutil

SRC = r"D:\FarFlight\mechatronics\eura"
DST = r"D:\FarFlight\mechatronics\assets\images\products"

PRODUCTS = {
    "sm-series-servo-motor": {
        "dir": "2026311SM同步伺服电机",
        "photo": "同步伺服电机实拍图800.png",
        "front": "同步伺服电机正面图800.png",
        "side": "同步伺服电机侧面图800.png",
        "back": "同步伺服电机背面图800.png",
        "detail": "同步伺服电机细节图800.png",
    },
    "sd20-e-bus-servo-drive": {
        "dir": "2026311总线型伺服驱动系统SD20-E",
        "photo": "SD20-Es实拍图800.jpg",
        "front": "SD20-E正面图800.jpg",
        "side": "SD20-E侧面图800.jpg",
        "back": "SD20-E背面面图800.jpg",
        "detail": "SD20-E细节图800.jpg",
    },
    "sd20-g-servo-drive": {
        "dir": "2026311通用型伺服驱动系统SD20-G",
        "photo": "SD20-G实拍图800.jpg",
        "front": "SD20-G正面图800.jpg",
        "side": "SD20-G侧面图800.jpg",
        "back": "SD20-G背面面图800.jpg",
        "detail": "SD20-G细节图800.jpg",
    },
    "sde20-g-servo-drive": {
        "dir": "2026311高性能通用型伺服驱动系统SDE20-G",
        "photo": "SDE20-G实拍图800.jpg",
        "front": "SDE20-G正面图800.jpg",
        "side": "SDE20-G侧面图800.jpg",
        "back": "SDE20-G背面图800.jpg",
        "detail": "SDE20-G细节图800.jpg",
    },
    "sd20-d-dual-axis-servo-drive": {
        "dir": "双轴伺服驱动系统SD20-D",
        "photo": "SD20-D实拍图800.jpg",
        "front": "SD20-D正面图800.png",
        "side": "SD20-D侧面图800.jpg",
        "back": "SD20-D背面图800.jpg",
        "detail": "SD20-D详细图800.jpg",
    },
    "em30-integrated-inverter": {
        "dir": "电机驱动一体专用变频器EM30-IP67",
        "photo": "电机驱动一体专用变频器EM30-IP67实拍图.png",
        "front": "电机驱动一体专用变频器EM30-IP67正面图.png",
        "side": "电机驱动一体专用变频器EM30-IP67侧面图.png",
        "back": "电机驱动一体专用变频器EM30-IP67背面图.png",
        "detail": "电机驱动一体专用变频器EM30-IP67细节图.png",
    },
    "e800-vector-inverter": {
        "dir": "通用矢量变频器E800系列",
        "subdir": "通用矢量型变频器E800系列图",
        "photo": "通用矢量型变频器E800系列实拍图.png",
        "front": "通用矢量型变频器E800系列正面图.png",
        "side": "通用矢量型变频器E800系列侧面图.png",
        "back": "通用矢量型变频器E800系列背面图.png",
        "detail": "通用矢量型变频器E800系列细节图.png",
    },
    "ep66-inverter": {
        "dir": "高防护等级变频器EP66",
        "photo": "高防护等级变频器EP66-IP66实拍图.png",
        "front": "高防护等级变频器EP66-IP66正面图.png",
        "side": "高防护等级变频器EP66-IP66侧面图.png",
        "back": "高防护等级变频器EP66-IP66背面图.png",
        "detail": "高防护等级变频器EP66-IP66细节图.png",
    },
}

EXTRA = [
    (r"D:\FarFlight\Public\farflight_logo.png", r"D:\FarFlight\mechatronics\assets\images\logo.png"),
    (r"D:\FarFlight\Public\farflight_logo.png", r"D:\FarFlight\mechatronics\assets\images\favicon.png"),
    (r"D:\FarFlight\Public\PayInfo\Alipay\payee_justin.jpg", r"D:\FarFlight\mechatronics\assets\images\alipay-qr.jpg"),
]


def main():
    copied = 0
    for slug, spec in PRODUCTS.items():
        src_dir = os.path.join(SRC, spec["dir"])
        if spec.get("subdir"):
            src_dir = os.path.join(src_dir, spec["subdir"])
        dst_dir = os.path.join(DST, slug)
        os.makedirs(dst_dir, exist_ok=True)
        for key in ("photo", "front", "side", "back", "detail"):
            src_file = os.path.join(src_dir, spec[key])
            ext = os.path.splitext(spec[key])[1].lower()
            dst_file = os.path.join(dst_dir, key + ext)
            shutil.copy2(src_file, dst_file)
            copied += 1
        print("OK", slug, "->", dst_dir)
    for src_file, dst_file in EXTRA:
        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
        shutil.copy2(src_file, dst_file)
        copied += 1
        print("OK", src_file, "->", dst_file)
    print("TOTAL copied:", copied)


if __name__ == "__main__":
    main()
