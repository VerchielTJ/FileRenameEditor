# -*- coding: utf-8 -*-
"""
映射列表组件 - 用于文件名替换
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Tuple


class MappingListWidget:
    """映射列表组件"""
    
    def __init__(self, parent):
        self.parent = parent
        self.mappings = {}  # 存储映射关系
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        self.frame = ttk.LabelFrame(self.parent, text="文件名映射替换", padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.frame.columnconfigure(1, weight=1)
        
        # 输入区域
        input_frame = ttk.Frame(self.frame)
        input_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=1)
        
        # 原文本输入
        ttk.Label(input_frame, text="原文本:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.key_entry = ttk.Entry(input_frame, width=20)
        self.key_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # 替换文本输入
        ttk.Label(input_frame, text="替换为:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.value_entry = ttk.Entry(input_frame, width=20)
        self.value_entry.bind('<Return>', lambda e: self.add_mapping())
        self.value_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # 添加按钮
        ttk.Button(input_frame, text="添加映射", 
                  command=self.add_mapping).grid(row=0, column=4)
        
        # 映射列表
        list_frame = ttk.Frame(self.frame)
        list_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # 创建Treeview
        columns = ('原文本', '替换为')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=6)
        
        # 设置列标题
        self.tree.heading('原文本', text='原文本')
        self.tree.heading('替换为', text='替换为')
        
        # 设置列宽
        self.tree.column('原文本', width=150)
        self.tree.column('替换为', width=150)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 绑定双击事件
        self.tree.bind('<Double-1>', self.edit_mapping)
        
        # 按钮区域
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        ttk.Button(button_frame, text="编辑选中", 
                  command=self.edit_mapping).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="删除选中", 
                  command=self.delete_mapping).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(button_frame, text="清空列表", 
                  command=self.clear_mappings).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(button_frame, text="导入映射", 
                  command=self.import_mappings).grid(row=0, column=3, padx=(0, 5))
        ttk.Button(button_frame, text="导出映射", 
                  command=self.export_mappings).grid(row=0, column=4)
        
        # 配置框架权重
        self.frame.rowconfigure(1, weight=1)
    
    def add_mapping(self):
        """添加映射"""
        key = self.key_entry.get().strip()
        value = self.value_entry.get().strip()
        
        if not key:
            messagebox.showerror("错误", "请输入原文本！")
            return
        
        if key in self.mappings:
            if messagebox.askyesno("确认", f"'{key}' 已存在，是否覆盖？"):
                self.mappings[key] = value
                self.refresh_tree()
            else:
                return
        else:
            self.mappings[key] = value
            self.refresh_tree()
        
        # 清空输入框
        self.key_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)
        self.key_entry.focus()
    
    def edit_mapping(self, event=None):
        """编辑映射"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要编辑的映射！")
            return
        
        item = self.tree.item(selection[0])
        key = item['values'][0]
        value = item['values'][1]
        
        # 创建编辑对话框
        self.edit_dialog(key, value)
    
    def edit_dialog(self, old_key, old_value):
        """编辑对话框"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("编辑映射")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # 居中显示
        dialog.geometry("+%d+%d" % (self.parent.winfo_rootx() + 50, 
                                   self.parent.winfo_rooty() + 50))
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 原文本
        ttk.Label(frame, text="原文本:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        key_entry = ttk.Entry(frame, width=30)
        key_entry.insert(0, old_key)
        key_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 替换文本
        ttk.Label(frame, text="替换为:").grid(row=1, column=0, sticky=tk.W, pady=(0, 20))
        value_entry = ttk.Entry(frame, width=30)
        value_entry.insert(0, old_value)
        value_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # 按钮
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
        def save_edit():
            new_key = key_entry.get().strip()
            new_value = value_entry.get().strip()
            
            if not new_key:
                messagebox.showerror("错误", "原文本不能为空！")
                return
            
            # 如果键名改变了，需要删除旧的
            if new_key != old_key:
                if new_key in self.mappings:
                    messagebox.showerror("错误", f"'{new_key}' 已存在！")
                    return
                del self.mappings[old_key]
            
            self.mappings[new_key] = new_value
            self.refresh_tree()
            dialog.destroy()
        
        ttk.Button(button_frame, text="保存", command=save_edit).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT)
        
        # 配置权重
        frame.columnconfigure(1, weight=1)
        key_entry.focus()
    
    def delete_mapping(self):
        """删除映射"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要删除的映射！")
            return
        
        item = self.tree.item(selection[0])
        key = item['values'][0]
        
        if messagebox.askyesno("确认", f"确定要删除映射 '{key}' 吗？"):
            del self.mappings[key]
            self.refresh_tree()
    
    def clear_mappings(self):
        """清空所有映射"""
        if not self.mappings:
            messagebox.showinfo("提示", "映射列表已为空！")
            return
        
        if messagebox.askyesno("确认", "确定要清空所有映射吗？"):
            self.mappings.clear()
            self.refresh_tree()
    
    def import_mappings(self):
        """导入映射（从文本输入）"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("导入映射")
        dialog.geometry("500x400")
        dialog.resizable(True, True)
        dialog.transient(self.parent)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="每行一个映射，格式：原文本=替换文本").pack(anchor=tk.W, pady=(0, 10))
        
        text_widget = tk.Text(frame, height=15, width=50)
        text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        def import_data():
            content = text_widget.get(1.0, tk.END).strip()
            if not content:
                messagebox.showwarning("警告", "请输入映射数据！")
                return
            
            imported_count = 0
            for line in content.split('\n'):
                line = line.strip()
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    if key:
                        self.mappings[key] = value
                        imported_count += 1
            
            self.refresh_tree()
            dialog.destroy()
            messagebox.showinfo("成功", f"成功导入 {imported_count} 个映射！")
        
        ttk.Button(frame, text="导入", command=import_data).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT)
    
    def export_mappings(self):
        """导出映射"""
        if not self.mappings:
            messagebox.showinfo("提示", "没有映射可导出！")
            return
        
        dialog = tk.Toplevel(self.parent)
        dialog.title("导出映射")
        dialog.geometry("500x400")
        dialog.resizable(True, True)
        dialog.transient(self.parent)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="映射数据（可复制到文件保存）:").pack(anchor=tk.W, pady=(0, 10))
        
        text_widget = tk.Text(frame, height=15, width=50)
        text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 填充数据
        content = ""
        for key, value in self.mappings.items():
            content += f"{key}={value}\n"
        text_widget.insert(1.0, content)
        
        ttk.Button(frame, text="关闭", command=dialog.destroy).pack()
    
    def refresh_tree(self):
        """刷新树形视图"""
        # 清空现有项目
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 添加映射项目
        for key, value in self.mappings.items():
            self.tree.insert('', tk.END, values=(key, value))
    
    def get_mappings(self) -> Dict[str, str]:
        """获取映射字典"""
        return self.mappings.copy()
    
    def set_mappings(self, mappings: Dict[str, str]):
        """设置映射字典"""
        self.mappings = mappings.copy()
        self.refresh_tree()
    
    def apply_mappings(self, filename: str) -> str:
        """应用映射到文件名"""
        result = filename
        for key, value in self.mappings.items():
            if key in result:
                result = result.replace(key, value)
        return result
