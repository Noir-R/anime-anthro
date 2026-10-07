# 在另一台电脑上使用本技能（WorkBuddy）

## 方式一：解压技能包（推荐）

1. 把 `ai-model-anime-anthro.zip` 复制到另一台电脑。
2. 解压到 WorkBuddy 的用户技能目录：

   | 系统 | 目标路径 |
   |---|---|
   | Windows | `C:\Users\<你的用户名>\.workbuddy\skills\` |
   | macOS / Linux | `~/.workbuddy/skills/` |

   解压后确认存在这个文件（**多一层目录是常见错误**）：

   ```
   ~/.workbuddy/skills/ai-model-anime-anthro/SKILL.md
   ```

3. **重启 WorkBuddy**（技能在会话启动时加载；正在运行的旧会话不会自动识别新技能）。
4. 新会话中直接说需求即可触发，例如："给 Gemini 画个拟人立绘"、"娘化林黛玉，Q版"。
   也可显式调用：`/ai-model-anime-anthro`。

## 方式二：直接拷贝文件夹

把整个 `ai-model-anime-anthro` 文件夹（含 `assets/`）复制过去，放到同上目录。效果与方式一等同。

## 目录结构说明

```
ai-model-anime-anthro/
├── SKILL.md                      主流程（含四问步骤、审图清单）
├── INSTALL.md                    本文件
├── references/
│   ├── style-guide.md            技法规范 + 符号映射先例库 + Q版规范 + 负面清单
│   └── prompt-templates.md       正常比例 / Q版 / 转Q版 三套提示词模板
└── assets/                       全套参考图（已内置，无需外部图片）
    ├── style-ref-*.jpg           正常比例系列参考 14 张（按模型命名：
    │                             GPT-白龙 / Claude-古书 / Grok-战斧 / Kimi-三棱镜长裙 /
    │                             DeepSeek-鲸鱼女仆 / 智谱-国风礼服 / Qwen-轮椅病号服 /
    │                             MiniMax-场记板 / Mistral-法棍猫耳 / 混元-冬装围巾 /
    │                             LLaMA-羊驼睡衣 / Zai-黑狐 / 未确认-紫星猫耳 / 09-待确认）
    └── chibi-ref-*.webp          Q版参考 5 张（黑蓝舞娘 / 紫黑慵懒 /
                                  国风斗篷冷淡 / 白金制服 / 运动服）
```

## 注意事项

- **assets 必须一起带走**，否则换电脑后参考图缺失，画风锁不住。
- 技能内已内置娘化防跑偏规则（历史人物/武侠题材会强制少女化提示词），无需额外配置。
- 生成图像会调用图像模型并消耗积分，与在哪台电脑运行无关，走的是同一个账号。
- 若另一台电脑已有同名技能目录，先备份再覆盖。
