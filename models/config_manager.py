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
    """配置管理器类"""
    
    def __init__(self):
        # 配置文件版本，用于未来兼容性
        self.config_version = "1.0"
        
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
            "mappings": mappings
        })
        
        return config
    
    def save_config(self, config: Dict[str, Any], file_path: str) -> bool:
        """保存配置到 .fre 文件"""
        try:
            # 更新保存时间
            config["updated_at"] = datetime.now().isoformat()
            
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # 保存为 JSON 格式
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False
    
    def load_config(self, file_path: str) -> Optional[Dict[str, Any]]:
        """从 .fre 文件加载配置"""
        try:
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 验证配置文件格式
            if not self.validate_config(config):
                return None
            
            return config
            
        except Exception as e:
            print(f"加载配置失败: {e}")
            return None
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """验证配置文件格式"""
        try:
            # 检查必需字段
            required_fields = ["version", "work_path", "prefix", "suffix", "mappings"]
            for field in required_fields:
                if field not in config:
                    print(f"配置文件缺少必需字段: {field}")
                    return False
            
            # 检查字段类型
            if not isinstance(config["work_path"], str):
                print("work_path 必须是字符串")
                return False
            
            if not isinstance(config["prefix"], str):
                print("prefix 必须是字符串")
                return False
            
            if not isinstance(config["suffix"], str):
                print("suffix 必须是字符串")
                return False
            
            if not isinstance(config["mappings"], dict):
                print("mappings 必须是字典")
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
        """合并配置（用于更新现有配置）"""
        merged = base_config.copy()
        
        # 更新基本字段
        for key in ["name", "description", "work_path", "prefix", "suffix"]:
            if key in new_config:
                merged[key] = new_config[key]
        
        # 合并映射
        if "mappings" in new_config:
            merged["mappings"].update(new_config["mappings"])
        
        # 合并设置
        if "settings" in new_config:
            if "settings" not in merged:
                merged["settings"] = {}
            merged["settings"].update(new_config["settings"])
        
        # 更新时间
        merged["updated_at"] = datetime.now().isoformat()
        
        return merged
    
    def export_config_summary(self, config: Dict[str, Any]) -> str:
        """导出配置摘要为文本"""
        info = self.get_config_info(config)
        mappings = config.get("mappings", {})
        
        summary = f"""配置名称: {info['name']}
描述: {info['description']}
工作路径: {info['work_path']}
前缀: {config.get('prefix', '')}
后缀: {config.get('suffix', '')}
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
        
        return summary
