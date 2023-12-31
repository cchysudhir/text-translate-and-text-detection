
# Import all required libraries
import secrets
from PIL import Image
from flask import Flask,render_template,request,redirect,url_for
import numpy as np
from gtts import gTTS
import pytesseract 
from googletrans import Translator
import os
import PyPDF2
import pyttsx3
import cv2


app = Flask(__name__)
app.secret_key = "your secret key here"
@app.route("/",methods=['GET','POST'])
def home():
    return render_template('home.html')

@app.route("/about",methods=['GET','POST'])
def about():
    return render_template('about.html')


@app.route("/contact",methods=['GET','POST'])
def contact():
    return render_template('contact.html')

@app.route("/submit",methods=['GET','POST'])
def submit():
    if request.method == "POST":
        fname = request.form.get("first_name")
        mname = request.form.get("millde_name")
        lname = request.form.get("last_name")
        num = request.form.get("number")
        email=request.form.get("email-1")
        print(fname,mname,lname,num,email)

        return "Your form has been submitted successfully"


    return render_template('contact.html')




imgExts=[".png",".jpg",".jpeg"]
# docExts=[".txt",".docx",".doc",".pdf"]
docExts=[".pdf"]
LANGUAGES = {
    'en': 'english',
    'hi': 'hindi',
    'kn': 'kannada',
    'ne': 'nepali'
}

