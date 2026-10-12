
import json
import time

from google import genai
from google.genai import types

from config import GEMINI_API_KEY
from models.analysis import ImageAnalysis


class AIService:

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model = "gemini-3.1-flash-lite"

    def _generate_response(self, contents, max_attempts=3):
        for attempt in range(max_attempts):
            try:
                return self.client.models.generate_content(
                    model=self.model,
                    contents=contents
                )
            except Exception as error:
                if "503" not in str(error) or attempt == max_attempts - 1:
                    raise

                time.sleep(3 * (attempt + 1))

    def analyze_image(self, image_file) -> ImageAnalysis:
        image_file.seek(0)

        contents = [
            types.Part.from_bytes(
                data=image_file.getvalue(),
                mime_type=image_file.type
            ),
            """
            Analyze this image and return ONLY valid JSON with this structure:
            {
                "description": "Detailed image description",
                "objects": ["Important objects"],
                "insights": ["Useful insights"],
                "recommendations": ["Practical recommendations"]
            }

            Provide 5-10 objects, 4-6 insights, and 3-5 recommendations
            when appropriate. Use clear language and do not invent facts.
            Return only JSON, without Markdown.
            """
        ]

        response = self._generate_response(contents)
        data = json.loads(response.text.strip())

        return ImageAnalysis(
            description=data.get("description", ""),
            objects=data.get("objects", []),
            insights=data.get("insights", []),
            recommendations=data.get("recommendations", [])
        )

    def ask_about_image(self, image_file, question):
        image_file.seek(0)

        contents = [
            types.Part.from_bytes(
                data=image_file.getvalue(),
                mime_type=image_file.type
            ),
            f"""
            Answer this question about the image:
            {question}

            Be clear and accurate. Do not invent details.
            """
        ]

        response = self._generate_response(contents)
        return response.text.strip()

    def compare_images(self, image1, image2):
        image1.seek(0)
        image2.seek(0)

        contents = [
            "Image 1:",
            types.Part.from_bytes(
                data=image1.getvalue(),
                mime_type=image1.type
            ),
            "Image 2:",
            types.Part.from_bytes(
                data=image2.getvalue(),
                mime_type=image2.type
            ),
            """
            Compare the images using these headings:
            1. Image descriptions
            2. Similarities
            3. Differences
            4. Uncertain details

            Use clear language and do not invent facts.
            """
        ]

        response = self._generate_response(contents)
        return response.text.strip()
