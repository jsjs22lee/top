import requests
import json

WORKER_NODES = [
    "http://211.183.4.128:5000/metrics",
    "http://211.183.4.129:5000/metrics",
    "http://211.183.4.130:5000/metrics",
    "http://211.183.4.131:5000/metrics",
    "http://211.183.4.132:5000/metrics",
    "http://211.183.4.133:5000/metrics"
]

def get_best_node():
    results = []
    for url in WORKER_NODES:
        try:
            res = requests.get(url, timeout=1)
            data = res.json()
            results.append((url.split('//')[1].split(':')[0], data["cpu"]))
        except Exception as e:
            print(f"[ERROR] {url} 호출 실패: {e}")
    if not results:
        return "localhost"
    return min(results, key=lambda x: x[1])[0]

def generate_dynamic_config():
    best_node = get_best_node()
    return f"""
http:
  routers:
    dynamic-router:
      rule: \"Host(`whoami.local`)\"
      service: dynamic-service
  services:
    dynamic-service:
      loadBalancer:
        servers:
          - url: \"http://{best_node}:9100\"
"""
