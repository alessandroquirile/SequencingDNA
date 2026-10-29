from manim import *
import numpy as np


class DNAPipelineAnimation(Scene):
    def construct(self):
        # Imposta sfondo scuro (#111111)
        self.camera.background_color = "#111111"

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

        # ----------------------------------------------------
        # FASE 0: Dataset Originale (human.txt)
        # ----------------------------------------------------
        title0 = Text("Data set", font_size=24, color=WHITE)
        title0.to_edge(UP, buff=0.4)
        self.play(Write(title0), run_time=1.2)
        self.wait(0.5)

        orig_headers = ["sequence", "class"]
        orig_data = [
            ["ATGCCCCAACTAAATACTACCGTATGGCCC...", "4"],
            ["ATGAACGAAAATCTGTTCGCTTCATTCATT...", "4"],
            ["ATGTGTGGCATTTGGGCGCTGTTTGGCAGT...", "3"],
            ["...", "..."],
            ["ATGCAGCAGTCCAGTCCTGTCCTAGTCCTA...", "2"],
            ["ATGGGGGGGCACGGCACCGCACGCGCACGC...", "6"],
            ["ATGCCCAGTCCTGTCCAGTCCTGTCCAGTC...", "0"],
        ]

        orig_table = Matrix(
            orig_data,
            element_to_mobject=Text,
            element_to_mobject_config={"font_size": 12, "font": "Monospace"},
            h_buff=1.2,
            v_buff=0.45
        )
        orig_table.move_to(UP * 0.1)

        col_headers_orig = VGroup()
        for j, h in enumerate(orig_headers):
            hdr = Text(h, font="Monospace", font_size=13, color=TEAL if j < 1 else GOLD)
            hdr.move_to([orig_table.get_columns()[j].get_center()[0], orig_table.get_top()[1] + 0.35, 0])
            col_headers_orig.add(hdr)

        orig_shape = Text("4.380 sequenze di DNA (righe) × 2 colonne", font_size=12, color=GRAY_B)
        orig_shape.next_to(orig_table, DOWN, buff=0.3)

        class_legend_orig = VGroup(
            Text("0: Recettori accoppiati a proteine G", font_size=11, color=GRAY_A),
            Text("1: Tirosin-chinasi", font_size=11, color=GRAY_A),
            Text("2: Tirosina fosfatasi", font_size=11, color=GRAY_A),
            Text("3: Sintetasi", font_size=11, color=GRAY_A),
            Text("4: Sintasi", font_size=11, color=GRAY_A),
            Text("5: Canale ionico", font_size=11, color=GRAY_A),
            Text("6: Fattore di trascrizione", font_size=11, color=GRAY_A),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        class_legend_orig.next_to(orig_table, RIGHT, buff=0.4)
        class_title_orig = Text("Classi (0-6):", font_size=12, color=WHITE, weight=BOLD).next_to(class_legend_orig, UP,
                                                                                                 buff=0.15)
        class_legend_group_orig = VGroup(class_title_orig, class_legend_orig)

        orig_table_group = VGroup(orig_table, col_headers_orig, class_legend_group_orig, orig_shape)

        self.play(FadeIn(orig_table_group), run_time=1.5)
        self.wait(0.5)

        # Evidenzia ogni riga del dataset
        highlight_row = SurroundingRectangle(
            orig_table.get_rows()[0],
            color=YELLOW, buff=0.08, corner_radius=0.05
        )
        self.play(Create(highlight_row), run_time=0.8)
        self.wait(0.5)

        for i in range(1, len(orig_data)):
            next_highlight = SurroundingRectangle(
                orig_table.get_rows()[i],
                color=YELLOW, buff=0.08, corner_radius=0.05
            )
            self.play(
                Transform(highlight_row, next_highlight),
                run_time=0.6
            )
            self.wait(0.4)

        self.play(FadeOut(highlight_row), run_time=0.5)
        self.wait(0.5)

        self.play(FadeOut(VGroup(title0, orig_table_group)), run_time=1.0)
        self.wait(0.5)

        # ----------------------------------------------------
        # FASE 1: Extract 6-mers (Sliding Window)
        # ----------------------------------------------------
        title1 = Text("Determinare i k-mers (k=6, step=1)", font_size=24, color=WHITE)
        title1.to_edge(UP, buff=0.4)
        self.play(Write(title1), run_time=1.2)
        self.wait(0.5)

        dna_str = "ATGCCCCAATGC"
        dna_text_mgroup = VGroup(*[
            Text(char, font="Monospace", font_size=26, color=TEAL) for char in dna_str
        ]).arrange(RIGHT, buff=0.16)

        dna_dots = Text("...", font="Monospace", font_size=26, color=TEAL)
        dna_full = VGroup(dna_text_mgroup, dna_dots).arrange(RIGHT, buff=0.16)
        dna_full.move_to(LEFT * 2.5 + UP * 1.2)

        dna_label = Text("Sequenza DNA (Seq 1):", font_size=18, color=GRAY_A).next_to(dna_full, UP, aligned_edge=LEFT,
                                                                                      buff=0.2)

        self.play(FadeIn(dna_label), FadeIn(dna_full), run_time=1.2)
        self.wait(0.5)

        tokens_label = Text("Esameri estratti:", font_size=18, color=GRAY_A).move_to(RIGHT * 2.5 + UP * 2.0)
        self.play(FadeIn(tokens_label), run_time=0.8)
        self.wait(0.3)

        window = SurroundingRectangle(dna_text_mgroup[:6], color=YELLOW, buff=0.08, corner_radius=0.05)
        self.play(Create(window), run_time=1.0)

        token_texts_vgroup = VGroup()

        kmers = [
            ("ATGCCC", 0, 6),
            ("TGCCCC", 1, 7),
            ("GCCCCA", 2, 8),
            ("CCCCAA", 3, 9),
            ("CCCAAT", 4, 10),
            ("CCAATG", 5, 11),
            ("CAATGC", 6, 12),
        ]

        prev_token = None
        for i, (kmer, start, end) in enumerate(kmers):
            token = Text(f"'{kmer}'", font="Monospace", font_size=17, color=YELLOW)
            if prev_token is None:
                token.next_to(tokens_label, DOWN, buff=0.2)
            else:
                token.next_to(prev_token, DOWN, buff=0.18)
            token_texts_vgroup.add(token)

            window_target = SurroundingRectangle(dna_text_mgroup[start:end], color=YELLOW, buff=0.08,
                                                 corner_radius=0.05)

            if i == 0:
                self.play(FadeIn(token, shift=LEFT * 0.2), run_time=0.8)
            else:
                self.play(Transform(window, window_target), FadeIn(token, shift=LEFT * 0.2), run_time=0.6)
            self.wait(0.4)
            prev_token = token

        window_dots_target = SurroundingRectangle(dna_dots, color=YELLOW, buff=0.08, corner_radius=0.05)
        token_dots = Text("...", font="Monospace", font_size=17, color=YELLOW)
        token_dots.next_to(prev_token, DOWN, buff=0.18)
        token_texts_vgroup.add(token_dots)

        self.play(Transform(window, window_dots_target), FadeIn(token_dots, shift=LEFT * 0.2), run_time=0.7)
        self.wait(1.2)

        phase1_elements = VGroup(
            title1, dna_label, dna_full, window, tokens_label, token_texts_vgroup
        )
        self.play(FadeOut(phase1_elements), run_time=1.0)
        self.wait(0.5)

        # ----------------------------------------------------
        # FASE 1.5: Dataset Processato (k-meri joined + class)
        # ----------------------------------------------------
        title_raw = Text("Data set processato", font_size=24, color=WHITE)
        title_raw.to_edge(UP, buff=0.4)
        self.play(Write(title_raw), run_time=1.2)
        self.wait(0.5)

        raw_headers = ["k-mers", "class"]
        raw_data = [
            ["ATGCCC TGCCCC GCCCCA CCCCAA CCCAAC CCAACT ...", "0"],
            ["ATGAAC TGAACG GAACGA AACGAA ACGAAA CGAAAT ...", "4"],
            ["ATGTGT TGTGTG GTGTGG TGTGGC GTGGCA TGGCAA ...", "1"],
            ["...", "..."],
            ["ATGCAG TGCAGT GCAGTC CAGTCC AGTCCT GTCCTA ...", "2"],
            ["ATGGGG TGGGGC GGGGCA GGGCAC GGCACC GCACGC ...", "6"],
            ["ATGCAG TGCAGT GCAGTC CAGTCC AGTCCT GTCCTT ...", "3"],
        ]

        raw_table = Matrix(
            raw_data,
            element_to_mobject=Text,
            element_to_mobject_config={"font_size": 12, "font": "Monospace"},
            h_buff=1.2,
            v_buff=0.45
        )
        raw_table.move_to(UP * 0.1)

        col_headers_raw = VGroup()
        for j, h in enumerate(raw_headers):
            hdr = Text(h, font="Monospace", font_size=13, color=TEAL if j < 1 else GOLD)
            hdr.move_to([raw_table.get_columns()[j].get_center()[0], raw_table.get_top()[1] + 0.35, 0])
            col_headers_raw.add(hdr)

        raw_shape = Text("4.380 righe × 2 colonne", font_size=12, color=GRAY_B)
        raw_shape.next_to(raw_table, DOWN, buff=0.3)

        class_legend = VGroup(
            Text("0: Recettori accoppiati a proteine G", font_size=11, color=GRAY_A),
            Text("1: Tirosin-chinasi", font_size=11, color=GRAY_A),
            Text("2: Tirosina fosfatasi", font_size=11, color=GRAY_A),
            Text("3: Sintetasi", font_size=11, color=GRAY_A),
            Text("4: Sintasi", font_size=11, color=GRAY_A),
            Text("5: Canale ionico", font_size=11, color=GRAY_A),
            Text("6: Fattore di trascrizione", font_size=11, color=GRAY_A),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        class_legend.next_to(raw_table, RIGHT, buff=0.4)
        class_title = Text("Classi:", font_size=12, color=WHITE, weight=BOLD).next_to(class_legend, UP, buff=0.15)
        class_legend_group = VGroup(class_title, class_legend)

        raw_table_group = VGroup(raw_table, col_headers_raw, class_legend_group, raw_shape)

        self.play(FadeIn(raw_table_group), run_time=1.5)
        self.wait(1.5)

        self.play(FadeOut(VGroup(title_raw, raw_table_group)), run_time=1.0)
        self.wait(0.5)

        # ----------------------------------------------------
        # FASE 2: Stratified Train / Test Split
        # ----------------------------------------------------
        title2 = Text("Stratified Split (80/20)", font_size=24, color=WHITE)
        title2.to_edge(UP, buff=0.4)
        self.play(Write(title2), run_time=1.2)
        self.wait(0.5)

        global_rect = RoundedRectangle(corner_radius=0.1, width=6.0, height=1.2, color=BLUE_B, fill_color=BLUE_E,
                                       fill_opacity=0.6)
        global_text = Text("Data Set (4.380 sequenze + etichette)", font_size=18, color=WHITE)
        global_block = VGroup(global_rect, global_text).move_to(UP * 2.0)

        self.play(FadeIn(global_block), run_time=1.2)
        self.wait(0.8)

        train_rect = RoundedRectangle(corner_radius=0.1, width=4.2, height=1.6, color=GREEN_B, fill_color="#1b4332",
                                      fill_opacity=0.8)
        train_t1 = Text("Training Set (80%)", font_size=16, color=WHITE, weight=BOLD)
        train_t2 = Text("x_train: 3.504 sequenze", font_size=13, color=GREEN_B)
        train_t3 = Text("y_train: 3.504 etichette", font_size=13, color=GREEN_B)
        train_content = VGroup(train_t1, train_t2, train_t3).arrange(DOWN, buff=0.08)
        train_block = VGroup(train_rect, train_content).move_to(LEFT * 3 + UP * 0.2)

        test_rect = RoundedRectangle(corner_radius=0.1, width=2.8, height=1.6, color=RED_A, fill_color="#4a1521",
                                     fill_opacity=0.8)
        test_t1 = Text("Test Set (20%)", font_size=16, color=WHITE, weight=BOLD)
        test_t2 = Text("x_test: 876 sequenze", font_size=13, color=RED_A)
        test_t3 = Text("y_test: 876 etichette", font_size=13, color=RED_A)
        test_content = VGroup(test_t1, test_t2, test_t3).arrange(DOWN, buff=0.08)
        test_block = VGroup(test_rect, test_content).move_to(RIGHT * 3 + UP * 0.2)

        split_arrow_left = Arrow(global_block.get_bottom(), train_block.get_top(), color=GRAY_B, buff=0.15)
        split_arrow_right = Arrow(global_block.get_bottom(), test_block.get_top(), color=GRAY_B, buff=0.15)

        self.play(
            Create(split_arrow_left),
            Create(split_arrow_right),
            ReplacementTransform(global_block.copy(), train_block),
            ReplacementTransform(global_block.copy(), test_block),
            run_time=1.5
        )
        self.wait(1.0)

        arrow_train = Arrow(train_block.get_bottom(), train_block.get_bottom() + DOWN * 1.2, color=GREEN_B, buff=0.15)
        fit_transform_label = Text("CountVectorizer.fit_transform()", font="Monospace", font_size=15, color=GREEN_B).next_to(
            arrow_train, RIGHT, buff=0.1)
        train_bow_label = Text("x_train_bow", font_size=20, color=GREEN_B).next_to(arrow_train, DOWN, buff=0.15)

        arrow_test = Arrow(test_block.get_bottom(), test_block.get_bottom() + DOWN * 1.2, color=RED_A, buff=0.15)
        transform_label = Text("CountVectorizer.transform()", font="Monospace", font_size=15, color=RED_A).next_to(arrow_test, RIGHT,
                                                                                                   buff=0.1)
        test_bow_label = Text("x_test_bow", font_size=20, color=RED_A).next_to(arrow_test, DOWN, buff=0.15)

        self.play(
            Create(arrow_train), Write(fit_transform_label), Write(train_bow_label),
            Create(arrow_test), Write(transform_label), Write(test_bow_label),
            run_time=1.2
        )
        self.wait(1.0)

        leakage_box = RoundedRectangle(corner_radius=0.1, width=8.5, height=0.8, color=GOLD, fill_color="#3a2e05",
                                       fill_opacity=0.9)
        leakage_box.move_to(DOWN * 3.0)
        leakage_text = Text(
            "NO DATA LEAKAGE: Il vocabolario viene appreso SOLO dal Training Set",
            font_size=15,
            color=GOLD,
            weight=BOLD
        ).move_to(leakage_box.get_center())
        leakage_badge = VGroup(leakage_box, leakage_text)

        self.play(FadeIn(leakage_badge, scale=0.9), run_time=1.2)
        self.wait(2.5)

        phase2_elements = VGroup(
            title2, global_block, split_arrow_left, split_arrow_right,
            train_block, test_block, arrow_train, fit_transform_label, train_bow_label,
            arrow_test, transform_label, test_bow_label, leakage_badge
        )
        self.play(FadeOut(phase2_elements), run_time=1.0)
        self.wait(0.5)

        # ----------------------------------------------------
        # FASE 3: Feature Extraction (Bag-of-Words Matrix)
        # ----------------------------------------------------
        title3 = Text("Bag-of-Words di training", font_size=24, color=WHITE)
        title3.to_edge(UP, buff=0.4)
        self.play(Write(title3), run_time=1.2)
        self.wait(0.5)

        matrix_data = [
            ["0", "0", "0", "1", "0", "...", "1"],
            ["1", "0", "0", "2", "0", "...", "0"],
            ["...", "...", "...", "...", "...", "...", "..."],
            ["2", "0", "1", "0", "0", "...", "1"]
        ]

        matrix = Matrix(
            matrix_data,
            element_to_mobject=Text,
            element_to_mobject_config={"font_size": 15, "font": "Monospace"},
            h_buff=1.3,
            v_buff=0.55
        )

        row_names = ["Seq 1", "Seq 2", "...", "Seq 3504"]
        row_labels = VGroup()
        for i, row_name in enumerate(row_names):
            lbl = Text(row_name, font_size=14, color=GRAY_A)
            lbl.move_to([matrix.get_left()[0] - 0.5, matrix.get_rows()[i].get_center()[1], 0])
            row_labels.add(lbl)

        col_names = ["AAAAAA", "AAAAAC", "AAAAAG", "AAAAAT", "CAAAAA", "...", "TTTTTT"]
        col_headers = VGroup()
        for j, col_name in enumerate(col_names):
            hdr = Text(col_name, font="Monospace", font_size=14, color=TEAL)
            hdr.move_to([matrix.get_columns()[j].get_center()[0], matrix.get_top()[1] + 0.35, 0])
            col_headers.add(hdr)

        vocab_header_label = Text("4.096 Colonne (Vocabolario)", font_size=14, color=TEAL)
        vocab_header_label.next_to(col_headers, UP, buff=0.3)

        full_matrix_block = VGroup(matrix, row_labels, col_headers, vocab_header_label)
        full_matrix_block.move_to(UP * 0.4)

        self.play(FadeIn(full_matrix_block), run_time=1.5)
        self.wait(1.0)

        highlight = SurroundingRectangle(
            matrix.get_rows()[0],
            color=YELLOW, buff=0.12, corner_radius=0.05
        )
        # feat_tag = Text("Vettore delle feature", font_size=13, color=YELLOW)
        feat_tag = MathTex(r"\text{Vettore delle feature } \mathbf{x}_i \in \mathbb{R}^{4096}",
                           font_size=13, color=YELLOW)
        feat_tag.next_to(highlight, RIGHT, buff=0.5)

        self.play(Create(highlight), FadeIn(feat_tag), run_time=1.0)
        self.wait(0.8)

        for i in range(1, 4):
            next_highlight = SurroundingRectangle(
                matrix.get_rows()[i],
                color=YELLOW, buff=0.12, corner_radius=0.05
            )

            self.play(
                Transform(highlight, next_highlight),
                UpdateFromFunc(feat_tag, lambda t: t.next_to(highlight, RIGHT, buff=0.5)),
                run_time=0.8
            )
            self.wait(0.6)

        shape_box = RoundedRectangle(corner_radius=0.1, width=8.0, height=1.3, color=BLUE_C, fill_color="#102030",
                                     fill_opacity=0.8)
        shape_box.move_to(DOWN * 1.9)

        train_shape_tex = MathTex(r"\text{x\_train\_bow.shape}: (3504 \times 4096)", font_size=20, color=GREEN_B)
        test_shape_tex = MathTex(r"\text{x\_test\_bow.shape}: (876 \times 4096)", font_size=20, color=RED_A)
        shapes_vgroup = VGroup(train_shape_tex, test_shape_tex).arrange(DOWN, buff=0.15)
        shapes_vgroup.move_to(shape_box.get_center())

        shape_info = VGroup(shape_box, shapes_vgroup)

        self.play(FadeIn(shape_info, shift=UP * 0.2), run_time=1.2)
        self.wait(2.0)

        phase3_elements = VGroup(
            title3, full_matrix_block, highlight, feat_tag, shape_info
        )
        self.play(FadeOut(phase3_elements), run_time=1.0)
        self.wait(0.5)

        # ----------------------------------------------------
        # FASE 4: Model Training (Logistic Regression - .fit())
        # ----------------------------------------------------
        title4 = Text("Addestramento Modello (LogisticRegression.fit())", font_size=24, color=WHITE)
        title4.to_edge(UP, buff=0.4)
        self.play(Write(title4), run_time=1.2)
        self.wait(0.5)

        xtrain_box = RoundedRectangle(corner_radius=0.1, width=3.2, height=0.8, color=GREEN_B, fill_color="#1b4332",
                                      fill_opacity=0.8)
        xtrain_txt = Text("x_train_bow\n(3504 × 4096)", font_size=12, color=WHITE)
        xtrain_txt.move_to(xtrain_box.get_center())
        xtrain_group = VGroup(xtrain_box, xtrain_txt).move_to(LEFT * 4.2 + UP * 2.2)

        ytrain_box = RoundedRectangle(corner_radius=0.1, width=3.2, height=0.8, color=GOLD, fill_color="#3a2e05",
                                      fill_opacity=0.8)
        ytrain_txt = Text("y_train\n(3504 etichette)", font_size=12, color=WHITE)
        ytrain_txt.move_to(ytrain_box.get_center())
        ytrain_group = VGroup(ytrain_box, ytrain_txt).move_to(LEFT * 4.2 + UP * 1.0)

        model_rect = RoundedRectangle(corner_radius=0.15, width=4.8, height=1.9, color=BLUE_B, fill_color="#0d2b45",
                                      fill_opacity=0.9)
        model_title = Text("LogisticRegression", font_size=15, color=WHITE, weight=BOLD)
        model_sub1 = Text("solver = 'lbfgs'", font="Monospace", font_size=12, color=TEAL)
        model_sub2 = Text("max_iter = 5000", font="Monospace", font_size=12, color=TEAL)
        model_sub3 = Text("multi_class = 'multinomial'", font="Monospace", font_size=11, color=GRAY_A)
        model_content = VGroup(model_title, model_sub1, model_sub2, model_sub3).arrange(DOWN, buff=0.1)
        model_block = VGroup(model_rect, model_content).move_to(RIGHT * 1.8 + UP * 1.6)

        fit_arrow1 = Arrow(xtrain_group.get_right(), model_block.get_left() + UP * 0.35, color=GREEN_B, buff=0.12)
        fit_arrow2 = Arrow(ytrain_group.get_right(), model_block.get_left() + DOWN * 0.35, color=GOLD, buff=0.12)
        fit_label = Text("fit", font="Monospace", font_size=13, color=YELLOW)
        fit_label.next_to(VGroup(fit_arrow1, fit_arrow2), UP, buff=0.1)

        self.play(
            FadeIn(xtrain_group),
            FadeIn(ytrain_group),
            FadeIn(model_block),
            Create(fit_arrow1),
            Create(fit_arrow2),
            Write(fit_label),
            run_time=1.4
        )
        self.wait(0.4)

        stream_dots = VGroup(*[
            Dot(color=GREEN_B if i % 2 == 0 else GOLD, radius=0.06).move_to(
                xtrain_group.get_right() if i % 2 == 0 else ytrain_group.get_right()
            )
            for i in range(6)
        ])

        stream_anims = []
        for i, dot in enumerate(stream_dots):
            target_pos = model_block.get_left() + (UP * 0.35 if i % 2 == 0 else DOWN * 0.35)
            stream_anims.append(
                dot.animate(rate_func=linear).move_to(target_pos)
            )

        self.play(FadeIn(stream_dots), run_time=0.3)
        self.play(*stream_anims, run_time=1.0)
        self.play(FadeOut(stream_dots), model_rect.animate.set_stroke(color=YELLOW, width=3), run_time=0.5)
        self.wait(0.5)

        axes = Axes(
            x_range=[0, 250, 50],
            y_range=[0, 2.0, 0.5],
            x_length=4.4,
            y_length=2.2,
            axis_config={"color": GRAY_C, "font_size": 10},
            tips=False
        )
        axes.move_to(LEFT * 2.6 + DOWN * 1.6)
        axes_labels = axes.get_axis_labels(
            x_label=Text("It", font_size=11, color=GRAY_A),
            y_label=Text("Loss J(W,b)", font_size=11, color=GRAY_A)
        )
        graph_group = VGroup(axes, axes_labels)

        opt_box = RoundedRectangle(corner_radius=0.1, width=5.2, height=2.5, color=PURPLE_B, fill_color="#210b33",
                                   fill_opacity=0.85)
        opt_box.move_to(RIGHT * 2.8 + DOWN * 1.6)

        opt_title = Text("Ottimizzazione L-BFGS", font_size=13, color=PURPLE_A, weight=BOLD)
        opt_title.move_to(opt_box.get_top() + DOWN * 0.25)

        iter_info = [
            ("Iterazione:", "1 / 5000"),
            ("Loss Cross-Entropy:", "1.9459"),
            ("Norma Gradiente:", "4.8210"),
        ]

        iter_vgroup = VGroup()
        for label, val in iter_info:
            lbl_t = Text(label, font_size=11, color=GRAY_A)
            val_t = Text(val, font="Monospace", font_size=11, color=YELLOW)
            row = VGroup(lbl_t, val_t).arrange(RIGHT, buff=0.2)
            iter_vgroup.add(row)
        iter_vgroup.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        iter_vgroup.move_to(opt_box.get_center() + UP * 0.15)

        progress_bg = Rectangle(width=4.4, height=0.2, color=GRAY_D, fill_color=GRAY_E, fill_opacity=0.5)
        progress_bg.move_to(opt_box.get_center() + DOWN * 0.65)

        progress_bar = Rectangle(width=0.1, height=0.2, color=RED_B, fill_color=RED_B, fill_opacity=0.9)
        progress_bar.move_to(progress_bg.get_left(), aligned_edge=LEFT)

        self.play(
            FadeIn(graph_group),
            FadeIn(opt_box),
            FadeIn(opt_title),
            FadeIn(iter_vgroup),
            FadeIn(progress_bg),
            FadeIn(progress_bar),
            run_time=1.2
        )
        self.wait(0.5)

        loss_dot = Dot(color=RED_B, radius=0.07).move_to(axes.c2p(0, 1.9459))
        self.play(FadeIn(loss_dot), run_time=0.3)

        iterations_data = [
            (50, "0.6120", "1.2050", 1.2, ORANGE, RED_B),
            (120, "0.1842", "0.3100", 2.6, YELLOW, ORANGE),
            (215, "0.0381", "0.00008 (< 1e-4)", 4.4, GREEN_B, GREEN_B),
        ]

        all_sub_curves = VGroup()
        prev_x = 0
        for it_num, loss_val, grad_val, bar_w, bar_color, dot_color in iterations_data:
            sub_curve = axes.plot(lambda x: 1.90 * np.exp(-0.02 * x) + 0.04, x_range=[prev_x, it_num], color=YELLOW)
            all_sub_curves.add(sub_curve)

            new_iter_vgroup = VGroup(
                VGroup(Text("Iterazione:", font_size=11, color=GRAY_A),
                       Text(f"{it_num} / 5000", font="Monospace", font_size=11, color=YELLOW)).arrange(RIGHT, buff=0.2),
                VGroup(Text("Loss Cross-Entropy:", font_size=11, color=GRAY_A),
                       Text(loss_val, font="Monospace", font_size=11, color=YELLOW)).arrange(RIGHT, buff=0.2),
                VGroup(Text("Norma Gradiente:", font_size=11, color=GRAY_A),
                       Text(grad_val, font="Monospace", font_size=11, color=YELLOW)).arrange(RIGHT, buff=0.2),
            ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(opt_box.get_center() + UP * 0.15)

            new_prog_bar = Rectangle(width=bar_w, height=0.2, color=bar_color, fill_color=bar_color, fill_opacity=0.9)
            new_prog_bar.move_to(progress_bg.get_left(), aligned_edge=LEFT)

            self.play(
                Create(sub_curve),
                loss_dot.animate.move_to(axes.c2p(it_num, float(loss_val) if it_num != 215 else 0.0381)).set_color(
                    dot_color),
                Transform(iter_vgroup, new_iter_vgroup),
                Transform(progress_bar, new_prog_bar),
                run_time=0.9
            )
            self.wait(0.4)
            prev_x = it_num

        conv_badge = RoundedRectangle(corner_radius=0.08, width=8.8, height=0.55, color=GREEN_B, fill_color="#103820",
                                      fill_opacity=0.95)
        conv_badge.move_to(DOWN * 3.4)
        conv_txt = Text("✓ CONVERGENZA RAGGIUNTA IN 215 ITERAZIONI (n_iter < max_iter=5000)", font_size=12,
                        color=GREEN_B, weight=BOLD)
        conv_txt.move_to(conv_badge.get_center())

        self.play(
            model_rect.animate.set_stroke(color=GREEN_B, width=3),
            FadeIn(conv_badge, scale=0.95),
            Write(conv_txt),
            run_time=1.0
        )
        self.wait(2.0)

        phase4_elements = VGroup(
            title4, xtrain_group, ytrain_group, model_block, fit_arrow1, fit_arrow2, fit_label,
            stream_dots, graph_group, opt_box, opt_title, iter_vgroup, progress_bg, progress_bar, loss_dot, conv_badge,
            conv_txt, all_sub_curves
        )
        self.play(FadeOut(phase4_elements), run_time=1.0)
        self.wait(0.5)

        # ----------------------------------------------------
        # FASE 5: 5-Fold Cross-Validation (StratifiedKFold)
        # ----------------------------------------------------
        title5 = Text("Cross-Validation (5-Fold StratifiedKFold)", font_size=24, color=WHITE)
        title5.to_edge(UP, buff=0.4)
        self.play(Write(title5), run_time=1.2)
        self.wait(0.5)

        cv_config = Text(
            "StratifiedKFold(n_splits=5, shuffle=True)",
            font="Monospace", font_size=13, color=GRAY_A
        )
        cv_config.move_to(UP * 2.3)
        self.play(FadeIn(cv_config), run_time=0.8)
        self.wait(0.3)

        f1_scores = [88.52, 86.40, 89.85, 86.91, 87.87]
        fold_colors = [BLUE_B, TEAL, GREEN_B, MAROON_B, PURPLE_B]

        cv_model_rect = RoundedRectangle(
            corner_radius=0.12, width=2.4, height=1.1,
            color=BLUE_B, fill_color="#0d2b45", fill_opacity=0.9
        )
        cv_model_title = Text("LogisticRegression", font_size=11, color=WHITE, weight=BOLD)
        cv_model_sub = Text("(L-BFGS)", font="Monospace", font_size=10, color=TEAL)
        cv_model_content = VGroup(cv_model_title, cv_model_sub).arrange(DOWN, buff=0.06)
        cv_model_block = VGroup(cv_model_rect, cv_model_content).move_to(DOWN * 0.1)

        self.play(FadeIn(cv_model_block), run_time=0.8)

        bar_chart_title = Text("F1-Score per Fold", font_size=11, color=TEAL, weight=BOLD)
        bar_chart_title.move_to(RIGHT * 4.2 + UP * 1.75)
        self.play(FadeIn(bar_chart_title), run_time=0.4)

        bar_base_y = -1.2
        bar_base_x = 2.8
        bar_max_height = 2.6
        bar_width = 0.32
        bar_spacing = 0.55
        score_min = 84.0
        score_max = 92.0

        bar_ticks = VGroup()
        for pct in [85, 87, 89, 91]:
            norm_h = (pct - score_min) / (score_max - score_min) * bar_max_height
            tick_y_pos = bar_base_y + norm_h
            tick_line = Line(
                np.array([bar_base_x - 0.05, tick_y_pos, 0]),
                np.array([bar_base_x + 5 * bar_spacing + 0.1, tick_y_pos, 0]),
                color=GRAY_E, stroke_width=0.5
            )
            tick_label = Text(f"{pct}%", font_size=8, color=GRAY_C)
            tick_label.next_to(tick_line, LEFT, buff=0.06)
            bar_ticks.add(VGroup(tick_line, tick_label))

        self.play(FadeIn(bar_ticks), run_time=0.5)

        all_fold_rows = VGroup()
        all_bars = VGroup()
        all_arrows = VGroup()

        current_weight_label = None

        for k in range(5):
            score_val = f1_scores[k]

            row_label = Text(f"k={k + 1}", font_size=11, color=WHITE, weight=BOLD)

            blocks = VGroup()
            for f in range(5):
                is_val = (f == k)
                fill_c = "#6b1010" if is_val else "#1b4332"
                stroke_c = RED_A if is_val else GREEN_B
                rect = RoundedRectangle(
                    corner_radius=0.05, width=0.55, height=0.26,
                    color=stroke_c, fill_color=fill_c, fill_opacity=0.85
                )
                lbl = Text("VAL" if is_val else "TR", font_size=7, color=WHITE if is_val else GREEN_B)
                lbl.move_to(rect.get_center())
                blocks.add(VGroup(rect, lbl))

            blocks.arrange(RIGHT, buff=0.06)
            row_group = VGroup(row_label, blocks).arrange(RIGHT, buff=0.15)
            row_group.move_to(LEFT * 4.0 + UP * (1.4 - k * 0.45))
            all_fold_rows.add(row_group)

            fold_arrow = Arrow(
                row_group.get_right(), cv_model_block.get_left(),
                color=fold_colors[k], buff=0.1, stroke_width=2.5, max_tip_length_to_length_ratio=0.15
            )
            all_arrows.add(fold_arrow)

            self.play(
                FadeIn(row_group, shift=RIGHT * 0.2),
                Create(fold_arrow),
                run_time=0.5
            )

            self.play(
                cv_model_rect.animate.set_stroke(color=fold_colors[k], width=4),
                run_time=0.25
            )

            new_weight_label = MathTex(f"W_{{{k + 1}}}, b_{{{k + 1}}}", font_size=18, color=fold_colors[k])
            new_weight_label.next_to(cv_model_block, DOWN, buff=0.12)

            if current_weight_label is None:
                self.play(FadeIn(new_weight_label, shift=UP * 0.1), run_time=0.25)
            else:
                self.play(Transform(current_weight_label, new_weight_label), run_time=0.25)
                new_weight_label = current_weight_label

            current_weight_label = new_weight_label

            bar_x_pos = bar_base_x + k * bar_spacing + bar_spacing / 2
            norm_h = (score_val - score_min) / (score_max - score_min) * bar_max_height

            bar_rect = Rectangle(
                width=bar_width, height=norm_h,
                color=fold_colors[k], fill_color=fold_colors[k], fill_opacity=0.85
            )
            bar_rect.move_to([bar_x_pos, bar_base_y + norm_h / 2, 0])

            bar_text = Text(f"{score_val:.1f}%", font_size=9, color=WHITE, weight=BOLD)
            bar_text.next_to(bar_rect, UP, buff=0.05)

            bar_group = VGroup(bar_rect, bar_text)
            all_bars.add(bar_group)

            self.play(
                Create(bar_rect),
                FadeIn(bar_text),
                run_time=0.5
            )
            self.wait(0.2)

        if current_weight_label is not None:
            self.play(FadeOut(current_weight_label), run_time=0.3)

        mean_score = np.mean(f1_scores)
        std_score = np.std(f1_scores)

        cv_res_box = RoundedRectangle(
            corner_radius=0.1, width=7.0, height=0.8,
            color=GOLD, fill_color="#3a2e05", fill_opacity=0.9
        ).move_to(DOWN * 2.8)

        cv_res_text = Text(
            f"F1-Score Medio (5-Fold CV): {mean_score:.2f}% (± {std_score:.2f}%)",
            font_size=15, color=GOLD, weight=BOLD
        ).move_to(cv_res_box.get_center())

        cv_res_group = VGroup(cv_res_box, cv_res_text)

        self.play(
            FadeOut(all_arrows),
            FadeIn(cv_res_group, scale=0.9),
            run_time=1.0
        )
        self.wait(2.5)

        phase5_elements = VGroup(
            title5, cv_config, cv_model_block, bar_chart_title, bar_ticks,
            all_fold_rows, all_bars, cv_res_group
        )
        self.play(FadeOut(phase5_elements), run_time=1.0)
        self.wait(0.5)

        # ----------------------------------------------------
        # FASE 6: Model Testing & Scikit-Learn Evaluation
        # ----------------------------------------------------
        title6 = Text("Testing del classificatore", font_size=22, color=WHITE)
        title6.to_edge(UP, buff=0.3)
        self.play(Write(title6), run_time=1.0)
        self.wait(0.3)

        # Step 1: Esecuzione di model.predict(X_test_bow)
        xtest_box = RoundedRectangle(corner_radius=0.1, width=3.0, height=0.8, color=RED_A, fill_color="#4a1521",
                                     fill_opacity=0.85)
        xtest_txt = Text("x_test_bow\n(876 × 4096)", font_size=11, color=WHITE)
        xtest_txt.move_to(xtest_box.get_center())
        xtest_group = VGroup(xtest_box, xtest_txt).move_to(LEFT * 4.8 + UP * 2.0)

        model_box_test = RoundedRectangle(corner_radius=0.1, width=3.2, height=0.8, color=BLUE_B, fill_color="#0d2b45",
                                          fill_opacity=0.9)
        model_txt_test = Text("Classificatore", font_size=11, color=WHITE, weight=BOLD)
        model_txt_test.move_to(model_box_test.get_center())
        model_test_group = VGroup(model_box_test, model_txt_test).move_to(LEFT * 0.8 + UP * 2.0)

        predict_arrow = Arrow(xtest_group.get_right(), model_test_group.get_left(), color=YELLOW, buff=0.1)

        ypred_box = RoundedRectangle(corner_radius=0.1, width=2.8, height=0.8, color=GOLD, fill_color="#3a2e05",
                                     fill_opacity=0.9)
        ypred_txt = Text("y_pred = model.predict(x_test_bow)\n[4, 0, 3, 2, 6, 1, ...]", font_size=12, color=YELLOW)
        ypred_txt.move_to(ypred_box.get_center())
        ypred_group = VGroup(ypred_box, ypred_txt).move_to(RIGHT * 3.4 + UP * 2.0)

        pred_out_arrow = Arrow(model_test_group.get_right(), ypred_group.get_left(), color=GOLD, buff=0.1)

        self.play(FadeIn(xtest_group), FadeIn(model_test_group), Create(predict_arrow), run_time=0.8)
        self.play(Create(pred_out_arrow), FadeIn(ypred_group), run_time=0.8)
        self.wait(1.0)

        # Step 2: Inserimento delle etichette reali y_test per il confronto
        ytest_box = RoundedRectangle(corner_radius=0.1, width=2.8, height=0.8, color=GREEN_B, fill_color="#1b4332",
                                     fill_opacity=0.9)
        ytest_txt = Text("y_test (Ground Truth)\n[4, 0, 3, 2, 6, 4, ...]", font_size=12, color=GREEN_B)
        ytest_txt.move_to(ytest_box.get_center())
        ytest_group = VGroup(ytest_box, ytest_txt).move_to(RIGHT * 3.4 + UP * 0.8)

        self.play(FadeIn(ytest_group, shift=UP * 0.2), run_time=0.8)
        self.wait(0.8)

        # Step 3: Evidenziare le funzioni sklearn metrics

        # Step 4: Visualizzazione Risultati Pesati
        res_box = RoundedRectangle(corner_radius=0.1, width=12.2, height=0.8, color=TEAL, fill_color="#062c2d",
                                   fill_opacity=0.95)
        res_box.move_to(DOWN * 1.0)

        r_acc = Text("Accuracy: 91.21%", font_size=12, color=WHITE, weight=BOLD)
        r_prec = Text("Precision: 91.36%", font_size=12, color=GREEN_B, weight=BOLD)
        r_rec = Text("Recall: 91.21%", font_size=12, color=BLUE_B, weight=BOLD)
        r_f1 = Text("F1-Score: 91.16%", font_size=12, color=GOLD, weight=BOLD)

        res_group = VGroup(r_acc, r_prec, r_rec, r_f1).arrange(RIGHT, buff=0.5)
        res_group.move_to(res_box.get_center())

        self.play(FadeIn(res_box), FadeIn(res_group), run_time=1.0)
        self.wait(1.5)

        # Ripulita interfaccia intermedia per mostrare la tabella finale completa
        self.play(
            FadeOut(VGroup(
                xtest_group, model_test_group, predict_arrow, ypred_group, pred_out_arrow,
                ytest_group
            )),
            res_box.animate.move_to(UP * 2.1),
            res_group.animate.move_to(UP * 2.1),
            run_time=1.0
        )

        # Step 5: Tabella di Valutazione Dettagliata per Classe
        class_table_data = [
            ["Recettori accoppiati a proteine G", "0.9223", "0.8962", "0.9091", "106"],
            ["Tirosin-chinasi", "0.9406", "0.8879", "0.9135", "107"],
            ["Tirosina fosfatasi", "0.9559", "0.9286", "0.9420", "70"],
            ["Sintetasi", "0.8993", "0.9328", "0.9158", "134"],
            ["Sintasi", "0.8768", "0.8521", "0.8643", "142"],
            ["Canale ionico", "1.0000", "0.7917", "0.8837", "48"],
            ["Fattore di trascrizione", "0.8997", "0.9665", "0.9319", "269"],
            ["Macro Avg", "0.9278", "0.8937", "0.9086", "876"],
            ["Weighted Avg", "0.9136", "0.9121", "0.9116", "876"],
        ]

        class_headers = ["Class", "Precision", "Recall", "F1-Score", "Support"]
        table_rows = VGroup()

        hdr_group = VGroup(
            Text(class_headers[0], font_size=11, color=TEAL, weight=BOLD).move_to(LEFT * 4.2),
            Text(class_headers[1], font_size=11, color=TEAL, weight=BOLD).move_to(LEFT * 1.5),
            Text(class_headers[2], font_size=11, color=TEAL, weight=BOLD).move_to(LEFT * 0.1),
            Text(class_headers[3], font_size=11, color=TEAL, weight=BOLD).move_to(RIGHT * 1.4),
            Text(class_headers[4], font_size=11, color=TEAL, weight=BOLD).move_to(RIGHT * 2.8),
        )
        hdr_group.move_to(UP * 1.2)
        table_rows.add(hdr_group)

        sep_line = Line(LEFT * 5.0 + UP * 1.02, RIGHT * 3.4 + UP * 1.02, color=GRAY_D, stroke_width=1)
        table_rows.add(sep_line)

        for idx, row in enumerate(class_table_data):
            y_pos = 0.85 - idx * 0.28
            is_avg_row = idx >= 7
            # row_color = GOLD if is_avg_row else WHITE
            row_color = WHITE

            c_name = Text(row[0], font_size=10, color=row_color, weight=BOLD if is_avg_row else NORMAL).move_to(
                LEFT * 4.2, aligned_edge=LEFT)
            c_prec = Text(row[1], font="Monospace", font_size=10, color=row_color).move_to(LEFT * 1.5)
            c_rec = Text(row[2], font="Monospace", font_size=10, color=row_color).move_to(LEFT * 0.1)
            c_f1 = Text(row[3], font="Monospace", font_size=10, color=row_color).move_to(RIGHT * 1.4)
            c_sup = Text(row[4], font="Monospace", font_size=10, color=GRAY_A).move_to(RIGHT * 2.8)

            r_group = VGroup(c_name, c_prec, c_rec, c_f1, c_sup)
            r_group.move_to(UP * y_pos)
            table_rows.add(r_group)

        table_bg = RoundedRectangle(corner_radius=0.1, width=10.2, height=3.2, color=GRAY_E, fill_color="#0a0a0a",
                                    fill_opacity=0.85)
        table_bg.move_to(DOWN * 0.4)

        full_table = VGroup(table_bg, table_rows)

        self.play(FadeIn(full_table, shift=UP * 0.2), run_time=1.5)
        self.wait(3.5)