import urllib.request, json

url = 'http://127.0.0.1:8000/food-env/predict/'
data = {
    "soda_price": 100.0,
    "fmrktpth16": 1.2,
    "grocpth09": 2.3,
    "pch_grocpth_09_14": 0.1,
    "fsrpth09": 3.4,
    "fsrpth14": 3.5,
    "pct_65older10": 15.0,
    "poploss10": -0.5
}
req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type':'application/json'})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        print('HTTP', resp.status)
        body = resp.read().decode('utf-8')
        print('BODY:', body)
except Exception as e:
    print('ERROR', repr(e))
