#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FileRenameEditor - 文件重命名工具
支持前缀后缀和映射替换功能
"""

from models.file_manager import FileManager
from views.main_window import MainWindow
from controllers.rename_controller import RenameController


class FileRenameEditor:
    """文件重命名编辑器主应用程序"""
    
    def __init__(self):
        # 初始化模型
        self.file_manager = FileManager()
        
        # 初始化视图
        self.view = MainWindow(self)
        
        # 初始化控制器
        self.controller = RenameController(self.view, self.file_manager)
        
        # 将控制器绑定到视图
        self.view.controller = self.controller
    
    def preview_rename(self):
        """预览重命名"""
        self.controller.preview_rename()
    
    def execute_rename(self):
        """执行重命名"""
        self.controller.execute_rename()
    
    def run(self):
        """运行应用程序"""
        self.view.run()


def main():
    """主函数"""
    app = FileRenameEditor()
    app.run()


if __name__ == "__main__":
    main()
