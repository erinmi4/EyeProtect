"""
20-20-20 护眼提醒器启动脚本
自动检查并安装依赖，然后启动程序
"""
import subprocess
import sys
import os


def install_requirements():
    """安装所需依赖包"""
    print("正在检查并安装依赖包...")
    
    try:
        # 获取当前脚本目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        requirements_file = os.path.join(current_dir, "requirements.txt")
        
        # 安装依赖
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", requirements_file
        ])
        print("依赖包安装完成！")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"依赖包安装失败: {e}")
        return False
    except FileNotFoundError:
        print("未找到 requirements.txt 文件")
        return False


def check_dependencies():
    """检查依赖是否已安装"""
    required_packages = ['pystray', 'PIL']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                __import__('PIL')
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages


def create_icons():
    """创建图标文件"""
    try:
        from create_icon import create_all_icons
        print("正在创建图标文件...")
        create_all_icons()
        print("图标文件创建完成！")
    except Exception as e:
        print(f"创建图标时出错: {e}")


def main():
    """主启动函数"""
    print("=" * 50)
    print("    20-20-20 护眼提醒器 启动程序")
    print("=" * 50)
    
    # 检查依赖
    missing = check_dependencies()
    if missing:
        print(f"缺少依赖包: {', '.join(missing)}")
        print("正在自动安装...")
        
        if not install_requirements():
            print("依赖安装失败，程序无法启动")
            input("按回车键退出...")
            return
    
    # 创建图标
    create_icons()
    
    # 启动主程序
    try:
        print("\n正在启动护眼提醒器...")
        print("程序将在系统托盘中运行")
        print("右键托盘图标可以控制程序")
        print("\n提示：您可以关闭此窗口，程序将继续在后台运行")
        print("-" * 50)
        
        from main import main as run_main
        run_main()
        
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
        input("按回车键退出...")


if __name__ == "__main__":
    main()
