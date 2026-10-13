"""
Animation Service for context-aware educational motion graphics and engagement overlays.
Draws procedural visual frames with Pillow and renders them into animated video overlays via FFmpeg.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import math
from PIL import Image, ImageDraw, ImageFont
from utils.media_utils import run_ffmpeg_cmd
from utils.logging_config import logger

class AnimationService:
    def __init__(self):
        pass

    def create_educational_animation(
        self,
        concept: str,
        animation_type: str,
        labels: List[str],
        duration_sec: float,
        output_video_path: Path,
        work_dir: Path,
        fps: int = 24
    ) -> Path:
        """
        Generate a standalone educational motion graphic clip based on concept type.
        Renders frame sequence and compiles to MP4 with FFmpeg.
        """
        width, height = 1280, 720
        total_frames = int(duration_sec * fps)
        frames_dir = work_dir / f"anim_frames_{animation_type.lower()}"
        frames_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Rendering {total_frames} frames for animation '{animation_type}'...")

        for f_idx in range(total_frames):
            t = f_idx / total_frames  # normalized 0.0 to 1.0
            img = Image.new("RGBA", (width, height), (15, 17, 26, 255))
            draw = ImageDraw.Draw(img)

            # Draw background grid pattern
            for x in range(0, width, 60):
                draw.line([(x, 0), (x, height)], fill=(25, 30, 45, 120), width=1)
            for y in range(0, height, 60):
                draw.line([(0, y), (width, y)], fill=(25, 30, 45, 120), width=1)

            # Header Banner
            draw.rectangle([(80, 50), (width - 80, 110)], fill=(30, 36, 56, 230), outline=(99, 102, 241, 255), width=2)
            draw.text((100, 68), f"CONCEPT EXPLORATION: {concept.upper()}", fill=(255, 255, 255, 255))

            if animation_type.upper() in ["ML_PIPELINE", "MACHINE_LEARNING"]:
                self._draw_ml_pipeline_frame(draw, t, width, height, labels)
            elif animation_type.upper() in ["NEURAL_NET", "DEEP_LEARNING"]:
                self._draw_neural_net_frame(draw, t, width, height, labels)
            elif animation_type.upper() in ["CYBER_PACKET", "SECURITY"]:
                self._draw_cyber_packet_frame(draw, t, width, height, labels)
            elif animation_type.upper() in ["BLOCKCHAIN_LEDGER", "BLOCKCHAIN"]:
                self._draw_blockchain_frame(draw, t, width, height, labels)
            elif animation_type.upper() in ["CODE_ALGORITHM", "PROGRAMMING"]:
                self._draw_code_algorithm_frame(draw, t, width, height, concept, labels)
            elif animation_type.upper() in ["MATHEMATICS_FORMULA", "MATH"]:
                self._draw_math_formula_frame(draw, t, width, height, concept, labels)
            else:
                self._draw_concept_card_frame(draw, t, width, height, concept, labels)

            frame_path = frames_dir / f"frame_{f_idx:04d}.png"
            img.save(frame_path)

        # Compile frames to MP4 using FFmpeg
        args = [
            "-y",
            "-framerate", str(fps),
            "-i", str(frames_dir / "frame_%04d.png"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "fast",
            str(output_video_path)
        ]
        run_ffmpeg_cmd(args, timeout_sec=120)
        return output_video_path

    def _draw_ml_pipeline_frame(self, draw: ImageDraw.Draw, t: float, w: int, h: int, labels: List[str]):
        """Render animated machine learning pipeline data flow."""
        stages = labels if len(labels) >= 3 else ["Data Ingestion", "Feature Engineering", "Model Training", "Inference API"]
        stage_w, stage_h = 220, 120
        gap = (w - 200 - len(stages) * stage_w) // (len(stages) - 1)
        start_x = 100
        y = h // 2 - stage_h // 2

        for i, stage in enumerate(stages):
            x = start_x + i * (stage_w + gap)
            # Box
            is_active = (t >= (i / len(stages)) and t < ((i + 1) / len(stages)))
            box_fill = (45, 55, 85, 240) if not is_active else (79, 70, 229, 255)
            border_color = (129, 140, 248, 255) if is_active else (67, 75, 105, 200)
            
            draw.rectangle([(x, y), (x + stage_w, y + stage_h)], fill=box_fill, outline=border_color, width=3)
            draw.text((x + 20, y + 45), stage, fill=(255, 255, 255, 255))

            # Connecting arrow to next
            if i < len(stages) - 1:
                arrow_start = x + stage_w
                arrow_end = arrow_start + gap
                draw.line([(arrow_start, y + stage_h // 2), (arrow_end, y + stage_h // 2)], fill=(129, 140, 248, 200), width=3)
                
                # Moving particle
                particle_pos = (t * 4) % 1.0
                px = int(arrow_start + particle_pos * gap)
                draw.ellipse([(px - 6, y + stage_h // 2 - 6), (px + 6, y + stage_h // 2 + 6)], fill=(244, 63, 94, 255))

    def _draw_neural_net_frame(self, draw: ImageDraw.Draw, t: float, w: int, h: int, labels: List[str]):
        """Render multi-layer neural network with propagating activations."""
        layers = [4, 6, 6, 3]
        layer_x = [250, 500, 750, 1000]
        y_center = h // 2 + 30

        # Draw synapses
        for l in range(len(layers) - 1):
            n1, n2 = layers[l], layers[l + 1]
            x1, x2 = layer_x[l], layer_x[l + 1]
            spacing1, spacing2 = 60, 60
            top1 = y_center - (n1 * spacing1) // 2
            top2 = y_center - (n2 * spacing2) // 2

            for i in range(n1):
                py1 = top1 + i * spacing1
                for j in range(n2):
                    py2 = top2 + j * spacing2
                    glow = int(120 + 80 * math.sin(t * 6 + l + i + j))
                    draw.line([(x1, py1), (x2, py2)], fill=(99, 102, 241, glow), width=1)

        # Draw nodes
        for l, n in enumerate(layers):
            x = layer_x[l]
            spacing = 60
            top = y_center - (n * spacing) // 2
            for i in range(n):
                py = top + i * spacing
                pulse = 16 + int(4 * math.sin(t * 8 + l * 2 + i))
                node_fill = (16, 185, 129, 255) if l == len(layers) - 1 else (99, 102, 241, 255)
                draw.ellipse([(x - pulse, py - pulse), (x + pulse, py + pulse)], fill=node_fill, outline=(255, 255, 255, 255), width=2)

    def _draw_cyber_packet_frame(self, draw: ImageDraw.Draw, t: float, w: int, h: int, labels: List[str]):
        """Render network packet transmission and firewall filtering."""
        draw.rectangle([(200, 250), (400, 450)], fill=(30, 41, 59, 240), outline=(56, 189, 248, 255), width=3)
        draw.text((230, 330), "CLIENT SOURCE", fill=(255, 255, 255, 255))

        draw.rectangle([(880, 250), (1080, 450)], fill=(30, 41, 59, 240), outline=(56, 189, 248, 255), width=3)
        draw.text((910, 330), "SECURE CLOUD", fill=(255, 255, 255, 255))

        # Firewall barrier in center
        draw.rectangle([(620, 200), (660, 500)], fill=(239, 68, 68, 220), outline=(255, 255, 255, 255), width=2)
        draw.text((615, 170), "FIREWALL", fill=(239, 68, 68, 255))

        # Animated packet moving from left to right
        px = int(400 + (t % 1.0) * 480)
        draw.rectangle([(px - 20, 330), (px + 20, 370)], fill=(234, 179, 8, 255), outline=(255, 255, 255, 255), width=2)
        draw.text((px - 15, 342), "DATA", fill=(0, 0, 0, 255))

    def _draw_concept_card_frame(self, draw: ImageDraw.Draw, t: float, w: int, h: int, concept: str, labels: List[str]):
        """Render a generalized educational highlight card."""
        cx, cy = w // 2, h // 2 + 20
        card_w, card_h = 800, 360
        draw.rectangle(
            [(cx - card_w // 2, cy - card_h // 2), (cx + card_w // 2, cy + card_h // 2)],
            fill=(30, 36, 56, 240),
            outline=(14, 165, 233, 255),
            width=3
        )
        draw.text((cx - card_w // 2 + 40, cy - card_h // 2 + 40), f"Key Concept: {concept}", fill=(244, 244, 245, 255))
        
        y_offset = cy - card_h // 2 + 100
        for i, lbl in enumerate(labels[:5]):
            draw.text((cx - card_w // 2 + 50, y_offset), f"•  {lbl}", fill=(203, 213, 225, 255))
            y_offset += 45

    def _draw_blockchain_frame(self, draw: ImageDraw.Draw, t: float, w: int, h: int, labels: List[str]):
        """Render animated blockchain distributed ledger blocks with linked hashes."""
        blocks = labels if len(labels) >= 3 else ["Block #101 (Genesis)", "Block #102 (Txs Verified)", "Block #103 (Consensus)"]
        bw, bh = 280, 160
        y = h // 2 - bh // 2 + 20
        gap = 80
        start_x = (w - (len(blocks) * bw + (len(blocks) - 1) * gap)) // 2

        for i, b_name in enumerate(blocks):
            x = start_x + i * (bw + gap)
            is_active = (t >= (i / len(blocks)) and t < ((i + 1) / len(blocks)))
            box_fill = (30, 41, 59, 240) if not is_active else (16, 185, 129, 230)
            border_col = (52, 211, 153, 255) if is_active else (71, 85, 105, 200)

            draw.rectangle([(x, y), (x + bw, y + bh)], fill=box_fill, outline=border_col, width=3)
            draw.text((x + 20, y + 25), b_name, fill=(255, 255, 255, 255))
            draw.text((x + 20, y + 65), f"Prev Hash: 0x{hash(b_name + str(i)) & 0xFFFFFF:06x}", fill=(148, 163, 184, 255))
            draw.text((x + 20, y + 100), f"Nonce: {int(t * 1000 + i * 42)}", fill=(251, 191, 36, 255))

            if i < len(blocks) - 1:
                # Link line
                lx1, lx2 = x + bw, x + bw + gap
                draw.line([(lx1, y + bh // 2), (lx2, y + bh // 2)], fill=(52, 211, 153, 200), width=4)
                # Link particle
                pos = (t * 3 + i) % 1.0
                px = int(lx1 + pos * gap)
                draw.ellipse([(px - 6, y + bh // 2 - 6), (px + 6, y + bh // 2 + 6)], fill=(244, 63, 94, 255))

    def _draw_code_algorithm_frame(self, draw: ImageDraw.Draw, t: float, w: int, h: int, concept: str, labels: List[str]):
        """Render an animated code syntax highlight execution window."""
        box_w, box_h = 860, 420
        bx = (w - box_w) // 2
        by = (h - box_h) // 2 + 30

        # Window Frame
        draw.rectangle([(bx, by), (bx + box_w, by + box_h)], fill=(15, 23, 42, 245), outline=(99, 102, 241, 255), width=2)
        # Window titlebar
        draw.rectangle([(bx, by), (bx + box_w, by + 35)], fill=(30, 41, 59, 255))
        draw.ellipse([(bx + 15, by + 12), (bx + 25, by + 22)], fill=(239, 68, 68, 255))
        draw.ellipse([(bx + 35, by + 12), (bx + 45, by + 22)], fill=(234, 179, 8, 255))
        draw.ellipse([(bx + 55, by + 12), (bx + 65, by + 22)], fill=(34, 197, 94, 255))
        draw.text((bx + 85, by + 10), f"algorithm_trace.py — {concept}", fill=(203, 213, 225, 255))

        # Code lines
        code_lines = labels if labels else [
            "def forward_attention(query, key, value):",
            "    scores = matmul(query, key.T) / sqrt(d_k)",
            "    weights = softmax(scores, dim=-1)",
            "    return matmul(weights, value)  # Visual synthesis",
            "output = forward_attention(Q, K, V)"
        ]

        active_idx = int(t * len(code_lines)) % len(code_lines)
        for idx, line in enumerate(code_lines[:6]):
            ly = by + 60 + idx * 48
            if idx == active_idx:
                draw.rectangle([(bx + 10, ly - 4), (bx + box_w - 10, ly + 36)], fill=(49, 46, 129, 200))
                draw.text((bx + 15, ly), "▶", fill=(234, 179, 8, 255))
            draw.text((bx + 40, ly), f"{idx + 1:02d}   {line}", fill=(248, 250, 252, 255) if idx == active_idx else (148, 163, 184, 255))

    def _draw_math_formula_frame(self, draw: ImageDraw.Draw, t: float, w: int, h: int, concept: str, labels: List[str]):
        """Render step-by-step mathematical derivation card."""
        box_w, box_h = 800, 380
        bx = (w - box_w) // 2
        by = (h - box_h) // 2 + 30

        draw.rectangle([(bx, by), (bx + box_w, by + box_h)], fill=(24, 24, 37, 245), outline=(245, 158, 11, 255), width=3)
        draw.text((bx + 35, by + 30), f"MATHEMATICAL DERIVATION: {concept.upper()}", fill=(251, 191, 36, 255))

        steps = labels if labels else [
            "1. Given: Input embeddings X in R^(N x d)",
            "2. Project: Q = X W_Q, K = X W_K, V = X W_V",
            "3. Compute Similarity: S_ij = (q_i . k_j) / sqrt(d_k)",
            "4. Probability Distribution: P = softmax(S)",
            "5. Context Vector Output: Context = sum(P_ij * v_j)"
        ]

        active_step = min(len(steps) - 1, int(t * len(steps)))
        for i, step in enumerate(steps[:5]):
            sy = by + 90 + i * 50
            is_visible = (i <= active_step)
            col = (255, 255, 255, 255) if is_visible else (71, 85, 105, 150)
            indicator = "✓ " if is_visible else "○ "
            draw.text((bx + 40, sy), f"{indicator}{step}", fill=col)

    def create_like_share_subscribe_overlay(
        self,
        channel_name: str,
        subscriber_count: str,
        duration_sec: float,
        output_video_path: Path,
        work_dir: Path,
        fps: int = 24
    ) -> Path:
        """
        Generate a professional animated Like, Share, and Subscribe lower-third card.
        """
        width, height = 1280, 720
        total_frames = int(duration_sec * fps)
        frames_dir = work_dir / "lss_frames"
        frames_dir.mkdir(parents=True, exist_ok=True)

        for f_idx in range(total_frames):
            t = f_idx / total_frames
            # Transparent background
            img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            # Slide up entry (0 to 0.15) and slide down exit (0.85 to 1.0)
            if t < 0.15:
                progress = t / 0.15
                y_pos = int(height - 180 * math.sin(progress * math.pi / 2))
            elif t > 0.85:
                progress = (t - 0.85) / 0.15
                y_pos = int(height - 180 * math.cos(progress * math.pi / 2))
            else:
                y_pos = height - 180

            card_x = (width - 760) // 2
            card_w = 760
            card_h = 100

            # Card background
            draw.rounded_rectangle(
                [(card_x, y_pos), (card_x + card_w, y_pos + card_h)],
                radius=18,
                fill=(20, 24, 38, 245),
                outline=(99, 102, 241, 230),
                width=2
            )

            # Channel Avatar circle
            draw.ellipse(
                [(card_x + 20, y_pos + 15), (card_x + 90, y_pos + 85)],
                fill=(79, 70, 229, 255),
                outline=(255, 255, 255, 255),
                width=2
            )
            draw.text((card_x + 45, y_pos + 38), "AI", fill=(255, 255, 255, 255))

            # Channel details
            draw.text((card_x + 110, y_pos + 22), channel_name, fill=(255, 255, 255, 255))
            draw.text((card_x + 110, y_pos + 52), subscriber_count, fill=(148, 163, 184, 255))

            # Animated Subscribe Button (Turns red to gray after t > 0.45)
            is_subscribed = t > 0.45
            btn_x = card_x + 420
            btn_w = 160
            btn_color = (51, 65, 85, 255) if is_subscribed else (225, 29, 72, 255)
            btn_text = "SUBSCRIBED" if is_subscribed else "SUBSCRIBE"
            
            draw.rounded_rectangle(
                [(btn_x, y_pos + 25), (btn_x + btn_w, y_pos + 75)],
                radius=12,
                fill=btn_color
            )
            draw.text((btn_x + 20, y_pos + 40), btn_text, fill=(255, 255, 255, 255))

            # Bell Icon / Chime shake
            bell_x = card_x + 610
            bell_shake = int(4 * math.sin(t * 30)) if (0.45 < t < 0.75) else 0
            draw.ellipse(
                [(bell_x + bell_shake, y_pos + 25), (bell_x + 50 + bell_shake, y_pos + 75)],
                fill=(234, 179, 8, 255) if is_subscribed else (71, 85, 105, 255)
            )
            draw.text((bell_x + 18 + bell_shake, y_pos + 40), "🔔", fill=(0, 0, 0, 255))

            # Like thumb
            like_x = card_x + 680
            draw.text((like_x, y_pos + 38), "👍", fill=(255, 255, 255, 255))

            frame_path = frames_dir / f"frame_{f_idx:04d}.png"
            img.save(frame_path)

        # Render to transparent video (ProRes / yuv420p with green fallback or direct overlay)
        args = [
            "-y",
            "-framerate", str(fps),
            "-i", str(frames_dir / "frame_%04d.png"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            str(output_video_path)
        ]
        run_ffmpeg_cmd(args, timeout_sec=120)
        return output_video_path

animation_service = AnimationService()
