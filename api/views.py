import google.generativeai as genai
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

def chat(request):
    if request.method == 'GET':
        user_message = request.GET.get("message", "")
    elif request.method == 'POST':
        user_message = request.POST.get("message", "")
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    
    if not user_message:
        return JsonResponse({"error": "No message provided"}, status=400)
    
    if not settings.GEMINI_API_KEY:
        return JsonResponse({"error": "API key not configured"}, status=500)
    
    try:
        # Use the latest available model
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Generate response
        response = model.generate_content(user_message)
        
        ai_message = response.text.strip()
        
        return JsonResponse({"response": ai_message})
        
    except Exception as e:
        error_message = str(e)
        
        if "quota" in error_message.lower():
            return JsonResponse({
                "error": "API quota exceeded. Please try again later."
            }, status=429)
        elif "api_key" in error_message.lower() or "authentication" in error_message.lower():
            return JsonResponse({
                "error": "Authentication error. Please check your API key."
            }, status=401)
        else:
            return JsonResponse({
                "error": f"An error occurred: {error_message}"
            }, status=500)

def index(request):
    return render(request, 'api/index.html')