# assets — 系列参考图

> **本文件的「文件清单」表格是参考图清单的唯一权威源。**
> `scripts/fetch_assets.py` 会解析这张表来决定下载什么；`SKILL.md` 与 `style-guide.md` 均引用此处，不再各自罗列。
> **增删改参考图时，改这里就够了。**

存放锁画风用的系列参考图，共 19 张（正常比例 14 张 + Q 版 5 张）。
生成新角色时选一张作为 ImageGen 的 **`image1`** 传入，用于锚定线稿与上色质感。

## 为什么这个目录可能是空的

SkillHub 平台拒收二进制媒体（`.png/.jpg/.jpeg/.webp/.svg` 等一律返回
400「不允许的文件类型」），因此**发布到 SkillHub 的版本不携带图片**。
从 GitHub 仓库克隆的版本则自带全套图片，无需额外操作。

## 缺失时如何补齐

在技能根目录运行：

```bash
python scripts/fetch_assets.py
```

脚本会从公开 CDN（jsDelivr → GitHub raw）拉取缺失的图片，已存在的自动跳过。
脚本已内置 UTF-8 输出自愈，正常情况下无需额外设置环境变量。

手动下载：<https://github.com/Noir-R/anime-anthro/tree/main/assets>

## 文件清单

| 文件 | 用途 |
| --- | --- |
| `style-ref-智谱-国风礼服.jpg` | 国风 / 中式题材默认 |
| `style-ref-Kimi-三棱镜长裙.jpg` | 少女感最强，娘化与柔和题材默认 |
| `style-ref-GPT-白龙.jpg` | 幻想种族默认 |
| `style-ref-DeepSeek-鲸鱼女仆.jpg` | 女仆系 |
| `style-ref-Claude-古书.jpg` | 书卷系 |
| `style-ref-Grok-战斧.jpg` | 黑红金高对比 |
| `style-ref-Qwen-轮椅病号服.jpg` | 病号服变体 |
| `style-ref-MiniMax-场记板.jpg` | 现代职业装 |
| `style-ref-Mistral-法棍猫耳.jpg` | 兽耳 + 道具 |
| `style-ref-混元-冬装围巾.jpg` | 冬装 |
| `style-ref-LLaMA-羊驼睡衣.jpg` | 睡衣 |
| `style-ref-Zai-黑狐.jpg` | 黑狐 / 兽化 |
| `style-ref-未确认-紫星猫耳.jpg` | 紫星猫耳 |
| `style-ref-09-待确认.jpg` | 备用 |
| `chibi-ref-1-黑蓝舞娘.webp` | Q 版：华丽纱裙 |
| `chibi-ref-2-紫黑慵懒.webp` | Q 版：外套混搭 |
| `chibi-ref-3-国风斗篷冷淡.webp` | Q 版：中式冷淡 |
| `chibi-ref-4-白金制服.webp` | Q 版：制服系 |
| `chibi-ref-5-运动服.webp` | Q 版：休闲运动 |
