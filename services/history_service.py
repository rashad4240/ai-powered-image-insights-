import json
import os


class HistoryService:

    def __init__(self):
        self.file_path = "data/history.json"

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as file:
                json.dump([], file)

    def save_analysis(self, filename, analysis):

        with open(self.file_path, "r") as file:
            history = json.load(file)

        record = {
            "filename": filename,
            "description": analysis.description,
            "objects": analysis.objects,
            "insights": analysis.insights,
            "recommendations": analysis.recommendations
        }

        history.append(record)

        with open(self.file_path, "w") as file:
            json.dump(history, file, indent=4)

    def get_history(self):

        with open(self.file_path, "r") as file:
            return json.load(file)
    
    def get_statistics(self):
        history = self.get_history()

        total_analyses = len(history)
        total_objects = sum(
            len(item.get("objects", [])) for item in history
        )
        total_insights = sum(
            len(item.get("insights", [])) for item in history
        )

        return {
            "total_analyses": total_analyses,
            "total_objects": total_objects,
            "total_insights": total_insights,
        }
    
    def clear_history(self):
        with open(self.file_path, "w") as file:
            json.dump([], file, indent=4)
