from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .engine import run_capture  # tu interpreteDos.py renombrado

@csrf_exempt
def run_code_ajax(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            code = data.get("code", "")
            output = run_capture.run_source_capture(code)
            return JsonResponse({"output": output})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    return JsonResponse({"error": "Método no permitido"})

from django.shortcuts import render

def index(request):
    return render(request, "interpreter_app/run_code.html")  # asegúrate de guardar tu HTML aquí
