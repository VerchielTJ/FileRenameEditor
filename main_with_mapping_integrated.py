#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FileRenameEditor - 集成映射组件的完整版本
支持文件名映射替换功能
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from typing import List, Tuple, Dict
from mapping_widget import MappingListWidget


# ==================== MODEL层 ====================
class FileManager:
    """文件管理器 - Model层"""
    
    def __init__(self):
        self.current_path = ""
        self.files = []
    
    def set_working_directory(self, path: str) -> bool:
        """设置工作目录"""
        try:
            if not os.path.exists(path) or not os.path.isdir(path):
                return False
            self.current_path = path
            self.files = [f for f in os.listdir(path) 
                         if os.path.isfile(os.path.join(path, f))]
            return True
        except Exception:
            return False
    
    def get_files(self) -> List[str]:
        return self.files.copy()
    
    def get_file_count(self) -> int:
        return len(self.files)


class RenameOperations:
    """重命名操作 - Model层"""
    
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
    
    def add_prefix_suffix(self, prefix: str = "", suffix: str = "") -> List[Tuple[str, str, bool, str]]:
        """添加前缀和后缀重命名"""
        if not self.file_manager.current_path:
            return []
        
        results = []
        for file in self.file_manager.files:
            try:
                name, ext = os.path.splitext(file)
                new_name = prefix + name + suffix + ext
                
                old_path = os.path.join(self.file_manager.current_path, file)
                new_path = os.path.join(self.file_manager.current_path, new_name)
                
                if os.path.exists(new_path):
                    results.append((file, new_name, False, "文件已存在"))
                    continue
                
                os.rename(old_path, new_path)
                results.append((file, new_name, True, ""))
                
            except Exception as e:
                results.append((file, new_name, False, str(e)))
        
        # 刷新文件列表
        self.file_manager.set_working_directory(self.file_manager.current_path)
        return results
    
    def apply_mapping_rename(self, mappings: Dict[str, str]) -> List[Tuple[str, str, bool, str]]:
        """应用映射重命名"""
        if not self.file_manager.current_path:
            return []
        
        results = []
        for file in self.file_manager.files:
            try:
                # 应用映射替换
                new_name = file
                for key, value in mappings.items():
                    if key in new_name:
                        new_name = new_name.replace(key, value)
                
                # 如果文件名没有变化，跳过
                if new_name == file:
                    results.append((file, new_name, False, "无需重命名"))
                    continue
                
                old_path = os.path.join(self.file_manager.current_path, file)
                new_path = os.path.join(self.file_manager.current_path, new_name)
                
                if os.path.exists(new_path):
                    results.append((file, new_name, False, "文件已存在"))
                    continue
                
                os.rename(old_path, new_path)
                results.append((file, new_name, True, ""))
                
            except Exception as e:
                results.append((file, new_name, False, str(e)))
        
        # 刷新文件列表
        self.file_manager.set_working_directory(self.file_manager.current_path)
        return results


