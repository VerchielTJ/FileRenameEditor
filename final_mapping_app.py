#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终版文件重命名工具 - 集成所有映射功能
包含基础版、增强版映射组件和持久化存储
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
from typing import List, Tuple, Dict
from enhanced_mapping_widget import EnhancedMappingListWidget
from mapping_persistence import MappingPersistence, MappingConfigManager


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
    
    def apply_mapping_rename(self, mappings: Dict[str, Dict]) -> List[Tuple[str, str, bool, str]]:
        """应用映射重命名"""
        if not self.file_manager.current_path:
            return []
        
        results = []
        for file in self.file_manager.files:
            try:
                # 应用映射替换
                new_name = file
                for key, mapping in mappings.items():
                    if mapping['use_regex']:
                        import re
                        flags = 0 if mapping['case_sensitive'] else re.IGNORECASE
                        pattern = re.compile(key, flags)
                        new_name = pattern.sub(mapping['value'], new_name)
                    else:
                        if mapping['case_sensitive']:
                            new_name = new_name.replace(key, mapping['value'])
                        else:
                            import re
                            new_name = re.sub(re.escape(key), mapping['value'], new_name, flags=re.IGNORECASE)
                
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
        self.root.title("文件重命名工具 - 最终版")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # 创建变量
        self.current_path = tk.StringVar()
        
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
        title_label = ttk.Label(main_frame, text="文件重命名工具 - 最终版", 
                               font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 创建选项卡
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 映射编辑选项卡
        mapping_frame = ttk.Frame(notebook, padding="10")
        notebook.add(mapping_frame, text="映射编辑")
        
        # 文件操作选项卡
        file_frame = ttk.Frame(notebook, padding="10")
        notebook.add(file_frame, text="文件操作")
        
        # 配置管理选项卡
        config_frame = ttk.Frame(notebook, padding="10")
        notebook.add(config_frame, text="配置管理")
        
        # 设置各个选项卡
        self.setup_mapping_tab(mapping_frame)
        self.setup_file_tab(file_frame)
        self.setup_config_tab(config_frame)
        
        # 打包滚动组件
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_mapping_tab(self, parent):
        """设置映射编辑选项卡"""
        # 增强版映射组件
        self.mapping_widget = EnhancedMappingListWidget(parent)
        
        # 测试区域
        test_frame = ttk.LabelFrame(parent, text="映射测试", padding="10")
        test_frame.pack(fill=tk.X, pady=(20, 0))
        
        # 文件名输入
        input_frame = ttk.Frame(test_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(input_frame, text="测试文件名:").pack(side=tk.LEFT, padx=(0, 10))
        self.test_entry = ttk.Entry(input_frame, width=50)
        self.test_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.test_entry.insert(0, "IMG_20231201_143022_001.jpg")
        
        ttk.Button(input_frame, text="测试映射", 
                  command=self.controller.test_mapping).pack(side=tk.LEFT)
        
        # 结果显示
        result_frame = ttk.Frame(test_frame)
        result_frame.pack(fill=tk.X)
        
        ttk.Label(result_frame, text="替换结果:").pack(anchor=tk.W)
        self.result_label = ttk.Label(result_frame, text="", 
                                     font=("Consolas", 10), 
                                     foreground="blue")
        self.result_label.pack(anchor=tk.W, pady=(5, 0))
        
        # 示例按钮
        example_frame = ttk.Frame(test_frame)
        example_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(example_frame, text="加载照片示例", 
                  command=self.controller.load_photo_example).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(example_frame, text="加载文档示例", 
                  command=self.controller.load_document_example).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(example_frame, text="加载正则示例", 
                  command=self.controller.load_regex_example).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(example_frame, text="清空映射", 
                  command=self.controller.clear_mapping).pack(side=tk.LEFT)
    
    def setup_file_tab(self, parent):
        """设置文件操作选项卡"""
        # 路径选择区域
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
        
        # 文件列表区域
        file_list_frame = ttk.LabelFrame(parent, text="文件列表", padding="10")
        file_list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        file_list_frame.columnconfigure(0, weight=1)
        file_list_frame.rowconfigure(0, weight=1)
        
        # 文件列表
        self.file_list = tk.Listbox(file_list_frame, font=("Consolas", 10))
        file_scrollbar = ttk.Scrollbar(file_list_frame, orient=tk.VERTICAL, command=self.file_list.yview)
        self.file_list.configure(yscrollcommand=file_scrollbar.set)
        
        self.file_list.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        file_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 操作按钮区域
        operation_frame = ttk.LabelFrame(parent, text="重命名操作", padding="10")
        operation_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(operation_frame, text="预览重命名", 
                  command=self.controller.preview_rename).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(operation_frame, text="执行重命名", 
                  command=self.controller.execute_rename).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(operation_frame, text="刷新文件列表", 
                  command=self.controller.refresh_file_list).pack(side=tk.LEFT)
        
        # 状态显示区域
        status_frame = ttk.LabelFrame(parent, text="操作状态", padding="10")
        status_frame.pack(fill=tk.BOTH, expand=True)
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)
        
        self.status_text = tk.Text(status_frame, height=8, wrap=tk.WORD, font=("Consolas", 9))
        status_scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=status_scrollbar.set)
        
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        status_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    
    def setup_config_tab(self, parent):
        """设置配置管理选项卡"""
        # 配置管理器
        self.config_manager = MappingConfigManager(parent, self.controller.persistence)
        self.config_manager.on_save_config = self.controller.save_config
        self.config_manager.on_load_config = self.controller.load_config
    
    def update_status(self, message: str):
        """更新状态信息"""
        self.status_text.insert(tk.END, message)
        self.status_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_file_list(self, files: List[str]):
        """更新文件列表"""
        self.file_list.delete(0, tk.END)
        for file in files:
            self.file_list.insert(tk.END, file)
    
    def get_path(self) -> str:
        return self.current_path.get().strip()
    
    def set_path(self, path: str):
        self.current_path.set(path)
    
    def get_test_filename(self) -> str:
        return self.test_entry.get().strip()
    
    def set_test_result(self, result: str):
        self.result_label.config(text=result)
    
    def get_mappings(self) -> Dict[str, Dict]:
        """获取映射字典"""
        return self.mapping_widget.get_enhanced_mappings()
    
    def set_mappings(self, mappings: Dict[str, Dict]):
        """设置映射字典"""
        self.mapping_widget.set_enhanced_mappings(mappings)
    
    def run(self):
        self.root.mainloop()


