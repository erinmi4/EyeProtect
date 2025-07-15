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


def get_resource_path(relative_path):
    """获取资源文件的绝对路径，支持PyInstaller打包后的路径"""
    try:
        # PyInstaller 创建临时文件夹，并将路径存储在 _MEIPASS 中
        base_path = sys._MEIPASS
    except AttributeError:
        # 如果没有_MEIPASS属性，说明是在开发环境中运行
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


class EyeRestReminder:
    def __init__(self):
        self.is_paused = False
        self.is_running = True
        self.work_timer = None
        self.tray_icon = None
        self.reminder_window = None
        self.update_timer = None
        self.work_start_time = None
        
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
        # 尝试加载外部图标文件
        try:
            icon_path = get_resource_path('icon.png')
            if os.path.exists(icon_path):
                # 如果找到图标文件，使用它
                image = Image.open(icon_path)
                # 调整尺寸为64x64
                image = image.resize((64, 64), Image.Resampling.LANCZOS)
                return image
        except Exception as e:
            if config.DEBUG_MODE:
                print(f"无法加载图标文件: {e}")
        
        # 如果没有找到图标文件，创建一个简单的眼睛图标
        image = Image.new('RGB', (64, 64), color='white')
        draw = ImageDraw.Draw(image)
        
        # 绘制眼睛外轮廓
        draw.ellipse([10, 20, 54, 44], fill='lightblue', outline='blue', width=2)
        
        # 绘制瞳孔
        draw.ellipse([28, 28, 36, 36], fill='black')
        
        # 绘制高光
        draw.ellipse([30, 30, 32, 32], fill='white')
        
        return image
    
    def get_remaining_time_text(self):
        """获取剩余时间的文本"""
        if self.is_paused:
            return "20-20-20 护眼提醒器 (已暂停)"
        
        if not self.work_start_time:
            return "20-20-20 护眼提醒器 (未启动)"
        
        # 计算已经过去的时间
        elapsed_time = time.time() - self.work_start_time
        remaining_time = self.work_duration - elapsed_time
        
        if remaining_time <= 0:
            return "20-20-20 护眼提醒器 (休息时间)"
        
        # 转换为分钟和秒
        remaining_minutes = int(remaining_time // 60)
        remaining_seconds = int(remaining_time % 60)
        
        if remaining_minutes > 0:
            return f"20-20-20 护眼提醒器 (还剩 {remaining_minutes}分{remaining_seconds:02d}秒)"
        else:
            return f"20-20-20 护眼提醒器 (还剩 {remaining_seconds}秒)"
    
    def update_tray_tooltip(self):
        """更新托盘图标的提示文本"""
        if self.tray_icon and config.SHOW_REMAINING_TIME:
            tooltip_text = self.get_remaining_time_text()
            self.tray_icon.title = tooltip_text
    
    def start_time_update_timer(self):
        """启动时间更新定时器"""
        if config.SHOW_REMAINING_TIME and self.is_running:
            self.update_tray_tooltip()
            
            # 同时更新菜单中的剩余时间显示
            if self.tray_icon:
                self.tray_icon.menu = self.create_tray_menu()
            
            # 设置下一次更新
            self.update_timer = threading.Timer(config.TIME_UPDATE_INTERVAL, self.start_time_update_timer)
            self.update_timer.start()
    
    def stop_time_update_timer(self):
        """停止时间更新定时器"""
        if self.update_timer:
            self.update_timer.cancel()
            self.update_timer = None

    def create_tray_menu(self):
        """创建托盘右键菜单"""
        menu_items = [
            pystray.MenuItem(
                "⏸ 暂停" if not self.is_paused else "▶ 继续",
                self.toggle_pause
            ),
            pystray.MenuItem("⏱ 立即休息", self.immediate_rest),
            pystray.MenuItem("", None),  # 分隔线
            pystray.MenuItem(
                f"⏰ {self.get_remaining_time_display()}", 
                None,  # 这是显示项，不可点击
                enabled=False
            ),
            pystray.MenuItem(
                "✓ 显示剩余时间" if config.SHOW_REMAINING_TIME else "显示剩余时间",
                self.toggle_time_display
            ),
            pystray.MenuItem("", None),  # 分隔线
            pystray.MenuItem("❌ 退出", self.quit_app)
        ]
        return pystray.Menu(*menu_items)
    
    def get_remaining_time_display(self):
        """获取用于菜单显示的剩余时间文本"""
        if self.is_paused:
            return "已暂停"
        
        if not self.work_start_time:
            return "未启动"
        
        # 计算已经过去的时间
        elapsed_time = time.time() - self.work_start_time
        remaining_time = self.work_duration - elapsed_time
        
        if remaining_time <= 0:
            return "休息时间"
        
        # 转换为分钟和秒
        remaining_minutes = int(remaining_time // 60)
        remaining_seconds = int(remaining_time % 60)
        
        if remaining_minutes > 0:
            return f"还剩 {remaining_minutes}分{remaining_seconds:02d}秒"
        else:
            return f"还剩 {remaining_seconds}秒"
    
    def toggle_time_display(self, icon, item):
        """切换剩余时间显示"""
        config.SHOW_REMAINING_TIME = not config.SHOW_REMAINING_TIME
        
        if config.SHOW_REMAINING_TIME:
            self.start_time_update_timer()
        else:
            self.stop_time_update_timer()
            # 恢复默认的托盘提示
            self.tray_icon.title = "20-20-20 护眼提醒器"
        
        # 更新托盘菜单
        icon.menu = self.create_tray_menu()
        
        if config.DEBUG_MODE:
            status = "启用" if config.SHOW_REMAINING_TIME else "禁用"
            print(f"剩余时间显示已{status}")
    
    def toggle_pause(self, icon, item):
        """暂停/继续功能"""
        self.is_paused = not self.is_paused
        
        if self.is_paused:
            # 暂停时取消当前计时器
            if self.work_timer:
                self.work_timer.cancel()
            self.stop_time_update_timer()
        else:
            # 继续时重新开始工作计时
            self.start_work_timer()
            if config.SHOW_REMAINING_TIME:
                self.start_time_update_timer()
        
        # 更新托盘菜单
        icon.menu = self.create_tray_menu()
        
        # 更新托盘提示文本
        self.update_tray_tooltip()
        
        status = "已暂停" if self.is_paused else "已继续"
        if config.DEBUG_MODE:
            print(f"护眼提醒器{status}")
    
    def immediate_rest(self, icon, item):
        """立即休息功能"""
        if not self.is_paused:
            # 取消当前工作计时器
            if self.work_timer:
                self.work_timer.cancel()
            
            # 停止时间更新
            self.stop_time_update_timer()
            
            # 立即显示休息窗口
            self.show_rest_reminder()
    
    def quit_app(self, icon, item):
        """退出应用"""
        self.is_running = False
        
        # 取消所有计时器
        if self.work_timer:
            self.work_timer.cancel()
        
        self.stop_time_update_timer()
        
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
        
        # 记录开始时间
        self.work_start_time = time.time()
        
        if config.DEBUG_MODE:
            print(f"开始工作计时：{self.work_duration // 60}分钟{self.work_duration % 60}秒")
        
        self.work_timer = threading.Timer(self.work_duration, self.show_rest_reminder)
        self.work_timer.start()
        
        # 启动时间更新定时器
        if config.SHOW_REMAINING_TIME:
            self.start_time_update_timer()
    
    def show_rest_reminder(self):
        """显示休息提醒窗口"""
        if not self.is_running:
            return
        
        # 停止时间更新定时器
        self.stop_time_update_timer()
        
        # 清除工作开始时间
        self.work_start_time = None
        
        # 更新托盘提示文本
        self.update_tray_tooltip()
        
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
                self.get_remaining_time_text(),  # 使用动态标题
                menu
            )
            
            # 启动第一个工作计时器（如果配置允许）
            if config.AUTO_START:
                self.start_work_timer()
            else:
                # 即使不自动启动，也要更新提示文本
                if config.SHOW_REMAINING_TIME:
                    self.start_time_update_timer()
            
            # 在单独线程中运行托盘图标
            tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
            tray_thread.start()
            
            print("20-20-20 护眼提醒器已启动")
            print("程序在系统托盘中运行，右键图标查看菜单")
            if config.SHOW_REMAINING_TIME:
                print("托盘图标会显示剩余时间")
            if config.TEST_MODE:
                print("⚠️ 当前运行在测试模式下")
            
            # 运行主循环
            self.root.mainloop()
            
        except Exception as e:
            print(f"程序运行出错: {e}")
        finally:
            # 确保清理资源
            self.stop_time_update_timer()
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