# ==================== VIEW层 ====================
class MainWindow:
    """主窗口 - View层"""
    
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("文件重命名工具 - 映射版")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # 创建变量
        self.current_path = tk.StringVar()
        self.prefix = tk.StringVar()
        self.suffix = tk.StringVar()
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建主框架和滚动条
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 主框架
        main_frame = ttk.Frame(scrollable_frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 配置权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="文件重命名工具 - 映射版", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 路径选择区域
        self.create_path_section(main_frame)
        
        # 映射组件区域
        self.create_mapping_section(main_frame)
        
        # 传统重命名设置区域
        self.create_rename_section(main_frame)
        
        # 状态显示区域
        self.create_status_section(main_frame)
        
        # 打包滚动组件
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_path_section(self, parent):
        """创建路径选择区域"""
        path_frame = ttk.LabelFrame(parent, text="工作路径", padding="10")
        path_frame.pack(fill=tk.X, pady=(0, 10))
        
        path_input_frame = ttk.Frame(path_frame)
        path_input_frame.pack(fill=tk.X)
        path_input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(path_input_frame, text="当前路径:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.path_entry = ttk.Entry(path_input_frame, textvariable=self.current_path, 
                                   width=50, font=("Consolas", 10))
        self.path_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(path_input_frame, text="浏览...", 
                  command=self.controller.browse_folder).grid(row=0, column=2)
        
        ttk.Button(path_input_frame, text="确认路径", 
                  command=self.controller.confirm_path).grid(row=1, column=0, columnspan=3, pady=(10, 0))
    
    def create_mapping_section(self, parent):
        """创建映射组件区域"""
        mapping_frame = ttk.LabelFrame(parent, text="文件名映射替换", padding="10")
        mapping_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 创建映射组件
        self.mapping_widget = MappingListWidget(mapping_frame)
        
        # 映射操作按钮
        mapping_buttons = ttk.Frame(mapping_frame)
        mapping_buttons.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(mapping_buttons, text="预览映射重命名", 
                  command=self.controller.preview_mapping_rename).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(mapping_buttons, text="执行映射重命名", 
                  command=self.controller.execute_mapping_rename).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(mapping_buttons, text="测试映射", 
                  command=self.controller.test_mapping).pack(side=tk.LEFT)
    
    def create_rename_section(self, parent):
        """创建传统重命名设置区域"""
        rename_frame = ttk.LabelFrame(parent, text="传统重命名设置", padding="10")
        rename_frame.pack(fill=tk.X, pady=(0, 10))
        rename_frame.columnconfigure(1, weight=1)
        
        # 前缀
        ttk.Label(rename_frame, text="添加前缀:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.prefix_entry = ttk.Entry(rename_frame, textvariable=self.prefix, 
                                     width=30, font=("Consolas", 10))
        self.prefix_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # 后缀
        ttk.Label(rename_frame, text="添加后缀:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.suffix_entry = ttk.Entry(rename_frame, textvariable=self.suffix, 
                                     width=30, font=("Consolas", 10))
        self.suffix_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        
        # 按钮
        ttk.Button(rename_frame, text="预览重命名", 
                  command=self.controller.preview_rename).grid(row=2, column=0, pady=(15, 0))
        ttk.Button(rename_frame, text="执行重命名", 
                  command=self.controller.execute_rename).grid(row=2, column=1, pady=(15, 0))
    
    def create_status_section(self, parent):
        """创建状态显示区域"""
        status_frame = ttk.LabelFrame(parent, text="状态信息", padding="10")
        status_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)
        
        self.status_text = tk.Text(status_frame, height=10, wrap=tk.WORD, font=("Consolas", 9))
        scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    
    def update_status(self, message: str):
        """更新状态信息"""
        self.status_text.insert(tk.END, message)
        self.status_text.see(tk.END)
        self.root.update_idletasks()
    
    def get_path(self) -> str:
        return self.current_path.get().strip()
    
    def set_path(self, path: str):
        self.current_path.set(path)
    
    def get_prefix(self) -> str:
        return self.prefix.get().strip()
    
    def get_suffix(self) -> str:
        return self.suffix.get().strip()
    
    def get_mappings(self) -> Dict[str, str]:
        """获取映射字典"""
        return self.mapping_widget.get_mappings()
    
    def run(self):
        self.root.mainloop()


