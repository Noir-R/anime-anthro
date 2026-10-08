# 提示词模板

> **权威负面清单在本文件末尾「反向提示词」一节，全技能仅此一份。**
> `style-guide.md` 不再维护负面清单副本。

## 零、ImageGen 调用参数速查（必读）

**ImageGen 只有 `prompt` 一个文本入参，没有 `negative_prompt`。** 所以反向提示词必须**并入 prompt 文本末尾**，格式见第一节末尾的 `Avoid in the result:` 行。

| 参数 | 立绘取值 | 说明 |
|---|---|---|
| `prompt` | 正向模板全文 + 末尾 `Avoid in the result: ...` | 唯一文本通道，正负面都走这里 |
| `size` | `1024x1824` | 竖版 9:16。**实测：工具会把尺寸向下对齐到 16px 粒度**（请求 `1024x1820` 实得 `1024x1808`）。写 16 的倍数可精确命中，误差 <1% 时无需裁剪 |
| `quality` | `high` | 立绘细节密集（蕾丝、链条、刺绣），最终出图建议 high；草稿/试画风可用 medium 省积分 |
| `image1` | 文生图画风锁定：系列参考图；微调：原成图 | **传图即进入图生图模式** |
| `image2` | 转 Q 版流程的 Q 版参考图 | 必须与 `image1` 同时传 |
| `input_fidelity` | **文生图 `medium`**；图生图 / 局部微调 / 转 Q 版 `high` | 仅图生图有效。**high 会把参考图的姿势与构图一并锁死** —— 文生图用 high 是动作同质化的主因 |
| `output_dir` | 见 `SKILL.md` Step 5「输出归档」 | 不指定则落在工作区 `generated-images` |

其他可用但本技能默认不设的参数：`style`、`background`（需抠图时可设 `transparent`）、`footnote`（≤16 字符角标文字）、`revise`。

## 一、槽位定义

八个槽位，全部由 `SKILL.md` Step 2/Step 3 的提问与符号确认结果填充：

| 槽位 | 含义 | 来源 |
|---|---|---|
| `{PROTOTYPE}` | 人物原型：人类少女 / 兽耳少女(具体动物) / 幻想种族(具体) | Step 2 第 1 问 |
| `{POSE}` | 动作，**必须从下方动作池选取具体条目**，不得使用笼统描述 | Step 2 第 2 问 |
| `{COLOR}` | 品牌 LOGO 主色 + 辅色（写明色相与明度） | Step 2 第 3 问 + Step 3 品牌主色 |
| `{BACKGROUND}` | 严格纯白 / 允许极淡装饰 | Step 2 第 4 问 |
| `{OUTFIT_DESC}` | 服装描述，**由 Step 3 人设逻辑推导** | Step 3（见 `style-guide.md` 服装体系） |
| `{PROP_DESC}` | 核心能力道具，**由 Step 3 符号提炼得出** | Step 3（一件主道具 + 至多两件小道具） |
| `{BODY_TYPE}` | 体型，默认 `slender feminine girl body` | 用户指定或默认 |
| `{NECKLINE}` | 领口，默认留空 | 用户指定或默认 |

> Step 3 提炼的三要素落位：代表动物/种族 → `{PROTOTYPE}`；品牌主色 → `{COLOR}`；核心能力道具 → `{PROP_DESC}`；服装由人设推导 → `{OUTFIT_DESC}`。

### 动作池（`{POSE}` 的唯一取值来源）

**禁止**用 "a small delicate gesture" 这类笼统描述——它每次都一样，且没有具体指引时模型会直接抄参考图的姿势。
必须从中选一条并原样填入 `{POSE}`：

| # | 动作 | 英文（直接填入 `{POSE}`） |
|---|---|---|
| 1 | 双手交叠于身前（文静） | `standing, both hands clasped gently in front of her, slight contrapposto` |
| 2 | 单手提裙摆，另一手垂身侧 | `standing, one hand lightly lifting the skirt hem, the other arm relaxed at her side` |
| 3 | 单手执道具于胸前，另一手下垂 | `standing, holding the prop with one hand at chest level, the other arm relaxed down` |
| 4 | 单手抬至锁骨处轻触 | `standing, one hand raised to lightly touch her collarbone, the other arm relaxed` |
| 5 | 侧身回眸，单手撩发 | `standing in a slight three-quarter turn looking back over her shoulder, one hand lifting a lock of hair` |
| 6 | 单手叉腰，另一手垂放 | `standing, one hand on her hip, the other arm relaxed at her side` |
| 7 | 双手捧小物于胸前 | `standing, holding a small object with both hands in front of her chest` |
| 8 | 单手向前微伸（邀请/指引） | `standing, one arm slightly extended forward with an open palm gesture` |
| 9 | 单手扶头饰 / 帽檐 | `standing, one hand raised to adjust her hair ornament, the other arm relaxed` |
| 10 | 双臂微张，裙摆展开 | `standing with both arms slightly open at her sides, skirt spreading outward` |

