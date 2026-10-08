# 防跑偏经验库（踩坑记录）

本文件沉淀"提示词里不写就会翻车"的实战规则。`SKILL.md` 主流程只留索引，不重复正文。

## 一、动作同质化（每次出图姿势都一样）—— 高频

**症状**：连续多次生成姿势雷同，尤其选了"AI 自主决定动作"时。

**根因（两条，通常同时发生）**：

1. 提示词里用了笼统的动作描述（如 `one hand making a small delicate gesture`）。
   模型没有具体指引，就会退化成复制参考图的姿势。
2. 文生图时 `input_fidelity` 用了 `high`。high 不只锁画风，会把参考图的**构图、镜头、姿势**一起锁死。

**处理（按序）**：

1. `{POSE}` 必须从 `prompt-templates.md` **动作池**里选一条具体条目，不得自由描述。
2. 文生图 `input_fidelity` 降到 **`medium`**；`high` 只留给图生图（微调 / 转 Q 版 / 重绘已有角色）。
3. 提示词保留这句：`the reference image is for ART STYLE ONLY — do NOT copy its pose, camera angle or composition`。
4. 若仍雷同，换一张姿势不同的参考图 —— 参考图的站姿往往就是出图的站姿。
5. 同批次多角色时，显式给每个角色分配池中不同条目，并把上一张的动作关键词写进 `Avoid` 段。

## 二、娘化防跑偏（历史人物 / 武侠 / 男性角色题材必做）

正向必须写：`clearly feminine bishoujo girl, delicate cute anime face`
`Avoid` 必须加：`male, boy, bishounen, masculine face, broad shoulders`

> 原因：只写 `hero / martial / warrior` 会稳定生成美少年脸。
> 参考图选少女感最强的 `style-ref-Kimi-三棱镜长裙`。

## 三、少年 / 男性角色防娘化（与上一条方向相反，题材本体是男性时必做）

正向必须写：`young teenage boy, male, slender boyish frame, flat chest`
`Avoid` 必须加：`female, girl, bishoujo, breasts, curves, feminine body`

> 重绘已有少年图时 `image1` 传原图即可锁性别与设计；参考图是少年本尊时无需另传少女参考。

## 四、平涂防厚涂（粗豪 / 武士 / 深肤色 / 重甲题材必做）

这类题材极易被带成厚涂 CG 风。

正向必须显式写：`STRICTLY match the reference's art style: FLAT coloring, very soft THIN single-layer shadows, bright airy clean colors`
`Avoid` 必须加：`heavy shading, painterly shading, dark shadows`
必要时把 `input_fidelity` 提到 `high` 强锁参考画风（图生图场景）。

## 五、动作参考图带画风污染

若动作参考是厚涂 CG 风（如 Fate Saber 类图），画风会被带厚。

处理方式：先生成姿势，再用一次图生图把画风压回平涂 ——
`redraw in much FLATTER anime cel-shading, thin single-layer shadows, remove painterly texture`
并**逐项复核头巾 / 配饰等易回退项**（画风重绘时小配饰最容易丢失）。

## 六、输出水印

生成图右下角可能自动带"AI 生成"等合规水印，在 prompt 里写去水印指令通常无效。

处理方式：角落为纯白时，用 `scripts/remove_watermark.py` 按阈值涂白（默认区域 `x > 0.72w, y > 0.90h`，亮度 >145 的像素置纯白），注意避开人物边缘。

```bash
python scripts/remove_watermark.py <图片路径> [--dry-run]
```

## 七、其他高频坑

| 症状 | 处理 |
|---|---|
| 兽化特征长到皮肤上 | 皮肤槽位句子必须逐字保留，不可省略；`Avoid` 段皮肤类词不可删 |
| 发色渐变被吃掉 | 正向写明 `hair gradient from A to B`，并在参考图里挑一张有渐变的 |
| 核心道具没画出来 | 把道具放在 `props:` 段首位并加 `clearly visible, held in hand`；一次只给一件主道具 |
| 手指畸形 | `Avoid` 保留 `extra fingers`；手部动作尽量用"托、拎、扶"等贴合身体的姿态，避免张开五指 |
| LOGO 字母变成乱码文字 | 用挂件 / 刺绣承载字母，且 `Avoid` 保留 `text, logo artifacts` |
| 人物被裁切 | 构图段 `head to toe visible, not cropped` 与 `Avoid` 的 `cropped, cut off` 双重保险 |
| 姿势抄参考图 | 见本文第一节 |
