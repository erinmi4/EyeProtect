"""
配置文件
用户可以修改此文件来自定义护眼提醒器的设置
"""

# ===== 时间设置 =====
# 工作时间（分钟）- 默认 20 分钟
WORK_DURATION_MINUTES = 20

# 休息时间（秒）- 默认 20 秒
REST_DURATION_SECONDS = 20

# ===== 窗口设置 =====
# 提醒窗口宽度
WINDOW_WIDTH = 400

# 提醒窗口高度
WINDOW_HEIGHT = 300

# 窗口背景色
WINDOW_BACKGROUND = '#f0f8ff'

# ===== 文本设置 =====
# 主标题
MAIN_TITLE = "🌟 休息时间到了！"

# 提醒消息
REMINDER_MESSAGE = """请看向远处，让眼睛休息一下。

遵循 20-20-20 护眼法则：
看向 20 英尺（6米）外的物体"""

# ===== 颜色设置 =====
# 倒计时数字颜色（正常）
COUNTDOWN_COLOR_NORMAL = '#27ae60'

# 倒计时数字颜色（警告 - 10秒内）
COUNTDOWN_COLOR_WARNING = '#f39c12'

# 倒计时数字颜色（紧急 - 5秒内）
COUNTDOWN_COLOR_URGENT = '#e74c3c'

# ===== 字体设置 =====
# 主标题字体
TITLE_FONT = ('微软雅黑', 18, 'bold')

# 消息文本字体
MESSAGE_FONT = ('微软雅黑', 12)

# 倒计时数字字体
COUNTDOWN_FONT = ('Courier New', 24, 'bold')

# 普通文本字体
NORMAL_FONT = ('微软雅黑', 10)

# ===== 行为设置 =====
# 启动时是否自动开始计时
AUTO_START = True

# 是否显示剩余时间
SHOW_REMAINING_TIME = True

# 剩余时间更新间隔（秒）
TIME_UPDATE_INTERVAL = 1

# 是否允许延长休息时间
ALLOW_EXTEND_REST = True

# 延长休息的时间（秒）
EXTEND_TIME_SECONDS = 10

# 是否在休息结束时播放提示音（暂未实现）
PLAY_SOUND = False

# ===== 调试设置 =====
# 是否启用调试模式（会在控制台输出更多信息）
DEBUG_MODE = True

# 测试模式（将分钟改为秒，方便测试）
TEST_MODE = False

# 如果启用测试模式，工作时间（秒）
TEST_WORK_DURATION_SECONDS = 10

# 如果启用测试模式，休息时间（秒）
TEST_REST_DURATION_SECONDS = 5
