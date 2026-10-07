---
name: ai-model-anime-anthro
slug: ai-model-anime-anthro
version: 1.0.0
displayName: AI 大模型拟人日系立绘
summary: 把任意 AI 模型、品牌或器物拟人化为日系平涂赛璐璐风格全身立绘，内置 19 张参考图锁定画风。
description: AI大模型拟人日系立绘生成技能。当用户要求为某个 AI 大模型/产品/品牌（如 GPT、Claude、DeepSeek、Kimi、智谱、Qwen、混元、MiniMax、Mistral、LLaMA、Z.ai 等）设计拟人化角色立绘，或要求生成"AI 娘"/模型拟人/品牌拟人少女立绘，或提及"模型拟人、AI拟人、品牌拟人、AI娘立绘"时使用本技能。产出日系平涂赛璐璐风格、纯色底、全身立绘的角色图，并遵循"模型特点→视觉符号"的设计逻辑。
tags: [AI娘, 模型拟人, 品牌拟人, 立绘, 插画, 日系, 赛璐璐, Q版]
license: MIT
homepage: https://github.com/Noir-R/anime-anthro
agent_created: true
---

# AI 大模型拟人日系立绘生成

将任意 AI 模型/品牌拟人化为日系动漫风格全身立绘，风格锚定为小红书 Astraumbra《各大主流AI大模型拟人形象整理》系列：干净黑线稿 + 日系平涂薄渐变赛璐璐 + 纯色底 + 静态站姿全身构图 + "模型梗→视觉符号"人设逻辑。

## 工作流

### Step 0 — 加载规范

始终先读取 `references/style-guide.md`（技法规范+负面清单）和 `references/prompt-templates.md`（提示词模板），不要凭记忆生成提示词。

### Step 1 — 确定目标对象

明确本次要拟人化的模型/产品名称。若用户未指定，先询问。随后快速梳理该模型的关键梗：所属公司、LOGO 色与 LOGO 图形、核心能力、社区知名梗（算力、长文本、开源、Sleep Mode、价格战等）。

### Step 2 — 必做提问步骤（不可跳过）

**第 0 问（最先问）——立绘比例模式**：

1. **正常比例**：6.5–7 头身写实比例少女，走原流程。
2. **Q版 chibi**：2–3 头身大头萌系，细节不降级，规范见 `references/style-guide.md` 第七节；提示词用 `references/prompt-templates.md` 的 Q版模板。
3. **已有立绘转 Q版**：用户指定一张已有成图，走"转Q版"流程（见 Step 5 末尾）。

随后确认以下 4 项（AskUserQuestion 单次最多 4 问，第 0 问可与其余分两次调用），每项都保留"AI 自主决定"选项：

1. **人物原型**：人类少女 / 兽耳拟人 / 幻想种族（龙、鲸、狐等）/ 由 AI 根据模型特性决定（原系列做法：GPT=白龙、DeepSeek=鲸、GLM=黑狐）。
2. **动作**：用户指定动作 / AI 在"放松静态站姿+轻小手势"框架内发挥（推荐）/ 完全由 AI 决定。
3. **配色**：用户指定主色辅色 / 锁定品牌 LOGO 色（推荐）/ AI 自由决定。
4. **背景**：逐张询问——严格纯白底 / 纯白底+允许极淡单色装饰元素（如 Kimi 的月亮乐谱）/ 其他。

用户答案未给出时不得自行假设，必须追问。四个答案写入后续提示词的对应槽位。

> **硬规矩（不可跳过）：先问齐、后动手**
>
> 1. **必须等所有提问项都得到明确回答之后，才允许调用 ImageGen。** 不允许"边问边画"、"问一部分就先画一版看看"，也不允许凭惯性沿用上一次的答案（同一批次可沿用，但须在提问中显式列出并让用户确认）。
> 2. **槽位变更 = 重新提问。** 不仅是首次生成，后续任何一次修改（换动作、换配色、换背景、换服装、改细节方向等）都属于槽位变更，必须先问再做；即便用户已经给出了大致方向（例如"动作改成 XX"），仍需就具体选项提问确认后再执行。
> 3. **回答不完整时继续等待。** 若用户回答中出现"稍后给参考图"、"待定"、"你看着办"等，须等待补充材料或明确授权后再动手，不得自行假设默认值开工。
> 4. 违反本规矩等同于流程失败——用户提出批评时应立即补提问，并把教训写入本文件。

