# 社团智能推荐系统 - 技术文档

## 一、系统概述

基于学生画像和社团数据，通过推荐算法为学生精准匹配适合的社团，并提供数据可视化展示。

### 核心功能

1. **智能推荐** - 基于加权匹配 + 协同过滤的混合推荐算法
2. **学生画像** - 收集学生的年级、专业、兴趣标签、活跃时间等信息
3. **数据分析** - 提供多维度的数据统计和可视化看板
4. **实时反馈** - 记录用户对推荐结果的反馈，持续优化推荐效果

---

## 二、技术架构

```
前端: Vue.js + ElementUI + ECharts
后端: Django REST Framework
数据库: SQLite / MySQL
缓存: Django Cache
算法: Python (协同过滤 + 加权匹配)
```

---

## 三、已创建的文件

### 1. 数据模型 (clubs/recommendation_models.py)

| 模型名 | 说明 |
|--------|------|
| StudentProfile | 学生扩展信息表 |
| InterestTag | 兴趣标签表 |
| StudentInterest | 学生兴趣关联表 |
| Club | 社团表（已扩展） |
| ClubTag | 社团官方标签表 |
| Activity | 活动表（已扩展） |
| ActivityParticipation | 活动参与记录表 |
| UserBehavior | 用户行为记录表 |
| ClubMembership | 社团成员关系表 |
| RecommendationResult | 推荐结果表 |
| SimilarityMatrix | 相似度矩阵表 |
| RecommendationFeedback | 推荐反馈表 |

### 2. 推荐算法引擎 (clubs/recommendation_engine.py)

**核心类: `RecommendationEngine`**

**算法实现:**

1. **加权匹配算法**
   - 年级匹配度 (15%)
   - 专业相关度 (15%)
   - 分类偏好匹配度 (30%)
   - 标签相似度 (25%)
   - 活跃时间匹配度 (15%)

2. **用户协同过滤 (User-Based CF)**
   - 基于余弦相似度计算用户相似度
   - 找到相似用户加入的社团进行推荐

3. **物品协同过滤 (Item-Based CF)**
   - 基于Jaccard相似度计算社团相似度
   - 推荐与用户已加入社团相似的其他社团

4. **混合推荐**
   - 加权匹配 40% + 用户CF 30% + 物品CF 30%

### 3. API视图 (clubs/recommendation_views.py)

| API端点 | 方法 | 说明 |
|---------|------|------|
| `/api/recommend/` | GET | 获取推荐列表 |
| `/api/recommend/` | POST | 记录推荐反馈 |
| `/api/recommend/profile/` | GET | 获取学生档案 |
| `/api/recommend/profile/` | POST | 更新学生档案 |
| `/api/recommend/tags/` | GET | 获取兴趣标签 |
| `/api/recommend/stats/` | GET | 获取统计数据 |
| `/api/recommend/timeline/` | GET | 获取活动时间线 |
| `/api/recommend/behavior/` | POST | 记录用户行为 |
| `/api/recommend/similarity/compute/` | POST | 触发相似度计算 |

### 4. 前端组件

- **推荐页面** (templates/recommendation/recommendation_page.html)
  - 用户档案卡片
  - 推荐列表展示（带匹配度圆形进度条）
  - 推荐理由标签
  - 申请加入/收藏功能

- **数据看板** (templates/recommendation/statistics_dashboard.html)
  - 概览统计卡片
  - 社团分类分布饼图
  - 热门社团排行柱状图
  - 学生年级分布环形图
  - 活动类型分布柱状图
  - 活动时间热力图
  - 近期活动时间线
  - 推荐效果统计

### 5. 管理命令

```bash
# 初始化示例数据
python manage.py init_recommendation_data

# 清空并重新初始化
python manage.py init_recommendation_data --clear
```

---

## 四、集成步骤

### 1. 注册新模块

在 `clubs/apps.py` 中添加:

```python
from django.apps import AppConfig

class RecommendationConfig(AppConfig):
    name = 'clubs.recommendation'
    verbose_name = '社团推荐系统'
```

### 2. 更新URL配置

在 `campus_club_site/urls.py` 中添加:

```python
from clubs import recommendation_urls

urlpatterns = [
    # ... existing urls ...
    path('api/recommend/', include(recommendation_urls.urlpatterns)),
]
```

### 3. 执行数据库迁移

```bash
python manage.py makemigrations clubs
python manage.py migrate
```

### 4. 初始化示例数据

```bash
python manage.py init_recommendation_data
```

### 5. 启动服务器

```bash
python manage.py runserver
```

---

## 五、推荐算法详解

### 5.1 加权匹配算法

```python
匹配度 = 0.15 × 年级匹配度 
        + 0.15 × 专业匹配度 
        + 0.30 × 分类匹配度 
        + 0.25 × 标签匹配度 
        + 0.10 × 时间匹配度
```

