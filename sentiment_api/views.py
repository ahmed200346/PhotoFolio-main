import os
import pandas as pd
from django.shortcuts import render
from transformers import pipeline
from django.http import JsonResponse

# Charger le modèle de sentiment
sentiment_analyzer = pipeline('sentiment-analysis')

# Analyse d'un commentaire
def analyze_comment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        if comment:
            result = sentiment_analyzer(comment)[0]
            return JsonResponse({'label': result['label'], 'score': result['score']})
    return render(request, 'sentiment_api/analyze_comment.html')

# Analyse d'un fichier
def analyze_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_extension = os.path.splitext(uploaded_file.name)[-1]
        
        if file_extension not in ['.json', '.csv']:
            return JsonResponse({'error': 'Unsupported file format. Please upload JSON or CSV.'})
        
        if file_extension == '.json':
            data = pd.read_json(uploaded_file)
        else:
            data = pd.read_csv(uploaded_file)
        
        # Vérifier la colonne des commentaires
        if 'comment' not in data.columns:
            return JsonResponse({'error': 'File must contain a "comment" column.'})
        
        sentiments = data['comment'].apply(lambda x: sentiment_analyzer(x)[0]['label'])
        counts = sentiments.value_counts().to_dict()
        
        return JsonResponse({'counts': counts})
    return render(request, 'sentiment_api/analyze_file.html')
