import random
import uuid

from app.services.gemini_service import GeminiService


class Part4Service:
    """Generate TOEIC Speaking Part 4 practice documents and questions 8-10."""

    def __init__(self):
        self.gemini = GeminiService()

    def generate_questions(self) -> dict:
        template = random.choice(self._document_templates())
        prompt = self._build_generation_prompt(template["topic"], template["document"])

        try:
            response = self.gemini.generate(prompt)
            parsed = self._parse_response(response, template)
        except Exception as exc:
            print(f"Part 4 generation fallback used: {exc}")
            parsed = self._build_fallback_questions(template)

        return {
            "id": str(uuid.uuid4())[:8],
            "part": 4,
            "task_type": "respond_to_questions",
            "instruction": "Read the business document carefully, then answer the three telephone questions using only the information in the document.",
            "topic": parsed["topic"],
            "document": parsed["document"],
            "questions": parsed["questions"],
        }

    def _document_templates(self) -> list[dict]:
        return [
            {
                "topic": "conference schedule",
                "document": "Conference Schedule\nEvent: Northwind Business Summit\nDate: October 18\nVenue: Grand Harbor Hotel, Room B\n9:00-9:30 Registration\n9:30-10:15 Keynote Speech\n10:15-10:45 Coffee Break\n11:00-12:00 Panel Discussion\n12:00-1:30 Lunch",
                "questions": [
                    "When does the keynote speech begin?",
                    "Where is the business summit being held?",
                    "What happens after the keynote speech?",
                ],
            },
            {
                "topic": "invoice",
                "document": "Invoice\nInvoice Number: INV-2048\nCustomer: GreenTech Solutions\nIssue Date: May 12\nDue Date: May 26\nAmount Due: $3,450\nPayment Method: Bank Transfer",
                "questions": [
                    "When is the invoice due?",
                    "Who is the customer?",
                    "How much money is due?",
                ],
            },
            {
                "topic": "travel itinerary",
                "document": "Travel Itinerary\nPassenger: Ms. Lee\nFlight: TK 482\nDeparture: Seoul, 7:40 a.m.\nArrival: Tokyo, 10:10 a.m.\nHotel: Harbor Plaza Hotel\nCheck-in Time: 3:00 p.m.",
                "questions": [
                    "What time does the flight depart from Seoul?",
                    "Where will Ms. Lee stay?",
                    "What time can she check in at the hotel?",
                ],
            },
        ]

    def _build_generation_prompt(self, topic: str, document: str) -> str:
        return f"""
Generate TOEIC Speaking Part 4 practice material for questions 8-10.
Topic: {topic}
Document:
{document}
Requirements:
- Create a business document that is realistic and easy to understand.
- Create three telephone-style questions based strictly on information in the document.
- Question 8 and 9 should each require a 15-second response.
- Question 10 should require a 30-second response.
Return EXACTLY:
[TOPIC] topic_name
[DOCUMENT] document text
[QUESTION8] question text
[QUESTION9] question text
[QUESTION10] question text
"""

    def _parse_response(self, response: str, fallback_template: dict) -> dict:
        topic = fallback_template["topic"]
        document = fallback_template["document"]
        questions = []

        for line in response.splitlines():
            stripped = line.strip()
            if stripped.startswith("[TOPIC]"):
                topic = stripped.replace("[TOPIC]", "").strip() or fallback_template["topic"]
            elif stripped.startswith("[DOCUMENT]"):
                document = stripped.replace("[DOCUMENT]", "").strip() or fallback_template["document"]
            elif stripped.startswith("[QUESTION8]"):
                questions.append(self._build_question(8, 15, stripped.replace("[QUESTION8]", "").strip()))
            elif stripped.startswith("[QUESTION9]"):
                questions.append(self._build_question(9, 15, stripped.replace("[QUESTION9]", "").strip()))
            elif stripped.startswith("[QUESTION10]"):
                questions.append(self._build_question(10, 30, stripped.replace("[QUESTION10]", "").strip()))

        if len(questions) != 3:
            return self._build_fallback_questions(fallback_template)

        return {"topic": topic, "document": document, "questions": questions}

    def _build_question(self, question_number: int, response_time: int, text: str) -> dict:
        return {
            "id": str(uuid.uuid4())[:8],
            "question_number": question_number,
            "part": 4,
            "task_type": "respond_to_questions",
            "instruction": "Answer the question clearly and only use information from the document.",
            "preparation_time": 45,
            "response_time": response_time,
            "text": text or "Please answer the telephone inquiry based on the document.",
            "topic": "business document",
        }

    def _build_fallback_questions(self, template: dict) -> dict:
        questions = [
            self._build_question(8, 15, template["questions"][0]),
            self._build_question(9, 15, template["questions"][1]),
            self._build_question(10, 30, template["questions"][2]),
        ]
        return {"topic": template["topic"], "document": template["document"], "questions": questions}