### Step 3 — 先定符号再画图

不要先画衣服。第一步提炼三个要素并先向用户复述确认：

- **代表动物/种族**（若 Step 2 选了非人类）
- **品牌主色**（LOGO 色提取，写明具体色相）
- **核心能力道具**（手持物直接对应模型能力，如 Claude=厚重古书、Kimi=三棱镜+乐谱、MiniMax=海螺+场记板、Grok=X形斧）

确认后再进入生成。

### Step 4 — 构建提示词

按 `references/prompt-templates.md` 的模板组装正向与反向提示词：

- 画风锚定词、全身立绘构图词、人物特征、服装（类型由人设决定，不限于洋装）、道具与配饰、背景规则（来自 Step 2 第 4 问）、负面清单完整附加。
- 画幅固定竖版 9:16。
- **皮肤红线**：兽化/种族特征一律不得作用于皮肤，肤色必须是正常人类肤色，皮肤上无鳞片、兽纹、斑纹或非人质感。种族感只从角、兽耳、尾巴、额饰、发色、瞳色瞳形、服装纹样、配饰、手套鞋袜这些"可摘除的配件层"表达。
- **体型与性感度可配置**：按角色人设调整（如丰满体型、大开领口），启用时遵循 `prompt-templates.md` 的合规护城河——明示 adult、附加负面词（nude/topless/nipples/see-through/child/loli）、裸露上限为锁骨/事业线/肩背/腿部，不露点不透。用户未提及则默认纤细体型+正常领口。注意：黝黑/蜜色等人类正常肤色范围不属于皮肤红线（如"黑旋风"李逵的深肤色是有效人设符号）。
- 服装类型遵循人设逻辑：默认复古洋装/洛丽塔/国风礼服，但 MiniMax 型现代职业装、Qwen 型病号服、LLaMA 型睡衣等"贴合模型人设的变体"同样合法——系列统一性靠线稿、上色质感与构图保证，不靠服装品类。
- **物品/家电/器物拟人（冰箱、洗衣机、电饭煲等）**：默认走**特征人设**，禁止"本体嫁接"。即：画一个正常人类少女，把物品特征降维成服装结构与配饰（功能部件→服装结构：门→对开襟/门缝压边、抽屉→分层裙、面板→腰包挂饰；标志色→配色；使用场景小物→手持道具），**不要把物品本体当身体或往身上挂**（如胸前背一台冰箱）。提示词须显式写 "a normal human girl wearing elegant clothing, NOT an appliance with arms and legs, the identity is expressed only through fashion details and accessories"。仅当用户点名要"本体造型"时才走本体嫁接。
- **服装风格必须匹配物品的时代属性**：现代工业/科技产物（家电、数码、家电品牌）→ 现代都市 / tech-wear / 制服系（参考图用 `style-ref-MiniMax-场记板` 或 `chibi-ref-4-白金制服`），**不得配复古洋装或古风礼服**；传统器物、非遗、古董、历史题材才用国风礼服/古装。

### Step 5 — 生成与锁画风

- 使用 ImageGen 生成。
- **生成新角色时，把系列中已有的一张图作为 Image reference 参考图传入**，锁定画风与线条。`assets/` 内已内置全套系列参考图（正常比例 14 张 + Q版 5 张，可移植）：
  - **正常比例（style-ref-*，按模型/题材命名）**：`style-ref-智谱-国风礼服`（国风/中式默认）、`style-ref-Kimi-三棱镜长裙`（少女感最强，娘化/柔和题材默认）、`style-ref-GPT-白龙`（幻想种族默认）、`style-ref-DeepSeek-鲸鱼女仆`（女仆系）、`style-ref-Claude-古书`（书卷系）、`style-ref-Grok-战斧`（黑红金高对比）、`style-ref-Qwen-轮椅病号服`、`style-ref-MiniMax-场记板`（现代装）、`style-ref-Mistral-法棍猫耳`、`style-ref-混元-冬装围巾`、`style-ref-LLaMA-羊驼睡衣`、`style-ref-Zai-黑狐`、`style-ref-未确认-紫星猫耳`、`style-ref-09-待确认`。
  - **Q版（chibi-ref-*）**：`chibi-ref-1-黑蓝舞娘`（华丽纱裙）、`chibi-ref-2-紫黑慵懒`（外套混搭）、`chibi-ref-3-国风斗篷冷淡`（中式冷淡）、`chibi-ref-4-白金制服`（制服系）、`chibi-ref-5-运动服`（休闲运动系）。
  - 选取原则：与目标角色的**种族/服装类型/色调**最接近的那张；若本机另有自备图集也可直接使用（路径由使用者自行决定，不在技能内硬编码）。
