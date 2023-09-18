import difflib
import os
import PyPDF2
from docx import Document
import openai

# Set your OpenAI API key here

openai.api_key = "your-key"

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            for page_num in range(pdf_reader.getNumPages()):
                page = pdf_reader.getPage(page_num)
                text += page.extractText()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text

# Function to extract text from a Word document
def extract_text_from_docx(docx_path):
    text = ""
    try:
        doc = Document(docx_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
    return text

# Function to compare text similarity using ChatGPT
def compare_text_similarity_with_gpt(text1, text2):
    prompt = f"Compare the suitability of the following resume to the job description:\n\nResume:\n{text1}\n\nJob Description:\n{text2}\n\nEvaluate the fitment."
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=100  # Adjust the max tokens as needed
        )
        
        response_text = response.choices[0].text.strip()  # Get the response text
        #print("OpenAPI response: ", response_text)
    except openai.OpenAIError as e:
        # Handles API-specific exceptions
        print("Error String", e)
        error_message = f"OpenAI API Error: {str(e)}"
        return error_message;
     
    return response_text

# Function to load job description from a file
def load_job_description(job_description_path):
    file_extension = os.path.splitext(job_description_path)[1].lower()
    if file_extension == ".pdf":
        return extract_text_from_pdf(job_description_path)
    elif file_extension == ".docx":
        return extract_text_from_docx(job_description_path)
    else:
        print("Unsupported file format for job description. Please provide a PDF or DOCX file.")
        return None

# Main function to generate the fitment report
def generate_fitment_report(resume_path, job_description_path):
    # Load job description text
    jd_text = load_job_description(job_description_path)
    if jd_text is None:
        return None

    # Extract text from the resume (PDF or Word)
    file_extension = os.path.splitext(resume_path)[1].lower()

    if file_extension == ".pdf":
        resume_text = extract_text_from_pdf(resume_path)
    elif file_extension == ".docx":
        resume_text = extract_text_from_docx(resume_path)
    else:
        print("Unsupported file format for resume. Please provide a PDF or DOCX file.")
        return None

    suitability = compare_text_similarity_with_gpt(resume_text, jd_text)

    fitment_report = {
        "Recommendation": suitability
    }

    return fitment_report


if __name__ == "__main__":
    # Provide the path to the candidate's resume in PDF or DOCX format
    resume_path = "scrum_test_master.docx"

    # Provide the path to the job description file (PDF or DOCX)
    job_description_path = "Full Stack . NET Dummy JD-2.docx" 

    # Generate the fitment report
    report = generate_fitment_report(resume_path, job_description_path)
    #report = generate_fitment_report_with_text(resume_path, job_description_path)
    # wrong compare_text_similarity_with_gpt(resume_path, job_description_path)

    # Display the fitment report
    if report is not None:
        print("Fitment Report:")
        for key, value in report.items():
            print(f"{key}: {value}")
