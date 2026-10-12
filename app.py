import streamlit as st
from services.report_service import ReportService

from services.image_service import ImageService
from services.ai_service import AIService

from services.history_service import HistoryService

from services.export_service import ExportService

class ImageInsightsApp:

    def __init__(self):
        self.report_service = ReportService()
        self.image_service = ImageService()
        self.ai_service = AIService()
        self.history_service = HistoryService()
        self.export_service = ExportService()

    def setup_page(self):
        st.set_page_config(
            page_title="AI Image Insights",
            page_icon="🔍",
            layout="wide"
        )

        st.markdown("""
        <style>

        .main-title {
            font-size: 42px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 5px;
        }

        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #777;
            margin-bottom: 35px;
        }

        .section-title {
            font-size: 25px;
            font-weight: 600;
            margin-top: 25px;
            margin-bottom: 10px;
        }

        .info-card {
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #ddd;
            margin-bottom: 15px;
        }

        </style>
        """, unsafe_allow_html=True)

    def run(self):

        self.setup_page()
        if "result" not in st.session_state:
            st.session_state.result = None

        if "analysis_filename" not in st.session_state:
            st.session_state.analysis_filename = None

        st.markdown(
            '<div class="main-title">🔍 AI Image Insights</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="subtitle">'
            'Upload an image and get detailed AI-powered insights'
            '</div>',
            unsafe_allow_html=True
        )
        st.markdown("---")
        st.subheader("🖼️ Compare Two Images")

        col1, col2 = st.columns(2)

        with col1:
            image1 = st.file_uploader(
                "Upload First Image",
                type=["jpg", "jpeg", "png"],
                key="compare_image1"
            )

        with col2:
            image2 = st.file_uploader(
                "Upload Second Image",
                type=["jpg", "jpeg", "png"],
                key="compare_image2"
            )

        if image1 and image2:
            col1, col2 = st.columns(2)

            with col1:
                st.image(image1, caption="Image 1", use_container_width=True)

            with col2:
                st.image(image2, caption="Image 2", use_container_width=True)

            if st.button("🔍 Compare Images", key="compare_button"):
                try:
                    with st.spinner("🤖 Comparing images..."):
                        comparison = self.ai_service.compare_images(
                            image1,
                            image2
                        )

                    st.subheader("📊 Comparison Results")
                    st.write(comparison)

                except Exception as error:
                    st.error(f"Comparison failed: {error}")
        uploaded_file = st.file_uploader(
            "📤 Upload your image",
            type=["jpg", "jpeg", "png"]
        )

        if uploaded_file:

            image = self.image_service.open_image(uploaded_file)

            st.image(
                image,
                caption="Uploaded Image",
                width=600
            )

            st.write("")

            if st.button(
                "✨ Analyze Image",
                use_container_width=True
            ):

                with st.spinner("🤖 AI is analyzing your image..."):

                    result = self.ai_service.analyze_image(
                        uploaded_file
                    )
                    st.session_state.result = result
                    st.session_state.analysis_filename = uploaded_file.name
                    
                    self.history_service.save_analysis(
                        uploaded_file.name,
                        result
                    )

                st.success("Analysis completed successfully!")

                st.markdown(
                    '<div class="section-title">📝 Description</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="info-card">{result.description}</div>',
                    unsafe_allow_html=True
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.markdown(
                        '<div class="section-title">🔍 Important Objects</div>',
                        unsafe_allow_html=True
                    )

                    for obj in result.objects:
                        st.markdown(f"- {obj}")

                with col2:

                    st.markdown(
                        '<div class="section-title">💡 Useful Insights</div>',
                        unsafe_allow_html=True
                    )

                    for insight in result.insights:
                        st.markdown(f"- {insight}")

                    st.markdown(
                        '<div class="section-title">📌 Recommendations</div>',
                        unsafe_allow_html=True
                    )
                    result = st.session_state.result

            if st.session_state.result is not None:
                result = st.session_state.result
                st.markdown("---")
                st.subheader("💬 Ask AI About This Image")

                with st.form("image_chat_form"):
                    question = st.text_input(
                        "Ask a question about this image:"
                    )
                    ask_button = st.form_submit_button("Ask AI")

                if ask_button and question.strip():
                    try:
                        with st.spinner("AI is thinking..."):
                            uploaded_file.seek(0)
                            answer = self.ai_service.ask_about_image(
                                uploaded_file,
                                question.strip()
                            )
                        st.write("**AI Answer:**")
                        st.write(answer)

                    except Exception as error:
                        st.error(f"Could not get an answer: {error}")
                pdf_report = self.report_service.create_pdf_report(
                    result,
                    uploaded_file
                )
                
                text_report = self.export_service.create_text_report(
                    result,
                    uploaded_file.name
                )

                json_report = self.export_service.create_json_report(
                    result,
                    uploaded_file.name
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.download_button(
                        label="📄 Download TXT",
                        data=text_report,
                        file_name="ai_image_insights_report.txt",
                        mime="text/plain",
                        use_container_width=True,
                        key="download_txt_report"
                    )

                with col2:
                    st.download_button(
                        label="📊 Download JSON",
                        data=json_report,
                        file_name="ai_image_insights_report.json",
                        mime="application/json",
                        use_container_width=True,
                        key="download_json_report"
                    )

                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_report,
                    file_name="ai_image_insights_report.pdf",
                    mime="application/pdf", 
                    use_container_width=True,
                    key="download_pdf_report"
                )
                st.markdown("---")

                st.markdown(
                    '<div class="section-title">📚 Analysis History</div>',
                    unsafe_allow_html=True
                )

                history = self.history_service.get_history()
                    
                if history:
                    if st.button(
                        "🗑️ Clear History",
                        key="clear_history"
                    ):
                        self.history_service.clear_history()
                        st.success("Analysis history cleared.")
                        st.rerun()

                    
                st.markdown("---")
                st.subheader("📊 Analysis Dashboard")

                stats = self.history_service.get_statistics()

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Total Analyses",
                    stats["total_analyses"]
                )

                col2.metric(
                    "Objects Identified",
                    stats["total_objects"]
                )

                col3.metric(
                    "Insights Generated",
                    stats["total_insights"]
                )


                if history:
                    for item in reversed(history):
                        with st.expander(f"🖼️ {item['filename']}"):
                            st.write("**Description:**")
                            st.write(item["description"])

                            st.write("**Objects:**")
                            for obj in item["objects"]:
                                st.write(f"- {obj}")

                            st.write("**Insights:**")
                            for insight in item["insights"]:
                                st.write(f"- {insight}")

                            st.write("**Recommendations:**")
                            for recommendation in item["recommendations"]:
                                st.write(f"- {recommendation}")
                else:
                    st.info("No analysis history yet.")


if __name__ == "__main__":
    app = ImageInsightsApp()
    app.run()