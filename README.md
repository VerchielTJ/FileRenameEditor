# 文件重命名工具 - 映射组件

这是一个功能强大的文件重命名工具，支持通过映射规则批量替换文件名中的特定文本。

## 功能特性

### 🎯 核心功能
- **映射替换**: 创建key-value映射规则，批量替换文件名中的特定文本
- **正则表达式支持**: 支持复杂的模式匹配和替换
- **大小写控制**: 可选择是否区分大小写
- **批量操作**: 支持批量添加、导入、导出映射规则
- **配置持久化**: 保存和加载映射配置到本地文件

### 📁 文件结构
```
FileRenameEditor/
├── mapping_widget.py              # 基础版映射组件
├── enhanced_mapping_widget.py     # 增强版映射组件
├── mapping_persistence.py         # 持久化存储模块
├── main_with_mapping_integrated.py # 集成版主程序
├── final_mapping_app.py           # 最终版完整应用
├── mapping_demo.py                # 演示程序
├── test_mapping.py                # 测试程序
└── README.md                      # 使用说明
```

## 快速开始

### 1. 运行基础测试
```bash
python test_mapping.py
```

### 2. 运行完整演示
```bash
python mapping_demo.py
```

### 3. 运行最终版应用
```bash
python final_mapping_app.py
```

## 使用指南

### 基础版映射组件

基础版映射组件提供简单的文本替换功能：

```python
from mapping_widget import MappingListWidget

# 创建映射组件
mapping_widget = MappingListWidget(parent)

# 添加映射规则
mapping_widget.set_mappings({
    "IMG_": "照片_",
    "2023": "2023年",
    "_": " "
})

# 应用映射
result = mapping_widget.apply_mappings("IMG_20231201_143022.jpg")
# 结果: "照片_2023年1201 143022.jpg"
```

### 增强版映射组件

增强版映射组件支持更多高级功能：

```python
from enhanced_mapping_widget import EnhancedMappingListWidget

# 创建增强版映射组件
mapping_widget = EnhancedMappingListWidget(parent)

# 设置映射规则（支持正则表达式）
mappings = {
    r"\d{4}(\d{2})(\d{2})": {
        'value': r'\1月\2日',
        'use_regex': True,
        'case_sensitive': True
    },
    "IMG_": {
        'value': "照片_",
        'use_regex': False,
        'case_sensitive': False
    }
}

mapping_widget.set_enhanced_mappings(mappings)
```

### 配置持久化

```python
from mapping_persistence import MappingPersistence

# 创建持久化管理器
persistence = MappingPersistence()

# 保存配置
persistence.save_mapping_config("照片重命名", mappings, "enhanced")

# 加载配置
config = persistence.load_mapping_config("照片重命名")

# 列出所有配置
configs = persistence.list_configs()
```

## 使用场景

### 1. 照片文件重命名
将相机拍摄的照片文件名转换为更易读的格式：
- `IMG_20231201_143022.jpg` → `照片_2023年12月01日 143022.jpg`

### 2. 文档文件整理
统一文档文件的命名格式：
- `doc_temp_report_v1.docx` → `文档_临时_报告_版本1.docx`

### 3. 批量编号处理
使用正则表达式处理复杂的编号格式：
- `DSC_001234.jpg` → `数码相机_001234.jpg`
- `PIC_20231201_001.jpg` → `图片_20231201_编号001.jpg`

## 高级功能

### 正则表达式支持
```python
# 日期格式转换
r"\d{4}(\d{2})(\d{2})" → r'\1月\2日'

# 编号重排
r"_(\d{3})$" → r'_编号\1'

# 大小写不敏感替换
"DSC_" → "数码相机_" (不区分大小写)
```

### 批量操作
- **批量添加**: 通过文本输入批量添加映射规则
- **文件导入**: 从JSON或文本文件导入映射配置
- **文件导出**: 将映射配置导出为文件
- **配置管理**: 保存、加载、删除映射配置

### 错误处理
- 正则表达式验证
- 文件操作错误处理
- 重复文件名检测
- 权限错误处理

## 界面说明

### 主界面布局
1. **映射编辑**: 创建和管理映射规则
2. **文件操作**: 选择文件夹和执行重命名
3. **配置管理**: 保存和加载映射配置

### 操作流程
1. 在"映射编辑"选项卡中添加映射规则
2. 使用"测试映射"功能验证规则
3. 在"文件操作"选项卡中选择工作文件夹
4. 预览重命名结果
5. 执行重命名操作
6. 在"配置管理"选项卡中保存配置

## 技术特点

- **MVC架构**: 清晰的模型-视图-控制器分离
- **模块化设计**: 组件可独立使用
- **类型提示**: 完整的类型注解
- **错误处理**: 完善的异常处理机制
- **用户友好**: 直观的图形界面

## 依赖要求

- Python 3.7+
- tkinter (通常随Python安装)
- 无其他外部依赖

## 注意事项

1. **备份文件**: 执行重命名前请备份重要文件
2. **测试规则**: 使用测试功能验证映射规则
3. **权限检查**: 确保对目标文件夹有写权限
4. **正则表达式**: 复杂正则表达式请先在测试中验证

## 扩展开发

### 添加新的映射类型
```python
class CustomMappingWidget(EnhancedMappingListWidget):
    def apply_custom_mapping(self, text, key, mapping):
        # 实现自定义映射逻辑
        pass
```

### 集成到其他应用
```python
# 在现有应用中集成映射组件
from enhanced_mapping_widget import EnhancedMappingListWidget

class MyApp:
    def __init__(self):
        self.mapping_widget = EnhancedMappingListWidget(self.parent)
```

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

---

**享受高效的文件重命名体验！** 🚀
