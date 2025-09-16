#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
映射组件完整演示程序
展示基础版和增强版映射组件的所有功能
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
from mapping_widget import MappingListWidget
from enhanced_mapping_widget import EnhancedMappingListWidget


class MappingDemoApp:
    """映射组件演示应用程序"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("映射组件完整演示")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        self.setup_ui()
        self.setup_examples()
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="映射组件完整演示", 
                               font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 创建选项卡
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 基础版选项卡
        basic_frame = ttk.Frame(notebook, padding="10")
        notebook.add(basic_frame, text="基础版映射组件")
        
        # 增强版选项卡
        enhanced_frame = ttk.Frame(notebook, padding="10")
        notebook.add(enhanced_frame, text="增强版映射组件")
        
        # 对比测试选项卡
        compare_frame = ttk.Frame(notebook, padding="10")
        notebook.add(compare_frame, text="功能对比测试")
        
        # 设置基础版
        self.setup_basic_tab(basic_frame)
        
        # 设置增强版
        self.setup_enhanced_tab(enhanced_frame)
        
        # 设置对比测试
        self.setup_compare_tab(compare_frame)
    
    def setup_basic_tab(self, parent):
        """设置基础版选项卡"""
        # 基础版映射组件
        self.basic_mapping = MappingListWidget(parent)
        
        # 测试区域
        test_frame = ttk.LabelFrame(parent, text="基础版测试", padding="10")
        test_frame.pack(fill=tk.X, pady=(20, 0))
        
        # 文件名输入
        input_frame = ttk.Frame(test_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(input_frame, text="测试文件名:").pack(side=tk.LEFT, padx=(0, 10))
        self.basic_test_entry = ttk.Entry(input_frame, width=50)
        self.basic_test_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.basic_test_entry.insert(0, "IMG_20231201_143022.jpg")
        
        ttk.Button(input_frame, text="应用映射", 
                  command=self.test_basic_mapping).pack(side=tk.LEFT)
        
        # 结果显示
        result_frame = ttk.Frame(test_frame)
        result_frame.pack(fill=tk.X)
        
        ttk.Label(result_frame, text="替换结果:").pack(anchor=tk.W)
        self.basic_result_label = ttk.Label(result_frame, text="", 
                                           font=("Consolas", 10), 
                                           foreground="blue")
        self.basic_result_label.pack(anchor=tk.W, pady=(5, 0))
        
        # 示例按钮
        example_frame = ttk.Frame(test_frame)
        example_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(example_frame, text="加载照片重命名示例", 
                  command=self.load_photo_example).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(example_frame, text="加载文档重命名示例", 
                  command=self.load_document_example).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(example_frame, text="清空映射", 
                  command=self.clear_basic_mapping).pack(side=tk.LEFT)
    
    def setup_enhanced_tab(self, parent):
        """设置增强版选项卡"""
        # 增强版映射组件
        self.enhanced_mapping = EnhancedMappingListWidget(parent)
        
        # 测试区域
        test_frame = ttk.LabelFrame(parent, text="增强版测试", padding="10")
        test_frame.pack(fill=tk.X, pady=(20, 0))
        
        # 文件名输入
        input_frame = ttk.Frame(test_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(input_frame, text="测试文件名:").pack(side=tk.LEFT, padx=(0, 10))
        self.enhanced_test_entry = ttk.Entry(input_frame, width=50)
        self.enhanced_test_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.enhanced_test_entry.insert(0, "DSC_20231201_143022_001.jpg")
        
        ttk.Button(input_frame, text="应用映射", 
                  command=self.test_enhanced_mapping).pack(side=tk.LEFT)
        
        # 结果显示
        result_frame = ttk.Frame(test_frame)
        result_frame.pack(fill=tk.X)
        
        ttk.Label(result_frame, text="替换结果:").pack(anchor=tk.W)
        self.enhanced_result_label = ttk.Label(result_frame, text="", 
                                              font=("Consolas", 10), 
                                              foreground="blue")
        self.enhanced_result_label.pack(anchor=tk.W, pady=(5, 0))
        
        # 示例按钮
        example_frame = ttk.Frame(test_frame)
        example_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(example_frame, text="加载正则表达式示例", 
                  command=self.load_regex_example).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(example_frame, text="加载批量处理示例", 
                  command=self.load_batch_example).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(example_frame, text="清空映射", 
                  command=self.clear_enhanced_mapping).pack(side=tk.LEFT)
    
    def setup_compare_tab(self, parent):
        """设置对比测试选项卡"""
        # 说明文本
        info_text = """
