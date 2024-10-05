

def body_title(parsed_data,task_number):
    task_number = task_number - 1
    if 'eligible'  in str(parsed_data['task_eligibility_yes_or_no'][task_number]) or 'yes' in str(parsed_data['task_eligibility_yes_or_no'][task_number]):
        print("task is eligible")
        title = "Congratulations! your Company is eligible for our VA program"
        body= """Dear Valued Client,

              Thank you for reaching out to Insurgen. We have received your information and appreciate your interest in our services. We wanted to inform you that you company is eligible for our VA program. One of our consultants will be in touch with you shortly to assist with your request.

            Please review the attached details we have received from you to ensure their accuracy. If any information is incorrect, kindly notify us at your earliest convenience.
            We look forward to serving you. Should you have any further questions or concerns, please do not hesitate to contact us.

    Best regards,
    Insurgen Team"""
        return title , body
    else:
        print("task is not eligible")
        title = "Your Company is not eligible for our VA program"
        body = """Dear Valued Client,

              Thank you for reaching out to Insurgen. We have received your information and appreciate your interest in our services. We wanted to inform you that you company is not eligible for our VA program. One of our consultants will be in touch with you shortly to assist with your request.

            Please review the attached details we have received from you to ensure their accuracy. If any information is incorrect, kindly notify us at your earliest convenience.
            We look forward to serving you. Should you have any further questions or concerns, please do not hesitate to contact us.

    Best regards,
    Insurgen Team"""
        return title , body
