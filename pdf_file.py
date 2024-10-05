from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image


def save_task_to_pdf(messages, image_path, filename_template='Task_{}.pdf'):
    """
    Generates a PDF for each task based on the provided messages and saves them as separate files.

    :param messages: Dictionary containing task details.
    :param image_path: Path to the image file (e.g., 'icon.png').
    :param filename_template: Template for the output filenames.
    """
    print("this is what i got",messages)
    # Get the total number of tasks
    num_tasks = int(messages['number_of_tasks'][0])

    # Iterate over each task index
    for i in range(num_tasks):
        # Prepare data for the table for each task
        data = [['Entity', 'Description']]  # Table header

        # Add task-specific data to the table
        data.append(['Company Name', messages['company_name'][0]])  # Assuming company name is the same
        data.append(['Email', messages['email'][0]])  # Assuming email is the same
        data.append(['Phone Number', messages['phone_number'][0]])  # Assuming phone number is the same
        data.append(['Task Name', messages['task_name'][i]])
        data.append(['Citizenship or Residency', messages['citizenship_or_residency'][i]])
        data.append(['In-Person Meeting', messages['in_person_meeting'][i]])
        data.append(['Compliance Requirements', messages['compliance_requirements'][i]])
        data.append(['Federal or State Licence', messages['federal_or_state_licence'][i]])
        data.append(['Task Eligibility', messages['task_eligibility_yes_or_no'][i]])

        # Create a PDF document for each task
        filename = filename_template.format(i + 1)
        pdf = SimpleDocTemplate(filename, pagesize=letter)

        # Create a Table object
        table = Table(data, colWidths=[8 * cm, 10 * cm])

        # Add style to the table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header background
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alignment
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
            ('FONTSIZE', (0, 0), (-1, 0), 12),  # Header font size
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Grid lines
        ])
        table.setStyle(style)

        # Alternate row colors
        for j in range(1, len(data)):
            bg_color = colors.whitesmoke if j % 2 == 0 else colors.lightgrey
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, j), (-1, j), bg_color),
            ]))

        # Create an Image object for the icon
        image = Image(image_path)

        # Get the original width and height of the image
        original_width, original_height = image.wrap(0, 0)

        # Scale the image proportionally (for example, 50% of original size)
        scale_factor = 0.4
        image.drawWidth = original_width * scale_factor
        image.drawHeight = original_height * scale_factor

        # Build the PDF with the image on top
        elements = [image, table]  # First the image, then the table
        pdf.build(elements)

        print(f"PDF saved as '{filename}'")

#save_task_to_pdf(messages, 'branding.png', filename_template='Task_{}.pdf')