功能对比说明：

基础版映射组件：
• 支持简单的文本替换
• 基本的增删改查功能
• 导入/导出映射配置
• 适合简单的文件名替换需求

增强版映射组件：
• 支持正则表达式替换
• 支持大小写敏感/不敏感选项
• 批量添加映射规则
• 从文件导入/导出映射
• 映射规则排序功能
• 单个映射规则测试
• 更丰富的错误处理

使用场景：
• 基础版：简单的文本替换，如 "IMG_" -> "照片_"
• 增强版：复杂的模式匹配，如日期格式转换、编号重排等
        """
        
        info_label = ttk.Label(parent, text=info_text, justify=tk.LEFT, 
                              font=("Arial", 10))
        info_label.pack(anchor=tk.W, pady=(0, 20))
        
        # 对比测试区域
        compare_frame = ttk.LabelFrame(parent, text="对比测试", padding="10")
        compare_frame.pack(fill=tk.BOTH, expand=True)
        
        # 测试输入
        input_frame = ttk.Frame(compare_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(input_frame, text="测试文件名:").pack(side=tk.LEFT, padx=(0, 10))
        self.compare_test_entry = ttk.Entry(input_frame, width=50)
        self.compare_test_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.compare_test_entry.insert(0, "IMG_20231201_143022_001.jpg")
        
        ttk.Button(input_frame, text="对比测试", 
                  command=self.compare_test).pack(side=tk.LEFT)
        
        # 结果显示
        result_frame = ttk.Frame(compare_frame)
        result_frame.pack(fill=tk.BOTH, expand=True)
        result_frame.columnconfigure(0, weight=1)
        result_frame.columnconfigure(1, weight=1)
        
        # 基础版结果
        basic_result_frame = ttk.LabelFrame(result_frame, text="基础版结果", padding="10")
        basic_result_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        basic_result_frame.columnconfigure(0, weight=1)
        basic_result_frame.rowconfigure(0, weight=1)
        
        self.compare_basic_text = tk.Text(basic_result_frame, height=10, wrap=tk.WORD, 
                                         font=("Consolas", 9))
        basic_scrollbar = ttk.Scrollbar(basic_result_frame, orient=tk.VERTICAL, 
                                       command=self.compare_basic_text.yview)
        self.compare_basic_text.configure(yscrollcommand=basic_scrollbar.set)
        
        self.compare_basic_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        basic_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 增强版结果
        enhanced_result_frame = ttk.LabelFrame(result_frame, text="增强版结果", padding="10")
        enhanced_result_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        enhanced_result_frame.columnconfigure(0, weight=1)
        enhanced_result_frame.rowconfigure(0, weight=1)
        
        self.compare_enhanced_text = tk.Text(enhanced_result_frame, height=10, wrap=tk.WORD, 
                                            font=("Consolas", 9))
        enhanced_scrollbar = ttk.Scrollbar(enhanced_result_frame, orient=tk.VERTICAL, 
                                          command=self.compare_enhanced_text.yview)
        self.compare_enhanced_text.configure(yscrollcommand=enhanced_scrollbar.set)
        
        self.compare_enhanced_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        enhanced_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 配置权重
        result_frame.rowconfigure(0, weight=1)
    
    def setup_examples(self):
        """设置示例数据"""
        # 基础版示例
        self.photo_example = {
            "IMG_": "照片_",
            "2023": "2023年",
            "12": "12月",
            "01": "01日",
            "_": " "
        }
        
        self.document_example = {
            "doc_": "文档_",
            "temp_": "临时_",
            "draft_": "草稿_",
            "final_": "最终_",
            "_v": "_版本"
        }
        
        # 增强版示例
        self.regex_example = {
            r"\d{4}(\d{2})(\d{2})": {
                'value': r'\1月\2日',
                'use_regex': True,
                'case_sensitive': True
            },
            r"DSC_(\d+)": {
                'value': r'数码相机_\1',
                'use_regex': True,
                'case_sensitive': False
            },
            r"_(\d{3})$": {
                'value': r'_编号\1',
                'use_regex': True,
                'case_sensitive': True
            }
        }
        
        self.batch_example = {
            "IMG_": {
                'value': "照片_",
                'use_regex': False,
                'case_sensitive': True
            },
            "DSC_": {
                'value': "数码相机_",
                'use_regex': False,
                'case_sensitive': False
            },
            "PIC_": {
                'value': "图片_",
                'use_regex': False,
                'case_sensitive': False
            },
            "2023": {
                'value': "2023年",
                'use_regex': False,
                'case_sensitive': True
            },
            "2024": {
                'value': "2024年",
                'use_regex': False,
                'case_sensitive': True
            }
        }
    
    def test_basic_mapping(self):
        """测试基础版映射"""
        filename = self.basic_test_entry.get().strip()
        if not filename:
            return
        
        result = self.basic_mapping.apply_mappings(filename)
        self.basic_result_label.config(text=result)
    
    def test_enhanced_mapping(self):
        """测试增强版映射"""
        filename = self.enhanced_test_entry.get().strip()
        if not filename:
            return
        
        result = self.enhanced_mapping.apply_mappings(filename)
        self.enhanced_result_label.config(text=result)
    
    def compare_test(self):
        """对比测试"""
        filename = self.compare_test_entry.get().strip()
        if not filename:
            return
        
        # 清空结果
        self.compare_basic_text.delete(1.0, tk.END)
        self.compare_enhanced_text.delete(1.0, tk.END)
        
        # 基础版测试
        basic_result = self.basic_mapping.apply_mappings(filename)
        self.compare_basic_text.insert(tk.END, f"输入: {filename}\n")
        self.compare_basic_text.insert(tk.END, f"输出: {basic_result}\n\n")
        self.compare_basic_text.insert(tk.END, "使用的映射规则:\n")
        for key, value in self.basic_mapping.get_mappings().items():
            self.compare_basic_text.insert(tk.END, f"  {key} -> {value}\n")
        
        # 增强版测试
        enhanced_result = self.enhanced_mapping.apply_mappings(filename)
        self.compare_enhanced_text.insert(tk.END, f"输入: {filename}\n")
        self.compare_enhanced_text.insert(tk.END, f"输出: {enhanced_result}\n\n")
        self.compare_enhanced_text.insert(tk.END, "使用的映射规则:\n")
        for key, mapping in self.enhanced_mapping.get_enhanced_mappings().items():
            mapping_type = "正则" if mapping['use_regex'] else "文本"
            case_info = "区分大小写" if mapping['case_sensitive'] else "不区分大小写"
            self.compare_enhanced_text.insert(tk.END, f"  {key} -> {mapping['value']} ({mapping_type}, {case_info})\n")
    
    def load_photo_example(self):
        """加载照片重命名示例"""
        self.basic_mapping.set_mappings(self.photo_example)
        messagebox.showinfo("成功", "已加载照片重命名示例！")
    
    def load_document_example(self):
        """加载文档重命名示例"""
        self.basic_mapping.set_mappings(self.document_example)
        messagebox.showinfo("成功", "已加载文档重命名示例！")
    
    def load_regex_example(self):
        """加载正则表达式示例"""
        self.enhanced_mapping.set_enhanced_mappings(self.regex_example)
        messagebox.showinfo("成功", "已加载正则表达式示例！")
    
    def load_batch_example(self):
        """加载批量处理示例"""
        self.enhanced_mapping.set_enhanced_mappings(self.batch_example)
        messagebox.showinfo("成功", "已加载批量处理示例！")
    
    def clear_basic_mapping(self):
        """清空基础版映射"""
        self.basic_mapping.set_mappings({})
        messagebox.showinfo("成功", "已清空基础版映射！")
    
    def clear_enhanced_mapping(self):
        """清空增强版映射"""
        self.enhanced_mapping.set_enhanced_mappings({})
        messagebox.showinfo("成功", "已清空增强版映射！")
    
    def run(self):
        """运行应用程序"""
        self.root.mainloop()


def main():
    """主函数"""
    app = MappingDemoApp()
    app.run()


if __name__ == "__main__":
    main()
