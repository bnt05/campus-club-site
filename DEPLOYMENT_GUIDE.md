# 部署指南 - 校园社团系统 (智枢青寰)

## 部署选项

### 选项1: PythonAnywhere (最简单，推荐新手)

**优点**: 专门支持 Python/Django，免费层可用，无需命令行
**缺点**: 服务器在国外，国内访问较慢

**步骤**:

1. **注册账号**: https://www.pythonanywhere.com

2. **上传代码到 GitHub** (如果还没有):
   - 在 GitHub 创建新仓库
   - 把 D:\campus_club_site 里的代码上传

3. **在 PythonAnywhere 操作**:
   - 打开 Bash 控制台
   - 克隆代码:
     ```bash
     git clone https://github.com/你的用户名/你的仓库名.git
     cd 你的仓库名
     ```

4. **创建虚拟环境**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或者在 Windows 使用:
   venv\Scripts\activate.bat
   ```

5. **安装依赖**:
   ```bash
   pip install -r requirements.txt
   ```

6. **配置环境变量** (重要!):
   ```bash
   export DASHSCOPE_API_KEY='你的API密钥'
   ```

7. **收集静态文件**:
   ```bash
   python manage.py collectstatic
   ```

8. **初始化数据库**:
   ```bash
   python manage.py migrate
   ```

9. **配置 Web App**:
   - 在 Web 标签页点击 "Add a new web app"
   - 选择 Manual configuration
   - 选择 Python 3.11
   - 设置虚拟环境路径: `/home/你的用户名/你的仓库名/venv/`

10. **配置 WSGI 文件**:
    - 编辑 `/var/www/你的用户名_pythonanywhere_com_wsgi.py`
    - 写入:
    ```python
    import os
    import sys
    path = '/home/你的用户名/你的仓库名'
    if path not in sys.path:
        sys.path.insert(0, path)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_club_site.settings')
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    ```

11. **配置静态文件**:
    - 在 Web 标签页的 Static files 部分添加:
    - URL: `/static/` -> Directory: `/home/你的用户名/你的仓库名/static/`
    - URL: `/media/` -> Directory: `/home/你的用户名/你的仓库名/media/`

12. **重载 Web App**:
    - 点击 Reload 按钮

---

### 选项2: 阿里云/腾讯云 (国内服务器)

**优点**: 国内访问快，服务器性能好
**缺点**: 需要付费，需要一定技术基础

**步骤**:

1. **购买云服务器** (学生套餐很便宜)

2. **连接服务器**:
   ```bash
   ssh root@你的服务器IP
   ```

3. **安装环境**:
   ```bash
   # 安装 Python 和 pip
   apt update
   apt install python3 python3-pip python3-venv nginx
   
   # 创建项目目录
   mkdir -p /var/www/campus_club_site
   cd /var/www/campus_club_site
   
   # 上传代码 (可以用 scp、rsync 或 Git)
   git clone https://github.com/你的用户名/你的仓库名.git .
   ```

4. **配置虚拟环境**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **配置环境变量**:
   ```bash
   export DASHSCOPE_API_KEY='你的API密钥'
   export DEBUG='False'
   export ALLOWED_HOSTS='你的域名或IP'
   ```

6. **收集静态文件**:
   ```bash
   python manage.py collectstatic
   ```

7. **配置 Gunicorn**:
   ```bash
   pip install gunicorn
   gunicorn campus_club_site.wsgi:application -b 127.0.0.1:8000
   ```

8. **配置 Nginx**:
   ```bash
   # 创建 /etc/nginx/sites-available/campus_club_site
   # 内容参考 Nginx 配置模板
   ```

---

## 快速部署检查清单

部署前确认以下文件存在:

- [x] requirements.txt (已创建)
- [ ] .gitignore (需要创建)
- [ ] 修改 DEBUG = False
- [ ] 设置 ALLOWED_HOSTS
- [ ] 配置 DASHSCOPE_API_KEY 环境变量
- [ ] 收集静态文件

---

## 重要提醒

⚠️ **API 密钥**: 部署时不要把 API 密钥硬编码在代码里，使用环境变量！

⚠️ **数据库**: SQLite 适合小规模演示，大规模使用建议换成 MySQL/PostgreSQL

⚠️ **静态文件**: 确保运行了 `python manage.py collectstatic`

⚠️ **安全**: 生产环境记得把 DEBUG=False

---

需要我帮你执行哪个平台的部署？或者有其他问题？
