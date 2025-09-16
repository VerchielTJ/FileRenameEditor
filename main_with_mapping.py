#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FileRenameEditor - 集成映射替换功能
主程序入口
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from mapping_widget import MappingListWidget


class FileRenameEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("文件重命名工具 - 支持映射替换")
        self.root.geometry("900x700")
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
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="文件重命名工具", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # 路径选择区域
        self.create_path_section(main_frame, 1)
        
        # 映射替换区域
        self.create_mapping_section(main_frame, 2)
        
        # 重命名设置区域
        self.create_rename_section(main_frame, 3)
        
        # 状态显示区域
        self.create_status_section(main_frame, 4)
        
    def create_path_section(self, parent, row):
        """创建路径选择区域"""
        path_frame = ttk.LabelFrame(parent, text="工作路径", padding="10")
        path_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
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
    
    def create_mapping_section(self, parent, row):
        """创建映射替换区域"""
        # 映射组件
        self.mapping_widget = MappingListWidget(parent)
        self.mapping_widget.frame.grid(row=row, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # 设置示例映射
        example_mappings = {
            "IMG_": "照片_",
            "DSC_": "图片_",
            "2023": "2023年",
            "2024": "2024年",
            "12": "12月",
            "01": "01日",
            "02": "02日",
            "03": "03日",
            "_": " "
        }
        self.mapping_widget.set_mappings(example_mappings)
    
    def create_rename_section(self, parent, row):
        """创建重命名设置区域"""
        rename_frame = ttk.LabelFrame(parent, text="重命名设置", padding="10")
        rename_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
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
        
        # 按钮区域
        button_frame = ttk.Frame(rename_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(15, 0))
        
        ttk.Button(button_frame, text="预览重命名", 
                  command=self.preview_rename).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="执行重命名", 
                  command=self.execute_rename).pack(side=tk.LEFT)
    
    def create_status_section(self, parent, row):
        """创建状态显示区域"""
        status_frame = ttk.LabelFrame(parent, text="状态信息", padding="10")
        status_frame.grid(row=row, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
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
        
        # 初始状态信息
        self.update_status("欢迎使用文件重命名工具！\n")
        self.update_status(f"当前工作路径: {self.current_path.get()}\n")
        self.update_status("支持功能：\n")
        self.update_status("1. 添加前缀和后缀\n")
        self.update_status("2. 映射替换（将文件名中的指定文本替换为其他文本）\n")
        self.update_status("3. 预览重命名结果\n")
        
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
        path = self.current_path.get().strip()
        prefix = self.prefix.get().strip()
        suffix = self.suffix.get().strip()
        
        if not path:
            messagebox.showerror("错误", "请先确认工作路径！")
            return
        
        try:
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            if not files:
                messagebox.showwarning("警告", "该文件夹中没有文件！")
                return
            
            self.update_status(f"\n重命名预览:\n")
            self.update_status(f"前缀: '{prefix}'\n")
            self.update_status(f"后缀: '{suffix}'\n")
            self.update_status(f"映射替换: {len(self.mapping_widget.get_mappings())} 个规则\n\n")
            
            for file in files:
                # 应用映射替换
                mapped_name = self.mapping_widget.apply_mappings(file)
                
                # 分离文件名和扩展名
                name, ext = os.path.splitext(mapped_name)
                new_name = prefix + name + suffix + ext
                
                self.update_status(f"  {file} -> {new_name}\n")
                
        except Exception as e:
            messagebox.showerror("错误", f"预览失败: {e}")
    
    def execute_rename(self):
        """执行重命名"""
        path = self.current_path.get().strip()
        prefix = self.prefix.get().strip()
        suffix = self.suffix.get().strip()
        
        if not path:
            messagebox.showerror("错误", "请先确认工作路径！")
            return
        
        try:
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            if not files:
                messagebox.showwarning("警告", "该文件夹中没有文件！")
                return
            
            # 确认对话框
            if not messagebox.askyesno("确认", f"确定要重命名 {len(files)} 个文件吗？"):
                return
            
            self.update_status(f"\n开始重命名操作...\n")
            
            renamed_count = 0
            for file in files:
                try:
                    # 应用映射替换
                    mapped_name = self.mapping_widget.apply_mappings(file)
                    
                    # 分离文件名和扩展名
                    name, ext = os.path.splitext(mapped_name)
                    new_name = prefix + name + suffix + ext
                    
                    old_path = os.path.join(path, file)
                    new_path = os.path.join(path, new_name)
                    
                    # 检查新文件名是否已存在
                    if os.path.exists(new_path):
                        self.update_status(f"跳过: {file} -> {new_name} (文件已存在)\n")
                        continue
                    
                    # 执行重命名
                    os.rename(old_path, new_path)
                    self.update_status(f"✓ {file} -> {new_name}\n")
                    renamed_count += 1
                    
                except Exception as e:
                    self.update_status(f"✗ {file} -> {new_name} (错误: {e})\n")
            
            self.update_status(f"\n重命名完成！成功重命名 {renamed_count} 个文件\n")
            
        except Exception as e:
            messagebox.showerror("错误", f"重命名操作失败: {e}")
            
    def update_status(self, message):
        """更新状态信息"""
        self.status_text.insert(tk.END, message)
        self.status_text.see(tk.END)
        self.root.update_idletasks()
        
    def run(self):
        """运行应用程序"""
        self.root.mainloop()


def main():
    """主函数"""
    app = FileRenameEditor()
    app.run()


if __name__ == "__main__":
    main()
