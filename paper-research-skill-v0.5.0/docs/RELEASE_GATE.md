# 4.0 发布门禁

发布前依次执行单元测试、包校验、每个 skill 的快速校验和公开镜像的隐私/发布门禁。测试 fixture 必须是合成数据；私有论文正文、真实台账、审稿意见、全文、二进制稿件、作者信息和本地路径均不得复制到公开镜像。

安装前先运行 `install.py --dry-run --prune-legacy`，再运行 `--force --prune-legacy`。安装后比较唯一源 skill 和安装目录的文件哈希；其他 `$CODEX_HOME/skills` 内容必须保持不变。
