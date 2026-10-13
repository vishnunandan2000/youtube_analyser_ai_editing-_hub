"""
Multilingual Captions and Audio Dubbing Tab.
"""

import gradio as gr
from pathlib import Path
from services.translation_service import translation_service, SUPPORTED_LANGUAGES
from services.transcription_service import transcription_service
from services.tts_service import tts_service
from utils.error_handlers import format_error_for_ui
from config import settings

def create_captions_tab():
    with gr.Tab("Multilingual Captions & Dubbing", id="tab_captions"):
        gr.Markdown("## 🌐 Multilingual Speech Transcription, Subtitles & Dubbing")
        gr.Markdown("Support for 12 languages with preservation of mathematical equations, technical terms, and code syntax.")

        with gr.Row():
            with gr.Column():
                audio_or_video_input = gr.File(label="Upload Video or Audio File", file_types=["video", "audio"])
                target_lang = gr.Dropdown(
                    label="Target Translation & Dubbing Language",
                    choices=[(f"{name} ({code})", code) for code, name in SUPPORTED_LANGUAGES.items()],
                    value="hi"
                )
                with gr.Row():
                    transcribe_btn = gr.Button("🎙️ Transcribe Original Speech", variant="secondary")
                    translate_btn = gr.Button("🌍 Translate Subtitles", variant="secondary")
                    dub_btn = gr.Button("🔊 Synthesize Neural Dubbed Audio", variant="primary", elem_classes=["action-btn-primary"])

                with gr.Row():
                    load_demo_lecture_btn = gr.Button("📄 Load Educational Speech Transcript Sample", variant="secondary", size="sm")

            with gr.Column():
                transcription_text = gr.TextArea(
                    label="Original Speech Transcript (Editable)",
                    value="Welcome to this comprehensive masterclass on Generative Artificial Intelligence. Today, we dissect how transformer architectures compute scaled dot-product attention: Attention(Q, K, V) = softmax(QK^T / sqrt(d_k))V. By projecting input embeddings into query, key, and value matrices, modern foundational models achieve unparalleled natural language reasoning and code generation capabilities.",
                    lines=6,
                    interactive=True
                )
                translated_text = gr.TextArea(label="Translated Subtitle Content (Editable)", lines=6, interactive=True)
                dubbed_audio_preview = gr.Audio(label="Dubbed Neural Speech Preview")

        with gr.Row():
            srt_download = gr.File(label="Download SubRip (.srt)")
            vtt_download = gr.File(label="Download WebVTT (.vtt)")

        status_box = gr.Markdown("Ready. Upload media or translate the sample transcript directly into any of the 12 target languages.")

        # Transcribe handler
        def handle_transcription(file_obj):
            if not file_obj:
                return "⚠️ Please upload a media file.", "", None, None
            try:
                p = Path(file_obj.name)
                # If video, extract audio
                wav_p = settings.cache_dir / f"{p.stem}_16k.wav"
                if p.suffix.lower() in [".mp4", ".mov", ".mkv", ".webm", ".avi"]:
                    transcription_service.extract_audio(p, wav_p)
                else:
                    wav_p = p

                res = transcription_service.transcribe(wav_p)
                srt_p = settings.exports_dir / f"{p.stem}.srt"
                vtt_p = settings.exports_dir / f"{p.stem}.vtt"
                transcription_service.export_srt(res.segments, srt_p)
                transcription_service.export_vtt(res.segments, vtt_p)

                return f"✅ Transcription complete ({res.duration:.1f}s, {len(res.segments)} segments).", res.text, str(srt_p), str(vtt_p)
            except Exception as e:
                return format_error_for_ui(e), "", None, None

        # Translate handler
        def handle_translation(file_obj, orig_text, lang_code):
            if not orig_text or not orig_text.strip():
                return "⚠️ Please transcribe speech first or enter original text.", ""
            try:
                from models.schemas import SubtitleSegment
                segments = [SubtitleSegment(id=1, start=0.0, end=10.0, text=orig_text[:500])]
                translated = translation_service.translate_segments(segments, lang_code)
                translated_str = " ".join([s.text for s in translated])
                return f"✅ Translation to {lang_code.upper()} completed successfully.", translated_str
            except Exception as e:
                return format_error_for_ui(e), ""

        # Dubbing handler
        def handle_dubbing(trans_text, lang_code):
            if not trans_text or not trans_text.strip():
                return "⚠️ No translated text available to dub.", None
            try:
                out_audio = settings.exports_dir / f"dubbed_{lang_code}.mp3"
                tts_service.synthesize_speech(trans_text, lang_code, out_audio)
                return f"✅ Neural voice dubbed in {lang_code.upper()}!", str(out_audio)
            except Exception as e:
                return format_error_for_ui(e), None

        transcribe_btn.click(
            fn=handle_transcription,
            inputs=[audio_or_video_input],
            outputs=[status_box, transcription_text, srt_download, vtt_download]
        )
        translate_btn.click(
            fn=handle_translation,
            inputs=[audio_or_video_input, transcription_text, target_lang],
            outputs=[status_box, translated_text]
        )
        dub_btn.click(
            fn=handle_dubbing,
            inputs=[translated_text, target_lang],
            outputs=[status_box, dubbed_audio_preview]
        )

        load_demo_lecture_btn.click(
            fn=lambda: "Welcome to this comprehensive masterclass on Generative Artificial Intelligence. Today, we dissect how transformer architectures compute scaled dot-product attention: Attention(Q, K, V) = softmax(QK^T / sqrt(d_k))V. By projecting input embeddings into query, key, and value matrices, modern foundational models achieve unparalleled natural language reasoning and code generation capabilities.",
            inputs=[],
            outputs=[transcription_text]
        )