**年级匹配度计算:**
- 老牌社团（成立5年以上）更欢迎大一、大二学生 → 90分
- 新社团 → 70分
- 其他 → 50-70分

**专业匹配度计算:**
- 建立专业关键词与社团描述的映射
- 如：计算机专业 ↔ 技术/编程/AI类社团 → 85分

**分类匹配度计算:**
- 学生兴趣最高的分类与社团分类匹配 → 70-100分

**标签匹配度计算:**
- 使用Jaccard相似度
- Jaccard = |学生标签 ∩ 社团标签| / |学生标签 ∪ 社团标签|

**时间匹配度计算:**
- 统计学生活跃时间段与社团活动时间段的重叠率

### 5.2 协同过滤算法

**用户协同过滤 (User-Based CF):**
1. 构建用户-社团行为矩阵
2. 计算用户之间的余弦相似度
3. 找到与目标用户最相似的K个用户
4. 推荐这些相似用户加入的社团

**物品协同过滤 (Item-Based CF):**
1. 构建用户-社团矩阵
2. 计算社团之间的Jaccard相似度
3. 对于用户已加入的社团，推荐相似的其他社团

### 5.3 冷启动处理

**新用户冷启动:**
- 引导填写兴趣问卷
- 使用基于内容的推荐（仅依赖标签/专业）
- 返回热门社团作为备选

**新社团冷启动:**
- 使用社团标签与已有社团的相似度推荐
- 置顶展示给匹配的用户

---

## 六、可视化图表

### 6.1 ECharts 图表类型

| 图表 | 类型 | 用途 |
|------|------|------|
| 社团分类分布 | 饼图 | 展示各类社团数量占比 |
| 热门社团排行 | 水平柱状图 | 展示成员数TOP10社团 |
| 学生年级分布 | 环形图 | 展示各年级学生比例 |
| 活动类型分布 | 柱状图 | 展示各类型活动数量 |
| 活动时间热力图 | 柱状图 | 展示各月活动数量 |
| 推荐匹配度 | 环形进度条 | 展示推荐分数 |

### 6.2 图表交互

- 悬停提示（Hover Tooltip）
- 点击跳转详情
- 响应式自适应
- 动态刷新

---

## 七、性能优化

### 7.1 缓存策略

- 推荐结果缓存：`recommend:{user_id}`，有效期1小时
- 相似用户缓存：`similar_users:{user_id}`，有效期1小时
- 统计数据的缓存：按类型设置不同TTL

### 7.2 离线计算

- 每日凌晨批量计算用户/社团相似度矩阵
- 存储到 `SimilarityMatrix` 表
- 实时推荐时直接查询已计算的相似度

### 7.3 数据库优化

- 常用字段添加索引
- 使用 `select_related` 和 `prefetch_related` 减少查询
- 分页加载大量数据

---

## 八、扩展建议

### 8.1 算法优化

1. **引入机器学习**
   - 使用TensorFlow/PyTorch构建深度学习推荐模型
   - 使用矩阵分解（如SVD）进行协同过滤

2. **实时特征更新**
   - 接入Kafka/Flink处理实时用户行为
   - 实时更新用户画像

3. **A/B测试**
   - 实现算法对比实验
   - 评估不同算法的推荐效果

### 8.2 功能扩展

1. **社团智能匹配**
   - 社团可设置招收偏好（年级、专业等）
   - 系统自动匹配合适的学生

2. **活动推荐**
   - 基于学生兴趣推荐可能喜欢的活动
   - 活动提醒和预约

3. **社群发现**
   - 基于用户行为发现兴趣相似的用户群
   - 推荐加入或创建社群

### 8.3 数据源扩展

1. **接入更多数据**
   - 学生课程成绩
   - 图书馆借阅数据
   - 食堂消费数据（经过脱敏处理）

2. **外部数据**
   - 社团社交媒体数据
   - 第三方评价数据

---

## 九、常见问题

### Q1: 推荐结果不准确怎么办？
A: 
1. 检查学生档案是否完善（年级、专业、兴趣标签）
2. 触发重新计算：`/api/recommend/?refresh=true`
3. 管理员手动计算相似度矩阵：`/api/recommend/similarity/compute/`

### Q2: 如何提高推荐准确性？
A:
1. 鼓励用户完善个人信息和兴趣标签
2. 收集用户对推荐结果的反馈
3. 定期更新相似度矩阵

### Q3: 系统性能下降怎么办？
A:
1. 启用Redis缓存
2. 增加相似度矩阵的离线计算频率
3. 优化数据库查询

---

## 十、联系方式

如有问题，请联系开发团队。

---

*最后更新: 2026-04-22*
