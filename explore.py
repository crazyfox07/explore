from flask import Flask, render_template,jsonify
from flask_restful import Resource, Api

from view.huanqiu_view import blueprint_huanqiu
from view.crawl_spider_two import crawl_huanqiu


def create_app():
    app = Flask(__name__)
    app.register_blueprint(blueprint_huanqiu)#, url_prefix='/explore')
    return app


app = create_app()


@app.route('/hello')
def hello_world():
    # return 'Hello World!'MYSQLS_DB_NAME
    return jsonify({'name':'frank'})


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=8889, debug=True)
    crawl_huanqiu()
