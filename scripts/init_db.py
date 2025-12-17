"""
数据库初始化脚本
"""
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.db.session import init_db
from app.models import Item  # 导入所有模型以确保它们被注册


def main():
    """主函数"""
    print("🔧 开始初始化数据库...")
    try:
        init_db()
        print("✅ 数据库初始化完成！")
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
