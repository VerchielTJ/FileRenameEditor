#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试映射加载功能
"""

import json
import os
import tempfile
from models.config_manager import ConfigManager
from views.components.mapping_widget import MappingListWidget
import tkinter as tk

def test_mapping_loading():
    """测试映射加载功能"""
    print("=== 映射加载功能测试 ===\n")
    
    # 创建配置管理器
    config_manager = ConfigManager()
    
    # 创建测试配置
    test_config = {
        "version": "1.0",
        "name": "映射测试配置",
        "description": "测试映射加载功能",
        "work_path": "/test/path",
        "prefix": "TEST_",
        "suffix": "_v1",
        "delete_chars": "",
        "mappings": {
            "old_name": "new_name",
            "temp": "final",
            "IMG_": "照片_",
            "2023": "2023年",
            "_": " "
        }
    }
    
    # 保存测试配置
    with tempfile.NamedTemporaryFile(mode='w', suffix='.fre', delete=False, encoding='utf-8') as f:
        json.dump(test_config, f, ensure_ascii=False, indent=2)
        temp_file = f.name
    
    try:
        print("1. 测试配置加载")
        loaded_config = config_manager.load_config(temp_file)
        
        if loaded_config:
            print("✓ 配置加载成功")
            mappings = loaded_config.get("mappings", {})
            print(f"✓ 映射数量: {len(mappings)}")
            print("映射内容:")
            for key, value in mappings.items():
                print(f"  '{key}' -> '{value}'")
        else:
            print("✗ 配置加载失败")
            return
        
        print("\n2. 测试映射组件")
        
        # 创建临时Tkinter根窗口（用于测试）
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        
        # 创建映射组件
        mapping_widget = MappingListWidget(root)
        
        # 测试设置映射
        print("设置映射到组件...")
        mapping_widget.set_mappings(mappings)
        
        # 验证映射是否正确设置
        retrieved_mappings = mapping_widget.get_mappings()
        print(f"✓ 组件中的映射数量: {len(retrieved_mappings)}")
        
        # 验证映射内容
        for key, value in mappings.items():
            if key in retrieved_mappings and retrieved_mappings[key] == value:
                print(f"✓ 映射 '{key}' -> '{value}' 正确")
            else:
                print(f"✗ 映射 '{key}' -> '{value}' 错误")
                print(f"  期望: '{value}', 实际: '{retrieved_mappings.get(key, 'None')}'")
        
        # 清理
        root.destroy()
        
        print("\n3. 测试配置保存")
        
        # 修改映射
        modified_mappings = {
            "new_key": "new_value",
            "test": "demo",
            "updated": "changed"
        }
        
        # 更新配置
        loaded_config["mappings"] = modified_mappings
        
        # 保存配置
        save_file = temp_file.replace('.fre', '_saved.fre')
        if config_manager.save_config(loaded_config, save_file):
            print("✓ 配置保存成功")
            
            # 验证保存的配置
            with open(save_file, 'r', encoding='utf-8') as f:
                saved_config = json.load(f)
            
            saved_mappings = saved_config.get("mappings", {})
            print(f"✓ 保存的映射数量: {len(saved_mappings)}")
            
            for key, value in modified_mappings.items():
                if key in saved_mappings and saved_mappings[key] == value:
                    print(f"✓ 保存的映射 '{key}' -> '{value}' 正确")
                else:
                    print(f"✗ 保存的映射 '{key}' -> '{value}' 错误")
            
            os.unlink(save_file)
        else:
            print("✗ 配置保存失败")
        
        print("\n=== 测试完成 ===")
        
    finally:
        # 清理临时文件
        os.unlink(temp_file)

if __name__ == "__main__":
    test_mapping_loading()
