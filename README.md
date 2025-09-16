# 文件重命名工具

一个功能强大的文件重命名工具，支持前缀后缀和映射替换功能。

## 功能特性

### 🎯 核心功能
- **前缀后缀**: 为文件名添加前缀或后缀
- **映射替换**: 创建key-value映射规则，批量替换文件名中的特定文本
- **实时预览**: 重命名前预览效果
- **批量操作**: 一次性处理多个文件
- **错误处理**: 完善的异常处理机制

### 📁 项目结构
```
FileRenameEditor/
├── app.py                          # 主应用程序入口
├── main.py                         # 程序启动入口
├── models/                         # 数据模型层
│   ├── __init__.py
│   └── file_manager.py            # 文件管理器
├── views/                          # 视图层
│   ├── __init__.py
│   ├── main_window.py             # 主窗口界面
│   └── components/                # UI组件
│       ├── __init__.py
│       └── mapping_widget.py      # 映射组件
├── controllers/                    # 控制器层
│   ├── __init__.py
│   └── rename_controller.py       # 重命名控制器
├── config/                         # 配置模块
│   └── __init__.py
├── core/                          # 核心模块
│   └── __init__.py
├── gui/                           # GUI模块
│   └── __init__.py
├── utils/                         # 工具模块
│   └── __init__.py
├── requirements.txt               # 依赖包列表
├── 启动映射工具.bat               # Windows启动脚本
├── 启动映射工具.ps1               # PowerShell启动脚本
├── 安装检查.bat                   # 环境检查脚本
├── 使用说明.txt                   # 快速使用指南
└── 项目说明.md                    # 项目详细说明
```

## 快速开始

### 方法一：使用启动器（推荐）
1. 双击 `启动映射工具.bat` 或 `启动映射工具.ps1`
2. 选择要运行的程序
3. 按照界面提示操作

### 方法二：直接运行
```bash
python main.py
```

### 方法三：使用应用程序入口
```bash
python app.py
```

## 系统要求

- **操作系统**: Windows 7/8/10/11
- **Python版本**: 3.7 或更高版本
- **依赖模块**: tkinter, os, pathlib（通常随Python安装）
- **额外软件**: 无需安装其他软件

## 安装检查

运行 `安装检查.bat` 可以：
- ✅ 检查Python环境
- ✅ 验证必要模块
- ✅ 检查项目文件完整性
- ✅ 测试程序运行
- ✅ 创建必要目录

## 使用指南

### 基础操作流程
1. 启动程序
2. 选择工作文件夹
3. 设置重命名规则：
   - 添加前缀或后缀
   - 创建映射替换规则
4. 预览重命名效果
5. 执行重命名操作

### 映射替换示例
```
输入: IMG_20231201_143022.jpg
映射规则:
- IMG_ → 照片_
- 2023 → 2023年
- _ → (空格)
输出: 照片_2023年1201 143022.jpg
```

### 前缀后缀示例
```
输入: document.pdf
前缀: 重要_
后缀: _v1
输出: 重要_document_v1.pdf
```

## 技术特点

- **MVC架构**: 清晰的模型-视图-控制器分离
- **模块化设计**: 组件可独立使用和测试
- **类型提示**: 完整的类型注解
- **错误处理**: 完善的异常处理机制
- **用户友好**: 直观的图形界面

## 架构说明

### MVC模式
- **Model (模型)**: `models/file_manager.py` - 处理文件操作和数据管理
- **View (视图)**: `views/` - 处理用户界面和用户交互
- **Controller (控制器)**: `controllers/rename_controller.py` - 处理业务逻辑

### 组件化设计
- **主窗口**: `views/main_window.py` - 主界面布局和事件处理
- **映射组件**: `views/components/mapping_widget.py` - 映射规则管理
- **文件管理器**: `models/file_manager.py` - 文件操作封装

## 扩展开发

### 添加新功能
```python
# 在controllers中添加新的控制器
class NewFeatureController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
    
    def new_feature_method(self):
        # 实现新功能
        pass
```

### 添加新组件
```python
# 在views/components中添加新组件
class NewWidget:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        # 设置UI
        pass
```

## 故障排除

### 常见问题
1. **Python未找到**: 安装Python并添加到PATH
2. **模块缺失**: 检查Python安装是否完整
3. **权限错误**: 以管理员身份运行
4. **文件损坏**: 重新下载项目文件

### 解决步骤
1. 运行 `安装检查.bat` 诊断问题
2. 检查Python版本和PATH设置
3. 验证所有.py文件完整性
4. 检查目标文件夹权限

## 注意事项

1. **备份文件**: 执行重命名前请备份重要文件
2. **测试规则**: 使用预览功能验证重命名规则
3. **权限检查**: 确保对目标文件夹有写权限
4. **重复文件名**: 程序会自动跳过已存在的文件名

## 许可证

本项目采用MIT许可证，可自由使用和修改。

---

**🎉 享受高效的文件重命名体验！**