**选取规则**：

- 同一批次（多个角色）内**不得重复**使用同一条。
- 与上一张成图**不得相同**（哪怕跨批次），生成前先确认上一张用了哪条。
- 必须考虑与 `{PROP_DESC}` 的兼容：手持道具时优先选 2/3/7；道具挂腰间可选 1/5/6。

### 少年 / 男性动作池（题材本体为男性时**只从此表取**）

上表全为少女向（含 her / skirt hem），少年题材套用会污染性别特征。男性角色必须用下表：

| # | 动作 | 英文（直接填入 `{POSE}`） |
|---|---|---|
| B1 | 单手插兜，另一手垂放 | `standing, one hand casually in his trouser pocket, the other arm relaxed at his side` |
| B2 | 双臂抱胸，微侧身 | `standing with both arms crossed over his chest, slight three-quarter turn` |
| B3 | 单手叉腰，另一手垂放 | `standing, one hand on his hip, the other arm relaxed at his side` |
| B4 | 单手执道具扛肩 / 垂握 | `standing, holding the prop resting on his shoulder, the other arm relaxed down` |
| B5 | 侧身回眸 | `standing in a slight three-quarter turn looking back over his shoulder, both arms relaxed` |
| B6 | 单手抬起扶帽檐 / 头饰 | `standing, one hand raised to adjust his headwear, the other arm relaxed` |
| B7 | 双手插兜，双肩微松 | `standing with both hands in his trouser pockets, shoulders loose` |

同样遵守「同批次不重复、与上一张不重复」。少年题材的正向护栏见 `references/pitfalls.md` 第三节。
- AI 自主发挥 = 从本池挑选，**不是自由描述**；并在回复中明确告知用户选了第几条。

### 防"参考图带跑姿势"（文生图必加）

参考图只用来锁画风，**不能让它决定姿势**。两道保险：

1. 正向提示词必须包含这一句（放在 `composition:` 段之前）：
   ```
   pose note: the reference image is for ART STYLE ONLY — linework, coloring and shading; do NOT copy its pose, camera angle or composition, the pose must follow the {POSE} description above,
   ```
2. 文生图时 `input_fidelity` 用 **`medium`**（不是 high）。high 会把参考图的构图与姿势一并锁死，这是动作同质化的主因之一。
   `high` 只用于**图生图**（局部微调、转 Q 版、重绘已有角色）——那种场景需要锁住人物设计本身。

## 二、体型/性感度槽位的合规护城河（启用 `{BODY_TYPE}` 或 `{NECKLINE}` 加强版时必须附加）

1. 正向必须明示 `adult`（成年角色）。
2. `Avoid` 段必须附加：`nude, naked, topless, exposed nipples, see-through clothes, explicit sexual content, child, loli`。
3. 裸露尺度上限：露锁骨、事业线、肩背与腿部；不露点、不透、不做性暗示姿势。
4. 皮肤红线不受体型槽位影响，仍然生效。

## 三、正向提示词模板

```
masterpiece, best quality, anime style illustration, Japanese fashion magazine illustration style,
full body character sheet, single full-body figure, standing, {PROTOTYPE}, {BODY_TYPE},
{POSE},
face: delicate bishoujo face, large expressive anime eyes with small highlight in pupil, slender face, calm gentle expression, realistic proportions, about 7 head tall slender girl, NOT chibi,
hair: very long wavy hair, layered flowing strands, hair color matches {COLOR} primary color,
outfit: {OUTFIT_DESC}, {NECKLINE}, ribbon bows, chains, tassels, metal and gem charms, brand motifs printed on skirt and accessories, letter charms,
props: {PROP_DESC},
skin: normal human skin tone, smooth natural human skin, no scales or animal patterns on skin, ethnic traits expressed only through removable accessories: horns, ears, tail, head ornament, hair color, eye color and pupil shape, clothing patterns, gloves and footwear,
colors: {COLOR}, soft cel-shading, thin soft gradients, clean flat colors, moderate saturation, small delicate highlights, subtle pearlescent sheen,
{BACKGROUND},
pose note: the reference image is for ART STYLE ONLY — linework, coloring and shading; do NOT copy its pose, camera angle or composition, the pose must follow the {POSE} description above,
composition: the figure's total height must be about 78% of the image height, leaving generous empty white space — at least 8% clear margin above the head and at least 8% clear margin below the feet, margins on all four sides, the figure must NOT fill or touch the frame edges, small full-body figure floating in a large white field, front three-quarter view, eye-level, no perspective distortion, not cropped, head to toe visible,
clean crisp black outlines, line weight variation, thick outer contour thin inner details, no hatching, no sketch lines,
Avoid in the result: {NEGATIVE}
```

### 画风锚定短版（有参考图时，先试一张锁画风）

```
same art style as the reference image (linework, coloring and shading ONLY — do NOT copy its pose or composition): clean black outlines with line weight variation, Japanese flat coloring with soft thin gradients, cel-shaded, small refined highlights, pure white background, full body standing portrait, {POSE}, character centered occupying 80% of frame, 9:16 vertical,
Avoid in the result: {NEGATIVE}
```

