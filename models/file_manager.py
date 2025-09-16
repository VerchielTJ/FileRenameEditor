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
            return [f for f in os.listdir(path) 
                   if os.path.isfile(os.path.join(path, f))]
        except Exception:
            return []
    
    def get_files(self) -> List[str]:
        """获取当前目录的文件列表"""
        return self.files.copy()
    
    def get_file_count(self) -> int:
        """获取文件数量"""
        return len(self.files)
    
    def refresh_files(self) -> bool:
        """刷新文件列表"""
        if not self.current_path:
            return False
        try:
            self.files = self._get_files_in_directory(self.current_path)
            return True
        except Exception:
            return False


class RenameOperations:
    """重命名操作类 - 处理各种重命名操作"""
    
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
        self.rename_history = []
    
    def add_prefix_suffix(self, prefix: str = "", suffix: str = "") -> List[Tuple[str, str, bool, str]]:
        """添加前缀和后缀重命名
        
        Returns:
            List of (old_name, new_name, success, error_message)
        """
        if not self.file_manager.current_path:
            return []
        
        results = []
        files = self.file_manager.get_files()
        
        for file in files:
            try:
                # 分离文件名和扩展名
                name, ext = os.path.splitext(file)
                new_name = prefix + name + suffix + ext
                
                old_path = os.path.join(self.file_manager.current_path, file)
                new_path = os.path.join(self.file_manager.current_path, new_name)
                
                # 检查新文件名是否已存在
                if os.path.exists(new_path):
                    results.append((file, new_name, False, "文件已存在"))
                    continue
                
                # 执行重命名
                os.rename(old_path, new_path)
                results.append((file, new_name, True, ""))
                
                # 记录到历史
                self.rename_history.append({
                    'operation': 'add_prefix_suffix',
                    'old_name': file,
                    'new_name': new_name,
                    'prefix': prefix,
                    'suffix': suffix
                })
                
            except Exception as e:
                results.append((file, new_name, False, str(e)))
        
        # 刷新文件列表
        self.file_manager.refresh_files()
        return results
    
    def preview_rename(self, prefix: str = "", suffix: str = "") -> List[Tuple[str, str]]:
        """预览重命名结果
        
        Returns:
            List of (old_name, new_name)
        """
        if not self.file_manager.current_path:
            return []
        
        preview = []
        files = self.file_manager.get_files()
        
        for file in files:
            name, ext = os.path.splitext(file)
            new_name = prefix + name + suffix + ext
            preview.append((file, new_name))
        
        return preview
    
    def get_rename_history(self) -> List[dict]:
        """获取重命名历史"""
        return self.rename_history.copy()
    
    def clear_history(self):
        """清空重命名历史"""
        self.rename_history.clear()
