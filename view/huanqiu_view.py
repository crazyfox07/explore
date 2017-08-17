# -*- coding:utf-8 -*-
"""
File Name: huanqiu
Version:
Description:
Author: liuxuewen
Date: 2017/8/11 10:58
"""
from flask_restful import Resource
from flask import request, render_template, jsonify, Blueprint
from model.huanqiu_model import db_session, HuanQiuOrm
from sqlalchemy import desc
import re

blueprint_huanqiu = Blueprint('blueprint_huanqiu', __name__)

TOTAL_PAGE = 30
ROWS = 3
COLS = 4


# class HuanQiu(Resource):
#     def get(self):
#         page=int(request.args.get('page','1'))
#         resutls=db_session.query(HuanQiuOrm).order_by(desc(HuanQiuOrm.id)).offset((page-1)*ROWS*COLS).limit(ROWS*COLS).all()
#         infos=[{'id':item.id,'title':item.title,'link':item.link,'brief':item.brief,'create_time':item.create_time} for item in resutls]
#         #return jsonify({'name':infos})
#         html='''<html><title>home page</title><body>hello</body></html>'''
#         return render_template('test.html')#,resutls=infos,current_page=5
# return html

def func(item):
    if item.img_url:
        return {'id': item.id, 'title': item.title, 'link': item.link, 'brief': item.brief,
                'create_time': item.create_time, 'img_name': re.findall('imgs/(.*png)', item.img_url)}
    else:
        return {'id': item.id, 'title': item.title, 'link': item.link, 'brief': item.brief,
                'create_time': item.create_time, 'img_name': ''}


@blueprint_huanqiu.route('/', methods=['GET'])
def huanqiu():
    page = int(request.args.get('page', '1'))
    resutls = db_session.query(HuanQiuOrm).order_by(desc(HuanQiuOrm.create_time)).offset(
        (page - 1) * ROWS * COLS).limit(
        ROWS * COLS).all()
    infos = list()
    for item in resutls:
        if item.img_url:
            infos.append(
                {'id': item.id, 'title': item.title, 'link': item.link, 'brief': item.brief.replace('[详细]', ''),
                 'create_time': item.create_time, 'img_name': re.findall('imgs/(.*png)', item.img_url)[0]})
        else:
            infos.append(
                {'id': item.id, 'title': item.title, 'link': item.link, 'brief': item.brief.replace('[详细]', ''),
                 'create_time': item.create_time, 'img_name': ''})
    print(infos)
    if page > TOTAL_PAGE:
        page = TOTAL_PAGE
    return render_template('home.html', resutls=infos, rows=ROWS, cols=COLS, current_page=page, total_page=TOTAL_PAGE)
