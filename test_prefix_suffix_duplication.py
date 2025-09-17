#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试前缀后缀重复添加问题
"""

def test_prefix_suffix_logic():
    """测试修复后的前缀后缀逻辑"""
    print("=== 前缀后缀重复添加问题测试 ===\n")
    
    # 导入修复后的控制器
    from controllers.rename_controller import RenameController
    
    # 创建控制器实例
    class MockView:
        pass
    
    class MockModel:
        pass
    
    controller = RenameController(MockView(), MockModel())
    
    # 模拟修复后的重命名逻辑
    def fixed_rename_logic(filename, prefix, suffix):
        """修复后的重命名逻辑"""
        return controller.apply_prefix_suffix(filename, prefix, suffix)
    
    import os
    
    # 测试用例
    test_cases = [
        {
            "filename": "IMG_20231201_143022.jpg",
            "prefix": "IMG_",
            "suffix": "",
            "expected": "IMG_20231201_143022.jpg",  # 应该保持不变
            "description": "文件已有前缀，不应该重复添加"
        },
        {
            "filename": "document_v1.pdf",
            "prefix": "",
            "suffix": "_v1",
            "expected": "document_v1.pdf",  # 应该保持不变
            "description": "文件已有后缀，不应该重复添加"
        },
        {
            "filename": "IMG_photo_v1.jpg",
            "prefix": "IMG_",
            "suffix": "_v1",
            "expected": "IMG_photo_v1.jpg",  # 应该保持不变
            "description": "文件已有前缀和后缀，不应该重复添加"
        },
        {
            "filename": "photo.jpg",
            "prefix": "IMG_",
            "suffix": "_v1",
            "expected": "IMG_photo_v1.jpg",  # 应该添加前缀和后缀
            "description": "文件没有前缀和后缀，应该添加"
        },
        {
            "filename": "IMG_photo.jpg",
            "prefix": "IMG_",
            "suffix": "_v1",
            "expected": "IMG_photo_v1.jpg",  # 应该只添加后缀
            "description": "文件有前缀但没有后缀，应该只添加后缀"
        },
        {
            "filename": "photo_v1.jpg",
            "prefix": "IMG_",
            "suffix": "_v1",
            "expected": "IMG_photo_v1.jpg",  # 应该只添加前缀
            "description": "文件有后缀但没有前缀，应该只添加前缀"
        }
    ]
    
    print("修复后的逻辑:")
    print("-" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        filename = test_case["filename"]
        prefix = test_case["prefix"]
        suffix = test_case["suffix"]
        expected = test_case["expected"]
        description = test_case["description"]
        
        # 使用修复后的逻辑
        result = fixed_rename_logic(filename, prefix, suffix)
        
        print(f"测试 {i}: {description}")
        print(f"  输入: {filename}")
        print(f"  前缀: '{prefix}', 后缀: '{suffix}'")
        print(f"  期望: {expected}")
        print(f"  实际: {result}")
        
        if result == expected:
            print("  ✓ 结果正确")
        else:
            print("  ✗ 结果错误 - 存在重复添加问题")
        
        print()

if __name__ == "__main__":
    test_prefix_suffix_logic()
