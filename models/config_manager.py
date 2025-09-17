# -*- coding: utf-8 -*-
"""
配置管理器 - 负责工作配置的保存和加载
支持 .fre 配置文件格式
"""

import json
import os
from typing import Dict, Any, Optional
from datetime import datetime


class ConfigManager:
    """配置管理器类 - 支持字段向前和向后兼容"""
    
    def __init__(self):
        # 配置文件版本，用于未来兼容性
        self.config_version = "1.0"
        
        # 当前工具支持的字段（核心字段）
        self.supported_fields = {
            "version": str,
            "created_at": str,
            "updated_at": str,
            "name": str,
            "description": str,
            "work_path": str,
            "prefix": str,
            "suffix": str,
            "delete_chars": str,
            "mappings": dict,
            "settings": dict
        }
        
        # 默认配置结构
        self.default_config = {
            "version": self.config_version,
            "created_at": "",
            "updated_at": "",
            "name": "",
            "description": "",
            "work_path": "",
            "prefix": "",
            "suffix": "",
            "delete_chars": "",
            "mappings": {},
            # 未来可扩展的字段
            "settings": {
                "case_sensitive": True,
                "include_subfolders": False,
                "backup_original": False
            }
        }
    
    def create_config(self, 
                     work_path: str,
                     prefix: str = "",
                     suffix: str = "",
                     delete_chars: str = "",
                     mappings: Dict[str, str] = None,
                     name: str = "",
                     description: str = "") -> Dict[str, Any]:
        """创建配置字典"""
        if mappings is None:
            mappings = {}
        
        config = self.default_config.copy()
        config.update({
            "version": self.config_version,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "name": name or f"配置_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "description": description,
            "work_path": work_path,
            "prefix": prefix,
            "suffix": suffix,
            "delete_chars": delete_chars,
            "mappings": mappings
        })
        
        return config
    
    def save_config(self, config: Dict[str, Any], file_path: str) -> bool:
        """保存配置到 .fre 文件 - 保留所有字段"""
        try:
            # 创建配置副本，避免修改原始配置
            save_config = config.copy()
            
            # 更新保存时间
            save_config["updated_at"] = datetime.now().isoformat()
            
            # 确保版本字段存在
            if "version" not in save_config:
                save_config["version"] = self.config_version
            
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # 保存为 JSON 格式，保留所有字段
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(save_config, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False
    
    def load_config(self, file_path: str) -> Optional[Dict[str, Any]]:
        """从 .fre 文件加载配置 - 支持字段兼容性"""
        try:
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)
            
            # 使用兼容性加载，保留所有字段
            config = self._load_config_with_compatibility(loaded_config)
            
            return config
            
        except Exception as e:
            print(f"加载配置失败: {e}")
            return None
    
    def _load_config_with_compatibility(self, loaded_config: Dict[str, Any]) -> Dict[str, Any]:
        """兼容性加载配置 - 处理字段匹配和缺失"""
        # 从默认配置开始
        config = self.default_config.copy()
        
        # 保留所有原始字段（包括未知字段）
        config.update(loaded_config)
        
        # 处理支持的字段，确保类型正确
        for field_name, expected_type in self.supported_fields.items():
            if field_name in loaded_config:
                value = loaded_config[field_name]
                
                # 类型检查和转换
                if expected_type == str and not isinstance(value, str):
                    config[field_name] = str(value) if value is not None else ""
                elif expected_type == dict and not isinstance(value, dict):
                    config[field_name] = {} if value is None else {}
                elif expected_type == bool and not isinstance(value, bool):
                    config[field_name] = bool(value) if value is not None else False
                else:
                    config[field_name] = value
            else:
                # 字段不存在，使用默认值
                if field_name in self.default_config:
                    config[field_name] = self.default_config[field_name]
        
        # 特殊处理嵌套字典（如settings）
        if "settings" in loaded_config and isinstance(loaded_config["settings"], dict):
            # 合并settings，保留未知设置
            if "settings" not in config:
                config["settings"] = {}
            config["settings"].update(loaded_config["settings"])
        
        # 确保mappings是字典
        if "mappings" not in config or not isinstance(config["mappings"], dict):
            config["mappings"] = {}
        
        # 更新时间戳
        if "updated_at" not in loaded_config:
            config["updated_at"] = datetime.now().isoformat()
        
        return config
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """验证配置文件格式 - 宽松验证，只检查关键字段"""
        try:
            # 只检查最基本的必需字段
            critical_fields = ["version"]
            for field in critical_fields:
                if field not in config:
                    print(f"配置文件缺少关键字段: {field}")
                    return False
            
            # 检查是否为有效的字典
            if not isinstance(config, dict):
                print("配置文件必须是有效的JSON对象")
                return False
            
            # 检查版本字段
            if not isinstance(config.get("version"), str):
                print("version 字段必须是字符串")
                return False
            
            return True
            
        except Exception as e:
            print(f"配置文件验证失败: {e}")
            return False
    
    def get_config_info(self, config: Dict[str, Any]) -> Dict[str, str]:
        """获取配置信息摘要"""
        return {
            "name": config.get("name", "未命名配置"),
            "description": config.get("description", "无描述"),
            "work_path": config.get("work_path", ""),
            "created_at": config.get("created_at", ""),
            "updated_at": config.get("updated_at", ""),
            "version": config.get("version", "未知版本")
        }
    
    def merge_configs(self, base_config: Dict[str, Any], 
                     new_config: Dict[str, Any]) -> Dict[str, Any]:
        """合并配置（用于更新现有配置） - 保留所有字段"""
        merged = base_config.copy()
        
        # 特殊处理嵌套字典（先处理，避免被覆盖）
        if "mappings" in new_config and isinstance(new_config["mappings"], dict):
            if "mappings" not in merged:
                merged["mappings"] = {}
            merged["mappings"].update(new_config["mappings"])
        
        if "settings" in new_config and isinstance(new_config["settings"], dict):
            if "settings" not in merged:
                merged["settings"] = {}
            merged["settings"].update(new_config["settings"])
        
        # 更新其他字段，包括未知字段
        for key, value in new_config.items():
            if key in ["mappings", "settings"]:
                # 已经处理过的嵌套字典，跳过
                continue
            elif key in self.supported_fields:
                # 支持的字段，进行类型检查
                expected_type = self.supported_fields[key]
                if expected_type == str and not isinstance(value, str):
                    merged[key] = str(value) if value is not None else ""
                elif expected_type == dict and not isinstance(value, dict):
                    merged[key] = {} if value is None else {}
                else:
                    merged[key] = value
            else:
                # 未知字段，直接保留
                merged[key] = value
        
        # 确保mappings和settings字段存在
        if "mappings" not in merged:
            merged["mappings"] = {}
        if "settings" not in merged:
            merged["settings"] = {}
        
        # 更新时间
        merged["updated_at"] = datetime.now().isoformat()
        
        return merged
    
    def get_supported_fields(self) -> Dict[str, type]:
        """获取当前工具支持的字段列表"""
        return self.supported_fields.copy()
    
    def get_unknown_fields(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """获取配置中的未知字段"""
        unknown_fields = {}
        for key, value in config.items():
            if key not in self.supported_fields:
                unknown_fields[key] = value
        return unknown_fields
    
    def add_supported_field(self, field_name: str, field_type: type, default_value: Any = None):
        """动态添加支持的字段（用于扩展）"""
        self.supported_fields[field_name] = field_type
        if default_value is not None:
            self.default_config[field_name] = default_value
    
    def is_field_supported(self, field_name: str) -> bool:
        """检查字段是否被当前工具支持"""
        return field_name in self.supported_fields
    
    def export_config_summary(self, config: Dict[str, Any]) -> str:
        """导出配置摘要为文本 - 包含未知字段信息"""
        info = self.get_config_info(config)
        mappings = config.get("mappings", {})
        unknown_fields = self.get_unknown_fields(config)
        
        summary = f"""配置名称: {info['name']}
描述: {info['description']}
工作路径: {info['work_path']}
前缀: {config.get('prefix', '')}
后缀: {config.get('suffix', '')}
删除字符: {config.get('delete_chars', '')}
映射规则数量: {len(mappings)}
创建时间: {info['created_at']}
更新时间: {info['updated_at']}
版本: {info['version']}

映射规则:
"""
        
        if mappings:
            for key, value in mappings.items():
                summary += f"  '{key}' -> '{value}'\n"
        else:
            summary += "  无映射规则\n"
        
        # 显示未知字段信息
        if unknown_fields:
            summary += f"\n未知字段 (保留在配置中):\n"
            for key, value in unknown_fields.items():
                summary += f"  {key}: {value}\n"
        
        # 显示支持的字段信息
        supported_fields = list(self.supported_fields.keys())
        summary += f"\n当前工具支持的字段: {', '.join(supported_fields)}\n"
        
        return summary
