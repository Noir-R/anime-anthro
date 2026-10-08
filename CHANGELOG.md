# 变更记录

## 1.1.5（2026-10-08）

海族三张 Q 版（转 Q 版路径）实测后补充。

- **新增 Q 版化程度量化验证**：只写 `2.5 head-body ratio` 实测只转成 3.5–4 头身（"像 Q 版但不够萌"）。
  判据为**头宽/身高**（人物 bbox 顶部 25% 身高区间的平均宽度 ÷ 总高）：≥0.30 达标、0.22–0.30 偏保守、
  <0.22 视为失败。三张海族首转实测 0.260 / 0.246 / 0.191（原图基线 0.13–0.18），均未达标。
  `prompt-templates.md` 第七节补入测法、阈值表与加码写法（`the head alone must occupy about 40% of
  the total body height, tiny short limbs, stubby arms and legs`）；SKILL Step 6 审图清单新增对应项。
- **转 Q 版的其他实测结论**：`image1` 用画布已扩展的 `*_framed` 版（留白充分，转换不易贴边）优于用原图；
  Q 版参考图需先从 `.webp` 转 `.png`（工具对 webp 支持未验证）；`chibi-ref-4` 原图 4096×4096，需先缩到 1024。
  Q 版构图用 `fit_canvas.py --fill 0.70`（规范 60–75%）。

## 1.1.4（2026-10-08）

小鱼（鲨鱼少年）实测后补充。

- **新增 `scripts/fit_canvas.py`**：把 1.1.3 的画布扩展补救法脚本化。
  `fit_canvas.py <图> --report` 先测量（人物占比 + 四周留白），不加参数则另存 `*_framed.png`。
  支持 `--fill`（目标高度占比，默认 0.80）与 `--ratio`（默认 9 16）。
  实测三张：94.9% → 80.2%（1216x2160）、92.5% → 79.8%（1184x2112）、96.7% → 80.0%（1248x2208）。
  顺带解决"右侧贴边"——小鱼图右边距仅 0.6%（鲨尾伸出），修正后左右各 15.6% / 15.9%。
- **新增少年 / 男性动作池（B1–B7）**：原 10 条动作池全是少女向（含 `her` / `skirt hem`），
  少年题材无池可用只能自由描述，既违反"`{POSE}` 必须取自池"的规则，又有污染性别特征的风险。
  男性角色现在只从 B 表取值（`his trouser pocket` / `arms crossed` / `prop resting on his shoulder` 等）。

## 1.1.3（2026-10-08）

实测小虾 v2 后发现：1.1.2 的构图修复未生效，且去水印脚本出现误判。

- **构图修复未生效**：1.1.2 的 `occupies about 80% of the frame HEIGHT` 实测仍出到 **94.9%**
  （下边距 1.6%）。改为更强约束：`the figure's total height must be about 78% of the image height`
  + `at least 8% clear margin above the head and ... below the feet` +
  `small full-body figure floating in a large white field`，并显式否定 `must NOT fill or touch the frame edges`。
- **新增画布扩展补救法**（Step 6 审图清单）：留白不达标时用 Pillow 把成图贴到更大的 9:16 白画布，
  零重采样、零画质损失，**不为此重 roll**（重 roll 会换掉整张脸和服装）。
  实测：1024x1824 出图 → 画布 1216x2160、偏移 (96,150) → 高度占比 94.9% → 80.2%，上下留白 9.8%/10.0%。
- **`remove_watermark.py` 误判修复**：判据「右下角区域 + 亮度区间」会把伸进角落的裙摆当成水印
  （小虾图误判 2964 像素，最大连通块 1973）。新增连通域形态过滤 `--max-block`（默认 400px）：
  水印 = 多个小笔画块 + 贴底边；裙摆 = 一两个大块 + 不贴底。dry-run 输出块数 / 最大块 / 底边命中数
  三项形态指标供人工判断，误判风险由"直接涂白"降级为"报告 + 人工确认"。
- 附注：动作修复（1.1.1）本轮二次验证有效——蟹 v3 vs 虾 v2 剪影 IoU = **0.493**（明显不同），
  优于上一轮的 0.764。

## 1.1.2（2026-10-08）

实测两张立绘（螃蟹娘 v2/v3）后发现的构图与脚本问题。

- **构图偏满**：审图要求"人物占画面 75–85%"，实测两版高度占比达 **94.6% / 96.7%**，
  下边距仅 0.9% / 0.7%（脚几乎贴底边）。原因是 prompt 里 `occupies 80% of frame` 被模型理解成"占满"。
  修复：构图段改为 `occupies about 80% of the frame HEIGHT, with clear white margin above the head
  and below the feet and at least 5% margin on all four sides`；审图清单新增「四周留白 ≥5%」项。
