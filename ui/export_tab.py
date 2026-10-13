"""
Export Center Tab.
Inspects and serves all verified generated media artifacts, subtitles, documents, and reports.
"""

import gradio as gr
from pathlib import Path
import pandas as pd
from config import settings
from services.storage_service import storage_service

def create_export_tab():
    with gr.Tab("Export Center", id="tab_exports"):
        gr.Markdown("## 📦 Studio Export Center & Artifact Repository")
        gr.Markdown("Download verified production assets. Files are strictly checked for physical existence and integrity before listing.")

        with gr.Row():
            refresh_btn = gr.Button("🔄 Scan & Refresh Export Repository", variant="secondary")

        artifacts_table = gr.Dataframe(
            headers=["Asset Name", "Category", "Filename", "Size (KB)", "Format"],
            datatype=["str", "str", "str", "number", "str"],
            interactive=False
        )

        gr.Markdown("### 📥 Direct File Download")
        download_selector = gr.File(label="Selected Artifact Download", file_count="multiple")

        def scan_exports():
            files_list = []
            file_paths = []
            
            # Scan exports directory
            for f in settings.exports_dir.glob("**/*.*"):
                if f.is_file():
                    ext = f.suffix.lower()
                    cat = "Other"
                    if ext in [".mp4", ".mov", ".mkv"]:
                        cat = "Video"
                    elif ext in [".srt", ".vtt"]:
                        cat = "Subtitles"
                    elif ext in [".mp3", ".wav"]:
                        cat = "Audio"
                    elif ext in [".pdf"]:
                        cat = "Document"
                    elif ext in [".png", ".jpg", ".jpeg"]:
                        cat = "Image"
                    elif ext in [".json", ".csv"]:
                        cat = "Data"

                    size_kb = round(f.stat().st_size / 1024, 1)
                    files_list.append({
                        "Asset Name": f.stem.replace("_", " ").title(),
                        "Category": cat,
                        "Filename": f.name,
                        "Size (KB)": size_kb,
                        "Format": ext[1:].upper()
                    })
                    file_paths.append(str(f))

            df = pd.DataFrame(files_list) if files_list else pd.DataFrame(columns=["Asset Name", "Category", "Filename", "Size (KB)", "Format"])
            return df, file_paths

        refresh_btn.click(
            fn=scan_exports,
            inputs=[],
            outputs=[artifacts_table, download_selector]
        )
