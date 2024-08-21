from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import random

# List of random employee names
employee_names = [
    "John Doe", "Jane Smith", "Michael Johnson", "Emily Brown", 
    "David Williams", "Sarah Miller", "Kevin Davis", "Emma Garcia", 
    "Chris Martinez", "Olivia Wilson"
]

# Generate random PTO days already taken for each employee
pto_data = {name: random.randint(0, 25) for name in employee_names}

# Create a PDF file
pdf_filename = "employee_pto_data.pdf"
c = canvas.Canvas(pdf_filename, pagesize=letter)

# Set up PDF content
c.setFont("Helvetica", 12)
c.drawString(50, 800, "Employee PTO Data")
c.line(50, 790, 250, 790)

# Write employee data to PDF
y_position = 750
for name, days_taken in pto_data.items():
    c.drawString(50, y_position, f"{name}: {days_taken} days taken")
    y_position -= 20

# Save the PDF file
c.save()

print(f"PDF file '{pdf_filename}' has been generated.")
