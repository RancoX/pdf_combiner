import PyPDF2, pathlib, logging

'''
Please ensure you've installed PyPDF2 before running the code

To install PyPDF2 please execute 'pip install PyPDF2' from your command line

Fore more information on how to install PyPDF2 please refer to https://pypi.org/project/PyPDF2/

This a demo program that combines any number od pdf files nominated by the user

It will retain all the pages in each pdf and output to a combined file

To use this program, put all candidate pdfs in the same folder as this python script

Then add the pdf name to candidate list below

To encrypt output pdf with ppassword, please modify variable 'encryppt_or_not' below

'''
### USER INPUTS ###
candidates=['grant_letter.pdf','transcript.pdf']

# change empty string to the password you wanna use otherwise leave as is or change it to None
encrypt_or_not=''

########################################## DO NOT ALTER BELOW CODE ###################################################


# logging set up
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.info('PDF combiner initiated...')

# get list of all candidate pdfs in order
BASE_DIR=pathlib.Path(__file__).resolve().parent
logging.info(BASE_DIR)

# raise exception if len of the candidates is less than 2
if len(candidates)<2:
    raise IndexError('Less than 2 files, no need to merge!')

# loop thru all candidates to read them and add page to pdfWriter
# initiate pdfWriter
pdfWriter=PyPDF2.PdfFileWriter()

# initiate binary pdf cache
binary_pdf_cache=[]

for count, candidate in enumerate(candidates):
    logging.info(f"Now opening {candidate}...")
    binary_pdf_cache.append(open(BASE_DIR / candidate,'rb'))
    pdf=PyPDF2.PdfFileReader(binary_pdf_cache[count])

    # loop thru all pages in current pdf
    for i in range(pdf.numPages):
        page=pdf.getPage(i)
        
        # add to pdfWriter
        pdfWriter.add_page(page)

    # check if the last file has been read
    if count == len(candidates)-1:
        # output to target file
        with open(BASE_DIR / 'combined_pdf.pdf', 'wb') as wf:
            logging.info('Now writing to combined file...')
            if encrypt_or_not:
                pdfWriter.encrypt(encrypt_or_not)
                logging.info('combined file is encrypted!')
            pdfWriter.write(wf)

    logging.info(f"All pages in {candidate} were relocated!")

# close all cache binary pdfs
for binary_pdf in binary_pdf_cache:
    binary_pdf.close()

logging.info('All files have been merged')