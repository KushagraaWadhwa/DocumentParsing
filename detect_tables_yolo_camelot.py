import os
import sys
import copy
from camelot import io as camelot
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PyPDF2 import PdfFileWriter, PdfReader
from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image
from ultralyticsplus import YOLO, render_result


def norm_pdf_page(pdf_file, pg):
    pdf_doc = PdfReader(open(pdf_file, "rb"))
    pdf_page = pdf_doc.pages[pg-1]
    pdf_page.cropbox.upper_left = (0, list(pdf_page.mediabox)[-1])
    pdf_page.cropbox.lower_right = (list(pdf_page.mediabox)[-2], 0)
    return pdf_page

def pdf_page2img(pdf_file, pg, save_image=True):
    img_page = convert_from_path(pdf_file, first_page=pg, last_page=pg)[0]
    # Check whether the specified path exists or not
    new_path = os.path.join(pdf_file.strip(".pdf"), 'PDFimages')
    isExist = os.path.exists(new_path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(new_path)
        print(f"The new directory {new_path} is created!")
    if save_image:
        img=os.path.join(new_path, f"Page_{pg}.jpg")
        img_page.save(img)
    return np.array(img_page)

def img_dim(img, bbox):
    H_img,W_img,_=img.shape
    x1_img, y1_img, x2_img, y2_img,_,_=bbox
    w_table, h_table=x2_img-x1_img, y2_img-y1_img
    return [[x1_img, y1_img, x2_img, y2_img], [w_table, h_table], [H_img,W_img]]


def norm_bbox(img, bbox, x_corr=0.05, y_corr=0.05):
    [[x1_img, y1_img, x2_img, y2_img], [w_table, h_table], [H_img,W_img]]=img_dim(img, bbox)
    x1_img_norm,y1_img_norm,x2_img_norm,y2_img_norm=x1_img/W_img, y1_img/H_img, x2_img/W_img, y2_img/H_img
    w_img_norm, h_img_norm=w_table/W_img, h_table/H_img
    w_corr=w_img_norm*x_corr
    h_corr=h_img_norm*x_corr

    return [x1_img_norm-w_corr,y1_img_norm-h_corr/2,x2_img_norm+w_corr,y2_img_norm+2*h_corr]


def bboxes_pdf(img, pdf_page, bbox):
    W_pdf=float(pdf_page.cropBox.getLowerRight()[0])
    H_pdf=float(pdf_page.cropBox.getUpperLeft()[1])

    [x1_img_norm,y1_img_norm,x2_img_norm,y2_img_norm]=norm_bbox(img, bbox)
    x1, y1 = x1_img_norm*W_pdf, (1-y1_img_norm)*H_pdf
    x2, y2 = x2_img_norm*W_pdf, (1-y2_img_norm)*H_pdf
    return [x1, y1, x2, y2]

def load_model(custom=False):
    if not custom:
        # load model
        model = YOLO('keremberke/yolov8m-table-extraction')

        # set model parameters
        model.overrides['conf'] = 0.25  # NMS confidence threshold
        model.overrides['iou'] = 0.45  # NMS IoU threshold
        model.overrides['agnostic_nms'] = False  # NMS class-agnostic
        model.overrides['max_det'] = 1000  # maximum number of detections per image
    else:
        print('Custom model code not setup. please exit and try again')
        sys.exit(2)
    return model

def extract_tables(pdf_file, pg, model):
    pdf_page=norm_pdf_page(pdf_file, pg)
    img = pdf_page2img(pdf_file, pg, save_image=True)    
    height, width = Image.fromarray(img).height, Image.fromarray(img).width
    # perform inference
    results = model.predict(img)
    # Check whether the specified path exists or not
    new_path = os.path.join(pdf_file.strip(".pdf"), 'Annotated_images')
    isExist = os.path.exists(new_path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(new_path)
        print(f"The new directory {new_path} is created!")
    img_path=os.path.join(new_path, f"Annotated_Page_{pg}.png")
    render_img = render_result(model=model, image=img, result=results[0])
    render_img.save(img_path)        
    probable_table_areas=[]
    output = results[0].boxes.cpu().data.numpy()
    for x in output:
        x1, y1, x2, y2, _, _ = tuple(int(item) for item in x)
        print(x1, y1, x2, y2, _, _)
        # cropping
        # cropped_image = img[y1:y2, x1:x2]
        # cropped_image = Image.fromarray(cropped_image)
        # [x1, y1, x2, y2]=bboxes_pdf(img, pdf_page, x)
        x = x1, y1, x2, y2, _, _
        [X1, Y1, X2, Y2]=bboxes_pdf(img, pdf_page, x)
        bbox_camelot = ",".join([str(X1), str(Y1), str(X2), str(Y2)])   # x1,y1,x2,y2 where (x1, y1) -> left-top and (x2, y2) -> right-bottom in PDF coordinate space
        print(bbox_camelot)
        probable_table_areas.append(bbox_camelot)
    output_camelot = camelot.read_pdf(
    filepath=pdf_file, pages=str(pg), flavor="stream",table_areas=probable_table_areas)
    output_camelot=[x.df for x in output_camelot]
    output_dir = os.path.join(pdf_file.strip(".pdf"), 'Output_tables')
    isExist = os.path.exists(output_dir)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(output_dir)
        print(f"The new directory {output_dir} is created!")    
    for i,db in enumerate(output_camelot):
        output_path = os.path.join(output_dir, f"Page-{pg}-table-{i}.xlsx")
        print(f"Page {pg} Found tables {i} of shape {db.shape} stored at {output_path}")
        db.to_excel(output_path)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__) or '.'))
    current_wd = os.getcwd()
    pdf_file = os.path.join(current_wd,'4Q19-Press-Release.pdf')
    pg = 2
    model = load_model(custom=False)
    extract_tables(pdf_file, pg, model)
    
    
