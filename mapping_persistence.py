# -*- coding: utf-8 -*-
"""
映射配置持久化存储模块
支持保存和加载映射配置到本地文件
"""

import json
import os
import pickle
from typing import Dict, Any, Optional
from datetime import datetime


class MappingPersistence:
    """映射配置持久化管理器"""
    
    def __init__(self, config_dir: str = "mapping_configs"):
        """
        初始化持久化管理器
        
        Args:
            config_dir: 配置文件夹路径
        """
        self.config_dir = config_dir
        self.ensure_config_dir()
    
    def ensure_config_dir(self):
        """确保配置目录存在"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
    
    def save_mapping_config(self, name: str, mappings: Dict[str, Any], 
                           config_type: str = "basic") -> bool:
        """
        保存映射配置
        
        Args:
            name: 配置名称
            mappings: 映射数据
            config_type: 配置类型 ("basic" 或 "enhanced")
            
        Returns:
            是否保存成功
        """
        try:
            config_data = {
                "name": name,
                "type": config_type,
                "mappings": mappings,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            # 保存为JSON格式
            json_file = os.path.join(self.config_dir, f"{name}.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
            
            # 同时保存为pickle格式（用于复杂对象）
            pickle_file = os.path.join(self.config_dir, f"{name}.pkl")
            with open(pickle_file, 'wb') as f:
                pickle.dump(config_data, f)
            
            return True
            
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False
    
    def load_mapping_config(self, name: str) -> Optional[Dict[str, Any]]:
        """
        加载映射配置
        
        Args:
            name: 配置名称
            
        Returns:
            配置数据，如果不存在则返回None
        """
        try:
            # 优先尝试加载JSON格式
            json_file = os.path.join(self.config_dir, f"{name}.json")
            if os.path.exists(json_file):
                with open(json_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            # 如果JSON不存在，尝试pickle格式
            pickle_file = os.path.join(self.config_dir, f"{name}.pkl")
            if os.path.exists(pickle_file):
                with open(pickle_file, 'rb') as f:
                    return pickle.load(f)
            
            return None
            
        except Exception as e:
            print(f"加载配置失败: {e}")
            return None
    
    def list_configs(self) -> list:
        """
        列出所有可用的配置
        
        Returns:
            配置名称列表
        """
        configs = []
        try:
            for filename in os.listdir(self.config_dir):
                if filename.endswith('.json'):
                    name = filename[:-5]  # 移除.json扩展名
                    configs.append(name)
        except Exception as e:
            print(f"列出配置失败: {e}")
        
        return sorted(configs)
    
    def delete_config(self, name: str) -> bool:
        """
        删除配置
        
        Args:
            name: 配置名称
            
        Returns:
            是否删除成功
        """
        try:
            json_file = os.path.join(self.config_dir, f"{name}.json")
            pickle_file = os.path.join(self.config_dir, f"{name}.pkl")
            
            deleted = False
            if os.path.exists(json_file):
                os.remove(json_file)
                deleted = True
            
            if os.path.exists(pickle_file):
                os.remove(pickle_file)
                deleted = True
            
            return deleted
            
        except Exception as e:
            print(f"删除配置失败: {e}")
            return False
    
    def get_config_info(self, name: str) -> Optional[Dict[str, Any]]:
        """
        获取配置信息（不包含映射数据）
        
        Args:
            name: 配置名称
            
        Returns:
            配置信息字典
        """
        config = self.load_mapping_config(name)
        if config:
            return {
                "name": config.get("name", name),
                "type": config.get("type", "unknown"),
                "created_at": config.get("created_at", "unknown"),
                "updated_at": config.get("updated_at", "unknown"),
                "mapping_count": len(config.get("mappings", {}))
            }
        return None
    
    def export_config(self, name: str, export_path: str) -> bool:
        """
        导出配置到指定路径
        
        Args:
            name: 配置名称
            export_path: 导出路径
            
        Returns:
            是否导出成功
        """
        try:
            config = self.load_mapping_config(name)
            if not config:
                return False
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"导出配置失败: {e}")
            return False
    
    def import_config(self, import_path: str, name: Optional[str] = None) -> bool:
        """
        从指定路径导入配置
        
        Args:
            import_path: 导入路径
            name: 新配置名称，如果为None则使用原名称
            
        Returns:
            是否导入成功
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            if name:
                config["name"] = name
            
            config["updated_at"] = datetime.now().isoformat()
            
            return self.save_mapping_config(
                config["name"], 
                config["mappings"], 
                config.get("type", "basic")
            )
            
        except Exception as e:
            print(f"导入配置失败: {e}")
            return False


