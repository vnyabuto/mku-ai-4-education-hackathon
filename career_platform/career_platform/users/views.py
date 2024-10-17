from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import pickle
import requests
from django.http import JsonResponse

# Load the career recommendation model
try:
    with open(r'C:\Users\User\Desktop\career_platform\career_platform\users\career_recommendation_model.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    model = None

def home(request):
    return render(request, 'users/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def dashboard(request):
    recommendations = [
        {"name": "Electrical Engineer", "description": "Design and develop electrical systems."},
        {"name": "Journalist, Author", "description": "Research and report on news events, write articles, and create content for print and digital media."},
        {"name": "Agribusiness, Sales", "description": "Manage and promote agricultural products, services, and technologies to increase sales and efficiency in the agriculture sector."},
        {"name": "Software Engineer", "description": "Develop and maintain software applications."},
        {"name": "Data Scientist", "description": "Analyze and interpret complex data."},
        {"name": "Web Developer", "description": "Create and maintain websites."},
        {"name": "Database Administrator", "description": "Manage and maintain database systems."},
        {"name": "Network Engineer", "description": "Design and maintain computer networks."},
        {"name": "Cybersecurity Analyst", "description": "Protect systems from cyber threats."},
        {"name": "Machine Learning Engineer", "description": "Build and deploy machine learning models."},
        {"name": "Artificial Intelligence Specialist", "description": "Develop AI technologies."},
        {"name": "Cloud Solutions Architect", "description": "Design cloud-based solutions."},
        {"name": "Data Analyst", "description": "Interpret data and generate insights."},
        {"name": "Business Analyst", "description": "Analyze business needs and solutions."},
        {"name": "Game Developer", "description": "Design and develop video games."},
        {"name": "DevOps Engineer", "description": "Integrate development and operations."},
        {"name": "Quality Assurance Tester", "description": "Ensure software quality and performance."},
        {"name": "IT Support Specialist", "description": "Provide technical support to users."},
        {"name": "Digital Marketing Specialist", "description": "Manage online marketing campaigns."},
        {"name": "SEO Specialist", "description": "Optimize websites for search engines."},
        {"name": "Content Writer", "description": "Create engaging content for various platforms."},
        {"name": "Social Media Manager", "description": "Manage social media accounts and strategy."},
        {"name": "Graphic Designer", "description": "Create visual content using design software."},
        {"name": "Sales Manager", "description": "Lead and manage sales teams."},
        {"name": "Marketing Manager", "description": "Develop marketing strategies and campaigns."},
        {"name": "Financial Analyst", "description": "Analyze financial data and trends."},
        {"name": "Accountant", "description": "Prepare and analyze financial statements."},
        {"name": "Human Resources Manager", "description": "Manage HR functions and employee relations."},
        {"name": "Project Manager", "description": "Oversee and manage projects from inception to completion."},
        {"name": "Operations Manager", "description": "Manage daily operations and processes."},
        {"name": "Research Scientist", "description": "Conduct research in various scientific fields."},
        {"name": "Biotechnology Engineer", "description": "Work with biological systems and organisms."},
        {"name": "Environmental Consultant", "description": "Provide advice on environmental practices."},
        {"name": "Civil Engineer", "description": "Design and supervise construction projects."},
        {"name": "Mechanical Engineer", "description": "Design and develop mechanical systems."},
        {"name": "Chemical Engineer", "description": "Apply chemistry and engineering principles to produce chemicals."},
        {"name": "Pharmacist", "description": "Dispense medications and provide pharmaceutical care."},
        {"name": "Nurse", "description": "Provide patient care and support."},
        {"name": "Medical Doctor", "description": "Diagnose and treat patients."},
        {"name": "Dentist", "description": "Provide dental care and treatments."},
        {"name": "Psychologist", "description": "Study and treat mental health issues."},
        {"name": "Physical Therapist", "description": "Help patients improve movement and manage pain."},
        {"name": "Veterinarian", "description": "Provide medical care for animals."},
        {"name": "Social Worker", "description": "Support individuals and communities."},
        {"name": "Teacher", "description": "Educate students in various subjects."},
        {"name": "Education Consultant", "description": "Advise on educational practices and policies."},
        {"name": "Librarian", "description": "Manage library resources and assist users."},
        {"name": "Non-Profit Manager", "description": "Oversee non-profit organizations."},
        {"name": "Event Planner", "description": "Organize and manage events."},
        {"name": "Real Estate Agent", "description": "Assist clients in buying and selling properties."},
        {"name": "Interior Designer", "description": "Design and enhance interior spaces."},
        {"name": "Fashion Designer", "description": "Create clothing and accessories."},
        {"name": "Culinary Artist", "description": "Prepare and present food creatively."},
        {"name": "Chef", "description": "Oversee kitchen operations and meal preparation."},
        {"name": "Film Producer", "description": "Manage the production of films."},
        {"name": "Photographer", "description": "Capture images for various purposes."},
        {"name": "Musician", "description": "Create and perform music."},
        {"name": "Actor", "description": "Perform in films, theater, or television."},
        {"name": "Writer", "description": "Create written content across various mediums."},
        {"name": "Journalist", "description": "Report on news and current events."},
        {"name": "Translator", "description": "Convert written text from one language to another."},
        {"name": "Air Traffic Controller", "description": "Manage air traffic and ensure safety."},
        {"name": "Pilot", "description": "Fly aircraft and ensure safe travel."},
        {"name": "Logistics Coordinator", "description": "Manage supply chain and logistics operations."},
        {"name": "Supply Chain Manager", "description": "Oversee supply chain processes."},
        {"name": "Insurance Agent", "description": "Sell and manage insurance policies."},
        {"name": "Market Research Analyst", "description": "Analyze market trends and consumer behavior."},
        {"name": "Stockbroker", "description": "Buy and sell stocks for clients."},
        {"name": "Investment Banker", "description": "Provide financial and advisory services."},
        {"name": "Financial Planner", "description": "Help clients manage their finances."},
        {"name": "Credit Analyst", "description": "Evaluate credit data and financial statements."},
        {"name": "Actuary", "description": "Analyze financial risk using mathematics and statistics."},
        {"name": "Tax Consultant", "description": "Advise clients on tax strategies."},
        {"name": "Public Relations Specialist", "description": "Manage communication between organizations and the public."},
        {"name": "Lobbyist", "description": "Influence legislation and policy."},
        {"name": "Urban Planner", "description": "Design and develop urban areas."},
        {"name": "Cartographer", "description": "Create maps and visual representations of geographic areas."},
        {"name": "Geologist", "description": "Study the Earth's structure and materials."},
        {"name": "Wildlife Biologist", "description": "Study and protect wildlife."},
        {"name": "Meteorologist", "description": "Study weather patterns and phenomena."},
        {"name": "Astronomer", "description": "Study celestial bodies and the universe."},
        {"name": "Philosopher", "description": "Explore fundamental questions about existence."},
        {"name": "Historian", "description": "Study and interpret historical events."},
        {"name": "Anthropologist", "description": "Study human behavior and societies."},
        {"name": "Archaeologist", "description": "Excavate and study historical artifacts."},
        {"name": "Sociologist", "description": "Study social behavior and society."},
        {"name": "Political Scientist", "description": "Analyze political systems and behavior."},
        {"name": "Economist", "description": "Study production and distribution of resources."},
        {"name": "Statistician", "description": "Analyze data to extract insights."},
        {"name": "Operations Research Analyst", "description": "Use analytical methods to help organizations solve problems and make better decisions."}
    ]
    return render(request, 'users/dashboard.html', {'recommendations': recommendations})


def chat_api(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        response = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"sender": "user", "message": user_message})
        bot_response = response.json()
        return JsonResponse(bot_response, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

class CareerAssessmentView(View):
    def get(self, request):
        return render(request, 'users/career_assessment.html')

    def post(self, request):
        context = {'results': []}
        return render(request, 'users/career_assessment_results.html', context)

class RecommendationsView(View):
    def get(self, request):
        return render(request, 'users/recommendations.html', {'recommendations': None})

    def post(self, request):
        # Extract user inputs from the form
        student_id = request.POST.get('student_id')
        full_name = request.POST.get('full_name')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        primary_school = request.POST.get('primary_school')
        kcpe_score = request.POST.get('kcpe_score')
        high_school = request.POST.get('high_school')
        kcse_grade = request.POST.get('kcse_grade')
        subjects_taken = request.POST.get('subjects_taken')
        strengths = request.POST.get('strengths')
        extracurricular = request.POST.get('extracurricular')
        hobbies = request.POST.get('hobbies')
        volunteer_work = request.POST.get('volunteer_work')
        career_aspirations = request.POST.get('career_aspirations')
        guardian_occupation = request.POST.get('guardian_occupation')
        personality_type = request.POST.get('personality_type')
        performance_stem = request.POST.get('performance_stem')
        performance_arts = request.POST.get('performance_arts')
        preferred_study_mode = request.POST.get('preferred_study_mode')
        learning_disabilities = request.POST.get('learning_disabilities')

        try:
            # Sample logic: create recommendations based on the inputs (Replace with actual model usage logic)
            recommendations = [
                f"Based on your KCSE grade {kcse_grade}, a career in {career_aspirations} suits you well.",
                f"Since you excel in {strengths}, consider pursuing fields related to these subjects.",
                f"With your interest in {hobbies}, extracurricular activities like {extracurricular} will complement your career growth.",
                f"Having a guardian as a {guardian_occupation} might give you insights into career paths related to their field.",
                f"Your preference for {preferred_study_mode} study mode aligns with practical or theoretical fields."
            ]

            context = {
                'recommendations': recommendations,
                'student_id': student_id,
                'full_name': full_name,
                'gender': gender,
                'age': age,
                'primary_school': primary_school,
                'kcpe_score': kcpe_score,
                'high_school': high_school,
                'kcse_grade': kcse_grade,
                'subjects_taken': subjects_taken,
                'strengths': strengths,
                'extracurricular': extracurricular,
                'hobbies': hobbies,
                'volunteer_work': volunteer_work,
                'career_aspirations': career_aspirations,
                'guardian_occupation': guardian_occupation,
                'personality_type': personality_type,
                'performance_stem': performance_stem,
                'performance_arts': performance_arts,
                'preferred_study_mode': preferred_study_mode,
                'learning_disabilities': learning_disabilities,
            }

            return render(request, 'users/recommendations.html', context)

        except Exception as e:
            return render(request, 'users/recommendations.html', {'error': f"Error: {str(e)}"})

def chatbot_view(request):
    if request.method == "POST":
        user_input = request.POST.get('message')
        response = {"response": f"Bot response to '{user_input}'"}  # Replace with actual logic
        return JsonResponse(response)
    return render(request, 'chatbot/chat.html')
