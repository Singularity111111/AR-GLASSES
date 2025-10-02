from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np

class HUD:
    def __init__(self, font_path="msyh.ttc", font_size=32, max_messages=5):
        # 初始化字体
        self.font = ImageFont.truetype(font_path, font_size)
        # 初始化消息列表
        self.messages = ["Hello AR"]
        # 最大消息数
        self.max_messages = max_messages

    def add_message(self, message):
        # 添加新消息
        self.messages.append(message)
        # 超过最大消息数则删除最旧的
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)

    def draw_hud(self, frame):
        # 将 OpenCV 图像转换为 PIL Image
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)
        y = 50
        # 绘制所有消息
        for msg in self.messages:
            draw.text((50, y), msg, font=self.font, fill=(255, 255, 255))
            y += 40
        # 转回 OpenCV 图像并返回
        return cv2.cvtColor(np.asarray(pil_image), cv2.COLOR_RGB2BGR)


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    hud = HUD()
    while True:
        ret, frame = cap.read()
        if not ret:
            print("无法读取摄像头画面")
            break

        frame = hud.draw_hud(frame)
        cv2.imshow("frame", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):  # Q键退出
            break
        elif key == ord("s"):  # S键添加消息
            hud.add_message(f"消息 {len(hud.messages)+1}")

    cap.release()
    cv2.destroyAllWindows()
