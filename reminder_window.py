"""
休息提醒窗口模块
显示20秒倒计时的置顶窗口
"""
import tkinter as tk
from tkinter import ttk
import threading
import config


class ReminderWindow:
    def __init__(self, parent, duration, callback):
        """
        初始化提醒窗口
        
        Args:
            parent: 父窗口
            duration: 倒计时时长（秒）
            callback: 倒计时结束后的回调函数
        """
        self.parent = parent
        self.duration = duration
        self.callback = callback
        self.remaining_time = duration
        self.is_closed = False
        
        # 创建顶级窗口
        self.window = tk.Toplevel(parent)
        self.setup_window()
        self.create_widgets()
        self.start_countdown()
    
    def setup_window(self):
        """设置窗口属性"""
        # 窗口标题
        self.window.title("休息一下")
        
        # 窗口大小
        window_width = config.WINDOW_WIDTH
        window_height = config.WINDOW_HEIGHT
        
        # 获取屏幕尺寸
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # 计算居中位置
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # 设置窗口位置和大小
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 设置窗口属性
        self.window.attributes('-topmost', True)  # 置顶显示
        self.window.resizable(False, False)       # 禁止调整大小
        self.window.focus_force()                 # 强制获取焦点
        
        # 绑定关闭事件
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        
        # 设置窗口样式
        self.window.configure(bg=config.WINDOW_BACKGROUND)
    
    def create_widgets(self):
        """创建窗口组件"""
        # 主框架
        main_frame = tk.Frame(self.window, bg=config.WINDOW_BACKGROUND)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # 标题标签
        title_label = tk.Label(
            main_frame,
            text=config.MAIN_TITLE,
            font=config.TITLE_FONT,
            fg='#2c3e50',
            bg=config.WINDOW_BACKGROUND
        )
        title_label.pack(pady=(0, 20))
        
        # 提醒文本
        message_label = tk.Label(
            main_frame,
            text=config.REMINDER_MESSAGE,
            font=config.MESSAGE_FONT,
            fg='#34495e',
            bg=config.WINDOW_BACKGROUND,
            justify='center'
        )
        message_label.pack(pady=(0, 30))
        
        # 倒计时显示框架
        countdown_frame = tk.Frame(main_frame, bg=config.WINDOW_BACKGROUND)
        countdown_frame.pack(pady=(0, 20))
        
        # 倒计时标签
        countdown_text_label = tk.Label(
            countdown_frame,
            text="剩余时间：",
            font=config.MESSAGE_FONT,
            fg='#7f8c8d',
            bg=config.WINDOW_BACKGROUND
        )
        countdown_text_label.pack(side='left')
        
        # 倒计时数字
        self.countdown_label = tk.Label(
            countdown_frame,
            text=str(self.remaining_time),
            font=config.COUNTDOWN_FONT,
            fg=config.COUNTDOWN_COLOR_NORMAL,
            bg=config.WINDOW_BACKGROUND
        )
        self.countdown_label.pack(side='left', padx=(10, 0))
        
        # 秒单位标签
        seconds_label = tk.Label(
            countdown_frame,
            text="秒",
            font=config.MESSAGE_FONT,
            fg='#7f8c8d',
            bg=config.WINDOW_BACKGROUND
        )
        seconds_label.pack(side='left', padx=(5, 0))
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=self.duration,
            length=300,
            mode='determinate',
            style='TProgressbar'
        )
        self.progress_bar.pack(pady=(20, 20))
        
        # 按钮框架
        button_frame = tk.Frame(main_frame, bg=config.WINDOW_BACKGROUND)
        button_frame.pack()
        
        # 跳过按钮
        skip_button = tk.Button(
            button_frame,
            text="跳过休息",
            command=self.close,
            font=config.NORMAL_FONT,
            bg='#95a5a6',
            fg='white',
            relief='flat',
            padx=20,
            pady=5,
            cursor='hand2'
        )
        skip_button.pack(side='left', padx=(0, 10))
        
        # 延长休息按钮（如果配置允许）
        if config.ALLOW_EXTEND_REST:
            extend_button = tk.Button(
                button_frame,
                text=f"延长{config.EXTEND_TIME_SECONDS}秒",
                command=self.extend_time,
                font=config.NORMAL_FONT,
                bg='#3498db',
                fg='white',
                relief='flat',
                padx=20,
                pady=5,
                cursor='hand2'
            )
            extend_button.pack(side='left')
        
        # 设置初始进度
        self.progress_var.set(0)
    
    def start_countdown(self):
        """开始倒计时"""
        self.update_countdown()
    
    def update_countdown(self):
        """更新倒计时显示"""
        if self.is_closed:
            return
        
        if self.remaining_time > 0:
            # 更新倒计时显示
            self.countdown_label.config(text=str(self.remaining_time))
            
            # 更新进度条
            progress_value = self.duration - self.remaining_time
            self.progress_var.set(progress_value)
            
            # 改变倒计时数字颜色（根据配置）
            if self.remaining_time <= 5:
                self.countdown_label.config(fg=config.COUNTDOWN_COLOR_URGENT)
            elif self.remaining_time <= 10:
                self.countdown_label.config(fg=config.COUNTDOWN_COLOR_WARNING)
            else:
                self.countdown_label.config(fg=config.COUNTDOWN_COLOR_NORMAL)
            
            # 递减时间
            self.remaining_time -= 1
            
            # 设置下一次更新（1秒后）
            self.window.after(1000, self.update_countdown)
        else:
            # 倒计时结束，自动关闭窗口
            self.close()
    
    def extend_time(self):
        """延长休息时间"""
        extend_seconds = config.EXTEND_TIME_SECONDS
        self.remaining_time += extend_seconds
        self.duration += extend_seconds
        self.progress_bar.config(maximum=self.duration)
        if config.DEBUG_MODE:
            print(f"休息时间延长{extend_seconds}秒")
    
    def close(self):
        """关闭窗口"""
        if self.is_closed:
            return
        
        self.is_closed = True
        
        try:
            self.window.destroy()
        except:
            pass
        
        # 调用回调函数
        if self.callback:
            # 在新线程中调用回调，避免阻塞
            threading.Thread(target=self.callback, daemon=True).start()
        
        if config.DEBUG_MODE:
            print("休息窗口已关闭")


# 测试代码
if __name__ == "__main__":
    def test_callback():
        print("休息完成回调被调用")
    
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    # 创建测试窗口
    reminder = ReminderWindow(root, 10, test_callback)  # 10秒测试
    
    root.mainloop()
