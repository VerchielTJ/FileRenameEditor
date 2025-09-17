# -*- coding: utf-8 -*-
"""
主窗口视图 - 文件重命名工具的主界面
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from typing import Dict, Any
from .components.mapping_widget import MappingListWidget
from models.config_manager import ConfigManager


class MainWindow:
    """主窗口类"""
    
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("文件重命名工具 - 支持映射替换")
        self.root.geometry("900x900")
        self.root.resizable(True, True)
        
        # 当前工作路径
        self.current_path = tk.StringVar()
        self.current_path.set(os.getcwd())
        
        # 前缀和后缀
        self.prefix = tk.StringVar()
        self.suffix = tk.StringVar()
        
        # 配置管理器
        self.config_manager = ConfigManager()
        
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
        
        # 标题和菜单栏
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        title_frame.columnconfigure(0, weight=1)
        
        title_label = ttk.Label(title_frame, text="文件重命名工具", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # 配置管理按钮
        config_frame = ttk.Frame(title_frame)
        config_frame.grid(row=0, column=1, sticky=tk.E)
        
        ttk.Button(config_frame, text="保存配置", 
                  command=self.save_config).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(config_frame, text="加载配置", 
                  command=self.load_config).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(config_frame, text="配置管理", 
                  command=self.show_config_manager).pack(side=tk.LEFT)
        
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
        rename_frame = ttk.LabelFrame(parent, text="重命名设置", padding="15")
        rename_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        rename_frame.columnconfigure(1, weight=1)
        
        # 前缀和后缀设置区域
        prefix_suffix_frame = ttk.Frame(rename_frame)
        prefix_suffix_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        prefix_suffix_frame.columnconfigure(1, weight=1)
        prefix_suffix_frame.columnconfigure(3, weight=1)
        
        # 前缀设置
        prefix_label = ttk.Label(prefix_suffix_frame, text="添加前缀:", font=("Arial", 10, "bold"))
        prefix_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.prefix_entry = ttk.Entry(prefix_suffix_frame, textvariable=self.prefix, 
                                     width=25, font=("Consolas", 11))
        self.prefix_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 20))
        
        # 后缀设置
        suffix_label = ttk.Label(prefix_suffix_frame, text="添加后缀:", font=("Arial", 10, "bold"))
        suffix_label.grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        
        self.suffix_entry = ttk.Entry(prefix_suffix_frame, textvariable=self.suffix, 
                                     width=25, font=("Consolas", 11))
        self.suffix_entry.grid(row=0, column=3, sticky=(tk.W, tk.E))
        
        # 映射列表组件
        self.mapping_widget = MappingListWidget(rename_frame)
        
        # 重命名按钮区域
        button_frame = ttk.Frame(rename_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=(20, 0))
        
        # 按钮样式
        button_style = ttk.Style()
        button_style.configure("Action.TButton", font=("Arial", 10, "bold"))
        
        preview_btn = ttk.Button(button_frame, text="预览重命名", 
                                command=self.preview_rename, style="Action.TButton")
        preview_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        execute_btn = ttk.Button(button_frame, text="执行重命名", 
                                command=self.execute_rename, style="Action.TButton")
        execute_btn.pack(side=tk.LEFT)
    
    def create_status_section(self, parent, row):
        """创建状态显示区域"""
        status_frame = ttk.LabelFrame(parent, text="状态信息", padding="15")
        status_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), 
                         pady=(10, 0))
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)
        
        # 状态文本框
        self.status_text = tk.Text(status_frame, height=12, wrap=tk.WORD, 
                                  font=("Consolas", 10))
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
    
    def save_config(self):
        """保存当前配置"""
        # 获取当前配置信息
        work_path = self.get_current_path()
        prefix = self.get_prefix()
        suffix = self.get_suffix()
        mappings = self.get_mappings()
        
        if not work_path:
            messagebox.showerror("错误", "请先设置工作路径！")
            return
        
        # 创建保存配置对话框
        self.show_save_config_dialog(work_path, prefix, suffix, mappings)
    
    def show_save_config_dialog(self, work_path: str, prefix: str, suffix: str, mappings: Dict[str, str]):
        """显示保存配置对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("保存工作配置")
        dialog.geometry("500x300")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 100, self.root.winfo_rooty() + 100))
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 配置名称
        ttk.Label(frame, text="配置名称:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        name_var = tk.StringVar()
        name_var.set(f"配置_{self.get_timestamp()}")
        name_entry = ttk.Entry(frame, textvariable=name_var, width=40)
        name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 配置描述
        ttk.Label(frame, text="配置描述:").grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        desc_text = tk.Text(frame, height=4, width=40)
        desc_text.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 配置预览
        preview_frame = ttk.LabelFrame(frame, text="配置预览", padding="10")
        preview_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        preview_frame.columnconfigure(0, weight=1)
        
        preview_text = tk.Text(preview_frame, height=6, width=50, font=("Consolas", 9))
        preview_text.pack(fill=tk.BOTH, expand=True)
        
        # 生成预览内容
        preview_content = f"""工作路径: {work_path}
前缀: {prefix or '(无)'}
后缀: {suffix or '(无)'}
映射规则: {len(mappings)} 条"""
        
        if mappings:
            preview_content += "\n\n映射详情:"
            for key, value in mappings.items():
                preview_content += f"\n  '{key}' -> '{value}'"
        
        preview_text.insert(tk.END, preview_content)
        preview_text.config(state=tk.DISABLED)
        
        # 按钮
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(20, 0))
        
        def save_config_file():
            name = name_var.get().strip()
            description = desc_text.get("1.0", tk.END).strip()
            
            if not name:
                messagebox.showerror("错误", "请输入配置名称！")
                return
            
            # 选择保存位置
            file_path = filedialog.asksaveasfilename(
                title="保存配置文件",
                defaultextension=".fre",
                filetypes=[("文件重命名配置", "*.fre"), ("所有文件", "*.*")],
                initialname=f"{name}.fre"
            )
            
            if file_path:
                # 创建配置
                config = self.config_manager.create_config(
                    work_path=work_path,
                    prefix=prefix,
                    suffix=suffix,
                    mappings=mappings,
                    name=name,
                    description=description
                )
                
                # 保存配置
                if self.config_manager.save_config(config, file_path):
                    messagebox.showinfo("成功", f"配置已保存到:\n{file_path}")
                    dialog.destroy()
                else:
                    messagebox.showerror("错误", "保存配置失败！")
        
        ttk.Button(button_frame, text="保存", command=save_config_file).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT)
    
    def load_config(self):
        """加载配置文件"""
        file_path = filedialog.askopenfilename(
            title="加载配置文件",
            filetypes=[("文件重命名配置", "*.fre"), ("所有文件", "*.*")]
        )
        
        if file_path:
            config = self.config_manager.load_config(file_path)
            if config:
                self.apply_config(config)
                messagebox.showinfo("成功", f"配置已加载:\n{config.get('name', '未命名配置')}")
            else:
                messagebox.showerror("错误", "加载配置文件失败！")
    
    def apply_config(self, config: Dict[str, Any]):
        """应用配置到界面"""
        # 设置工作路径
        if config.get("work_path"):
            self.current_path.set(config["work_path"])
        
        # 设置前缀和后缀
        if config.get("prefix"):
            self.prefix.set(config["prefix"])
        else:
            self.prefix.set("")
        
        if config.get("suffix"):
            self.suffix.set(config["suffix"])
        else:
            self.suffix.set("")
        
        # 设置映射
        mappings = config.get("mappings", {})
        self.mapping_widget.set_mappings(mappings)
        
        # 更新状态
        self.update_status(f"已加载配置: {config.get('name', '未命名配置')}\n")
        self.update_status(f"工作路径: {config.get('work_path', '')}\n")
        self.update_status(f"前缀: {config.get('prefix', '')}\n")
        self.update_status(f"后缀: {config.get('suffix', '')}\n")
        self.update_status(f"映射规则: {len(mappings)} 条\n")
    
    def show_config_manager(self):
        """显示配置管理器"""
        dialog = tk.Toplevel(self.root)
        dialog.title("配置管理器")
        dialog.geometry("600x400")
        dialog.resizable(True, True)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        frame = ttk.Frame(dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        ttk.Label(frame, text="配置管理器", font=("Arial", 14, "bold")).pack(pady=(0, 10))
        
        # 说明文字
        info_label = ttk.Label(frame, 
                              text="选择配置文件进行加载，或查看配置详情",
                              font=("Arial", 10))
        info_label.pack(pady=(0, 10))
        
        # 文件选择区域
        file_frame = ttk.Frame(frame)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(file_frame, text="选择配置文件", 
                  command=lambda: self.select_config_file(dialog)).pack(side=tk.LEFT, padx=(0, 10))
        
        # 配置详情显示区域
        detail_frame = ttk.LabelFrame(frame, text="配置详情", padding="10")
        detail_frame.pack(fill=tk.BOTH, expand=True)
        
        detail_text = tk.Text(detail_frame, wrap=tk.WORD, font=("Consolas", 9))
        scrollbar = ttk.Scrollbar(detail_frame, orient=tk.VERTICAL, command=detail_text.yview)
        detail_text.configure(yscrollcommand=scrollbar.set)
        
        detail_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 按钮区域
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        def load_selected_config():
            # 这里可以实现加载选中配置的逻辑
            pass
        
        ttk.Button(button_frame, text="加载配置", 
                  command=load_selected_config).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="关闭", 
                  command=dialog.destroy).pack(side=tk.LEFT)
        
        # 存储对话框引用以便其他方法使用
        dialog.detail_text = detail_text
    
    def select_config_file(self, dialog):
        """选择配置文件并显示详情"""
        file_path = filedialog.askopenfilename(
            title="选择配置文件",
            filetypes=[("文件重命名配置", "*.fre"), ("所有文件", "*.*")]
        )
        
        if file_path:
            config = self.config_manager.load_config(file_path)
            if config:
                # 显示配置详情
                summary = self.config_manager.export_config_summary(config)
                dialog.detail_text.delete("1.0", tk.END)
                dialog.detail_text.insert("1.0", summary)
            else:
                dialog.detail_text.delete("1.0", tk.END)
                dialog.detail_text.insert("1.0", "加载配置文件失败！")
    
    def get_timestamp(self):
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().strftime('%Y%m%d_%H%M%S')
    
    def run(self):
        """运行应用程序"""
        self.root.mainloop()
