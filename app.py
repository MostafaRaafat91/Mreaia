#!/usr/bin/env python3
"""
Mreaia Web Application & Hugging Face Spaces Deployment
=======================================================
Universal Zero-Token File Engine, Hardware-Bound Cryptography,
Multilingual Speech-to-Text, Computer Vision & LLM Context Bridge.

Author & Creator: Mostafa Raafat
Engineered with: Autonomous AI Cyber-Security Swarm (Antigravity Technology)
License: Mreaia Source-Available Non-Commercial License
"""

import os
import sys
import json
import shutil
import tempfile
import gradio as gr

from mreaia_core import HierarchicalExtractor, GhostReader, HardwareSecurityLayer


def process_uploaded_file(file_obj, query_prompt):
    if file_obj is None:
        return (
            "⚠️ Please upload a file to analyze.",
            "{}",
            "No audio or transcript",
            "No visual features",
            "No prompt generated",
            None,
        )

    file_path = file_obj.name
    filename = os.path.basename(file_path)
    orig_size = os.path.getsize(file_path)

    # 1. Compile and node-lock into ghost
    temp_dir = tempfile.mkdtemp()
    ghost_output = os.path.join(temp_dir, f"{filename}.ghost")

    try:
        src_sz, ghost_sz, ratio = HierarchicalExtractor.compile_ghost(
            file_path, output_ghost=ghost_output
        )

        # 2. In-memory decryption & extraction
        blueprint = GhostReader.read_ghost_in_memory(ghost_output, file_path)
        prompt_context = GhostReader.to_llm_prompt_context(ghost_output, file_path)

        # Build Status Summary
        status_md = f"""### ⚡ Distillation & Security Metrics
- **Source File:** `{filename}`
- **Original Size:** `{src_sz:,} bytes` ({src_sz / (1024*1024):.2f} MB)
- **Mreaia Ghost Size:** `{ghost_sz:,} bytes`
- **Compression Ratio:** `🔥 {ratio:.2f}% Reduction`
- **Security Protocol:** `AES-256-GCM + Hardware Node-Locked & Source-Bound Salt`
- **Volatile RAM Ingestion:** `100% In-Memory (Zero Plaintext Disk Residue)`
"""

        # Speech & Acoustics
        speech_info = blueprint.get("speech_transcript_intelligence", {})
        audio_info = blueprint.get("audio_frequency_profile", {})

        speech_md = "#### 🎙️ Speech Transcript & Vocal Acoustics\n"
        if speech_info.get("transcription_available"):
            speech_md += f"**Full Spoken Transcript:**\n> \"{speech_info.get('full_spoken_transcript')}\"\n\n"
            speech_md += f"- **Engine:** `{speech_info.get('engine')}`\n"
        else:
            speech_md += "*No spoken vocal dialogue detected or audio track absent.*\n\n"

        if audio_info.get("audio_detected"):
            speech_md += f"- **Fundamental Pitch ($F_0$):** `{audio_info.get('fundamental_vocal_pitch_hz')} Hz` ({audio_info.get('vocal_register')})\n"
            speech_md += f"- **Loudness:** `{audio_info.get('rms_loudness_dbfs')} dBFS`\n"
            bands = audio_info.get("frequency_bands", {})
            speech_md += f"- **Speech Clarity Band (300-3400Hz):** `{bands.get('speech_clarity_300_3400hz_pct')}%`\n"
            speech_md += f"- **Bass (<300Hz):** `{bands.get('bass_sub_300hz_pct')}%` | **Treble (>3400Hz):** `{bands.get('treble_air_above_3400hz_pct')}%`\n"

        # Vision & Emotions
        vision_info = blueprint.get("visual_scene_intelligence", {})
        vision_md = "#### 👁️ Computer Vision & Emotional Dynamics\n"
        if vision_info.get("vision_available"):
            vision_md += f"- **Faces Detected:** `{vision_info.get('faces_detected')}`\n"
            faces = vision_info.get("faces", [])
            for idx, face in enumerate(faces, 1):
                vision_md += f"  - **Face {idx} Primary Emotion:** `{face.get('primary_emotion')}` (Confidence: {face.get('emotion_confidence', 0)*100:.0f}%)\n"

            objects = vision_info.get("objects_and_entities", [])
            if objects:
                vision_md += "\n**Detected Objects & Scene Entities:**\n"
                for obj in objects:
                    vision_md += f"- `{obj.get('name')}`: {obj.get('confidence', 0)*100:.0f}% confidence\n"
        else:
            vision_md += "*No visual frames or vision processing not applicable for this file format.*\n"

        # Document & Topology overview
        doc_preview = blueprint.get("document_text_content") or blueprint.get("preview_text") or ""
        if doc_preview:
            doc_preview_md = f"#### 📄 Document Content Preview:\n```text\n{doc_preview[:1500]}\n```"
        else:
            doc_preview_md = f"```json\n{json.dumps(blueprint, indent=2)[:1500]}\n```"

        final_prompt = f"{prompt_context}\n\nUSER QUERY: {query_prompt or 'Analyze this dataset and provide insights.'}"

        return (
            status_md,
            doc_preview_md,
            speech_md,
            vision_md,
            final_prompt,
            ghost_output,
        )

    except Exception as exc:
        return (
            f"❌ Error processing file: {str(exc)}",
            "{}",
            "",
            "",
            "",
            None,
        )


