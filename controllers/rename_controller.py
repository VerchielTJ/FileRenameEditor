# -*- coding: utf-8 -*-
"""
重命名控制器 - 处理文件重命名的业务逻辑
"""

import os
from typing import List, Tuple
from models.file_manager import FileManager


class RenameController:
    """重命名控制器"""
    
    def __init__(self, view, file_manager: FileManager):
        self.view = view
        self.file_manager = file_manager
    
    def apply_mappings(self, filename: str, mappings: dict) -> str:
        """应用映射替换"""
        result = filename
        
        for key, value in mappings.items():
            if key in result:
                result = result.replace(key, value)
        
        return result
    
    def apply_delete_chars(self, filename: str, delete_chars: str) -> str:
        """应用删除字符 - 整段匹配删除"""
        if not delete_chars:
            return filename
        
        result = filename
        
        # 检查是否包含逗号分隔符
        if ',' in delete_chars:
            # 按逗号分割，支持多个删除模式
            delete_patterns = [pattern.strip() for pattern in delete_chars.split(',') if pattern.strip()]
        else:
            # 单个删除模式
            delete_patterns = [delete_chars]
        
        for pattern in delete_patterns:
            # 整段匹配删除
            result = result.replace(pattern, "")
        
        return result
    
    def apply_prefix_suffix(self, filename: str, prefix: str, suffix: str) -> str:
        """智能应用前缀和后缀 - 避免重复添加"""
        if not prefix and not suffix:
            return filename
        
        # 分离文件名和扩展名
        name, ext = os.path.splitext(filename)
        
        # 检查并添加前缀
        if prefix and not name.startswith(prefix):
            name = prefix + name
        
        # 检查并添加后缀
        if suffix and not name.endswith(suffix):
            name = name + suffix
        
        return name + ext
    
    def preview_rename(self):
        """预览重命名"""
        path = self.view.get_current_path()
        prefix = self.view.get_prefix()
        suffix = self.view.get_suffix()
        delete_chars = self.view.get_delete_chars()
        mappings = self.view.get_mappings()
        
        if not path:
            self.view.update_status("错误：请先确认工作路径！\n")
            return
        
        if not prefix and not suffix and not delete_chars and not mappings:
            self.view.update_status("错误：请至少设置一种重命名方式！\n")
            return
        
        try:
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            if not files:
                self.view.update_status("警告：该文件夹中没有文件！\n")
                return
            
            self.view.update_status(f"\n重命名预览:\n")
            self.view.update_status(f"前缀: '{prefix}'\n")
            self.view.update_status(f"后缀: '{suffix}'\n")
            self.view.update_status(f"删除字符: '{delete_chars}'\n")
            
            if mappings:
                self.view.update_status(f"映射替换: {len(mappings)} 条规则\n")
            
            self.view.update_status(f"将重命名 {len(files)} 个文件\n\n")
            
            for file in files:
                # 应用映射替换
                mapped_name = self.apply_mappings(file, mappings)
                
                # 应用删除字符
                deleted_name = self.apply_delete_chars(mapped_name, delete_chars)
                
                # 智能应用前缀和后缀
                new_name = self.apply_prefix_suffix(deleted_name, prefix, suffix)
                
                if file != new_name:
                    self.view.update_status(f"  {file} -> {new_name}\n")
                else:
                    self.view.update_status(f"  {file} (无变化)\n")
                    
        except Exception as e:
            self.view.update_status(f"预览失败: {e}\n")
    
    def execute_rename(self):
        """执行重命名"""
        path = self.view.get_current_path()
        prefix = self.view.get_prefix()
        suffix = self.view.get_suffix()
        delete_chars = self.view.get_delete_chars()
        mappings = self.view.get_mappings()
        
        if not path:
            self.view.update_status("错误：请先确认工作路径！\n")
            return
        
        if not prefix and not suffix and not delete_chars and not mappings:
            self.view.update_status("错误：请至少设置一种重命名方式！\n")
            return
        
        # 确认对话框
        from tkinter import messagebox
        if not messagebox.askyesno("确认", "确定要执行重命名操作吗？"):
            return
        
        try:
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            if not files:
                self.view.update_status("警告：该文件夹中没有文件！\n")
                return
            
            self.view.update_status(f"\n开始重命名操作...\n")
            
            renamed_count = 0
            for file in files:
                # 应用映射替换
                mapped_name = self.apply_mappings(file, mappings)
                
                # 应用删除字符
                deleted_name = self.apply_delete_chars(mapped_name, delete_chars)
                
                # 智能应用前缀和后缀
                new_name = self.apply_prefix_suffix(deleted_name, prefix, suffix)
                
                if file == new_name:
                    self.view.update_status(f"跳过: {file} (无变化)\n")
                    continue
                
                old_path = os.path.join(path, file)
                new_path = os.path.join(path, new_name)
                
                # 检查新文件名是否已存在
                if os.path.exists(new_path):
                    self.view.update_status(f"跳过: {file} -> {new_name} (文件已存在)\n")
                    continue
                
                try:
                    os.rename(old_path, new_path)
                    self.view.update_status(f"重命名: {file} -> {new_name}\n")
                    renamed_count += 1
                except Exception as e:
                    self.view.update_status(f"失败: {file} -> {new_name} (错误: {e})\n")
            
            self.view.update_status(f"\n重命名完成！成功重命名 {renamed_count} 个文件\n")
            
        except Exception as e:
            self.view.update_status(f"重命名操作失败: {e}\n")