- **`remove_watermark.py` 阈值逻辑缺陷**：原逻辑 `lum > threshold` 对近白背景同样成立，
  dry-run 命中率虚高到 97.6%（等于会把整片背景和人物浅色边缘一起涂白）。
  修复：只处理 `threshold ≤ lum ≤ NEAR_WHITE(250)` 的灰色像素，跳过纯白背景与人物暗部。
  修复后实测：v2 命中 77 像素（真实水印，已清除）、v3 命中 0 像素（无水印）。
- 附注：本轮用 Pillow 计算剪影 IoU 验证了 1.1.1 的动作修复——v2 与 v3 剪影 IoU = 0.764（中等区间）。

## 1.1.1（2026-10-08）

修复"每次默认动作都一样"的动作同质化问题。

- **根因一**：模板默认 `{POSE}` 是硬编码的一句笼统描述（`standing relaxed, ... one hand making a small delicate gesture`），
  选"AI 自主发挥"时每次字面内容完全相同；且描述太模糊，模型没有具体指引就退化成复制参考图姿势。
- **根因二**：文生图时 `input_fidelity: high` 会把参考图的**构图与姿势一起锁死**，不只是画风。
- **修复**：
  - `prompt-templates.md` 新增**动作池**（10 条具体动作，中英对照），`{POSE}` 只能从中取值，禁止自由描述；
    规定同批次不重复、与上一张不重复、AI 自主发挥=从池中挑选并报出第几条。
  - 主模板与画风锚定短版加入"参考图只锁画风、不要抄姿势"声明。
  - `input_fidelity` 规则改为：**文生图 medium，图生图/微调/转 Q 版 high**。
  - `SKILL.md` Step 2 第 2 问改为从动作池选（提问时给 3 个候选），并新增「动作多样性规则」块。
  - `pitfalls.md` 新增第一节「动作同质化」（症状/根因/5 步处理），原六节顺延编号。

## 1.1.0（2026-10-08）

修复 4 个会导致实际执行出错的问题，并做一致性收敛与体验增强。

### P0 修复

- **负面清单可落地**：ImageGen 没有 `negative_prompt` 入参，反向提示词改为并入正向模板末尾的
  `Avoid in the result:` 行。新增「ImageGen 调用参数速查」章节。
- **画幅落到调用层**：明确 `size: 1024x1824`。实测工具接受任意尺寸但会向下对齐到 16px 粒度
  （请求 `1024x1820` 实得 `1024x1808`），故取 16 的倍数精确命中 9:16。
- **槽位定义补齐**：新增 `{OUTFIT_DESC}`、`{PROP_DESC}` 定义，并把已定义却未使用的
  `{BODY_TYPE}`、`{NECKLINE}` 接进正向模板；明确 Step 3 符号与槽位的对应关系。
- **输出归档规范**：新增 `output_dir` 与命名约定（`<题材>/<对象>-<版本>.png`）。

### P1 一致性

- 参考图清单收敛为 `assets/README.md` 单一权威源，`fetch_assets.py` 直接解析该表，
  `SKILL.md` / `style-guide.md` 改为引用（原先 5 处重复维护）。
- 负面清单收敛为 `prompt-templates.md` 一份，`style-guide.md` 不再维护副本。
- 统一数量口径为 19 张（原 `style-guide.md` 标题写"13 张"）。

### P2 增强

- 新增 `references/pitfalls.md`：娘化防跑偏、少年防娘化、平涂防厚涂、动作参考污染、
  水印与高频坑表，主文件只留索引。
- 新增 Step 5.1 图生图微调规则：局部修改必须 `image1` 传原图，禁止重新文生图导致符号漂移。
- 新增快速路径：用户明确授权"你看着办"时可直接用推荐默认值开工，但须显式列出默认值。
- 新增重 roll 策略（最多 3 次，逐次加码：重跑 → 换参考图 → 前置失败项）。
- `fetch_assets.py`：新增魔数校验（防止 HTML 错误页被当成图片）、stdout 编码自愈、
  清单改为从 README 解析；去掉对 `PYTHONIOENCODING` 的外部依赖。
- 新增 `scripts/remove_watermark.py`（水印处理从 SKILL 正文抽出为可执行脚本）。
- `description` / `tags` 扩充触发词：娘化、历史人物、武侠、器物拟人、海族兽设、转 Q 版。
- 硬规矩第 4 条改为"不要自行修改本技能文件"，避免执行时擅自改动 SKILL。

## 1.0.0

初版：正常比例 + Q 版双模式、19 张参考图、皮肤红线、四问流程。