# =====================================================================
# Gradio Modern Web Interface
# =====================================================================
with gr.Blocks(title="Mreaia - Universal Zero-Token Engine") as demo:
    gr.Markdown(
        """
        # 🪞 Mreaia (مرآيا) — Universal Zero-Token Engine & Ghost Cryptography
        ### Turn multi-gigabyte files (Video, Audio, PDF, Word, Excel, SQL, Archives) into sub-kilobyte encrypted blueprints for LLMs.
        **Conceived & Created by:** [Mostafa Raafat](https://github.com/MostafaRaafat91) | **Engineered with:** Google DeepMind Antigravity Technology
        """
    )

    with gr.Tabs():
        with gr.TabItem("🧪 Try File Distillation (Upload & Test)"):
            with gr.Row():
                with gr.Column(scale=1):
                    file_input = gr.File(
                        label="Upload Any File (Video, Audio, PDF, Word, Excel, SQL, Zip)",
                        type="filepath",
                    )
                    query_input = gr.Textbox(
                        label="AI Query / Instruction",
                        placeholder="e.g. Who is speaking and what are the main topics?",
                        value="Analyze this file topology, extract key entities, and summarize.",
                    )
                    submit_btn = gr.Button("🚀 Run Mreaia Distillation & Encrypt", variant="primary")

                with gr.Column(scale=2):
                    metrics_output = gr.Markdown("### Upload a file on the left to see live metrics.")
                    download_ghost = gr.File(label="🔐 Download Encrypted mreaia.ghost Container")

            with gr.Row():
                with gr.Tab("🎙️ Speech & Acoustics"):
                    speech_output = gr.Markdown("Speech transcript and acoustic pitch will appear here.")
                with gr.Tab("👁️ Vision & Emotions"):
                    vision_output = gr.Markdown("Objects and facial emotions will appear here.")
                with gr.Tab("📄 Document & Topology"):
                    topology_output = gr.Markdown("Extracted text or schema blueprint will appear here.")
                with gr.Tab("🤖 LLM Prompt Context"):
                    prompt_output = gr.Textbox(
                        label="Zero-Token Prompt Context (Ready for ChatGPT / Claude / Ollama)",
                        lines=12,
                    )

            submit_btn.click(
                fn=process_uploaded_file,
                inputs=[file_input, query_input],
                outputs=[
                    metrics_output,
                    topology_output,
                    speech_output,
                    vision_output,
                    prompt_output,
                    download_ghost,
                ],
            )

        with gr.TabItem("🔌 REST API & Integration"):
            gr.Markdown(
                """
                ### 🌐 How to Use Mreaia as an API

                You can call Mreaia programmatically via Python, cURL, or JavaScript from anywhere in the world:

                #### 1. Python API (`gradio_client`):
                ```python
                from gradio_client import Client, handle_file

                client = Client("MostafaRaafat91/Mreaia")
                result = client.predict(
                    file_obj=handle_file("path/to/my_heavy_video.mp4"),
                    query_prompt="Who is the speaker?",
                    api_name="/predict"
                )
                print("Extracted LLM Context:", result[4])
                ```

                #### 2. cURL REST API:
                ```bash
                curl -X POST "https://mostafaraafat91-mreaia.hf.space/api/predict" \\
                     -H "Content-Type: application/json" \\
                     -d '{"data": ["path_to_file", "Analyze this document"]}'
                ```

                #### 3. CLI On-Demand on macOS/Linux:
                ```bash
                ask-mreaia path/to/file.pdf "Summarize this document"
                ```
                """
            )

        with gr.TabItem("⚖️ License & Authorship"):
            gr.Markdown(
                """
                ### 🤝 Authorship & Legal Notice
                - **Concept & Visionary Owner:** Mostafa Raafat
                - **Engineering Swarm:** Autonomous AI Cyber-Security Swarm (Antigravity Technology)
                - **License:** Mreaia Source-Available Non-Commercial License (Commercial rights exclusively reserved to the author).
                - **Commercial Deployment Inquiries:** Contact Mostafa Raafat via GitHub.
                """
            )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
