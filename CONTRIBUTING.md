# 贡献指南

感谢您对 FileRenameEditor 项目的关注！我们欢迎任何形式的贡献，包括但不限于：

- 🐛 报告Bug
- ✨ 提出新功能建议
- 📝 改进文档
- 🔧 提交代码修复
- 🎨 改进用户界面

## 🚀 快速开始

### 1. Fork 和克隆项目

```bash
# Fork 项目到您的GitHub账户，然后克隆
git clone https://github.com/yourusername/FileRenameEditor.git
cd FileRenameEditor

# 添加上游仓库
git remote add upstream https://github.com/originalowner/FileRenameEditor.git
```

### 2. 设置开发环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 创建特性分支

```bash
# 从main分支创建新分支
git checkout -b feature/your-feature-name

# 或者修复bug
git checkout -b fix/issue-number
```

## 📝 开发规范

### 代码风格

我们遵循以下代码规范：

1. **Python代码风格**: 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/)
2. **类型提示**: 为所有函数和方法添加类型提示
3. **文档字符串**: 使用Google风格的文档字符串
4. **命名规范**: 使用有意义的变量和函数名

### 代码示例

```python
def rename_files(self, file_list: List[str], rules: Dict[str, str]) -> List[str]:
    """
    根据规则重命名文件列表
    
    Args:
        file_list: 要重命名的文件路径列表
        rules: 重命名规则字典
        
    Returns:
        重命名后的文件路径列表
        
    Raises:
        FileNotFoundError: 当文件不存在时
        PermissionError: 当没有写权限时
    """
    # 实现代码
    pass
```

### 提交信息规范

使用清晰的提交信息，格式如下：

```
类型(范围): 简短描述

详细描述（可选）

相关Issue: #123
```

类型包括：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

示例：
```
feat(mapping): 添加批量映射规则导入功能

- 支持从CSV文件导入映射规则
- 添加映射规则验证
- 更新用户界面以支持批量导入

相关Issue: #45
```

## 🧪 测试

### 运行测试

```bash
# 运行所有测试
python -m pytest

# 运行特定测试文件
python -m pytest tests/test_file_manager.py

# 运行测试并显示覆盖率
python -m pytest --cov=models --cov=controllers --cov=views
```

### 编写测试

为新增功能编写测试用例：

```python
import unittest
from models.file_manager import FileManager

class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.file_manager = FileManager()
    
    def test_rename_single_file(self):
        """测试单个文件重命名"""
        # 测试代码
        pass
    
    def test_rename_multiple_files(self):
        """测试多个文件重命名"""
        # 测试代码
        pass
```

## 📋 提交流程

### 1. 提交更改

```bash
# 添加更改的文件
git add .

# 提交更改
git commit -m "feat: 添加新功能描述"

# 推送到您的fork
git push origin feature/your-feature-name
```

### 2. 创建Pull Request

1. 在GitHub上创建Pull Request
2. 填写PR模板信息
3. 等待代码审查
4. 根据反馈进行修改

### 3. PR模板

```markdown
## 更改描述
简要描述此PR的更改内容

## 更改类型
- [ ] Bug修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 代码重构
- [ ] 性能优化
- [ ] 其他

## 测试
- [ ] 已添加测试用例
- [ ] 所有测试通过
- [ ] 手动测试通过

## 相关Issue
关闭 #(issue编号)

## 截图（如适用）
添加界面更改的截图

## 检查清单
- [ ] 代码遵循项目规范
- [ ] 已添加必要的文档
- [ ] 已添加测试用例
- [ ] 所有测试通过
- [ ] 代码已自测
```

## 🐛 报告Bug

### Bug报告模板

```markdown
**Bug描述**
清晰简洁地描述bug

**重现步骤**
1. 进入 '...'
2. 点击 '....'
3. 滚动到 '....'
4. 看到错误

**预期行为**
描述您期望发生的事情

**实际行为**
描述实际发生的事情

**环境信息**
- 操作系统: [例如 Windows 10]
- Python版本: [例如 3.9.0]
- 程序版本: [例如 v1.0.0]

**截图**
如果适用，添加截图

**附加信息**
添加任何其他相关信息
```

## ✨ 功能建议

### 功能请求模板

```markdown
**功能描述**
清晰简洁地描述您希望添加的功能

**使用场景**
描述此功能的使用场景和好处

**可能的实现方案**
如果您有想法，请描述可能的实现方案

**附加信息**
添加任何其他相关信息
```

## 📚 项目结构说明

```
FileRenameEditor/
├── models/          # 数据模型层
├── views/           # 视图层
├── controllers/     # 控制器层
├── config/          # 配置模块
├── core/           # 核心模块
├── gui/            # GUI模块
├── utils/          # 工具模块
├── tests/          # 测试文件
└── docs/           # 文档
```

### 添加新功能指南

1. **确定功能位置**: 根据功能类型选择适当的模块
2. **更新模型**: 如果需要，在models中添加新的数据模型
3. **更新视图**: 在views中添加或修改UI组件
4. **更新控制器**: 在controllers中添加业务逻辑
5. **添加测试**: 为新功能编写测试用例
6. **更新文档**: 更新README和相关文档

## 🤝 社区准则

### 行为准则

- 保持友善和尊重
- 欢迎不同观点和经验
- 接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

### 沟通渠道

- GitHub Issues: 用于bug报告和功能请求
- GitHub Discussions: 用于一般讨论和问题
- Pull Requests: 用于代码贡献

## 📞 获取帮助

如果您在贡献过程中遇到问题：

1. 查看现有文档和README
2. 搜索已有的Issues和Discussions
3. 创建新的Issue描述您的问题
4. 联系维护者

## 🎉 感谢

感谢您对FileRenameEditor项目的贡献！每一个贡献都让这个项目变得更好。

---

**让我们一起构建更好的文件重命名工具！** 🚀
