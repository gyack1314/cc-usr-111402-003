# 资料及接口契约

支持AST节点label、seq、alt、repeat(min,max,greedy)，max可null但整体模式不允许接受空串。标签谓词使用eq/gt/is_null，按SQL三值，UNKNOWN不匹配。每个起点取一个优先匹配：alt子项按声明顺序；repeat按greedy优先更多或更少重复；seq按深度优先的组合优先序，定义等价于保留所有有限路径后按分支选择序比较。skip为past_last或next_row；每个分区按(time,row_id)升序，输出中每个绑定是(label,row_id,ordinal)。不支持回溯引用、任意Python代码或跨货件状态。baseline.py仅有标签谓词、排序和AST合法性检查，尚无模式执行。

所有记录为合成仓资料；data/source.json保存原始字段和身份。storage.py负责摘要读取，table.py保存独立关系版本，relations.py保留SQL三值和袋语义。inspect只调用现有基础接口，不提供新增查询或管理能力。
