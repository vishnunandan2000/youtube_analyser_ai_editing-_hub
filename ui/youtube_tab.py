"""
Division A — YouTube Intelligence and Performance Analytics Tab.
"""

import gradio as gr
import pandas as pd
from agents.youtube_analytics_agent import youtube_analytics_agent
from utils.error_handlers import format_error_for_ui
from utils.logging_config import logger

def create_youtube_tab():
    with gr.Tab("YouTube Intelligence", id="tab_youtube"):
        gr.HTML("""
        <div style="margin-bottom:16px;">
            <span class="division-badge-a">DIVISION A</span>
            <h2 style="display:inline-block; margin-left:12px; margin-top:0; color:#F8FAFC;">YouTube Intelligence & Performance Analytics</h2>
        </div>
        """)

        with gr.Row():
            with gr.Column(scale=3):
                url_input = gr.Textbox(
                    label="YouTube Video URL",
                    placeholder="https://www.youtube.com/watch?v=NRmAXDWJVnU or https://youtu.be/...",
                    value="https://youtu.be/NRmAXDWJVnU",
                    lines=1
                )
            with gr.Column(scale=1):
                comment_limit = gr.Slider(
                    label="Max Comments to Analyze",
                    minimum=5,
                    maximum=50,
                    value=20,
                    step=5
                )
            with gr.Column(scale=1):
                analyze_btn = gr.Button("🔍 Analyze Video", variant="primary", elem_classes=["action-btn-primary"])

        with gr.Row():
            auth_simulation_toggle = gr.Checkbox(
                label="🔓 Enable Channel Owner Authorized Analytics Mode (OAuth Simulation)",
                value=True,
                info="Enables authorized metrics: shares, subscriber conversion, total watch hours, and audience retention."
            )
            load_ref_btn = gr.Button("🎬 Load Simplilearn GenAI Reference Video", variant="secondary", size="sm")

        status_box = gr.Markdown("Ready to analyze. Click 'Analyze Video' to run live extraction & Llama 3.2 sentiment classification.")

        gr.Markdown("---")
        gr.Markdown("### 📌 Video Metadata & Public Snapshot")
        
        with gr.Row():
            with gr.Column(scale=1):
                thumb_preview = gr.Image(label="Video Thumbnail", height=200)
            with gr.Column(scale=2):
                video_title_out = gr.Textbox(label="Video Title", interactive=False)
                channel_out = gr.Textbox(label="Channel / Creator", interactive=False)
                with gr.Row():
                    duration_out = gr.Textbox(label="Duration (sec)", interactive=False)
                    pub_date_out = gr.Textbox(label="Published Date", interactive=False)

        gr.Markdown("---")
        gr.Markdown("### 📈 Performance KPIs & Engagement Metrics")

        with gr.Row():
            kpi_views = gr.HTML("<div class='kpi-card'><div class='kpi-label'>Total Views</div><div class='kpi-number'>-</div></div>")
            kpi_likes = gr.HTML("<div class='kpi-card'><div class='kpi-label'>Total Likes</div><div class='kpi-number'>-</div></div>")
            kpi_comments = gr.HTML("<div class='kpi-card'><div class='kpi-label'>Total Comments</div><div class='kpi-number'>-</div></div>")
            kpi_like_ratio = gr.HTML("<div class='kpi-card'><div class='kpi-label'>Like/View Ratio</div><div class='kpi-number'>-</div></div>")
            kpi_engagement = gr.HTML("<div class='kpi-card'><div class='kpi-label'>Public Engagement</div><div class='kpi-number'>-</div></div>")

        with gr.Accordion("🔒 Authenticated Channel Analytics (Channel Owner Authorization)", open=True):
            gr.Markdown("""
            *These metrics require channel-owner authorization via YouTube Analytics API. Simulated authorized metrics are enabled below.*
            """)
            with gr.Row():
                kpi_shares = gr.HTML("<div class='kpi-card'><div class='kpi-label'>Total Shares</div><div class='kpi-number'>-</div></div>")
                kpi_subs = gr.HTML("<div class='kpi-card'><div class='kpi-label'>Subscribers Gained</div><div class='kpi-number'>-</div></div>")
                kpi_watch = gr.HTML("<div class='kpi-card'><div class='kpi-label'>Watch Time (Hours)</div><div class='kpi-number'>-</div></div>")
                kpi_retention = gr.HTML("<div class='kpi-card'><div class='kpi-label'>Avg View Duration</div><div class='kpi-number'>-</div></div>")

        gr.Markdown("---")
        gr.Markdown("### 📊 Audience Sentiment & Interaction Visualizations")

        with gr.Row():
            pie_plot = gr.Plot(label="Sentiment Distribution")
            bar_plot = gr.Plot(label="Comment Volume by Sentiment")

        with gr.Row():
            eng_plot = gr.Plot(label="Audience Reach Scale")

        gr.Markdown("---")
        gr.Markdown("### 💬 Llama 3.2 Classified Comments & Audience Feedback")

        comments_table = gr.Dataframe(
            headers=["Author", "Comment Text", "Sentiment", "Rationale", "Topic", "Actionable?"],
            datatype=["str", "str", "str", "str", "str", "bool"],
            interactive=False,
            wrap=True
        )

        with gr.Accordion("📋 Audience Feedback Synthesis Report", open=True):
            feedback_report_out = gr.Markdown("Run video analysis to generate topic clusters and audience feedback report.")

        # Event Handler
        def handle_youtube_analysis(url, max_c, enable_auth):
            if not url or not url.strip():
                return (
                    "⚠️ Please enter a valid YouTube URL.",
                    None, "", "", "", "",
                    "<div class='kpi-card'><div class='kpi-label'>Total Views</div><div class='kpi-number'>-</div></div>",
                    "<div class='kpi-card'><div class='kpi-label'>Total Likes</div><div class='kpi-number'>-</div></div>",
                    "<div class='kpi-card'><div class='kpi-label'>Total Comments</div><div class='kpi-number'>-</div></div>",
                    "<div class='kpi-card'><div class='kpi-label'>Like/View Ratio</div><div class='kpi-number'>-</div></div>",
                    "<div class='kpi-card'><div class='kpi-label'>Public Engagement</div><div class='kpi-number'>-</div></div>",
                    "<div class='kpi-card'><div class='kpi-label'>Total Shares</div><div class='kpi-number'>-</div></div>",
                    "<div class='kpi-card'><div class='kpi-label'>Subscribers Gained</div><div class='kpi-number'>-</div></div>",
                    "<div class='kpi-card'><div class='kpi-label'>Watch Time (Hours)</div><div class='kpi-number'>-</div></div>",
                    "<div class='kpi-card'><div class='kpi-label'>Avg View Duration</div><div class='kpi-number'>-</div></div>",
                    None, None, None,
                    pd.DataFrame(),
                    ""
                )

            try:
                res = youtube_analytics_agent.run_analysis(url.strip(), max_comments=int(max_c), enable_authorized_analytics=bool(enable_auth))
                meta = res["metadata"]
                kpis = res["kpis"]
                comments = res["comments"]
                summary = res["sentiment_summary"]
                report = res["feedback_report"]

                # Public KPI HTML cards
                views_str = f"{kpis.views:,}" if kpis.views is not None else "N/A"
                likes_str = f"{kpis.likes:,}" if kpis.likes is not None else "N/A"
                comm_str = f"{kpis.comments_count:,}" if kpis.comments_count is not None else "N/A"
                like_r_str = f"{kpis.like_to_view_ratio:.2f}%" if kpis.like_to_view_ratio is not None else "N/A"
                eng_r_str = f"{kpis.public_engagement_rate:.2f}%" if kpis.public_engagement_rate is not None else "N/A"

                v_card = f"<div class='kpi-card'><div class='kpi-label'>Total Views</div><div class='kpi-number'>{views_str}</div></div>"
                l_card = f"<div class='kpi-card'><div class='kpi-label'>Total Likes</div><div class='kpi-number'>{likes_str}</div></div>"
                c_card = f"<div class='kpi-card'><div class='kpi-label'>Total Comments</div><div class='kpi-number'>{comm_str}</div></div>"
                lr_card = f"<div class='kpi-card'><div class='kpi-label'>Like/View Ratio</div><div class='kpi-number'>{like_r_str}</div></div>"
                eng_card = f"<div class='kpi-card'><div class='kpi-label'>Public Engagement</div><div class='kpi-number'>{eng_r_str}</div></div>"

                # Authorized KPI HTML cards
                if kpis.is_authenticated:
                    sh_str = f"{kpis.shares:,}" if kpis.shares is not None else "N/A"
                    sb_str = f"+{kpis.subscribers_gained:,}" if kpis.subscribers_gained is not None else "N/A"
                    wt_str = f"{kpis.watch_time_hours:,.0f} hrs" if kpis.watch_time_hours is not None else "N/A"
                    ret_str = f"{int(kpis.average_view_duration_sec//60)}:{int(kpis.average_view_duration_sec%60):02d} ({kpis.average_percentage_viewed:.1f}%)" if kpis.average_view_duration_sec is not None else "N/A"

                    sh_card = f"<div class='kpi-card'><div class='kpi-label'>Total Shares</div><div class='kpi-number' style='color:#38BDF8;'>{sh_str}</div></div>"
                    sb_card = f"<div class='kpi-card'><div class='kpi-label'>Subscribers Gained</div><div class='kpi-number' style='color:#10B981;'>{sb_str}</div></div>"
                    wt_card = f"<div class='kpi-card'><div class='kpi-label'>Watch Time (Hours)</div><div class='kpi-number' style='color:#F59E0B;'>{wt_str}</div></div>"
                    ret_card = f"<div class='kpi-card'><div class='kpi-label'>Avg View Duration</div><div class='kpi-number' style='color:#EC4899;'>{ret_str}</div></div>"
                else:
                    sh_card = "<div class='kpi-card'><div class='kpi-label'>Total Shares</div><div class='kpi-number' style='font-size:13px;color:#94A3B8;'>Unavailable (OAuth required)</div></div>"
                    sb_card = "<div class='kpi-card'><div class='kpi-label'>Subscribers Gained</div><div class='kpi-number' style='font-size:13px;color:#94A3B8;'>Unavailable (OAuth required)</div></div>"
                    wt_card = "<div class='kpi-card'><div class='kpi-label'>Watch Time (Hours)</div><div class='kpi-number' style='font-size:13px;color:#94A3B8;'>Unavailable (OAuth required)</div></div>"
                    ret_card = "<div class='kpi-card'><div class='kpi-label'>Avg View Duration</div><div class='kpi-number' style='font-size:13px;color:#94A3B8;'>Unavailable (OAuth required)</div></div>"

                # Comments DataFrame
                table_rows = []
                for c in comments:
                    table_rows.append({
                        "Author": c.author,
                        "Comment Text": c.text,
                        "Sentiment": c.sentiment.value if c.sentiment else "Neutral",
                        "Rationale": c.rationale or "",
                        "Topic": c.topic or "",
                        "Actionable?": c.is_actionable
                    })
                df = pd.DataFrame(table_rows)

                # Feedback Markdown
                fb_md = f"#### 🎯 Recurring Topics & Audience Synthesis\n"
                for tc in report.topics[:5]:
                    fb_md += f"- **{tc.topic}** ({tc.count} comments) — Pos: {tc.sentiment_distribution.get('Positive', 0)}, Neg: {tc.sentiment_distribution.get('Negative', 0)}\n"
                
                if report.actionable_suggestions:
                    fb_md += "\n#### 💡 Actionable Feedback Suggestions\n"
                    for s in report.actionable_suggestions[:4]:
                        fb_md += f"- *\"{s}\"*\n"

                auth_status_str = "with Authenticated Channel Analytics Active" if kpis.is_authenticated else "(Public snapshot mode)"
                status_msg = f"✅ Successfully analyzed '{meta.title}' {auth_status_str}. {summary.total_comments} comments harvested & classified."

                return (
                    status_msg,
                    meta.thumbnail_url, meta.title, meta.channel_name, f"{meta.duration_seconds:.0f}s", meta.published_at,
                    v_card, l_card, c_card, lr_card, eng_card,
                    sh_card, sb_card, wt_card, ret_card,
                    res["pie_chart"], res["bar_chart"], res["engagement_chart"],
                    df,
                    fb_md
                )

            except Exception as e:
                err_msg = format_error_for_ui(e)
                return (
                    err_msg,
                    None, "", "", "", "",
                    "<div class='kpi-card'><div class='kpi-label'>Total Views</div><div class='kpi-number'>Error</div></div>",
                    "<div class='kpi-card'><div class='kpi-label'>Total Likes</div><div class='kpi-number'>Error</div></div>",
                    "<div class='kpi-card'><div class='kpi-label'>Total Comments</div><div class='kpi-number'>Error</div></div>",
                    "<div class='kpi-card'><div class='kpi-label'>Like/View Ratio</div><div class='kpi-number'>Error</div></div>",
                    "<div class='kpi-card'><div class='kpi-label'>Public Engagement</div><div class='kpi-number'>Error</div></div>",
                    "<div class='kpi-card'><div class='kpi-label'>Total Shares</div><div class='kpi-number'>Error</div></div>",
                    "<div class='kpi-card'><div class='kpi-label'>Subscribers Gained</div><div class='kpi-number'>Error</div></div>",
                    "<div class='kpi-card'><div class='kpi-label'>Watch Time (Hours)</div><div class='kpi-number'>Error</div></div>",
                    "<div class='kpi-card'><div class='kpi-label'>Avg View Duration</div><div class='kpi-number'>Error</div></div>",
                    None, None, None,
                    pd.DataFrame(),
                    ""
                )

        analyze_btn.click(
            fn=handle_youtube_analysis,
            inputs=[url_input, comment_limit, auth_simulation_toggle],
            outputs=[
                status_box,
                thumb_preview, video_title_out, channel_out, duration_out, pub_date_out,
                kpi_views, kpi_likes, kpi_comments, kpi_like_ratio, kpi_engagement,
                kpi_shares, kpi_subs, kpi_watch, kpi_retention,
                pie_plot, bar_plot, eng_plot,
                comments_table,
                feedback_report_out
            ]
        )

        load_ref_btn.click(
            fn=lambda: "https://youtu.be/NRmAXDWJVnU",
            inputs=[],
            outputs=[url_input]
        )

