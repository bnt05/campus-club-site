#!/usr/bin/env python
# -*- coding: utf-8 -*-
filepath = r'D:\campus_club_site\clubs\templates\clubs\ai_floating_widget.html'
with open(filepath, 'rb') as f:
    content = f.read()

# 查找 getCookie 使用的位置，然后在合适的地方添加函数
# getCookie('csrftoken') 应该改为类似 getCSRFToken() 的函数

# 查找最后一个 <script> 标签，在它之前添加 getCookie 函数
# 或者直接替换 getCookie('csrftoken') 为 document.cookie 方式

# 更简单的方法：添加一个 getCookie 函数
# 找到 <script> 标签的位置
script_tag = b'<script>'
last_script_idx = content.rfind(script_tag)

if last_script_idx != -1:
    # 在最后一个 <script> 标签后添加 getCookie 函数
    getCookie_func = b'''
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
'''
    content = content[:last_script_idx + len(script_tag)] + getCookie_func + content[last_script_idx + len(script_tag):]
    
    with open(filepath, 'wb') as f:
        f.write(content)
    print('SUCCESS: Added getCookie function')
else:
    print('ERROR: No <script> tag found')
