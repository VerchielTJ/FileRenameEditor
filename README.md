# FileRenameEditor

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

一个功能强大的文件重命名工具，支持前缀后缀和映射替换功能。采用MVC架构设计，提供清晰的代码结构和良好的可维护性。

## ✨ 功能特性

### 🎯 核心功能
- **前缀后缀**: 为文件名添加前缀或后缀
- **映射替换**: 创建key-value映射规则，批量替换文件名中的特定文本
- **实时预览**: 重命名前预览效果，避免误操作
- **批量操作**: 一次性处理多个文件
- **错误处理**: 完善的异常处理机制
- **配置保存**: 支持保存和加载映射配置

### 🏗️ 技术特点
- **MVC架构**: 清晰的模型-视图-控制器分离
- **模块化设计**: 组件可独立使用和测试
- **类型提示**: 完整的类型注解
- **用户友好**: 直观的图形界面
- **跨平台**: 基于Python和tkinter，支持多平台

## 📸 界面预览

> 界面截图将在后续版本中添加

## 🚀 快速开始

### 系统要求
- **操作系统**: Windows 7/8/10/11 (推荐Windows 10+)
- **Python版本**: 3.7 或更高版本
- **依赖模块**: tkinter, os, pathlib（通常随Python安装）

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/yourusername/FileRenameEditor.git
   cd FileRenameEditor
   ```

2. **检查环境** (Windows用户)
   ```bash
   # 双击运行安装检查脚本
   安装检查.bat
   ```

3. **启动程序**
   ```bash
   # 方法一：使用启动器（推荐）
   启动映射工具.bat
   
   # 方法二：直接运行
   python main.py
   
   # 方法三：使用应用程序入口
   python app.py
   ```

## 📁 项目结构

```
FileRenameEditor/
├── 🐍 核心应用程序
│   ├── app.py                          # 主应用程序入口
│   └── main.py                         # 程序启动入口
│
├── 📂 MVC架构模块
│   ├── models/                         # 数据模型层
│   │   ├── __init__.py
│   │   ├── file_manager.py            # 文件管理器
│   │   └── config_manager.py          # 配置管理器
│   ├── views/                          # 视图层
│   │   ├── __init__.py
│   │   ├── main_window.py             # 主窗口界面
│   │   └── components/                # UI组件
│   │       ├── __init__.py
│   │       └── mapping_widget.py      # 映射组件
│   └── controllers/                    # 控制器层
│       ├── __init__.py
│       └── rename_controller.py       # 重命名控制器
│
├── 🔧 配置和工具模块
│   ├── config/                         # 配置模块
│   ├── core/                          # 核心模块
│   ├── gui/                           # GUI模块
│   └── utils/                         # 工具模块
│
├── 🚀 Windows启动脚本
│   ├── 启动映射工具.bat               # 主启动器（批处理）
│   ├── 启动映射工具.ps1               # 主启动器（PowerShell）
│   └── 安装检查.bat                   # 环境检查脚本
│
├── 📖 文档文件
│   ├── README.md                      # 项目说明（本文件）
│   ├── 使用说明.txt                   # 快速使用指南
│   ├── 项目说明.md                    # 详细项目说明
│   └── requirements.txt               # 依赖包列表
│
└── 📂 运行时目录（自动创建）
    └── mapping_configs/               # 映射配置存储目录
```

## 🎮 使用指南

### 基础操作流程
1. **启动程序** - 运行启动脚本或直接执行Python文件
2. **选择文件夹** - 点击"选择文件夹"按钮选择要处理的目录
3. **设置规则** - 配置重命名规则：
   - 添加前缀或后缀
   - 创建映射替换规则
4. **预览效果** - 点击"预览"查看重命名效果
5. **执行重命名** - 确认无误后点击"执行重命名"

### 使用示例

#### 映射替换示例
```
输入文件: IMG_20231201_143022.jpg
映射规则:
- IMG_ → 照片_
- 2023 → 2023年
- _ → (空格)
输出结果: 照片_2023年1201 143022.jpg
```

#### 前缀后缀示例
```
输入文件: document.pdf
前缀: 重要_
后缀: _v1
输出结果: 重要_document_v1.pdf
```

#### 文档重命名示例
```
输入文件: doc_temp_report_v1.docx
映射规则:
- doc_ → 文档_
- temp_ → 临时_
- _v → _版本
输出结果: 文档_临时_报告_版本1.docx
```

## 🎯 适用场景

- **📸 照片整理**: 相机照片批量重命名，统一命名格式
- **📄 文档管理**: 统一文档命名格式，便于分类管理
- **🗂️ 文件归档**: 批量文件分类整理，提高工作效率
- **🧹 数据清理**: 清理不规范的文件名，统一命名规范
- **⚡ 批量处理**: 大量文件的统一处理，节省时间

## 🏗️ 架构设计

### MVC模式
项目采用经典的MVC（Model-View-Controller）架构模式：

- **Model (模型层)**: 负责数据管理和业务逻辑
  - `FileManager`: 处理文件操作和目录管理
  - `ConfigManager`: 处理配置文件的保存和加载

- **View (视图层)**: 负责用户界面和用户交互
  - `MainWindow`: 主窗口界面
  - `MappingWidget`: 映射规则管理组件

- **Controller (控制器层)**: 负责协调模型和视图
  - `RenameController`: 处理重命名业务逻辑

### 组件化设计
- **模块化**: 每个功能模块独立，便于维护和测试
- **可扩展**: 易于添加新功能和组件
- **可复用**: 组件可以在其他项目中复用

## 🔧 开发指南

### 环境设置
```bash
# 克隆项目
git clone https://github.com/yourusername/FileRenameEditor.git
cd FileRenameEditor

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖（如果需要）
pip install -r requirements.txt
```

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

## 🐛 故障排除

### 常见问题

1. **Python未找到**
   - 确保已安装Python 3.7+
   - 检查Python是否添加到系统PATH

2. **模块缺失**
   - 运行 `安装检查.bat` 诊断问题
   - 检查Python安装是否完整

3. **权限错误**
   - 以管理员身份运行程序
   - 检查目标文件夹的写权限

4. **文件损坏**
   - 重新下载项目文件
   - 验证所有.py文件完整性

### 解决步骤
1. 运行 `安装检查.bat` 诊断问题
2. 检查Python版本和PATH设置
3. 验证所有.py文件完整性
4. 检查目标文件夹权限

## ⚠️ 注意事项

1. **备份文件**: 执行重命名前请备份重要文件
2. **测试规则**: 使用预览功能验证重命名规则
3. **权限检查**: 确保对目标文件夹有写权限
4. **重复文件名**: 程序会自动跳过已存在的文件名

## 🤝 贡献指南

我们欢迎任何形式的贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

### 开发规范
- 遵循PEP 8代码风格
- 添加适当的类型提示
- 编写清晰的文档字符串
- 确保代码通过测试

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持与反馈

如果您遇到问题或有任何建议，请：

1. 查看 [故障排除](#-故障排除) 部分
2. 搜索 [Issues](https://github.com/yourusername/FileRenameEditor/issues)
3. 创建新的 Issue 描述您的问题
4. 联系维护者

## 🎉 致谢

感谢所有为这个项目做出贡献的开发者！

---

**🎉 享受高效的文件重命名体验！**

如果这个项目对您有帮助，请给我们一个 ⭐ Star！