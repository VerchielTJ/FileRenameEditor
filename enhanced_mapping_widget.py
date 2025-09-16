# -*- coding: utf-8 -*-
"""
增强版映射列表组件 - 支持正则表达式和批量操作
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
import json
import os
from typing import Dict, List, Tuple


class EnhancedMappingListWidget:
    """增强版映射列表组件"""
    
    def __init__(self, parent):
        self.parent = parent
        self.mappings = {}  # 存储映射关系
        self.use_regex = tk.BooleanVar(value=False)  # 是否使用正则表达式
        self.case_sensitive = tk.BooleanVar(value=True)  # 是否区分大小写
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        self.frame = ttk.LabelFrame(self.parent, text="增强版文件名映射替换", padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.frame.columnconfigure(1, weight=1)
        
        # 选项区域
        options_frame = ttk.Frame(self.frame)
        options_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Checkbutton(options_frame, text="使用正则表达式", 
                       variable=self.use_regex).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Checkbutton(options_frame, text="区分大小写", 
                       variable=self.case_sensitive).pack(side=tk.LEFT)
        
        # 输入区域
        input_frame = ttk.Frame(self.frame)
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=1)
        
        # 原文本输入
        ttk.Label(input_frame, text="原文本/正则:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
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
        
        # 批量操作区域
        batch_frame = ttk.Frame(self.frame)
        batch_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(batch_frame, text="批量添加", 
                  command=self.batch_add_dialog).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(batch_frame, text="从文件导入", 
                  command=self.import_from_file).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(batch_frame, text="导出到文件", 
                  command=self.export_to_file).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(batch_frame, text="清空所有", 
                  command=self.clear_mappings).pack(side=tk.LEFT)
        
        # 映射列表
        list_frame = ttk.Frame(self.frame)
        list_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # 创建Treeview
        columns = ('原文本', '替换为', '类型', '状态')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)
        
        # 设置列标题
        self.tree.heading('原文本', text='原文本/正则')
        self.tree.heading('替换为', text='替换为')
        self.tree.heading('类型', text='类型')
        self.tree.heading('状态', text='状态')
        
        # 设置列宽
        self.tree.column('原文本', width=200)
        self.tree.column('替换为', width=150)
        self.tree.column('类型', width=80)
        self.tree.column('状态', width=80)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 绑定双击事件
        self.tree.bind('<Double-1>', self.edit_mapping)
        
        # 按钮区域
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        ttk.Button(button_frame, text="编辑选中", 
                  command=self.edit_mapping).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="删除选中", 
                  command=self.delete_mapping).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(button_frame, text="测试选中", 
                  command=self.test_selected).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(button_frame, text="上移", 
                  command=self.move_up).grid(row=0, column=3, padx=(0, 5))
        ttk.Button(button_frame, text="下移", 
                  command=self.move_down).grid(row=0, column=4)
        
        # 配置框架权重
        self.frame.rowconfigure(3, weight=1)
    
    def add_mapping(self):
        """添加映射"""
        key = self.key_entry.get().strip()
        value = self.value_entry.get().strip()
        
        if not key:
            messagebox.showerror("错误", "请输入原文本！")
            return
        
        # 验证正则表达式
        if self.use_regex.get():
            try:
                flags = 0 if self.case_sensitive.get() else re.IGNORECASE
                re.compile(key, flags)
                mapping_type = "正则"
                status = "有效"
            except re.error as e:
                messagebox.showerror("错误", f"正则表达式无效: {e}")
                return
        else:
            mapping_type = "文本"
            status = "有效"
        
        if key in self.mappings:
            if messagebox.askyesno("确认", f"'{key}' 已存在，是否覆盖？"):
                self.mappings[key] = {
                    'value': value,
                    'use_regex': self.use_regex.get(),
                    'case_sensitive': self.case_sensitive.get()
                }
                self.refresh_tree()
            else:
                return
        else:
            self.mappings[key] = {
                'value': value,
                'use_regex': self.use_regex.get(),
                'case_sensitive': self.case_sensitive.get()
            }
            self.refresh_tree()
        
        # 清空输入框
        self.key_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)
        self.key_entry.focus()
    
    def batch_add_dialog(self):
        """批量添加对话框"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("批量添加映射")
        dialog.geometry("600x500")
        dialog.resizable(True, True)
        dialog.transient(self.parent)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="批量添加映射规则:").pack(anchor=tk.W, pady=(0, 10))
        ttk.Label(frame, text="每行一个映射，格式：原文本=替换文本").pack(anchor=tk.W, pady=(0, 10))
        
        text_widget = tk.Text(frame, height=20, width=60, font=("Consolas", 10))
        text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 添加示例
        example = """IMG_=照片_
2023=2023年
12=12月
01=01日
_= 
DSC=数码相机
PIC=图片"""
        text_widget.insert(1.0, example)
        
        def batch_add():
            content = text_widget.get(1.0, tk.END).strip()
            if not content:
                messagebox.showwarning("警告", "请输入映射数据！")
                return
            
            added_count = 0
            for line in content.split('\n'):
                line = line.strip()
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    if key:
                        self.mappings[key] = {
                            'value': value,
                            'use_regex': self.use_regex.get(),
                            'case_sensitive': self.case_sensitive.get()
                        }
                        added_count += 1
            
            self.refresh_tree()
            dialog.destroy()
            messagebox.showinfo("成功", f"成功添加 {added_count} 个映射！")
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="添加", command=batch_add).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT)
    
    def import_from_file(self):
        """从文件导入映射"""
        file_path = filedialog.askopenfilename(
            title="选择映射文件",
            filetypes=[("JSON文件", "*.json"), ("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            if file_path.endswith('.json'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.mappings.update(data)
                    else:
                        messagebox.showerror("错误", "JSON文件格式不正确！")
                        return
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    for line in content.split('\n'):
                        line = line.strip()
                        if '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            if key:
                                self.mappings[key] = {
                                    'value': value,
                                    'use_regex': False,
                                    'case_sensitive': True
                                }
            
            self.refresh_tree()
            messagebox.showinfo("成功", f"成功从文件导入映射！")
            
        except Exception as e:
            messagebox.showerror("错误", f"导入失败: {e}")
    
    def export_to_file(self):
        """导出映射到文件"""
        if not self.mappings:
            messagebox.showinfo("提示", "没有映射可导出！")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="保存映射文件",
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json"), ("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            if file_path.endswith('.json'):
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.mappings, f, ensure_ascii=False, indent=2)
            else:
                with open(file_path, 'w', encoding='utf-8') as f:
                    for key, mapping in self.mappings.items():
                        f.write(f"{key}={mapping['value']}\n")
            
            messagebox.showinfo("成功", f"映射已导出到: {file_path}")
            
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {e}")
    
    def edit_mapping(self, event=None):
        """编辑映射"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要编辑的映射！")
            return
        
        item = self.tree.item(selection[0])
        key = item['values'][0]
        mapping = self.mappings[key]
        
        # 创建编辑对话框
        self.edit_dialog(key, mapping)
    
    def edit_dialog(self, old_key, mapping):
        """编辑对话框"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("编辑映射")
        dialog.geometry("500x300")
        dialog.resizable(False, False)
        dialog.transient(self.parent)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 原文本
        ttk.Label(frame, text="原文本/正则:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        key_entry = ttk.Entry(frame, width=40)
        key_entry.insert(0, old_key)
        key_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 替换文本
        ttk.Label(frame, text="替换为:").grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        value_entry = ttk.Entry(frame, width=40)
        value_entry.insert(0, mapping['value'])
        value_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 选项
        use_regex_var = tk.BooleanVar(value=mapping['use_regex'])
        case_sensitive_var = tk.BooleanVar(value=mapping['case_sensitive'])
        
        ttk.Checkbutton(frame, text="使用正则表达式", 
                       variable=use_regex_var).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        ttk.Checkbutton(frame, text="区分大小写", 
                       variable=case_sensitive_var).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(0, 20))
        
        # 按钮
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(0, 10))
        
        def save_edit():
            new_key = key_entry.get().strip()
            new_value = value_entry.get().strip()
            
            if not new_key:
                messagebox.showerror("错误", "原文本不能为空！")
                return
            
            # 验证正则表达式
            if use_regex_var.get():
                try:
                    flags = 0 if case_sensitive_var.get() else re.IGNORECASE
                    re.compile(new_key, flags)
                except re.error as e:
                    messagebox.showerror("错误", f"正则表达式无效: {e}")
                    return
            
            # 如果键名改变了，需要删除旧的
            if new_key != old_key:
                if new_key in self.mappings:
                    messagebox.showerror("错误", f"'{new_key}' 已存在！")
                    return
                del self.mappings[old_key]
            
            self.mappings[new_key] = {
                'value': new_value,
                'use_regex': use_regex_var.get(),
                'case_sensitive': case_sensitive_var.get()
            }
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
    
    def test_selected(self):
        """测试选中的映射"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要测试的映射！")
            return
        
        item = self.tree.item(selection[0])
        key = item['values'][0]
        mapping = self.mappings[key]
        
        # 创建测试对话框
        dialog = tk.Toplevel(self.parent)
        dialog.title("测试映射")
        dialog.geometry("500x300")
        dialog.resizable(False, False)
        dialog.transient(self.parent)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text=f"测试映射: {key} -> {mapping['value']}").pack(anchor=tk.W, pady=(0, 10))
        ttk.Label(frame, text="输入测试文本:").pack(anchor=tk.W, pady=(0, 10))
        
        test_entry = ttk.Entry(frame, width=50, font=("Consolas", 10))
        test_entry.pack(fill=tk.X, pady=(0, 10))
        test_entry.insert(0, "IMG_20231201_143022.jpg")
        
        result_label = ttk.Label(frame, text="", font=("Consolas", 10), foreground="blue")
        result_label.pack(anchor=tk.W, pady=(10, 0))
        
        def apply_test():
            text = test_entry.get().strip()
            if not text:
                return
            
            try:
                result = self.apply_single_mapping(text, key, mapping)
                result_label.config(text=f"结果: {result}")
            except Exception as e:
                result_label.config(text=f"错误: {e}", foreground="red")
        
        ttk.Button(frame, text="测试", command=apply_test).pack(pady=(10, 0))
        ttk.Button(frame, text="关闭", command=dialog.destroy).pack(pady=(10, 0))
        
        test_entry.focus()
    
    def move_up(self):
        """上移选中的映射"""
        selection = self.tree.selection()
        if not selection:
            return
        
        # 将映射转换为有序列表
        items = list(self.mappings.items())
        current_index = None
        
        for i, (key, value) in enumerate(items):
            if key == selection[0]:
                current_index = i
                break
        
        if current_index is not None and current_index > 0:
            # 交换位置
            items[current_index], items[current_index - 1] = items[current_index - 1], items[current_index]
            
            # 重建映射字典
            self.mappings = dict(items)
            self.refresh_tree()
            
            # 重新选中
            new_key = items[current_index - 1][0]
            for item in self.tree.get_children():
                if self.tree.item(item)['values'][0] == new_key:
                    self.tree.selection_set(item)
                    break
    
    def move_down(self):
        """下移选中的映射"""
        selection = self.tree.selection()
        if not selection:
            return
        
        # 将映射转换为有序列表
        items = list(self.mappings.items())
        current_index = None
        
        for i, (key, value) in enumerate(items):
            if key == selection[0]:
                current_index = i
                break
        
        if current_index is not None and current_index < len(items) - 1:
            # 交换位置
            items[current_index], items[current_index + 1] = items[current_index + 1], items[current_index]
            
            # 重建映射字典
            self.mappings = dict(items)
            self.refresh_tree()
            
            # 重新选中
            new_key = items[current_index + 1][0]
            for item in self.tree.get_children():
                if self.tree.item(item)['values'][0] == new_key:
                    self.tree.selection_set(item)
                    break
    
    def clear_mappings(self):
        """清空所有映射"""
        if not self.mappings:
            messagebox.showinfo("提示", "映射列表已为空！")
            return
        
        if messagebox.askyesno("确认", "确定要清空所有映射吗？"):
            self.mappings.clear()
            self.refresh_tree()
    
    def refresh_tree(self):
        """刷新树形视图"""
        # 清空现有项目
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 添加映射项目
        for key, mapping in self.mappings.items():
            mapping_type = "正则" if mapping['use_regex'] else "文本"
            status = "有效"
            
            # 验证正则表达式
            if mapping['use_regex']:
                try:
                    flags = 0 if mapping['case_sensitive'] else re.IGNORECASE
                    re.compile(key, flags)
                except re.error:
                    status = "无效"
            
            self.tree.insert('', tk.END, values=(key, mapping['value'], mapping_type, status))
    
    def apply_single_mapping(self, text: str, key: str, mapping: Dict) -> str:
        """应用单个映射"""
        if mapping['use_regex']:
            flags = 0 if mapping['case_sensitive'] else re.IGNORECASE
            pattern = re.compile(key, flags)
            return pattern.sub(mapping['value'], text)
        else:
            if mapping['case_sensitive']:
                return text.replace(key, mapping['value'])
            else:
                # 不区分大小写的替换
                import re
                return re.sub(re.escape(key), mapping['value'], text, flags=re.IGNORECASE)
    
    def apply_mappings(self, filename: str) -> str:
        """应用所有映射到文件名"""
        result = filename
        for key, mapping in self.mappings.items():
            result = self.apply_single_mapping(result, key, mapping)
        return result
    
    def get_mappings(self) -> Dict[str, str]:
        """获取简化的映射字典（兼容原版）"""
        return {key: mapping['value'] for key, mapping in self.mappings.items()}
    
    def set_mappings(self, mappings: Dict[str, str]):
        """设置映射字典（兼容原版）"""
        self.mappings = {}
        for key, value in mappings.items():
            self.mappings[key] = {
                'value': value,
                'use_regex': False,
                'case_sensitive': True
            }
        self.refresh_tree()
    
    def get_enhanced_mappings(self) -> Dict[str, Dict]:
        """获取增强版映射字典"""
        return self.mappings.copy()
    
    def set_enhanced_mappings(self, mappings: Dict[str, Dict]):
        """设置增强版映射字典"""
        self.mappings = mappings.copy()
        self.refresh_tree()
