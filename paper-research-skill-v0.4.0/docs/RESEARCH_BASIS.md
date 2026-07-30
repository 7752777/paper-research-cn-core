# v0.2 研究依据与设计取舍

## 选题与空白

- 空白必须写成可证伪、有限定范围的声明，并包含反证条件。
- “没搜到”不能证明空白；需要多源、多语种、同义词、引文链和明确停止原因。
- 最近邻论文与最危险邻居比泛泛的“文献较少”更能检验重复风险。
- 趋势、共词网络或文献计量只作佐证，不单独证明价值或创新。

参考：

- https://www.prisma-statement.org/
- https://developers.openalex.org/
- https://www.semanticscholar.org/product/api
- https://www.crossref.org/
- https://github.com/asreview/asreview
- https://www.bibliometrix.org/
- https://www.vosviewer.com/

## 文献与 Zotero

- 中文商业数据库无通用免费公开 API 时，采用授权终端人工检索导出、Agent 去重整理的混合模式。
- Google Scholar 不作为批量可复现 API。
- 全文只来自开放获取、作者/机构仓储、用户合法订阅或馆际互借。
- Zotero 是文献元数据源；证据账本是筛选与主张支持状态源。

参考：

- https://api.ies.ed.gov/eric/
- https://core.ac.uk/services/api
- https://doaj.org/api/docs
- https://unpaywall.org/products/api
- https://www.zotero.org/support/dev/web_api/v3/start
- https://www.zotero.org/support/kb/importing_standardized_formats
- https://retorque.re/zotero-better-bibtex/

## 教育与新传方法

- 方法按主张类型和识别要求选择，而不是按“看起来高级”选择。
- 默认优先数据字典、抽样与许可清晰的公共二手数据。
- 教育数据重点检查权重、合理值、嵌套与测量等值。
- 平台数据重点检查接口可见总体、排序/删除、条款、隐私和时间漂移。
- 计算文本必须有人类验证和误差传播分析。

参考：

- https://www.oecd.org/en/data/datasets/pisa-2022-database.html
- https://iea.nl/data-tools/repository
- https://www.gdeltproject.org/
- https://www.mediacloud.org/documentation
- https://www.aoir.org/reports/ethics3.pdf
- https://aapor.org/standards-and-ethics/
- https://www.testingstandards.net/

## 写作、排版与审稿

- 主张—证据结构先于流畅文本。
- Zotero/Better BibTeX + Quarto/Pandoc/CSL 可实现单源多产出；Word 原生也是可选路径，但两者不能并行成为正文权威源。
- 三轮审稿保持职责正交和意见独立，统一以修订矩阵和回归检查关闭问题。

参考：

- https://apastyle.apa.org/jars
- https://www.equator-network.org/
- https://publicationethics.org/guidance/guidelines
- https://pandoc.org/MANUAL.html
- https://quarto.org/docs/guide/
- https://citationstyles.org/
