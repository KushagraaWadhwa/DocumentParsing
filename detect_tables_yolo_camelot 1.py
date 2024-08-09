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
import pdfplumber
from operator import itemgetter
from ultralyticsplus import YOLO, render_result
import json

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


def check_bboxes(word, table_bbox):
    """
    Check whether word is inside a table bbox.
    """
    l = word['x0'], word['top'], word['x1'], word['bottom']
    r = table_bbox
    return l[0] > r[0] and l[1] > r[1] and l[2] < r[2] and l[3] < r[3]        
        
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

def detect_tables(pdf_file, pg, model):
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
    return probable_table_areas


def extract_tables(pdf_file, pg, probable_table_areas):
    table_bboxes = [i.split(',') for i in probable_table_areas]
    table_bboxes_dict = {}
    for i, j in enumerate(probable_table_areas):
        table_bboxes_dict[j] = j.split(',')
    tables_df_dict = {}
    for i,j in enumerate(probable_table_areas):
        tables_df_dict[j] = camelot.read_pdf(
            filepath=pdf_file, pages=str(pg), flavor="stream",table_areas=[j])[0].df.to_json()
    tables = [{'table': tables_df_dict[i], 'top': float(table_bboxes_dict[i][1]), 'bbox': table_bboxes_dict[i]} for i in probable_table_areas]
    # Extracting tables
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
    return tables


def extract_text_with_tables(pdf_file, pg, tables):
    with pdfplumber.open(pdf_file) as pdf:
        page = pdf.pages[pg-1]
        #t = page.extract_text()
        height, width = page.height, page.width  
        # When using camelot bbox 
        ##table_bboxes = [i['bbox'] for i in tables]
        table_bboxes = [i.bbox for i in page.find_tables()]
        #tables = [{'table': i.extract(), 'top': height - i.bbox[1]} for i in tables]
        print('Before', tables[0])
        for i, j in enumerate(tables):
            tables[i]['top'] = height - tables[i]['top']
        print('After',tables[0])
        all_words = [word for word in page.extract_words()]
        # #adjust height of top 
        # all_words_adj = [word for word in page.extract_words()]
        # for i, word in enumerate(all_words_adj):
        #     all_words_adj[i]['top'] = height - all_words_adj[i]['top'] 
        non_table_words = [word for word in all_words if not any(
            [check_bboxes(word, table_bbox) for table_bbox in table_bboxes])]
        lines = []
        for cluster in pdfplumber.utils.cluster_objects(
                non_table_words + tables, itemgetter('top'), tolerance=5):
            if 'text' in cluster[0]:
                lines.append(' '.join([i['text'] for i in cluster]))
            elif 'table' in cluster[0]:
                lines.append(cluster[0]['table'])
    output_dir = os.path.join(pdf_file.strip(".pdf"), 'Output_text')
    isExist = os.path.exists(output_dir)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(output_dir)
        print(f"The new directory {output_dir} is created!") 
    output_path = os.path.join(output_dir, f"Page-{pg}.json")
    with open(output_path, 'w') as output:
        json.dump(lines, output, indent=4)        
        

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__) or '.'))
    current_wd = os.getcwd()
    pdf_file = os.path.join(current_wd,'4Q19-Press-Release.pdf')
    #pdf_file = os.path.join(current_wd, 'handbook.pdf')
    pdf_doc = PdfReader(open(pdf_file, "rb"))
    total_pages = len(pdf_doc.pages)
    print(f"Pdf pages {total_pages}")
    model = load_model(custom=False)
    #for pg in range(total_pages):
    pg = 2
    print(f"Processing page {pg}")
    probable_table_areas = detect_tables(pdf_file, pg, model)
    tables = extract_tables(pdf_file, pg, probable_table_areas)
    extract_text_with_tables(pdf_file, pg, tables)
        
    
    
