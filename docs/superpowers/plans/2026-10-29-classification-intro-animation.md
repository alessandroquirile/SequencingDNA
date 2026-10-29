# DNA Classification Intro Animation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an introductory didactic animation ("FASE INTRO: Cos'è la Classificazione?") at the start of `DNAPipelineAnimation` in `dna_pipeline.py`, showing an AI reading a DNA sequence and sorting it into one of the 7 molecular classes.

**Architecture:** Implement a 3-block visual layout (Input DNA with nucleotide coloring -> Central AI Scanner Box -> 7 Target Class Boxes) with routing animation to Class 4 ("Sintasi") and clean fadeout before Phase 0.

**Tech Stack:** Python 3, Manim Community Edition (v0.21.0).

## Global Constraints
- Target file: `dna_pipeline.py`
- Position: Start of `DNAPipelineAnimation.construct()`, between background color setting and FASE 0.
- Colors: Dark theme (`#111111`), A (Green `#2ECC71`), C (Blue `#3498DB`), G (Gold `#F39C12`), T (Red `#E74C3C`).
- Must render cleanly with `manim -ql -s dna_pipeline.py DNAPipelineAnimation`.

---

### Task 1: Add FASE INTRO Animation to `DNAPipelineAnimation`

**Files:**
- Modify: `dna_pipeline.py:8-12`
- Test: Verification via Manim render command (`manim -ql -s dna_pipeline.py DNAPipelineAnimation`)

**Interfaces:**
- Consumes: `manim` library primitives (`Scene`, `VGroup`, `Text`, `RoundedRectangle`, `SurroundingRectangle`, `Line`, `CurvedArrow`, `FadeIn`, `FadeOut`, `Write`, `Create`, `Indicate`, `Transform`)
- Produces: Integrated visual animation at the start of `DNAPipelineAnimation`

- [ ] **Step 1: Write test rendering script to verify baseline**

Run:
```bash
source .venv/bin/activate && python -c "from dna_pipeline import DNAPipelineAnimation; print('Import successful')"
```
Expected: `Import successful`

- [ ] **Step 2: Implement FASE INTRO in `dna_pipeline.py`**

Insert the following intro sequence right after line 8 (`self.camera.background_color = "#111111"`):

