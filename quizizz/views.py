from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import logging
from bs4 import BeautifulSoup
from .models import ClassCode, Question 
logger = logging.getLogger(__name__)
from .models import ClassCode, Quiz  

def home(request):
    return render(request, 'app/index.html')

def check_student_and_join_code(request):
    student_code = request.GET.get('student_code', '')
    join_code = request.GET.get('join_code', '')

    if not student_code or not join_code:
        return HttpResponse("Missing student code or join code", status=400)

    if not ClassCode.objects.filter(join_code=join_code).exists():
        return HttpResponse("Invalid join code", status=404)

    options = Options()
    options.headless = True
    service = Service(r"C:\Users\trong\Documents\chromedriver.exe")
    driver = webdriver.Chrome(options=options, service=service)

    try:
        driver.get('https://qldt.ptit.edu.vn/#/home')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username'))).send_keys('B20DCCN242')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys('hieucn01')

        # Scroll to the button and wait until it is clickable
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'button')))
        ActionChains(driver).move_to_element(button).click().perform()

        # Wait for the page to load and get the response
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        body_text = driver.find_element(By.TAG_NAME, 'body').text

        # Parse the response as JSON
        response_data = json.loads(body_text)
        if response_data.get('code') == '200':
            request.session['student_code'] = student_code  # Store student code in session if needed
            return redirect('/pre_game/')  # Correct redirect path
        else:
            return HttpResponse("Invalid student code", status=404)
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return HttpResponse(f"Error processing request: {str(e)}", status=500)
    finally:
        driver.quit()

def pre_game(request):
    return render(request, 'app/pre_game.html')

def countdown(request):
    name = request.GET.get('name', 'Guest')
    request.session['name'] = name
    return render(request, 'app/countdown.html', {'name': name})
def quiz(request):
    name = request.session.get('name', 'Guest')
    questions = Question.objects.all()
    questions_data = []

    for question in questions:
        answers = question.answers.all()
        questions_data.append({
            'text': question.text,
            'answers': [{'text': answer.text, 'is_correct': answer.is_correct} for answer in answers]
        })

    context = {
        'name': name,
        'questions': json.dumps(questions_data)
    }
    return render(request, 'app/quiz.html', context)