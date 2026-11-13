"""事件标签与行模式AST的静态合法性。"""
from .relations import predicate,validate

def nullable(node,labels,depth=0):
    if depth>60 or len(node)!=1:raise ValueError('模式结构非法或过深')
    if 'label' in node:
        if node['label'] not in labels:raise ValueError('未定义标签')
        return False
    if 'seq' in node or 'alt' in node:
        kind=next(iter(node));children=node[kind]
        if not children:raise ValueError('空模式分支')
        values=[nullable(c,labels,depth+1) for c in children]
        return all(values) if kind=='seq' else any(values)
    if 'repeat' in node:
        r=node['repeat'];minimum,maximum=r['min'],r['max']
        if type(minimum) is not int or minimum<0 or (maximum is not None and (type(maximum) is not int or maximum<minimum)):raise ValueError('量词范围非法')
        child=nullable(r['node'],labels,depth+1)
        if child:raise ValueError('量词子项不可接受空串')
        if type(r['greedy']) is not bool:raise ValueError('量词优先级非法')
        return minimum==0
    raise ValueError('不支持的模式节点')

def inspect(data,storage,root):
    validate(data['events'])
    if nullable(data['pattern'],data['labels']):raise ValueError('模式不可接受空串')
    rows=sorted(data['events'],key=lambda r:(r['shipment'],r['time'],r['row_id']))
    return {'order':[r['row_id'] for r in rows],'labels':{r['row_id']:[name for name,expr in data['labels'].items() if predicate(r,expr) is True] for r in rows}}