# ==================== CONTROLLER层 ====================
class MainController:
    """主控制器 - Controller层"""
    
    def __init__(self):
        # 创建Model层实例
        self.file_manager = FileManager()
        self.rename_operations = RenameOperations(self.file_manager)
        self.persistence = MappingPersistence()
        
        # 创建View层实例
        self.view = MainWindow(self)
        
        # 初始化
        self.view.set_path(os.getcwd())
        self.view.update_status("欢迎使用文件重命名工具！(最终版)\n")
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
            self.view.update_file_list(files)
            
            if files:
                self.view.update_status("文件列表已更新\n")
            else:
                self.view.update_status("该文件夹为空\n")
        else:
            messagebox.showerror("错误", f"无法访问路径: {path}")
    
    def refresh_file_list(self):
        """刷新文件列表"""
        if self.file_manager.current_path:
            self.confirm_path()
        else:
            messagebox.showwarning("警告", "请先确认工作路径！")
    
    def test_mapping(self):
        """测试映射功能"""
        filename = self.view.get_test_filename()
        if not filename:
            return
        
        mappings = self.view.get_mappings()
        if not mappings:
            messagebox.showwarning("警告", "请先添加一些映射规则！")
            return
        
        result = self.view.mapping_widget.apply_mappings(filename)
        self.view.set_test_result(result)
    
    def preview_rename(self):
        """预览重命名"""
        mappings = self.view.get_mappings()
        if not mappings:
            messagebox.showwarning("警告", "请先添加映射规则！")
            return
        
        if not self.file_manager.current_path:
            messagebox.showerror("错误", "请先确认工作路径！")
            return
        
        self.view.update_status(f"\n重命名预览:\n")
        self.view.update_status(f"映射规则: {len(mappings)} 个\n")
        
        files = self.file_manager.get_files()
        for file in files:
            new_name = self.view.mapping_widget.apply_mappings(file)
            if new_name != file:
                self.view.update_status(f"  {file} -> {new_name}\n")
            else:
                self.view.update_status(f"  {file} (无需重命名)\n")
    
    def execute_rename(self):
        """执行重命名"""
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
        
        self.view.update_status(f"\n开始重命名操作...\n")
        
        results = self.rename_operations.apply_mapping_rename(mappings)
        
        success_count = 0
        for old_name, new_name, success, error in results:
            if success:
                self.view.update_status(f"✓ {old_name} -> {new_name}\n")
                success_count += 1
            else:
                self.view.update_status(f"✗ {old_name} -> {new_name} ({error})\n")
        
        self.view.update_status(f"\n重命名完成！成功重命名 {success_count} 个文件\n")
        
        # 刷新文件列表
        self.refresh_file_list()
    
    def load_photo_example(self):
        """加载照片重命名示例"""
        example = {
            "IMG_": {
                'value': "照片_",
                'use_regex': False,
                'case_sensitive': True
            },
            "2023": {
                'value': "2023年",
                'use_regex': False,
                'case_sensitive': True
            },
            "12": {
                'value': "12月",
                'use_regex': False,
                'case_sensitive': True
            },
            "01": {
                'value': "01日",
                'use_regex': False,
                'case_sensitive': True
            },
            "_": {
                'value': " ",
                'use_regex': False,
                'case_sensitive': True
            }
        }
        self.view.set_mappings(example)
        messagebox.showinfo("成功", "已加载照片重命名示例！")
    
    def load_document_example(self):
        """加载文档重命名示例"""
        example = {
            "doc_": {
                'value': "文档_",
                'use_regex': False,
                'case_sensitive': True
            },
            "temp_": {
                'value': "临时_",
                'use_regex': False,
                'case_sensitive': True
            },
            "draft_": {
                'value': "草稿_",
                'use_regex': False,
                'case_sensitive': True
            },
            "final_": {
                'value': "最终_",
                'use_regex': False,
                'case_sensitive': True
            },
            "_v": {
                'value': "_版本",
                'use_regex': False,
                'case_sensitive': True
            }
        }
        self.view.set_mappings(example)
        messagebox.showinfo("成功", "已加载文档重命名示例！")
    
    def load_regex_example(self):
        """加载正则表达式示例"""
        example = {
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
        self.view.set_mappings(example)
        messagebox.showinfo("成功", "已加载正则表达式示例！")
    
    def clear_mapping(self):
        """清空映射"""
        self.view.set_mappings({})
        messagebox.showinfo("成功", "已清空映射！")
    
    def save_config(self, name: str):
        """保存配置"""
        mappings = self.view.get_mappings()
        if self.persistence.save_mapping_config(name, mappings, "enhanced"):
            messagebox.showinfo("成功", f"配置 '{name}' 已保存！")
            self.view.config_manager.refresh_list()
        else:
            messagebox.showerror("错误", "保存配置失败！")
    
    def load_config(self, config: Dict[str, any]):
        """加载配置"""
        mappings = config.get("mappings", {})
        self.view.set_mappings(mappings)
        messagebox.showinfo("成功", f"配置 '{config['name']}' 已加载！")


# ==================== 程序入口 ====================
def main():
    """主函数"""
    app = MainController()
    app.run()


if __name__ == "__main__":
    main()
