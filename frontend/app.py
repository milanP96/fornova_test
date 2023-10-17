import requests
from flask import Flask, render_template, request

app = Flask(__name__)

api_url = "http://localhost:8000/"

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/browse')
def browse():
    global api_url
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    res = requests.get(f"{api_url}all?page={page}&per_page={per_page}").json()
    print(res['has_more'])

    return render_template(
        'browse.html',
        hotels=res['res'],
        page=page,
        next=f"/browse?page={page+1}",
        prev=f"/browse?page={page-1}",
        has_more=res['has_more']
    )


@app.route('/search')
def search():
    global api_url
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    text = request.args.get('text', "")

    if text:
        res = requests.post(
            f"{api_url}search?page={page}&per_page={per_page}",
            json={
                "text": text
            }
        ).json()
    else:
        res = {"res": [], "prev": "", "next": "", "has_more": False}

    if not res.get('detail'):

        return render_template(
            'search.html',
            hotels=res['res'],
            page=page,
            next=f"/browse?page={page + 1}",
            prev=f"/browse?page={page - 1}",
            has_more=res['has_more'],
            text=text
        )

    else:
        return render_template(
            'bad_search.html'
        )


if __name__ == '__main__':
    app.run()
