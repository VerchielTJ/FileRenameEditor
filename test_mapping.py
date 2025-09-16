#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
映射组件测试程序
"""

import tkinter as tk
from tkinter import ttk
from mapping_widget import MappingListWidget


class MappingTestApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("映射列表组件测试")
        self.root.geometry("800x600")
        
        self.setup_ui()
    
    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="映射列表组件测试", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 映射组件
        self.mapping_widget = MappingListWidget(main_frame)
        
        # 测试区域
        test_frame = ttk.LabelFrame(main_frame, text="测试映射替换", padding="10")
        test_frame.pack(fill=tk.X, pady=(20, 0))
        
        # 文件名输入
        input_frame = ttk.Frame(test_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(input_frame, text="测试文件名:").pack(side=tk.LEFT, padx=(0, 10))
        self.test_entry = ttk.Entry(input_frame, width=50)
        self.test_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.test_entry.insert(0, "IMG_20231201_143022.jpg")
        
        ttk.Button(input_frame, text="应用映射", 
                  command=self.test_mapping).pack(side=tk.LEFT)
        
        # 结果显示
        result_frame = ttk.Frame(test_frame)
        result_frame.pack(fill=tk.X)
        
        ttk.Label(result_frame, text="替换结果:").pack(anchor=tk.W)
        self.result_label = ttk.Label(result_frame, text="", 
                                     font=("Consolas", 10), 
                                     foreground="blue")
        self.result_label.pack(anchor=tk.W, pady=(5, 0))
        
        # 示例映射
        self.setup_example_mappings()
    
    def setup_example_mappings(self):
        """设置示例映射"""
        example_mappings = {
            "IMG_": "照片_",
            "2023": "2023年",
            "12": "12月",
            "01": "01日",
            "_": " "
        }
        self.mapping_widget.set_mappings(example_mappings)
    
    def test_mapping(self):
        """测试映射替换"""
        filename = self.test_entry.get().strip()
        if not filename:
            return
        
        result = self.mapping_widget.apply_mappings(filename)
        self.result_label.config(text=result)
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MappingTestApp()
    app.run()
