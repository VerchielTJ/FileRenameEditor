# -*- coding: utf-8 -*-
"""
FileRenameEditor - Model层
文件操作和重命名业务逻辑
"""

import os
from pathlib import Path
from typing import List, Tuple, Optional


class FileManager:
    """文件管理器 - 处理文件操作"""
    
    def __init__(self):
        self.current_path = ""
        self.files = []
    
    def set_working_directory(self, path: str) -> bool:
        """设置工作目录"""
        try:
            if not os.path.exists(path):
                return False
            if not os.path.isdir(path):
                return False
            
            self.current_path = path
            self.files = self._get_files_in_directory(path)
            return True
        except Exception:
            return False
    
    def _get_files_in_directory(self, path: str) -> List[str]:
        """获取目录中的文件列表"""
        try:
            files = []
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isfile(item_path):
                    files.append(item)
            return files
        except Exception:
            return []
    
    def get_files(self) -> List[str]:
        """获取文件列表"""
        return self.files.copy()
    
    def get_file_count(self) -> int:
        """获取文件数量"""
        return len(self.files)
    
    def get_current_path(self) -> str:
        """获取当前路径"""
        return self.current_path
    
    def rename_file(self, old_name: str, new_name: str) -> Tuple[bool, str]:
        """重命名文件"""
        try:
            if not self.current_path:
                return False, "未设置工作目录"
            
            old_path = os.path.join(self.current_path, old_name)
            new_path = os.path.join(self.current_path, new_name)
            
            if not os.path.exists(old_path):
                return False, f"源文件不存在: {old_name}"
            
            if os.path.exists(new_path):
                return False, f"目标文件已存在: {new_name}"
            
            os.rename(old_path, new_path)
            return True, "重命名成功"
            
        except Exception as e:
            return False, f"重命名失败: {str(e)}"
    
    def refresh_files(self) -> bool:
        """刷新文件列表"""
        if not self.current_path:
            return False
        
        try:
            self.files = self._get_files_in_directory(self.current_path)
            return True
        except Exception:
            return False