## 四、反向提示词 `{NEGATIVE}`（权威版，完整附加不删减）

```
cropped, cut off, out of frame, ugly, deformed, extra limbs, extra fingers, blurry, lowres, background scenery, complex background, environment, floor, shadow heavy, heavy shading, painterly shading, dark shadows, chibi, sd character, 3d render, realistic photo, thick heavy paint, impasto, oil painting, messy sketch, sketch lines, cross-hatching, hatching, watermark, signature, text, logo artifacts,
animal skin, scales on skin, reptilian skin, feathered skin, patterned skin, skin markings, green skin, blue skin, grey skin, non-human skin texture, glossy reptile scales on body
```

中文对照：裁切、断肢、畸形、多余肢体、模糊、复杂场景背景、Q 版、3D 渲染、厚涂、潦草草图、排线、水印、意外文字、皮肤异化。

**使用方式**：整段原样填入模板末尾的 `{NEGATIVE}`，不要删词。Q 版模式按第六节做替换。

## 五、组装规则

1. `{OUTFIT_DESC}` 必须与模型人设一致，从默认池（复古洋装 / 洛丽塔 / 国风礼服）或合法变体（现代职业装 / 病号服 / 睡衣 / 冬装）中选择，并写明品牌符号印在哪里（裙身刺绣、挂件、钥匙扣）。
2. `{PROP_DESC}` 必须与模型核心能力一一对应，一件主道具 + 至多两件小道具，不堆砌。
3. 特效小元素（星星、小云、音符）写在正向提示词末尾，附带 `faint, small, low saturation` 限定，防止抢主体。
4. 画幅始终 `size: 1024x1824`（9:16 竖版）。
5. 生成新角色时 `image1` 传入系列已有图，先用画风锚定短版试一张，确认风格一致后再用完整模板精修细节。
6. 初次生成用文生图；**已有成图做局部修改一律用图生图**（见 `SKILL.md` Step 5.1）。

## 六、Q 版（chibi）模式模板

在主模板基础上，替换人物比例与五官段落为：

```
chibi style, about 2.5 head-body ratio, oversized head, small rounded body, tiny hands and feet,
face: rounded face with soft baby-fat cheeks, very large expressive anime eyes occupying about one third of the face, small nose and small mouth, expression reflects the character personality (e.g. calm cold gaze, lazy half-lidded eyes, cheerful smile),
details fully preserved at reduced scale: layered hair strands, intricate outfit pleats, lace, embroidery, chains and charms all finely drawn,
```

构图段改为：

```
composition: character centered, occupies about 70% of frame, plain pure white background, full body visible head to toe, not cropped
```

**Q 版 `{NEGATIVE}`**：在主负面清单基础上**删除** `chibi`、`sd character`，**加入**：

```
realistic proportions, tall body, 7 head tall, long legs, adult body proportions
```

其余槽位沿用主模板。

## 七、已有立绘转 Q 版（图生图）

- `image1` = 原正常比例立绘；`image2` = Q 版参考图（按服装类型就近选用）。
- 提示词：

```
Convert the character in the first image into chibi style matching the second reference image:
keep the identical character design — same hairstyle, same hair color and gradient, same outfit with all its details, same accessories, props and color palette, same expression personality;
change only the body proportions to chibi: about 2.5 head-body ratio, oversized head, small rounded body, tiny hands and feet, big expressive anime eyes, rounded cheeks;
same art style as the second reference: clean black outlines, flat cel-shading with soft thin gradients, small refined highlights;
plain pure white background, no scenery, full body visible head to toe, not cropped, character centered,
Avoid in the result: {Q版 NEGATIVE}
```

- 转换后逐项核对：发型/发色、服装件数与细节、配饰、道具、配色、表情性格必须与原图一一对应，缺失即补 roll。
- 画幅：默认沿用原图画幅（9:16 或方图均可，与用户确认）。

**Q 版化程度必须量化验证**（只写 `2.5 head-body ratio` 经常只转成 3.5–4 头身，看着"像 Q 版但不够萌"）：

```bash
<python> scripts/fit_canvas.py <图> --report   # 顺带看构图占比
# 头宽/身高：人物 bbox 顶部 25% 身高区间的平均宽度 ÷ 人物总高
```

| 头宽/身高 | 判定 |
|---|---|
| ≥ 0.30 | 达标（约 2.5 头身） |
| 0.22–0.30 | 偏保守（3–3.5 头身），可用但不萌 |
| < 0.22 | 基本没转换成功，必须重转 |

不达标时的加码写法（替换比例段）：

```
EXTREMELY oversized head — the head alone must occupy about 40% of the total body height,
tiny short limbs, stubby arms and legs, small rounded body much narrower than the head,
```

实测参考：三张海族角色首次转换得 0.19–0.26（未达标），原图基线为 0.13–0.18。
