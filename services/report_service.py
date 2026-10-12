from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from PIL import Image
import io


class ReportService:

    def create_pdf_report(self, analysis, image_file):

        pdf_buffer = io.BytesIO()

        pdf = canvas.Canvas(pdf_buffer, pagesize=A4)

        page_width, page_height = A4

        # Title
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawString(50, page_height - 50, "AI Image Insights Report")

        # Add image
        image = Image.open(image_file)
        image.thumbnail((160, 160))

        image_buffer = io.BytesIO()
        image.save(image_buffer, format="PNG")
        image_buffer.seek(0)

        pdf.drawImage(
            ImageReader(image_buffer),
            page_width - 230,
            page_height - 230,
            width=160,
            height=160,
            preserveAspectRatio=True
        )

        y = page_height - 280

        # Description
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawString(50, page_height - 50, "AI Image Insights Report")

        y -= 25
        pdf.setFont("Helvetica", 10)

        for line in self.wrap_text(analysis.description, 80):
            pdf.drawString(50, y, line)
            y -= 15

        # Objects
        y -= 15
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y, "Important Objects")

        y -= 20
        pdf.setFont("Helvetica", 10)

        for obj in analysis.objects:
            for line in self.wrap_text("- " + obj, 80):
                pdf.drawString(50, y, line)
                y -= 15

        # Insights
        y -= 15
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y, "Useful Insights")

        y -= 20
        pdf.setFont("Helvetica", 10)

        for insight in analysis.insights:
            for line in self.wrap_text("- " + insight, 80):
                pdf.drawString(50, y, line)
                y -= 15

        # Recommendations
        y -= 15
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y, "Recommendations")

        y -= 20
        pdf.setFont("Helvetica", 10)

        for recommendation in analysis.recommendations:
            for line in self.wrap_text("- " + recommendation, 80):
                pdf.drawString(50, y, line)
                y -= 15

        pdf.save()

        pdf_buffer.seek(0)

        return pdf_buffer.getvalue()

    @staticmethod
    def wrap_text(text, width):
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 <= width:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        return lines