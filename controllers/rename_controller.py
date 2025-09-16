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
    
    def preview_rename(self):
        """预览重命名"""
        path = self.view.get_current_path()
        prefix = self.view.get_prefix()
        suffix = self.view.get_suffix()
        mappings = self.view.get_mappings()
        
        if not path:
            self.view.update_status("错误：请先确认工作路径！\n")
            return
        
        if not prefix and not suffix and not mappings:
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
            
            if mappings:
                self.view.update_status(f"映射替换: {len(mappings)} 条规则\n")
            
            self.view.update_status(f"将重命名 {len(files)} 个文件\n\n")
            
            for file in files:
                # 应用映射替换
                mapped_name = self.apply_mappings(file, mappings)
                
                # 分离文件名和扩展名
                name, ext = os.path.splitext(mapped_name)
                new_name = prefix + name + suffix + ext
                
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
        mappings = self.view.get_mappings()
        
        if not path:
            self.view.update_status("错误：请先确认工作路径！\n")
            return
        
        if not prefix and not suffix and not mappings:
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
                
                # 分离文件名和扩展名
                name, ext = os.path.splitext(mapped_name)
                new_name = prefix + name + suffix + ext
                
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
