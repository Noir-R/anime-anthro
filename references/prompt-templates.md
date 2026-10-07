# 提示词模板

## 槽位定义（由 SKILL Step 2 的四个提问结果填充）

- `{PROTOTYPE}`：人物原型——人类少女 / 兽耳少女(具体动物) / 幻想种族(具体：龙、鲸、狐等)
- `{POSE}`：动作——用户指定动作，或默认 "standing relaxed, slight contrapposto, one hand making a small delicate gesture"
- `{COLOR}`：配色——品牌 LOGO 主色 + 辅色，或用户指定色
- `{BACKGROUND}`：背景——严格纯白："plain pure white background, no scenery"；允许极淡装饰："+ very faint monochrome decorative elements matching the character theme (e.g. crescent moon, floating musical notes), low saturation, non-intrusive"
- `{BODY_TYPE}`：体型——默认 "slender feminine girl body"；可按角色人设改为 "adult voluptuous feminine figure, large bust, narrow waist, wide hips"（如莽汉型角色的丰满设定）
- `{NECKLINE}`：领口——默认正常领口；可改为 "deep open V collar showing the collarbone and cleavage, revealing but tasteful, no nudity"（大开领口型）

## 体型/性感度槽位的合规护城河（启用 {BODY_TYPE} 或 {NECKLINE} 加强版时必须附加）

1. 正向必须明示 "adult"（成年角色）。
2. 负面必须附加：`nude, naked, topless, exposed nipples, see-through clothes, explicit sexual content, child, loli`。
3. 裸露尺度上限：露锁骨、事业线、肩背与腿部；不露点、不透、不做性暗示姿势。
4. 皮肤红线不受体型槽位影响，仍然生效。

## 正向提示词模板（英文，喂给 ImageGen）

```
masterpiece, best quality, anime style illustration, Japanese fashion magazine illustration style,
full body character sheet, single full-body figure, standing, {PROTOTYPE},
{POSE},
face: delicate bishoujo face, large expressive anime eyes with small highlight in pupil, slender face, calm gentle expression, realistic proportions, about 7 head tall slender girl, NOT chibi,
hair: very long wavy hair, layered flowing strands, hair color matches {COLOR} primary color,
outfit: {OUTFIT_DESC — 服装描述，按人设选：ornate vintage lolita dress / improved chinese-style gown / modern casual outfit / etc.}, large skirt with layered frills and pleats, ribbon bows, chains, tassels, metal and gem charms, brand logo motifs printed on skirt and accessories, letter charms,
props: {PROP_DESC — 核心能力道具，如 holding a thick ancient book / prism refracting a rainbow beam / conch shell / X-shaped battle-axe},
colors: {COLOR — 主色+辅色，含明度描述}, soft cel-shading, thin soft gradients, clean flat colors, moderate saturation, small delicate highlights, subtle pearlescent sheen,
{BACKGROUND},
composition: character centered, occupies 80% of frame, front three-quarter view, eye-level, no perspective distortion, not cropped, head to toe visible,
clean crisp black outlines, line weight variation, thick outer contour thin inner details, no hatching, no sketch lines
```

### 画风锚定短版（有参考图时，重点在锁画风）

```
same art style as the reference image: clean black outlines with line weight variation, Japanese flat coloring with soft thin gradients, cel-shaded, soft low-contrast palette, small refined highlights, pure white background, full body standing portrait, character centered occupying 80% of frame, 9:16 vertical
```

## 反向提示词（完整附加，不删减）

```
cropped, cut off, out of frame, ugly, deformed, extra limbs, extra fingers, blurry, lowres, background scenery, complex background, environment, floor, shadow heavy, heavy shading, painterly shading, dark shadows, chibi, sd character, 3d render, realistic photo, thick heavy paint, impasto, oil painting, messy sketch, sketch lines, cross-hatching, hatching, watermark, signature, text, logo artifacts,
animal skin, scales on skin, reptilian skin, feathered skin, patterned skin, skin markings, green skin, blue skin, grey skin, non-human skin texture, glossy reptile scales on body
```

### 皮肤槽位（非人类角色时必须显式写明）

在正向提示词中加入固定句，防止兽化污染皮肤：

```
normal human skin tone, smooth natural human skin, no scales or animal patterns on skin,
ethnic traits expressed only through removable accessories: horns, ears, tail, head ornament, hair color, eye color and pupil shape, clothing patterns, gloves and footwear
```

## 组装规则

1. 服装描述 `{OUTFIT_DESC}` 必须与模型人设一致，从默认池（复古洋装/洛丽塔/国风礼服）或合法变体（现代职业装/病号服/睡衣/冬装）中选择，并写明品牌符号印在哪里（裙身刺绣、挂件、钥匙扣）。
2. `{PROP_DESC}` 必须与模型核心能力一一对应，一件主道具+至多两件小道具，不堆砌。
3. 特效小元素（星星、小云、音符）写在正向提示词末尾，附带 "faint, small, low saturation" 限定，防止抢主体。
4. 画幅始终 9:16 竖版。
5. 生成新角色时在 ImageGen 中传入系列已有图作为 Image reference，先用画风锚定短版试一张，确认风格一致后再用完整模板精修细节。

## Q版（chibi）模式模板

在主模板基础上，替换人物比例与五官段落为：

```
chibi style, about 2.5 head-body ratio, oversized head, small rounded body, tiny hands and feet,
face: rounded face with soft baby-fat cheeks, very large expressive anime eyes occupying about one third of the face, small nose and small mouth, expression reflects the character personality (e.g. calm cold gaze, lazy half-lidded eyes, cheerful smile),
details fully preserved at reduced scale: layered hair strands, intricate outfit pleats, lace, embroidery, chains and charms all finely drawn,
```

其余槽位（`{PROTOTYPE}`、`{POSE}`、`{COLOR}`、`{BACKGROUND}`、服装、道具、皮肤槽位）沿用主模板；构图段改为：

```
composition: character centered, occupies about 70% of frame, plain pure white background, full body visible head to toe, not cropped
```

**Q版负面清单**（在主负面清单基础上，删除 `chibi`、`sd character`，加入）：

```
realistic proportions, tall body, 7 head tall, long legs, adult body proportions
```

### 已有立绘转 Q版（image-to-image）

- `image1` = 原正常比例立绘；`image2` = Q版参考图（assets 内按服装类型就近选用）。
- 提示词：

```
Convert the character in the first image into chibi style matching the second reference image:
keep the identical character design — same hairstyle, same hair color and gradient, same outfit with all its details, same accessories, props and color palette, same expression personality;
change only the body proportions to chibi: about 2.5 head-body ratio, oversized head, small rounded body, tiny hands and feet, big expressive anime eyes, rounded cheeks;
same art style as the second reference: clean black outlines, flat cel-shading with soft thin gradients, small refined highlights;
plain pure white background, no scenery, full body visible head to toe, not cropped, character centered
```

- 负面清单同 Q版负面清单。
- 转换完成后逐项核对：发型/发色、服装件数与细节、配饰、道具、配色、表情性格必须与原图一一对应，缺失即补roll。
- 画幅：默认沿用原图画幅（9:16 或方图均可，与用户确认）。
