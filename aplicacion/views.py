from pathlib import Path
from django.shortcuts import render
from django.http import HttpRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import joblib
 

# Create your views here.
#la vista procesa
@csrf_exempt
def prediccionView(request):
    return render(request, 'transaccionesAA.html')


#@csrf_protect
@csrf_exempt
def hacerPrediccion(request):


    if( request.method == 'POST' ): 
 
        #cargar modelo
        ruta= str(Path(__file__, '../', './modelosAA/model_fraudulent_transactions_tree.joblib').resolve())
        print("ruta: ",ruta)

        try:
            model = joblib.load( ruta )
        except Exception as err:
            print("Error", err)
        
        #Cagar Body
        body = json.loads(request.body)
        print(body)
        
        #hacer predicción
        rs = model.predict([ 
            [
                body['distance_from_home'],
                body['distance_from_last_transaction'],
                body['ratio_to_median_purchase_price'],
                body['repeat_retailer'],
                body['used_chip'],
                body['used_pin_number'],
                body['online_order']
            ] 
        ])
        print(f"resultado de la predicción: {rs}")
         
        data = {
            'prediccion': rs[0],
            'values': body 
        }  

        resp = JsonResponse(data, status=200)
        return resp
    else:  
        return JsonResponse({ 'msg': 'No pudo realizar la predicción' }, status=400)
# Create your views here.
