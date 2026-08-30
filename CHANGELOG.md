# Changelog

本项目遵循语义化版本。所有影响 Skill 行为、模板或输出契约的变更都记录在这里。

## [0.1.0] - 2026-08-31

### Added

- Transformer 张量与矩阵运算专项 Skill。
- `formula`、`description`、`cell_values` 三项独立开关，默认全部关闭。
- Q/K/V 投影与多头拆分的横向 TikZ 模板。
- PNG、PDF 和 TikZ 三种交付格式约定。
- 带演示数字的三头拆分示例。

### Changed

- 将颜色从装饰性循环配色改为严格的 head 分区映射。
- 投影前输入使用中性色；投影后的列分区与输出 head 保持同色。

### Removed

- 默认图内署名、作者信息、水印和 Logo。