- **娘化防跑偏（历史人物/武侠/男性角色题材必做）**：正向必须写 "clearly feminine bishoujo girl, delicate cute anime face"，负面必须加 `male, boy, bishounen, masculine face, broad shoulders`；参考图选少女感强的 `style-ref-Kimi-三棱镜长裙`。仅写 "hero / martial / warrior" 会生成美少年脸。
- **平涂防厚涂（粗豪/武士/深肤色题材必做）**：这类题材极易被带成厚涂 CG 风。正向必须显式写 "STRICTLY match the reference's art style: FLAT coloring, very soft THIN single-layer shadows, bright airy clean colors"，负面加 `heavy shading, painterly shading, dark shadows`；必要时把 `input_fidelity` 提到 high 强锁参考画风。
- **Q版模式**：正向提示词改用 Q版模板，负面清单按 Q版规则调整（去掉 chibi，加入 realistic proportions 等）；参考图优先用 `assets/chibi-ref-1-黑蓝舞娘.webp` 或 `assets/chibi-ref-2-紫黑慵懒.webp` 锁 Q版质感。
- **已有立绘转 Q版（image-to-image）**：image1 传原立绘，image2 传一张 Q版参考图（assets 内二选一），提示词核心句："Convert the character in the first image into chibi style matching the second reference image: keep the identical character design — same hairstyle, hair color and gradient, same outfit with all details, same accessories, props and color palette; change only the body proportions to chibi (about 2.5 head-body ratio), oversized head, small rounded body, big expressive eyes, rounded cheeks; plain pure white background, full body visible head to toe, not cropped."转换后原设计的符号、服装、配色必须一一对应，逐项核对。
- **少年/男性角色防娘化（题材本体是男性/少年时必做，与上一条方向相反）**：正向必须写 "young teenage boy, male, slender boyish frame, flat chest"，负面必须加 `female, girl, bishoujo, breasts, curves, feminine body`；重绘已有少年图时 `image1` 传原图即可锁性别与设计。参考图是少年本尊时无需另传少女参考。
- **动作参考图带画风污染时**：若动作参考是厚涂 CG 风（如 Fate Saber 类图），画风会被带厚——先生成姿势，再用一次编辑把画风压回平涂（"redraw in much FLATTER anime cel-shading, thin single-layer shadows, remove painterly texture"），并逐项复核头巾/配饰等易回退项。
- **输出自动水印**：生成图右下角可能自动带"AI生成"等合规水印，ImageGen 去水印指令常无效；角落为纯白时直接用 PIL 按阈值涂白（x>0.72w, y>0.9h 区域，>140~150 亮度像素置纯白），注意避开人物边缘。
- 每次生成后立即用 Step 6 清单审图，不合格主动重roll，并告知用户可要求换模型或调整。

### Step 6 — 审图清单

逐项核对，任一不满足即修正后重roll：

- [ ] 全身完整从头到脚，无裁切（负面对照：cropped / cut off）
- [ ] 人物居中，占画面约 75–85%，纯色底无环境背景
- [ ] 干净黑轮廓线，外粗内细，无杂乱排线、无厚涂
- [ ] 日系少女脸（Q版模式为圆润大头萌脸），写实比例约 6.5–7 头身（Q版为 2–3 头身），不混淆
- [ ] 高光小而精，无大面积刺眼高光
- [ ] 视觉符号到位：代表动物/道具/LOGO 元素/品牌主色缺一不可
- [ ] 皮肤为正常人类肤色，无鳞片/兽纹/异色皮肤（种族特征只出现在配件层）
- [ ] 静态站姿+轻小手势（除非用户指定了动态）
- [ ] 对比度与品牌色调性匹配（浅色系→低对比梦幻；深色系→高对比华丽）
- [ ] 无意外文字叠加（LOGO 字母等设计内元素除外）

## 注意事项

- 涉及真实品牌时仅做同人风格视觉设计，不冒充官方形象；生成后提醒用户非官方。
- 用户中途要求修改时，优先改提示词槽位重roll，而不是推翻人设符号。
- 批量做多个模型时，逐张走 Step 2 第 4 问（背景），其余三项确认一次可沿用，但用户可随时推翻。