class MappingConfigManager:
    """映射配置管理器 - 提供GUI界面"""
    
    def __init__(self, parent, persistence: MappingPersistence):
        """
        初始化配置管理器
        
        Args:
            parent: 父组件
            persistence: 持久化管理器
        """
        self.parent = parent
        self.persistence = persistence
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        self.frame = ttk.LabelFrame(self.parent, text="映射配置管理", padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # 配置列表
        list_frame = ttk.Frame(self.frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # 创建Treeview
        columns = ('名称', '类型', '映射数量', '创建时间', '更新时间')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)
        
        # 设置列标题
        self.tree.heading('名称', text='配置名称')
        self.tree.heading('类型', text='类型')
        self.tree.heading('映射数量', text='映射数量')
        self.tree.heading('创建时间', text='创建时间')
        self.tree.heading('更新时间', text='更新时间')
        
        # 设置列宽
        self.tree.column('名称', width=150)
        self.tree.column('类型', width=80)
        self.tree.column('映射数量', width=80)
        self.tree.column('创建时间', width=120)
        self.tree.column('更新时间', width=120)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 按钮区域
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="刷新列表", 
                  command=self.refresh_list).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="保存当前配置", 
                  command=self.save_current_config).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="加载选中配置", 
                  command=self.load_selected_config).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="删除选中配置", 
                  command=self.delete_selected_config).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="导出配置", 
                  command=self.export_selected_config).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="导入配置", 
                  command=self.import_config).pack(side=tk.LEFT)
        
        # 初始化列表
        self.refresh_list()
    
    def refresh_list(self):
        """刷新配置列表"""
        # 清空现有项目
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 添加配置项目
        configs = self.persistence.list_configs()
        for name in configs:
            info = self.persistence.get_config_info(name)
            if info:
                self.tree.insert('', tk.END, values=(
                    info['name'],
                    info['type'],
                    info['mapping_count'],
                    info['created_at'][:19],  # 只显示日期时间部分
                    info['updated_at'][:19]
                ))
    
    def save_current_config(self):
        """保存当前配置"""
        from tkinter import simpledialog
        
        name = simpledialog.askstring("保存配置", "请输入配置名称:")
        if not name:
            return
        
        # 这里需要从实际的映射组件获取数据
        # 由于这是一个通用组件，需要子类重写此方法
        self.on_save_config(name)
    
    def load_selected_config(self):
        """加载选中的配置"""
        selection = self.tree.selection()
        if not selection:
            from tkinter import messagebox
            messagebox.showwarning("警告", "请选择要加载的配置！")
            return
        
        item = self.tree.item(selection[0])
        name = item['values'][0]
        
        config = self.persistence.load_mapping_config(name)
        if config:
            self.on_load_config(config)
        else:
            from tkinter import messagebox
            messagebox.showerror("错误", f"无法加载配置: {name}")
    
    def delete_selected_config(self):
        """删除选中的配置"""
        selection = self.tree.selection()
        if not selection:
            from tkinter import messagebox
            messagebox.showwarning("警告", "请选择要删除的配置！")
            return
        
        item = self.tree.item(selection[0])
        name = item['values'][0]
        
        from tkinter import messagebox
        if messagebox.askyesno("确认", f"确定要删除配置 '{name}' 吗？"):
            if self.persistence.delete_config(name):
                messagebox.showinfo("成功", f"配置 '{name}' 已删除！")
                self.refresh_list()
            else:
                messagebox.showerror("错误", f"删除配置 '{name}' 失败！")
    
    def export_selected_config(self):
        """导出选中的配置"""
        selection = self.tree.selection()
        if not selection:
            from tkinter import messagebox
            messagebox.showwarning("警告", "请选择要导出的配置！")
            return
        
        item = self.tree.item(selection[0])
        name = item['values'][0]
        
        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(
            title="导出配置",
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")],
            initialvalue=f"{name}.json"
        )
        
        if file_path:
            if self.persistence.export_config(name, file_path):
                from tkinter import messagebox
                messagebox.showinfo("成功", f"配置已导出到: {file_path}")
            else:
                from tkinter import messagebox
                messagebox.showerror("错误", "导出配置失败！")
    
    def import_config(self):
        """导入配置"""
        from tkinter import filedialog, simpledialog, messagebox
        
        file_path = filedialog.askopenfilename(
            title="导入配置",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if file_path:
            name = simpledialog.askstring("导入配置", "请输入新配置名称:")
            if name:
                if self.persistence.import_config(file_path, name):
                    messagebox.showinfo("成功", f"配置已导入为: {name}")
                    self.refresh_list()
                else:
                    messagebox.showerror("错误", "导入配置失败！")
    
    def on_save_config(self, name: str):
        """保存配置回调 - 需要子类重写"""
        pass
    
    def on_load_config(self, config: Dict[str, Any]):
        """加载配置回调 - 需要子类重写"""
        pass
