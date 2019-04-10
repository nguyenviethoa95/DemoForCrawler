import pytesseract
import boto3
#from PIL import Image
import pdf2image
import requests
from src.baseclass import BotoClient

# split pdf into images and save in S3
pdf_url = 'https://www.bernburg.de/media/dokumente/buerger/amtsblaetter/2019/maerz19.pdf'
#s3_client= BotoClient.BotoClient('s3')

req = requests.get(pdf_url, stream=True)

# apply tesseract to extract the text from images
images= pdf2image.convert_from_bytes(req.content, dpi=300, output_folder=None, fmt='jpeg', use_cropbox=False)
count = 0
count = 0
for image in images:
    image.save('page_'+str(count)+'.jpg','JPEG')
    count = count+1

#save text of each PDF into a txt file