```python
        # ----------------------------------------------------
        # FASE INTRO: Cos'è la Classificazione del DNA?
        # ----------------------------------------------------
        intro_title = Text("Cos'è la Classificazione del DNA?", font_size=24, color=WHITE)
        intro_title.to_edge(UP, buff=0.4)
        intro_subtitle = Text("Assegnare una sequenza di nucleotidi a una specifica classe funzionale", font_size=13, color=GRAY_A)
        intro_subtitle.next_to(intro_title, DOWN, buff=0.15)
        
        self.play(Write(intro_title), FadeIn(intro_subtitle), run_time=1.2)
        self.wait(0.5)

        # 1. BLOCCO SINISTRA: Sequenza DNA (Input)
        dna_input_title = Text("Sequenza DNA (Input)", font_size=13, color=TEAL, weight=BOLD)
        
        raw_dna = "ATGCCCCAACTAAAT"
        nuc_colors = {"A": "#2ECC71", "C": "#3498DB", "G": "#F39C12", "T": "#E74C3C"}
        dna_chars = VGroup(*[
            Text(char, font="Monospace", font_size=17, color=nuc_colors.get(char, WHITE), weight=BOLD)
            for char in raw_dna
        ]).arrange(RIGHT, buff=0.08)
        dna_dots_intro = Text("...", font="Monospace", font_size=17, color=GRAY_B).next_to(dna_chars, RIGHT, buff=0.08)
        dna_seq_group = VGroup(dna_chars, dna_dots_intro)
        
        dna_box = RoundedRectangle(
            corner_radius=0.1, width=3.4, height=1.1,
            color=TEAL, stroke_opacity=0.6, fill_color="#181818", fill_opacity=0.8
        )
        dna_content = VGroup(dna_input_title, dna_seq_group).arrange(DOWN, buff=0.18)
        dna_content.move_to(dna_box.get_center())
        left_group = VGroup(dna_box, dna_content).move_to(LEFT * 4.3 + UP * 0.1)

        # 2. BLOCCO CENTRO: Modello AI (Classificatore)
        ai_box = RoundedRectangle(
            corner_radius=0.15, width=2.4, height=1.6,
            color=BLUE_C, stroke_opacity=0.8, fill_color="#15202B", fill_opacity=0.9
        )
        ai_title = Text("Modello AI", font_size=15, color=WHITE, weight=BOLD)
        ai_sub = Text("Classificatore", font_size=12, color=BLUE_B)
        ai_icon_dots = VGroup(*[
            Dot(radius=0.05, color=c) for c in [TEAL, BLUE_B, GOLD, GREEN]
        ]).arrange(RIGHT, buff=0.12)
        ai_content = VGroup(ai_title, ai_sub, ai_icon_dots).arrange(DOWN, buff=0.15)
        ai_content.move_to(ai_box.get_center())
        center_group = VGroup(ai_box, ai_content).move_to(LEFT * 0.7 + UP * 0.1)

        # 3. BLOCCO DESTRA: 7 Classi Molecolari (Target)
        classes_info = [
            ("0", "Recettori GPCR"),
            ("1", "Tirosin-chinasi"),
            ("2", "Tirosina fosfatasi"),
            ("3", "Sintetasi"),
            ("4", "Sintasi"),
            ("5", "Canale ionico"),
            ("6", "Fattore trascrizione")
        ]
        
        target_boxes = VGroup()
        for idx, name in classes_info:
            c_num = Text(idx, font="Monospace", font_size=11, color=GOLD if idx == "4" else GRAY_B, weight=BOLD)
            c_name = Text(name, font_size=10, color=WHITE if idx == "4" else GRAY_A)
            row_txt = VGroup(c_num, c_name).arrange(RIGHT, buff=0.15)
            row_bg = RoundedRectangle(
                corner_radius=0.06, width=2.9, height=0.38,
                color=GOLD if idx == "4" else GRAY_D,
                stroke_opacity=0.6 if idx == "4" else 0.3,
                fill_color="#222222", fill_opacity=0.7
            )
            row_txt.move_to(row_bg.get_center())
            row_group = VGroup(row_bg, row_txt)
            target_boxes.add(row_group)
            
        target_boxes.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        target_title = Text("7 Classi Molecolari Target:", font_size=12, color=WHITE, weight=BOLD)
        target_title.next_to(target_boxes, UP, buff=0.15, aligned_edge=LEFT)
        right_group = VGroup(target_title, target_boxes).move_to(RIGHT * 3.7 + UP * 0.1)

        # Apparizione dei blocchi
        self.play(FadeIn(left_group, shift=RIGHT * 0.3), run_time=0.9)
        self.play(FadeIn(center_group, shift=RIGHT * 0.3), run_time=0.8)
        self.play(FadeIn(right_group, shift=LEFT * 0.3), run_time=1.0)
        self.wait(0.5)

        # Animazione di scansione AI (lettura nucleotidi)
        scan_line = Line(
            dna_chars.get_top() + UP * 0.15,
            dna_chars.get_bottom() + DOWN * 0.15,
            color=YELLOW, stroke_width=3
        )
        scan_line.move_to(dna_chars.get_left())
        scan_label = Text("Scansione nucleotidi...", font_size=11, color=YELLOW).next_to(dna_box, DOWN, buff=0.15)

        self.play(Create(scan_line), FadeIn(scan_label), run_time=0.5)
        self.play(scan_line.animate.move_to(dna_chars.get_right()), run_time=1.4)
        self.play(FadeOut(scan_line), FadeOut(scan_label), run_time=0.4)
        self.wait(0.3)

        # Feed into AI: freccia da sequenza ad AI
        arrow_to_ai = Arrow(
            dna_box.get_right(), ai_box.get_left(),
            buff=0.1, color=TEAL, stroke_width=3, max_tip_length_to_length_ratio=0.25
        )
        self.play(GrowArrow(arrow_to_ai), run_time=0.6)
        self.play(Indicate(ai_box, color=YELLOW, scale_factor=1.05), run_time=0.8)
        self.wait(0.3)

        # Routing verso la Classe 4 (Sintasi)
        target_class_4 = target_boxes[4]
        arrow_to_target = CurvedArrow(
            ai_box.get_right() + UP * 0.1,
            target_class_4.get_left(),
            angle=-0.25, color=GOLD, stroke_width=3.5
        )
        
        pred_badge = RoundedRectangle(
            corner_radius=0.08, width=2.9, height=0.38,
            color=GREEN, fill_color=GREEN, fill_opacity=0.25, stroke_width=2
        ).move_to(target_class_4.get_center())
        
        pred_label = Text("✓ Predizione: Classe 4 (Sintasi)", font_size=12, color=GREEN, weight=BOLD)
        pred_label.next_to(target_boxes, DOWN, buff=0.25)

        self.play(Create(arrow_to_target), run_time=0.8)
        self.play(
            FadeIn(pred_badge),
            target_class_4.animate.scale(1.08),
            FadeIn(pred_label),
            run_time=0.8
        )
        self.wait(1.0)

        # Messaggio didattico di sintesi in basso
        summary_intro = Text(
            "Input: Sequenza non etichettata  ➔  Output: Categoria biologica assegnata",
            font_size=13, color=WHITE
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(summary_intro), run_time=1.0)
        self.wait(1.5)

        # Pulizia scena prima di FASE 0
        intro_all = VGroup(
            intro_title, intro_subtitle, left_group, center_group, right_group,
            arrow_to_ai, arrow_to_target, pred_badge, pred_label, summary_intro
        )
        self.play(FadeOut(intro_all), run_time=1.0)
        self.wait(0.5)
```

- [ ] **Step 3: Run render verification to ensure syntax and animations render cleanly**

Run:
```bash
source .venv/bin/activate && manim -ql -s dna_pipeline.py DNAPipelineAnimation
```
Expected: Output image rendered successfully with exit code 0.

- [ ] **Step 4: Commit changes**

```bash
git add dna_pipeline.py docs/superpowers/plans/2026-10-29-classification-intro-animation.md
git commit -m "feat: add classification intro animation to dna_pipeline.py"
```
