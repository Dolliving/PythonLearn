import pyautogui
import time
import keyboard
import threading
from datetime import datetime


class SimpleGiftDetector:
    def __init__(self):
        """
        初始化礼物检测器
        请提前准备好礼物截图，保存为png格式
        """
        # 礼物图片路径（请替换为你的实际图片路径）
        self.gift_images = {
            '1': 'img/抖音大啤酒.png',  # 对应num1
            '2': 'img/抖音小心心.png',  # 对应num2
            '3': 'img/抖音玫瑰.png',  # 对应num3
        }

        # 检测区域 (x, y, 宽度, 高度)
        # 这是直播伴侣显示礼物的区域，需要根据你的屏幕调整
        self.detect_region = (1566, 380, 325, 201)

        # 检测置信度 (0.0-1.0)，值越高越严格
        self.confidence = 0.7

        # 检测间隔（秒）
        self.check_interval = 0.3

        # 冷却时间（秒，防止重复触发）
        self.cooldown_time = 0.5

        # 运行状态
        self.is_running = False

        # 上次触发时间记录
        self.last_trigger = {'1': 0, '2': 0, '3': 0}

        print("=" * 50)
        print("直播礼物检测器 - 简化版")
        print("=" * 50)
        print("快捷键:")
        print("  F1 - 开始检测")
        print("  F2 - 停止检测")
        print("  F3 - 退出程序")
        print("  F4 - 测试按键 (手动测试按键是否正常)")
        print("=" * 50)

        # 显示当前设置
        print(f"检测区域: {self.detect_region}")
        print(f"检测间隔: {self.check_interval}秒")
        print(f"冷却时间: {self.cooldown_time}秒")
        print(f"置信度: {self.confidence}")
        print("=" * 50)

    def test_keypress(self):
        """测试按键功能"""
        print("\n[测试] 正在测试按键...")
        for key in ['1', '2', '3']:
            pyautogui.press(key)
            print(f"  按下按键: {key}")
            time.sleep(0.2)
        print("[测试] 按键测试完成")

    def check_single_gift(self, gift_key, image_path):
        """检查单个礼物是否出现"""
        try:
            # 检查冷却时间
            current_time = time.time()
            if current_time - self.last_trigger[gift_key] < self.cooldown_time:
                return False

            # 在屏幕上查找礼物图片
            location = pyautogui.locateOnScreen(
                image_path,
                confidence=self.confidence,
                region=self.detect_region,
                grayscale=True  # 使用灰度匹配，速度更快
            )

            if location:
                # 触发按键
                pyautogui.press(gift_key)

                # 更新触发时间
                self.last_trigger[gift_key] = current_time

                # 记录日志
                timestamp = datetime.now().strftime("%H:%M:%S")
                gift_name = {
                    '1': '大啤酒',
                    '2': '玫瑰1',
                    '3': '小心心'
                }.get(gift_key, gift_key)

                print(f"[{timestamp}] ✓ 检测到: {gift_name} -> 按键{gift_key}")

                return True

        except Exception as e:
            # 如果图片文件不存在或其他错误
            if "matchTemplate" in str(e) or "confidence" in str(e):
                # 这是正常的，当图片没找到时会出现
                pass
            else:
                print(f"[错误] 检测{gift_key}时出错: {str(e)[:50]}...")

        return False

    def detection_loop(self):
        """检测循环"""
        print("[状态] 开始礼物检测...")

        # 显示检测信息
        print(f"[信息] 正在检测区域: {self.detect_region}")
        print("[信息] 按F2停止检测\n")

        check_count = 0

        while self.is_running:
            try:
                # 检查每个礼物
                for gift_key, image_path in self.gift_images.items():
                    self.check_single_gift(gift_key, image_path)

                # 简单的进度提示
                check_count += 1
                if check_count % 50 == 0:  # 每检查50次显示一次
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"[{timestamp}] 持续检测中...")

                # 等待下次检测
                time.sleep(self.check_interval)

            except Exception as e:
                print(f"[错误] 检测循环出错: {e}")
                time.sleep(1)

        print("[状态] 检测已停止")

    def start_detection(self):
        """开始检测"""
        if not self.is_running:
            self.is_running = True
            # 在新线程中运行检测，避免阻塞主线程
            thread = threading.Thread(target=self.detection_loop)
            thread.daemon = True
            thread.start()
        else:
            print("[提示] 检测已经在运行中")

    def stop_detection(self):
        """停止检测"""
        if self.is_running:
            self.is_running = False
            print("[状态] 正在停止检测...")
        else:
            print("[提示] 检测未运行")

    def exit_program(self):
        """退出程序"""
        print("\n[状态] 正在退出程序...")
        self.stop_detection()
        time.sleep(0.5)  # 等待检测线程停止
        print("[状态] 程序已退出")
        exit(0)


def main():
    """主函数"""
    # 创建检测器实例
    detector = SimpleGiftDetector()

    # 设置快捷键
    keyboard.add_hotkey('f1', detector.start_detection)
    keyboard.add_hotkey('f2', detector.stop_detection)
    keyboard.add_hotkey('f3', detector.exit_program)
    keyboard.add_hotkey('f4', detector.test_keypress)

    print("[提示] 程序已就绪，等待指令...")
    print("[提示] 按F1开始检测，F3退出程序\n")

    try:
        # 保持程序运行
        keyboard.wait()
    except KeyboardInterrupt:
        detector.exit_program()


if __name__ == "__main__":
    # 安装所需库：pip install pyautogui keyboard pillow
    # 注意：第一次运行可能需要权限（特别是macOS）

    main()