@app.route("/imagetospeechtest",methods=['GET','POST'])
def imagetospeechtest():
    error=True
    if request.method=="POST":
        img=request.files['imageFile']
        select=request.form.get('lang_list')
        image_path="./images/"+img.filename

        ado=False
        pdfaudio=False
        imgExts=[".png",".jpg",".jpeg"]
        # check the file extention 
        if os.path.splitext(image_path)[1].lower() in imgExts:
            ado=True
            img.save(image_path)
            imgread = cv2.imread(image_path)
            imgfile = cv2.resize(imgread, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)

            def noise_removal(image):
                import numpy as np
                kernel = np.ones((2, 2), np.uint8)
                image = cv2.dilate(image, kernel, iterations=1)
                kernel = np.ones((2, 2), np.uint8)
                image = cv2.erode(image, kernel, iterations=1)
                image = cv2.morphologyEx(image, cv2.MORPH_CLOSE,kernel)
                image = cv2.medianBlur(image,3)
                return image

            def normalization(img):
                resultimage = np.zeros((800, 800))
                normalizedimage = cv2.normalize(no_noise,resultimage, 0, 100, cv2.NORM_MINMAX)
                return normalizedimage

            def grayscale(image):
                gray_img = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
                return gray_img
            def thresholding(gray_image):#thresholding/binarizalation
                thresh,imbw =cv2.threshold(gray_image, 180, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                return imbw
            # preprocessing the images 
            no_noise = noise_removal(imgfile)
            normal_img = normalization(no_noise)
            gray_image = grayscale(normal_img)
            thre_img=thresholding(gray_image)
            # pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            text = pytesseract.image_to_string(thre_img,lang="eng+hin+nep")

            #To translate the text  in a selected language
            translater = Translator()
            text_to_translate = text
            if len(text_to_translate) !=0:
                out = translater.translate(text_to_translate, dest=select)
                translated_text = out.text
                translated = translated_text

                #Savein  mp3 format file of a translated text
                obj = gTTS(text = translated, slow=False, lang = select)
                adfiile=secrets.token_hex(5)
                obj.save("./static/"+adfiile)
                os.remove(image_path)
                return render_template('imgtospeech.html',extracted_text=text,transText=translated,data=LANGUAGES,ado=ado,error=error,adfile=adfiile)
            else:
                engine = pyttsx3.init()
                engine.say('Please choose a image again containing text.')
                engine.runAndWait()
                return redirect('imagetospeechtest')
        if os.path.splitext(image_path)[1].lower() in docExts:
            pdfaudio=True
            ado=False
            readPdf=PyPDF2.PdfFileReader(img)
            numOfPdfPage=readPdf.getNumPages()
            st=""
            for i in range(numOfPdfPage):
                st+=readPdf.getPage(i).extract_text()
            with open("text.txt","w",encoding="utf-8") as f:
                f.write(st)

            translater = Translator()
            out = translater.translate("somthig here", dest=select)
            print(type(out))
            translated_text = out.text
            translated = translated_text
            with open("text.txt","r") as f:
                engine=pyttsx3.init()
                engine.save_to_file(f.read(),"./static/convert.mp3")
                engine.runAndWait()
            return render_template('pdfHandle.html',extracted_text=st,data=LANGUAGES,ado=ado,pdfaudio=pdfaudio,error=error)
        else:
            engine = pyttsx3.init()
            engine.say('Please choose a valid file.')
            engine.runAndWait()

    return render_template('imgtospeech.html',data=LANGUAGES,error=error)



# camera code starts here 
@app.route("/camera",methods=["GET","POST"])
def camera():
    if request.method=="POST":
        return redirect(url_for('redirect_data'))
    return render_template("testcameradata.html",data=LANGUAGES)

@app.route('/redirect_data',methods=["GET","POST"])
def redirect_data():
    btnHandle=True
    audioHandle=False
    imageName="screen.jpg"
    path="C:\\Users\\SUDHEER\\OneDrive\\Pictures\\Screenshots"
    def getText():
        if imageName in os.listdir(path):     
            inputPath=os.path.join(path,imageName)
            img=Image.open(inputPath)
            imgread=cv2.imread(inputPath)
            # imgfile = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
            def noise_removal(image):
                import numpy as np
                kernel = np.ones((2, 2), np.uint8)
                image = cv2.dilate(image, kernel, iterations=1)
                kernel = np.ones((2, 2), np.uint8)
                image = cv2.erode(image, kernel, iterations=1)
                image = cv2.morphologyEx(image, cv2.MORPH_CLOSE,kernel)
                image = cv2.medianBlur(image,3)
                return image

            def normalization(img):
                resultimage = np.zeros((800, 800))
                normalizedimage = cv2.normalize(no_noise,resultimage, 0, 100, cv2.NORM_MINMAX)
                return normalizedimage

            def grayscale(image):
                gray_img = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
                return gray_img
            def thresholding(gray_image):#thresholding/binarizalation
                thresh,imbw =cv2.threshold(gray_image, 180, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                return imbw

            no_noise = noise_removal(imgread)
            normal_img = normalization(no_noise)
            gray_image = grayscale(normal_img)
            thre_img=thresholding(gray_image)
            # pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            text = pytesseract.image_to_string(img,lang="hin+nep+eng")
            print(text)
            os.remove(os.path.join(path,imageName))
            return text
    t=getText()
    if request.method=="POST":
        btnHandle=False
        audioHandle=True
        select=request.form.get('lang_list')
        print(select)
        translater = Translator()
        text_to_translate = t

        if len(text_to_translate)!=0:
            # try:
            out = translater.translate(text_to_translate, dest=select)
            translated_text = out.text
            translated = translated_text
            print(translated)
            obj = gTTS(text = translated, slow=False, lang = select)
            camadfiile=secrets.token_hex(5)
            obj.save("./static/"+camadfiile)
            return render_template("testdata.html",extracted_text=t,data=LANGUAGES,transText=translated,lang=select,audioHandle=audioHandle,camadfiile=camadfiile)
            # except AssertionError:
            #     engine = pyttsx3.init()
            #     engine.say('Please capture a image again containing text.')
            #     engine.runAndWait()
            #     return redirect('camera')

        else:
            engine = pyttsx3.init()
            engine.say('Please capture a image again containing text.')
            engine.runAndWait()
            return redirect('camera')
    return render_template("testdata.html",data=LANGUAGES,btnHandle=btnHandle)


if __name__ =='__main__':
    app.run(debug=True)