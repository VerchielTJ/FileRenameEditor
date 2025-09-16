#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FileRenameEditor - 文件重命名工具
支持前缀后缀和映射替换功能
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from typing import List, Tuple, Dict


class MappingListWidget:
    """映射列表组件"""
    
    def __init__(self, parent):
        self.parent = parent
        self.mappings = {}  # 存储映射关系
        self.setup_ui()
    
    def setup_ui(self):
        """设置映射列表界面"""
        # 映射列表框架
        mapping_frame = ttk.LabelFrame(self.parent, text="映射替换设置", padding="10")
        mapping_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        mapping_frame.columnconfigure(1, weight=1)
        
        # 输入区域
        input_frame = ttk.Frame(mapping_frame)
        input_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=1)
        
        # Key输入
        ttk.Label(input_frame, text="查找内容:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.key_entry = ttk.Entry(input_frame, width=20, font=("Consolas", 10))
        self.key_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Value输入
        ttk.Label(input_frame, text="替换为:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.value_entry = ttk.Entry(input_frame, width=20, font=("Consolas", 10))
        self.value_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # 按钮
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=0, column=4, padx=(10, 0))
        
        ttk.Button(button_frame, text="添加", command=self.add_mapping).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="删除", command=self.delete_mapping).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(button_frame, text="清空", command=self.clear_mappings).grid(row=0, column=2)
        
        # 映射列表显示
        list_frame = ttk.Frame(mapping_frame)
        list_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # 创建Treeview显示映射列表
        columns = ("key", "value")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=6)
        
        # 设置列标题
        self.tree.heading("key", text="查找内容")
        self.tree.heading("value", text="替换为")
        
        # 设置列宽
        self.tree.column("key", width=200)
        self.tree.column("value", width=200)
        
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
        info_label.grid(row=2, column=0, columnspan=3, pady=(10, 0))
    
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


class FileRenameEditor:
    def __init__(self):
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
        path_frame = ttk.LabelFrame(main_frame, text="工作路径", padding="10")
        path_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
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
        
        # 重命名设置区域
        rename_frame = ttk.LabelFrame(main_frame, text="重命名设置", padding="10")
        rename_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
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
        
        # 状态显示区域
        status_frame = ttk.LabelFrame(main_frame, text="状态信息", padding="10")
        status_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), 
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
        
        # 初始状态信息
        self.update_status("欢迎使用文件重命名工具！\n")
        self.update_status(f"当前工作路径: {self.current_path.get()}\n")
        
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
    
    def apply_mappings(self, filename: str) -> str:
        """应用映射替换"""
        result = filename
        mappings = self.mapping_widget.get_mappings()
        
        for key, value in mappings.items():
            if key in result:
                result = result.replace(key, value)
        
        return result
    
    def preview_rename(self):
        """预览重命名"""
        path = self.current_path.get().strip()
        prefix = self.prefix.get().strip()
        suffix = self.suffix.get().strip()
        
        if not path:
            messagebox.showerror("错误", "请先确认工作路径！")
            return
        
        if not prefix and not suffix and not self.mapping_widget.get_mappings():
            messagebox.showerror("错误", "请至少设置一种重命名方式！")
            return
        
        try:
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            if not files:
                messagebox.showwarning("警告", "该文件夹中没有文件！")
                return
            
            self.update_status(f"\n重命名预览:\n")
            self.update_status(f"前缀: '{prefix}'\n")
            self.update_status(f"后缀: '{suffix}'\n")
            
            mappings = self.mapping_widget.get_mappings()
            if mappings:
                self.update_status(f"映射替换: {len(mappings)} 条规则\n")
            
            self.update_status(f"将重命名 {len(files)} 个文件\n\n")
            
            for file in files:
                # 应用映射替换
                mapped_name = self.apply_mappings(file)
                
                # 分离文件名和扩展名
                name, ext = os.path.splitext(mapped_name)
                new_name = prefix + name + suffix + ext
                
                if file != new_name:
                    self.update_status(f"  {file} -> {new_name}\n")
                else:
                    self.update_status(f"  {file} (无变化)\n")
                    
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
        
        if not prefix and not suffix and not self.mapping_widget.get_mappings():
            messagebox.showerror("错误", "请至少设置一种重命名方式！")
            return
        
        # 确认对话框
        if not messagebox.askyesno("确认", "确定要执行重命名操作吗？"):
            return
        
        try:
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            if not files:
                messagebox.showwarning("警告", "该文件夹中没有文件！")
                return
            
            self.update_status(f"\n开始重命名操作...\n")
            
            renamed_count = 0
            for file in files:
                # 应用映射替换
                mapped_name = self.apply_mappings(file)
                
                # 分离文件名和扩展名
                name, ext = os.path.splitext(mapped_name)
                new_name = prefix + name + suffix + ext
                
                if file == new_name:
                    self.update_status(f"跳过: {file} (无变化)\n")
                    continue
                
                old_path = os.path.join(path, file)
                new_path = os.path.join(path, new_name)
                
                # 检查新文件名是否已存在
                if os.path.exists(new_path):
                    self.update_status(f"跳过: {file} -> {new_name} (文件已存在)\n")
                    continue
                
                try:
                    os.rename(old_path, new_path)
                    self.update_status(f"重命名: {file} -> {new_name}\n")
                    renamed_count += 1
                except Exception as e:
                    self.update_status(f"失败: {file} -> {new_name} (错误: {e})\n")
            
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
