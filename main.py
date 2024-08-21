import typer
from typing import Optional, List
from phi.assistant import Assistant
from phi.storage.assistant.postgres import PgAssistantStorage
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector2
import fitz  # PyMuPDF for PDF handling
import re

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

knowledge_base = PDFUrlKnowledgeBase(
    urls=["/Users/mahac/phidata/project1/employee_pto_data.pdf"],  # Replace with your actual file path
    vector_db=PgVector2(collection="pto_data", db_url=db_url),
)

storage = PgAssistantStorage(table_name="pdf_assistant", db_url=db_url)

def extract_pto_days(pdf_path):
    doc = fitz.open(pdf_path)
    employee_pto_data = []

    for page_num in range(len(doc)):
        page_text = doc[page_num].get_text()
        matches = re.findall(r'(\w+\s+\w+):\s+(\d+)\s+days taken', page_text)
        for match in matches:
            employee_name = match[0]
            days_taken = int(match[1])
            remaining_pto = 25 - days_taken  # Assuming 25 total PTO days
            employee_pto_data.append((employee_name, remaining_pto))

    doc.close()
    return employee_pto_data


def pdf_assistant(new: bool = False, user: str = "user"):
    run_id: Optional[str] = None

    if not new:
        existing_run_ids: List[str] = storage.get_all_run_ids(user)
        if len(existing_run_ids) > 0:
            run_id = existing_run_ids[0]

    assistant = Assistant(
        run_id=run_id,
        user_id=user,
        knowledge_base=knowledge_base,
        storage=storage,
        show_tool_calls=True,
        search_knowledge=True,
        read_chat_history=True,
    )

    if run_id is None:
        run_id = assistant.run_id
        print(f"Started Run: {run_id}\n")
    else:
        print(f"Continuing Run: {run_id}\n")

    employee_pto_data = extract_pto_days("/Users/mahac/phidata/project1/employee_pto_data.pdf")

    for employee, remaining_pto in employee_pto_data:
        print(f"{employee}: {remaining_pto} days remaining")

if __name__ == "__main__":
    pdf_assistant()