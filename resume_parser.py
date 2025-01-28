import argparse
import re
import spacy
import PyPDF2
import email_validator
import phonenumbers
import os
import csv

class ResumeParser:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.nlp = spacy.load('en_core_web_sm')
        self.text = self._extract_text()

    def _extract_text(self):
        with open(self.pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        return text

    def extract_name(self):
        doc = self.nlp(self.text)
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                return ent.text
        return None

    def extract_email(self):
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, self.text)
        return emails[0] if emails else None

    def extract_phone_numbers(self):
        phone_numbers = []
        for match in phonenumbers.PhoneNumberMatcher(self.text, "IN"):
            number = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            phone_numbers.append(number)
        return phone_numbers

    def extract_links(self):
        url_pattern = r'https?://\S+|www\.\S+'
        return re.findall(url_pattern, self.text)

    def extract_education(self):
        education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college']
        education_lines = [line for line in self.text.split('\n') if any(keyword in line.lower() for keyword in education_keywords)]
        return education_lines

    def extract_work_experience(self):
        experience_keywords = ['experience', 'worked', 'job', 'position', 'role']
        experience_lines = [line for line in self.text.split('\n') if any(keyword in line.lower() for keyword in experience_keywords)]
        return experience_lines
    
    def extract_previous_institutions(self):
        doc = self.nlp(self.text)
        institutions = [ent.text for ent in doc.ents if ent.label_ == 'ORG']
        return institutions

def main():
    parser = argparse.ArgumentParser(description='Resume Parser CLI')
    parser.add_argument('resume', nargs='?', help='Path to PDF resume')
    args = parser.parse_args()


    pdf_files = []
    if args.resume:
        pdf_files.append(args.resume)
    else:
        pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]

    if not pdf_files:
        print("No PDF files found in the current directory.")
        return
    

    with open('resume_details.csv', mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Name', 'Email', 'Phone Numbers', 'Links', 'Education', 'Work Experience', 'Previous Institutions']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for pdf_file in pdf_files:
            print(f"\nProcessing {pdf_file}...\n")
            resume_parser = ResumeParser(pdf_file)


            name = resume_parser.extract_name()
            email = resume_parser.extract_email()
            phone_numbers = resume_parser.extract_phone_numbers()
            links = resume_parser.extract_links()
            education = resume_parser.extract_education()
            work_experience = resume_parser.extract_work_experience()
            previous_institutions = resume_parser.extract_previous_institutions()

            writer.writerow({
                'Name': name,
                'Email': email,
                'Phone Numbers': ', '.join(phone_numbers),
                'Links': ', '.join(links),
                'Education': ' | '.join(education),
                'Work Experience': ' | '.join(work_experience),
                'Previous Institutions': ' | '.join(previous_institutions)

            })


            print("Resume Details:")
            print(f"Name: {resume_parser.extract_name()}")
            print(f"Email: {resume_parser.extract_email()}")
            print(f"Phone Numbers: {resume_parser.extract_phone_numbers()}")
            print(f"Links: {resume_parser.extract_links()}")
            print("\nEducation:")
            for edu in resume_parser.extract_education():
                print(f"- {edu}")
            print("\nWork Experience:")
            for exp in resume_parser.extract_work_experience():
                print(f"- {exp}")
            for inst in resume_parser.extract_previous_institutions():
                print(f"- {inst}")

    print("\nResume details saved to resume_details.csv")
    print("\nIn case of any error, please contact: vedantm@mkcl.org")


if __name__ == '__main__':
    main()
