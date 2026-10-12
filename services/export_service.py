
import json


class ExportService:

    @staticmethod
    def create_text_report(analysis, filename):
        lines = [
            "AI IMAGE INSIGHTS REPORT",
            "=" * 30,
            f"Image: {filename}",
            "",
            "DESCRIPTION",
            analysis.description,
            "",
            "IMPORTANT OBJECTS",
        ]

        lines.extend(f"- {item}" for item in analysis.objects)
        lines.extend(["", "USEFUL INSIGHTS"])
        lines.extend(f"- {item}" for item in analysis.insights)
        lines.extend(["", "RECOMMENDATIONS"])
        lines.extend(f"- {item}" for item in analysis.recommendations)

        return "\n".join(lines)

    @staticmethod
    def create_json_report(analysis, filename):
        report = {
            "filename": filename,
            "description": analysis.description,
            "objects": analysis.objects,
            "insights": analysis.insights,
            "recommendations": analysis.recommendations,
        }

        return json.dumps(report, indent=4, ensure_ascii=False)