# ==================== CONTROLLER层 ====================
class MainController:
    """主控制器 - Controller层"""
    
    def __init__(self):
        # 创建Model层实例
        self.file_manager = FileManager()
        self.rename_operations = RenameOperations(self.file_manager)
        
        # 创建View层实例
        self.view = MainWindow(self)
        
        # 初始化
        self.view.set_path(os.getcwd())
        self.view.update_status("欢迎使用文件重命名工具！(映射版)\n")
        self.view.update_status(f"当前工作路径: {os.getcwd()}\n")
        self.view.update_status("提示：您可以使用映射功能来批量替换文件名中的特定文本\n")
    
    def browse_folder(self):
        """浏览文件夹"""
        folder_path = filedialog.askdirectory(
            title="选择工作文件夹",
            initialdir=self.view.get_path()
        )
        if folder_path:
            self.view.set_path(folder_path)
            self.view.update_status(f"已选择路径: {folder_path}\n")
    
    def confirm_path(self):
        """确认路径"""
        path = self.view.get_path()
        
        if not path:
            messagebox.showerror("错误", "请输入有效路径！")
            return
        
        if self.file_manager.set_working_directory(path):
            self.view.update_status(f"路径确认成功！\n")
            self.view.update_status(f"文件夹: {path}\n")
            self.view.update_status(f"包含 {self.file_manager.get_file_count()} 个文件\n")
            
            files = self.file_manager.get_files()
            if files:
                self.view.update_status("文件列表:\n")
                for i, file in enumerate(files[:10], 1):
                    self.view.update_status(f"  {i}. {file}\n")
                if len(files) > 10:
                    self.view.update_status(f"  ... 还有 {len(files) - 10} 个文件\n")
            else:
                self.view.update_status("该文件夹为空\n")
        else:
            messagebox.showerror("错误", f"无法访问路径: {path}")
    
    def test_mapping(self):
        """测试映射功能"""
        mappings = self.view.get_mappings()
        if not mappings:
            messagebox.showwarning("警告", "请先添加一些映射规则！")
            return
        
        # 创建测试对话框
        dialog = tk.Toplevel(self.view.root)
        dialog.title("测试映射")
        dialog.geometry("500x300")
        dialog.resizable(False, False)
        dialog.transient(self.view.root)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="输入测试文件名:").pack(anchor=tk.W, pady=(0, 10))
        
        test_entry = ttk.Entry(frame, width=50, font=("Consolas", 10))
        test_entry.pack(fill=tk.X, pady=(0, 10))
        test_entry.insert(0, "IMG_20231201_143022.jpg")
        
        result_label = ttk.Label(frame, text="", font=("Consolas", 10), foreground="blue")
        result_label.pack(anchor=tk.W, pady=(10, 0))
        
        def apply_test():
            filename = test_entry.get().strip()
            if not filename:
                return
            
            result = filename
            for key, value in mappings.items():
                if key in result:
                    result = result.replace(key, value)
            
            result_label.config(text=f"结果: {result}")
        
        ttk.Button(frame, text="应用映射", command=apply_test).pack(pady=(10, 0))
        ttk.Button(frame, text="关闭", command=dialog.destroy).pack(pady=(10, 0))
        
        test_entry.focus()
    
    def preview_mapping_rename(self):
        """预览映射重命名"""
        mappings = self.view.get_mappings()
        if not mappings:
            messagebox.showwarning("警告", "请先添加映射规则！")
            return
        
        if not self.file_manager.current_path:
            messagebox.showerror("错误", "请先确认工作路径！")
            return
        
        self.view.update_status(f"\n映射重命名预览:\n")
        self.view.update_status(f"映射规则: {len(mappings)} 个\n")
        
        files = self.file_manager.get_files()
        for file in files:
            new_name = file
            for key, value in mappings.items():
                if key in new_name:
                    new_name = new_name.replace(key, value)
            
            if new_name != file:
                self.view.update_status(f"  {file} -> {new_name}\n")
            else:
                self.view.update_status(f"  {file} (无需重命名)\n")
    
    def execute_mapping_rename(self):
        """执行映射重命名"""
        mappings = self.view.get_mappings()
        if not mappings:
            messagebox.showwarning("警告", "请先添加映射规则！")
            return
        
        if not self.file_manager.current_path:
            messagebox.showerror("错误", "请先确认工作路径！")
            return
        
        # 确认对话框
        if not messagebox.askyesno("确认", f"确定要应用 {len(mappings)} 个映射规则进行重命名吗？"):
            return
        
        self.view.update_status(f"\n开始映射重命名操作...\n")
        
        results = self.rename_operations.apply_mapping_rename(mappings)
        
        success_count = 0
        for old_name, new_name, success, error in results:
            if success:
                self.view.update_status(f"✓ {old_name} -> {new_name}\n")
                success_count += 1
            else:
                self.view.update_status(f"✗ {old_name} -> {new_name} ({error})\n")
        
        self.view.update_status(f"\n映射重命名完成！成功重命名 {success_count} 个文件\n")
    
    def preview_rename(self):
        """预览传统重命名"""
        prefix = self.view.get_prefix()
        suffix = self.view.get_suffix()
        
        if not prefix and not suffix:
            messagebox.showerror("错误", "请至少输入前缀或后缀！")
            return
        
        if not self.file_manager.current_path:
            messagebox.showerror("错误", "请先确认工作路径！")
            return
        
        self.view.update_status(f"\n传统重命名预览:\n")
        self.view.update_status(f"前缀: '{prefix}'\n")
        self.view.update_status(f"后缀: '{suffix}'\n\n")
        
        files = self.file_manager.get_files()
        for file in files:
            name, ext = os.path.splitext(file)
            new_name = prefix + name + suffix + ext
            self.view.update_status(f"  {file} -> {new_name}\n")
    
    def execute_rename(self):
        """执行传统重命名"""
        prefix = self.view.get_prefix()
        suffix = self.view.get_suffix()
        
        if not prefix and not suffix:
            messagebox.showerror("错误", "请至少输入前缀或后缀！")
            return
        
        if not self.file_manager.current_path:
            messagebox.showerror("错误", "请先确认工作路径！")
            return
        
        # 确认对话框
        if not messagebox.askyesno("确认", "确定要执行重命名操作吗？"):
            return
        
        self.view.update_status(f"\n开始传统重命名操作...\n")
        
        results = self.rename_operations.add_prefix_suffix(prefix, suffix)
        
        success_count = 0
        for old_name, new_name, success, error in results:
            if success:
                self.view.update_status(f"✓ {old_name} -> {new_name}\n")
                success_count += 1
            else:
                self.view.update_status(f"✗ {old_name} -> {new_name} ({error})\n")
        
        self.view.update_status(f"\n传统重命名完成！成功重命名 {success_count} 个文件\n")
    
    def run(self):
        """运行应用程序"""
        self.view.run()


# ==================== 程序入口 ====================
def main():
    """主函数"""
    app = MainController()
    app.run()


if __name__ == "__main__":
    main()
