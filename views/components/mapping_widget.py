# -*- coding: utf-8 -*-
"""
映射列表组件 - 用于文件名替换
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict


class MappingListWidget:
    """映射列表组件"""
    
    def __init__(self, parent):
        self.parent = parent
        self.mappings = {}  # 存储映射关系
        self.setup_ui()
    
    def setup_ui(self):
        """设置映射列表界面"""
        # 映射列表框架
        mapping_frame = ttk.LabelFrame(self.parent, text="映射替换设置", padding="15")
        mapping_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        mapping_frame.columnconfigure(1, weight=1)
        
        # 输入区域
        input_frame = ttk.Frame(mapping_frame)
        input_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=1)
        
        # Key输入
        ttk.Label(input_frame, text="查找内容:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=(0, 8))
        self.key_entry = ttk.Entry(input_frame, width=22, font=("Consolas", 11))
        self.key_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 15))
        
        # Value输入
        ttk.Label(input_frame, text="替换为:", font=("Arial", 10, "bold")).grid(row=0, column=2, sticky=tk.W, padx=(0, 8))
        self.value_entry = ttk.Entry(input_frame, width=22, font=("Consolas", 11))
        self.value_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=(0, 15))
        
        # 按钮
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=0, column=4, padx=(15, 0))
        
        # 按钮样式
        button_style = ttk.Style()
        button_style.configure("Mapping.TButton", font=("Arial", 9))
        
        ttk.Button(button_frame, text="添加", command=self.add_mapping, 
                  style="Mapping.TButton").grid(row=0, column=0, padx=(0, 8))
        ttk.Button(button_frame, text="删除", command=self.delete_mapping, 
                  style="Mapping.TButton").grid(row=0, column=1, padx=(0, 8))
        ttk.Button(button_frame, text="清空", command=self.clear_mappings, 
                  style="Mapping.TButton").grid(row=0, column=2)
        
        # 映射列表显示
        list_frame = ttk.Frame(mapping_frame)
        list_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # 创建Treeview显示映射列表
        columns = ("key", "value")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)
        
        # 设置列标题
        self.tree.heading("key", text="查找内容")
        self.tree.heading("value", text="替换为")
        
        # 设置列宽
        self.tree.column("key", width=250)
        self.tree.column("value", width=250)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 绑定双击事件
        self.tree.bind("<Double-1>", self.on_double_click)
        
        # 说明文字
        info_label = ttk.Label(mapping_frame, 
                              text="说明：在文件名中查找左侧内容，替换为右侧内容。双击可编辑。",
                              font=("Arial", 9), foreground="gray")
        info_label.grid(row=2, column=0, columnspan=3, pady=(15, 0))
    
    def add_mapping(self):
        """添加映射"""
        key = self.key_entry.get().strip()
        value = self.value_entry.get().strip()
        
        if not key:
            messagebox.showerror("错误", "请输入查找内容！")
            return
        
        if key in self.mappings:
            messagebox.showwarning("警告", f"'{key}' 已存在，将更新其值")
        
        self.mappings[key] = value
        self.refresh_tree()
        
        # 清空输入框
        self.key_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)
    
    def delete_mapping(self):
        """删除选中的映射"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要删除的映射！")
            return
        
        item = selection[0]
        key = self.tree.item(item, "values")[0]
        
        if messagebox.askyesno("确认", f"确定要删除映射 '{key}' 吗？"):
            del self.mappings[key]
            self.refresh_tree()
    
    def clear_mappings(self):
        """清空所有映射"""
        if not self.mappings:
            return
        
        if messagebox.askyesno("确认", "确定要清空所有映射吗？"):
            self.mappings.clear()
            self.refresh_tree()
    
    def on_double_click(self, event):
        """双击编辑映射"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        key, value = self.tree.item(item, "values")
        
        # 创建编辑对话框
        self.edit_mapping_dialog(key, value)
    
    def edit_mapping_dialog(self, old_key, old_value):
        """编辑映射对话框"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("编辑映射")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # 居中显示
        dialog.geometry("+%d+%d" % (self.parent.winfo_rootx() + 50, self.parent.winfo_rooty() + 50))
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 查找内容
        ttk.Label(frame, text="查找内容:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        key_entry = ttk.Entry(frame, width=30, font=("Consolas", 10))
        key_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        key_entry.insert(0, old_key)
        
        # 替换为
        ttk.Label(frame, text="替换为:").grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        value_entry = ttk.Entry(frame, width=30, font=("Consolas", 10))
        value_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        value_entry.insert(0, old_value)
        
        # 按钮
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0))
        
        def save_mapping():
            new_key = key_entry.get().strip()
            new_value = value_entry.get().strip()
            
            if not new_key:
                messagebox.showerror("错误", "查找内容不能为空！")
                return
            
            # 删除旧的映射
            if old_key in self.mappings:
                del self.mappings[old_key]
            
            # 添加新的映射
            self.mappings[new_key] = new_value
            self.refresh_tree()
            dialog.destroy()
        
        ttk.Button(button_frame, text="保存", command=save_mapping).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT)
    
    def refresh_tree(self):
        """刷新树形视图"""
        # 清空现有项目
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 添加映射项目
        for key, value in self.mappings.items():
            self.tree.insert("", tk.END, values=(key, value))
    
    def get_mappings(self) -> Dict[str, str]:
        """获取映射字典"""
        return self.mappings.copy()
    
    def set_mappings(self, mappings: Dict[str, str]):
        """设置映射字典"""
        self.mappings = mappings.copy()
        self.refresh_tree()
