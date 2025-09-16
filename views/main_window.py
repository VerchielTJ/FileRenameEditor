# -*- coding: utf-8 -*-
"""
主窗口视图 - 文件重命名工具的主界面
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from typing import Dict
from .components.mapping_widget import MappingListWidget


class MainWindow:
    """主窗口类"""
    
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("文件重命名工具 - 支持映射替换")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 当前工作路径
        self.current_path = tk.StringVar()
        self.current_path.set(os.getcwd())
        
        # 前缀和后缀
        self.prefix = tk.StringVar()
        self.suffix = tk.StringVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="文件重命名工具", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 路径选择区域
        self.create_path_section(main_frame, 1)
        
        # 重命名设置区域
        self.create_rename_section(main_frame, 2)
        
        # 状态显示区域
        self.create_status_section(main_frame, 3)
        
        # 初始状态信息
        self.update_status("欢迎使用文件重命名工具！\n")
        self.update_status(f"当前工作路径: {self.current_path.get()}\n")
    
    def create_path_section(self, parent, row):
        """创建路径选择区域"""
        path_frame = ttk.LabelFrame(parent, text="工作路径", padding="10")
        path_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        path_frame.columnconfigure(1, weight=1)
        
        # 路径标签
        path_label = ttk.Label(path_frame, text="当前路径:")
        path_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        # 路径输入框
        self.path_entry = ttk.Entry(path_frame, textvariable=self.current_path, 
                                   width=50, font=("Consolas", 10))
        self.path_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # 浏览按钮
        browse_btn = ttk.Button(path_frame, text="浏览...", 
                               command=self.browse_folder)
        browse_btn.grid(row=0, column=2)
        
        # 确认路径按钮
        confirm_btn = ttk.Button(path_frame, text="确认路径", 
                                command=self.confirm_path)
        confirm_btn.grid(row=1, column=0, columnspan=3, pady=(10, 0))
    
    def create_rename_section(self, parent, row):
        """创建重命名设置区域"""
        rename_frame = ttk.LabelFrame(parent, text="重命名设置", padding="10")
        rename_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        rename_frame.columnconfigure(1, weight=1)
        
        # 前缀设置
        prefix_label = ttk.Label(rename_frame, text="添加前缀:")
        prefix_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.prefix_entry = ttk.Entry(rename_frame, textvariable=self.prefix, 
                                     width=30, font=("Consolas", 10))
        self.prefix_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # 后缀设置
        suffix_label = ttk.Label(rename_frame, text="添加后缀:")
        suffix_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        
        self.suffix_entry = ttk.Entry(rename_frame, textvariable=self.suffix, 
                                     width=30, font=("Consolas", 10))
        self.suffix_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        
        # 映射列表组件
        self.mapping_widget = MappingListWidget(rename_frame)
        
        # 重命名按钮
        button_frame = ttk.Frame(rename_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(15, 0))
        
        ttk.Button(button_frame, text="预览重命名", 
                  command=self.preview_rename).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="执行重命名", 
                  command=self.execute_rename).pack(side=tk.LEFT)
    
    def create_status_section(self, parent, row):
        """创建状态显示区域"""
        status_frame = ttk.LabelFrame(parent, text="状态信息", padding="10")
        status_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), 
                         pady=(10, 0))
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)
        
        # 状态文本框
        self.status_text = tk.Text(status_frame, height=8, wrap=tk.WORD, 
                                  font=("Consolas", 9))
        scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, 
                                 command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    
    def browse_folder(self):
        """浏览文件夹"""
        folder_path = filedialog.askdirectory(
            title="选择工作文件夹",
            initialdir=self.current_path.get()
        )
        if folder_path:
            self.current_path.set(folder_path)
            self.update_status(f"已选择路径: {folder_path}\n")
            
    def confirm_path(self):
        """确认路径"""
        path = self.current_path.get().strip()
        
        if not path:
            messagebox.showerror("错误", "请输入有效路径！")
            return
            
        # 检查路径是否存在
        if not os.path.exists(path):
            messagebox.showerror("错误", f"路径不存在: {path}")
            return
            
        if not os.path.isdir(path):
            messagebox.showerror("错误", f"请选择文件夹路径: {path}")
            return
            
        # 获取文件夹中的文件信息
        try:
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            self.update_status(f"路径确认成功！\n")
            self.update_status(f"文件夹: {path}\n")
            self.update_status(f"包含 {len(files)} 个文件\n")
            
            if files:
                self.update_status("文件列表:\n")
                for i, file in enumerate(files[:10], 1):  # 只显示前10个文件
                    self.update_status(f"  {i}. {file}\n")
                if len(files) > 10:
                    self.update_status(f"  ... 还有 {len(files) - 10} 个文件\n")
            else:
                self.update_status("该文件夹为空\n")
                
        except Exception as e:
            messagebox.showerror("错误", f"无法访问路径: {e}")
    
    def preview_rename(self):
        """预览重命名"""
        self.controller.preview_rename()
    
    def execute_rename(self):
        """执行重命名"""
        self.controller.execute_rename()
    
    def update_status(self, message):
        """更新状态信息"""
        self.status_text.insert(tk.END, message)
        self.status_text.see(tk.END)
        self.root.update_idletasks()
    
    def get_current_path(self) -> str:
        """获取当前路径"""
        return self.current_path.get().strip()
    
    def get_prefix(self) -> str:
        """获取前缀"""
        return self.prefix.get().strip()
    
    def get_suffix(self) -> str:
        """获取后缀"""
        return self.suffix.get().strip()
    
    def get_mappings(self) -> Dict[str, str]:
        """获取映射字典"""
        return self.mapping_widget.get_mappings()
    
    def run(self):
        """运行应用程序"""
        self.root.mainloop()
