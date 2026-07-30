# 公开发布与隐私净化

## 私库与公开库边界

私库可以保存个人论文项目、全文证据、投稿材料和审稿记录。公开库只发布通用 workflow、skill、agent 描述、空模板和辅助脚本。

## 公开前必须移除

- 本机用户名、本地路径、私库名、论文项目名、样板论文题名。
- CNKI 全文、CAJ/PDF、全文抽取文本、下载清单、带路径的文献管理导出。
- 投稿材料、审稿意见、作者身份、机构信息、授权截图。
- cookie、token、password、`.env`、浏览器配置、密钥。
- 未复核压缩包和二进制材料。

## 发布 gate

运行：

```powershell
python scripts/release_gate.py --public-root <path>
```

若公开库历史中已经出现隐私痕迹，且提交数量少、无人协作，应重建干净 root commit 并 force-with-lease 推送。
