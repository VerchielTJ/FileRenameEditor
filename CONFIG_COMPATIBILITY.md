# 配置兼容性功能说明

本文档详细说明了 FileRenameEditor 配置管理器的字段兼容性功能。

## 🎯 功能概述

配置管理器现在支持**向前兼容**和**向后兼容**，能够处理不同版本的配置文件，确保：

- ✅ 加载包含未知字段的配置文件
- ✅ 加载缺少某些字段的配置文件  
- ✅ 保留所有字段在内存中
- ✅ 保存时保留所有原始字段
- ✅ 自动类型转换和验证

## 🔧 核心特性

### 1. 字段兼容性处理

#### 支持的字段
当前工具支持以下字段：
- `version`: 配置文件版本
- `created_at`: 创建时间
- `updated_at`: 更新时间
- `name`: 配置名称
- `description`: 配置描述
- `work_path`: 工作路径
- `prefix`: 前缀
- `suffix`: 后缀
- `delete_chars`: 删除字符
- `mappings`: 映射规则
- `settings`: 设置选项

#### 未知字段处理
- 自动识别并保留未知字段
- 在内存中维护所有字段
- 保存时重新写入所有字段

### 2. 类型安全

#### 自动类型转换
- 字符串字段：自动转换为字符串类型
- 字典字段：确保为字典类型
- 布尔字段：自动转换为布尔类型
- 空值处理：None值转换为适当的默认值

#### 默认值处理
- 缺失字段自动使用默认值
- 类型错误字段使用默认值
- 保持配置文件的完整性

### 3. 配置合并

#### 智能合并策略
- 保留所有原始字段
- 正确合并嵌套字典（mappings, settings）
- 更新已知字段
- 保留未知字段

## 📋 使用示例

### 示例1: 加载包含未知字段的配置

```python
from models.config_manager import ConfigManager

# 创建配置管理器
config_manager = ConfigManager()

# 加载包含未知字段的配置文件
config = config_manager.load_config("future_config.fre")

if config:
    # 获取未知字段
    unknown_fields = config_manager.get_unknown_fields(config)
    print(f"未知字段: {list(unknown_fields.keys())}")
    
    # 使用已知字段
    print(f"工作路径: {config['work_path']}")
    print(f"前缀: {config['prefix']}")
    
    # 保存时保留所有字段
    config_manager.save_config(config, "updated_config.fre")
```

### 示例2: 处理缺少字段的配置

```python
# 加载缺少某些字段的配置文件
config = config_manager.load_config("legacy_config.fre")

if config:
    # 缺失字段会自动使用默认值
    print(f"前缀: {config.get('prefix', '')}")  # 默认空字符串
    print(f"映射: {config.get('mappings', {})}")  # 默认空字典
    
    # 可以正常使用
    config['prefix'] = 'NEW_'
    config_manager.save_config(config, "updated_legacy.fre")
```

### 示例3: 配置合并

```python
# 基础配置
base_config = {
    "name": "基础配置",
    "work_path": "/base/path",
    "mappings": {"a": "A"},
    "unknown_field": "基础未知字段"
}

# 新配置
new_config = {
    "name": "更新配置",
    "suffix": "_new",
    "mappings": {"b": "B"},
    "new_unknown_field": "新未知字段"
}

# 合并配置
merged = config_manager.merge_configs(base_config, new_config)

# 结果包含所有字段
print(merged["name"])  # "更新配置"
print(merged["mappings"])  # {"a": "A", "b": "B"}
print(merged["unknown_field"])  # "基础未知字段"
print(merged["new_unknown_field"])  # "新未知字段"
```

## 🔍 配置摘要功能

### 显示详细信息
配置摘要现在包含：
- 基本配置信息
- 映射规则列表
- 未知字段信息
- 支持的字段列表

```python
# 生成配置摘要
summary = config_manager.export_config_summary(config)
print(summary)
```

输出示例：
```
配置名称: 未来版本配置
描述: 包含新功能的配置文件
工作路径: /future/path
前缀: FUTURE_
后缀: _v2
删除字符:
映射规则数量: 2
创建时间: 2025-01-01T00:00:00
更新时间: 2025-01-01T12:00:00
版本: 2.0

映射规则:
  'legacy' -> 'modern'
  'old' -> 'new'

未知字段 (保留在配置中):
  advanced_settings: {'regex_mode': True, 'case_sensitive': False}
  file_filters: {'include_extensions': ['.jpg', '.png']}
  batch_size: 100

当前工具支持的字段: version, created_at, updated_at, name, description, work_path, prefix, suffix, delete_chars, mappings, settings
```

## 🛠️ 扩展功能

### 动态添加支持的字段

```python
# 添加新的支持字段
config_manager.add_supported_field("new_field", str, "默认值")

# 检查字段是否支持
if config_manager.is_field_supported("new_field"):
    print("字段被支持")
```

### 获取字段信息

```python
# 获取所有支持的字段
supported_fields = config_manager.get_supported_fields()
print(f"支持的字段: {list(supported_fields.keys())}")

# 检查字段类型
field_type = supported_fields.get("prefix")
print(f"prefix字段类型: {field_type}")
```

## ⚠️ 注意事项

### 1. 版本兼容性
- 配置文件必须包含 `version` 字段
- 建议在配置文件中明确标注版本信息
- 不同版本间的字段差异会被自动处理

### 2. 字段命名
- 建议使用有意义的字段名
- 避免使用特殊字符
- 保持字段名的一致性

### 3. 数据类型
- 确保字段值符合预期类型
- 复杂对象建议使用JSON格式
- 避免循环引用

### 4. 性能考虑
- 大型配置文件可能影响加载性能
- 建议定期清理不需要的字段
- 使用适当的缓存策略

## 🔮 未来扩展

### 计划中的功能
- 配置文件版本迁移工具
- 字段验证规则配置
- 配置文件模板系统
- 批量配置文件处理

### 扩展建议
- 添加配置文件加密支持
- 实现配置文件压缩
- 支持远程配置文件
- 添加配置文件历史记录

---

这个兼容性功能确保了 FileRenameEditor 能够处理各种版本的配置文件，为用户提供更好的使用体验。
