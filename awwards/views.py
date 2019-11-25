from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from .models import Project, Rate, Review
from django.contrib.auth.models import User
from .forms import( UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProjectPostForm, RateForm, ReviewForm)
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form':form})

def index(request):
    return render(request, 'index.html')

@login_required
def home(request):
    try:
        projects = Project.objects.all()
    except Exception as e:
        raise  Http404()
    return render(request, 'home.html', {'projects':projects})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account updated successfully!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form,
    }

    return render(request, 'users/profile.html', context)

@login_required
def post_project(request):
    current_user = request.user
    if request.method=='POST':
        form = ProjectPostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
        return redirect("home")
    else:
        form = ProjectPostForm()
    return render(request,'project_post.html',{'form':form})

@login_required
def project_details(request,project_id):
    projects = Project.objects.filter(id=project_id)
    all_rates = Rate.objects.filter(project=project_id)
  
    count = 0
    for i in all_rates:
        count+=i.usability
        count+=i.design
        count+=i.content

    if count > 0:
        av_rate = round(count/3,1) 
    else:
        av_rate = 0

    if request.method=='POST':
        form = RateForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.project = project_id
            rate.save()
            return redirect('project_details',project_id)
    else:
        form = RateForm()

    votes = Rate.objects.filter(project=project_id)
    usability = []
    design = []
    content = []

    for i in votes:
        usability.append(i.usability)
        design.append(i.design)
        content.append(i.content)
    if len(usability) > 0 or len(design)> 0 or len(content) >0:
        av_usability = round(sum(usability)/len(usability),1)
        av_design = round(sum(design)/len(design),1)
        av_content = round(sum(content)/len(content),1)
        avRating = round((av_content + av_design + av_usability)/3,1)
    else:
        av_usability = 0.0
        av_design = 0.0
        av_content = 0.0
        avRating = 0.0

    '''
    Restricting user to rate only once
    '''
    arr1=[]
    for use in votes:
        arr1.append(use.user_id)
    auth = arr1

    if request.method=='POST':
        r_form = ReviewForm(request.POST)
        if r_form.is_valid():
            review = r_form.save(commit=False)
            review.user = request.user
            review.profile_id = project_id
            review.save()
            return redirect('project_details',project_id)
    else:
        r_form = ReviewForm()
    r_form = ReviewForm()
    user_review = Review.objects.filter(profile_id=project_id)

    context = {
        'projects':projects,
        'form':form,
        'usability':av_usability, 
        'design':av_design,
        'content':av_content,
        'average':avRating,
        'auth':auth,
        'all_rates':all_rates,
        'av_rate':av_rate,
        'r_form':r_form,
        'review':user_review
        }
    return render(request,'project_details.html', context)

@login_required
def search(request):
    if 'search' in request.GET and request.GET['search']:
        search_term = request.GET.get('search')
        results = Project.search_project(search_term)
        return render(request,'search.html',{'projects': results})
    else:
        message="You have not searched any project"
        return render(request,'search.html',{'message': message})

@login_required
def apiView(request):
    user = request.user
    title="Api"
    profile = Profile.objects.filter(user=user)[0:1]
    return render(request,'api.html',{"title":title,'profile':profile})

