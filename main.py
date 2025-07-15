"""
20-20-20 护眼提醒器主程序
遵循20-20-20护眼法则：每20分钟看向20英尺外的物体20秒钟
"""
import tkinter as tk
from PIL import Image, ImageDraw
import pystray
import threading
import time
import os
import sys
from reminder_window import ReminderWindow
import config


class EyeRestReminder:
    def __init__(self):
        self.is_paused = False
        self.is_running = True
        self.work_timer = None
        self.tray_icon = None
        self.reminder_window = None
        
        # 从配置文件加载时间设置
        if config.TEST_MODE:
            self.work_duration = config.TEST_WORK_DURATION_SECONDS
            self.rest_duration = config.TEST_REST_DURATION_SECONDS
            if config.DEBUG_MODE:
                print("测试模式已启用")
        else:
            self.work_duration = config.WORK_DURATION_MINUTES * 60  # 转换为秒
            self.rest_duration = config.REST_DURATION_SECONDS
        
        if config.DEBUG_MODE:
            print(f"工作时间: {self.work_duration}秒, 休息时间: {self.rest_duration}秒")
        
        # 创建隐藏的主窗口
        self.root = tk.Tk()
        self.root.withdraw()  # 隐藏主窗口
        
    def create_icon(self):
        """创建托盘图标"""
        # 创建一个简单的眼睛图标
        image = Image.new('RGB', (64, 64), color='white')
        draw = ImageDraw.Draw(image)
        
        # 绘制眼睛外轮廓
        draw.ellipse([10, 20, 54, 44], fill='lightblue', outline='blue', width=2)
        
        # 绘制瞳孔
        draw.ellipse([28, 28, 36, 36], fill='black')
        
        # 绘制高光
        draw.ellipse([30, 30, 32, 32], fill='white')
        
        return image
    
    def create_tray_menu(self):
        """创建托盘右键菜单"""
        menu_items = [
            pystray.MenuItem(
                "⏸ 暂停" if not self.is_paused else "▶ 继续",
                self.toggle_pause
            ),
            pystray.MenuItem("⏱ 立即休息", self.immediate_rest),
            pystray.MenuItem("❌ 退出", self.quit_app)
        ]
        return pystray.Menu(*menu_items)
    
    def toggle_pause(self, icon, item):
        """暂停/继续功能"""
        self.is_paused = not self.is_paused
        
        if self.is_paused:
            # 暂停时取消当前计时器
            if self.work_timer:
                self.work_timer.cancel()
        else:
            # 继续时重新开始工作计时
            self.start_work_timer()
        
        # 更新托盘菜单
        icon.menu = self.create_tray_menu()
        
        status = "已暂停" if self.is_paused else "已继续"
        if config.DEBUG_MODE:
            print(f"护眼提醒器{status}")
    
    def immediate_rest(self, icon, item):
        """立即休息功能"""
        if not self.is_paused:
            # 取消当前工作计时器
            if self.work_timer:
                self.work_timer.cancel()
            
            # 立即显示休息窗口
            self.show_rest_reminder()
    
    def quit_app(self, icon, item):
        """退出应用"""
        self.is_running = False
        
        # 取消所有计时器
        if self.work_timer:
            self.work_timer.cancel()
        
        # 关闭提醒窗口
        if self.reminder_window:
            self.reminder_window.close()
        
        # 停止托盘图标
        icon.stop()
        
        # 退出主循环
        self.root.quit()
        
        if config.DEBUG_MODE:
            print("护眼提醒器已退出")
    
    def start_work_timer(self):
        """开始工作计时器（20分钟）"""
        if not self.is_running or self.is_paused:
            return
        
        if config.DEBUG_MODE:
            print(f"开始工作计时：{self.work_duration // 60}分钟{self.work_duration % 60}秒")
        
        self.work_timer = threading.Timer(self.work_duration, self.show_rest_reminder)
        self.work_timer.start()
    
    def show_rest_reminder(self):
        """显示休息提醒窗口"""
        if not self.is_running:
            return
        
        if config.DEBUG_MODE:
            print("显示休息提醒窗口")
        
        # 在主线程中创建窗口
        self.root.after(0, self._create_reminder_window)
    
    def _create_reminder_window(self):
        """在主线程中创建提醒窗口"""
        self.reminder_window = ReminderWindow(
            self.root, 
            self.rest_duration,
            self._on_rest_complete
        )
    
    def _on_rest_complete(self):
        """休息完成后的回调"""
        self.reminder_window = None
        
        if self.is_running and not self.is_paused:
            # 休息结束，开始下一个工作循环
            if config.DEBUG_MODE:
                print("休息结束，开始下一个工作周期")
            self.start_work_timer()
    
    def run(self):
        """运行主程序"""
        try:
            # 创建托盘图标
            icon_image = self.create_icon()
            menu = self.create_tray_menu()
            
            # 创建托盘图标
            self.tray_icon = pystray.Icon(
                "eye_rest_reminder",
                icon_image,
                "20-20-20 护眼提醒器",
                menu
            )
            
            # 启动第一个工作计时器（如果配置允许）
            if config.AUTO_START:
                self.start_work_timer()
            
            # 在单独线程中运行托盘图标
            tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
            tray_thread.start()
            
            print("20-20-20 护眼提醒器已启动")
            print("程序在系统托盘中运行，右键图标查看菜单")
            if config.TEST_MODE:
                print("⚠️ 当前运行在测试模式下")
            
            # 运行主循环
            self.root.mainloop()
            
        except Exception as e:
            print(f"程序运行出错: {e}")
        finally:
            # 确保清理资源
            if self.tray_icon:
                self.tray_icon.stop()


def main():
    """主函数"""
    # 检查依赖包
    try:
        import pystray
        from PIL import Image, ImageDraw
    except ImportError as e:
        print(f"缺少依赖包: {e}")
        print("请运行: pip install pystray pillow")
        return
    
    # 创建并运行应用
    app = EyeRestReminder()
    app.run()


if __name__ == "__main__":
    main()
