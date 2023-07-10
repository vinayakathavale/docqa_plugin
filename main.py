import json
import urllib
import quart
import quart_cors
from quart import request

from src.utils.utils import load_pdf, find_closest, process_doc
from src.run_indexer import make_index_from_docs, query_index_citation


app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")
index = make_index_from_docs()

curr_doc_text = None

@app.post("/docqa/<string:username>")
async def docqa_initdoc(username):
    request = await quart.request.get_json(force=True)

    if 'url' in request:
        try:
            # urllib.request.urlretrieve('https://assets.directline.com/motor-docs/policy-booklet-1122.pdf', 'test.pdf')
            urllib.request.urlretrieve(request['url'], '/tmp/test.pdf')
            curr_doc_text = load_pdf('/tmp/test.pdf')
            print(curr_doc_text, 'aaaa')
        except Exception as e:
            return quart.Response(response='Error in downloading url, please check the link and make sure it is a valid pdf', status=500)
        
        df = process_doc(curr_doc_text)
        closest_pages = find_closest(df, query=request['query'])
        return quart.Response(response=" ".join(closest_pages['page_text']), status=200)

    else:
        resp = query_index_citation(index, request['query'])
        print(resp)
        return quart.Response(response=json.dumps(resp), status=200)
        
    

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
