# zdatabase
基于flask_sqlalchemy的数据库工具库，集成过滤器、字段转换、冗余字段生成、表单验证等功能。


## 安装
```
pip install zdatabase
```


## 初始化
```python
# database.py
engine, metadata = db.init(SQLALCHEMY_DATABASE_URI)

# app.py
db.mount(app)
```

## 定义模型
```python
class Draft(Model):
    __table__ = Table('collect_draft', metadata, ForeignKeyConstraint(('project_id',), ("client_project.id",)), autoload=True, autoload_with=engine)
    tpl_path = 'inspect/draft/template.docx'
    project = relationship('Project', uselist=False, backref='draft')

    @property
    def key_derive_map(self):
        username_map = UserMapper.get_username_map()
        return {
            'chief': {
                'name': 'chief_name',
                'func': lambda x: username_map.get(x)
            },
            'members': {
                'name': 'member_names',
                'func': lambda members: ','.join([username_map.get(member) for member in members]) if members else ''
            }
        }
    
    def to_json(self):
        data = self.to_json_()
        project_data = self.project.to_json() if self.project else {}
        return {**project_data, **data}
```

## 定义映射器
```python
from app.criterion.models import Indicator
from utils.cache import cached, ttl_cache


class IndicatorMapper(Indicator):
    @classmethod
    def make_flts(cls, **kwargs):
        flts = cls.select_(kwargs, ['id'])
        flts += cls.select(kwargs, ['name'])
        return flts

    @classmethod
    def get_jsons(cls):
        attr_names = ['id', 'name', 'method', 'restriction']
        rows = cls.get_attrs(attr_names)
        return [dict(zip(attr_names, row)) for row in rows]

    @classmethod
    @cached(ttl_cache)
    def get_name_map(cls):
        return cls.get_map(['id', 'name'])
```

## 查询
```python
from app.sonar.mappers import EntryMapper
from typing import Optional
from sqlalchemy import func


class EntryReadResource:
    def post(page_id: Optional[int] = None, dataset_id: Optional[int] = None):
        entries = EntryMapper.get_list(
            is_read=0, page_id=page_id, dataset_id=dataset_id)
        for entry in entries:
            entry.read_time = func.now()
        EntryMapper.commit()

    def get(site_id: Optional[int] = None, page_id: Optional[int] = None, dataset_id: Optional[int] = None, page_num: Optional[int] = None, page_size: Optional[int] = None, **kwargs):
        return EntryMapper.get_jsons(is_read=0, site_id=site_id, page_id=page_id, dataset_id=dataset_id, order_key='id', order_way='desc', page_num=page_num, page_size=page_size)
```