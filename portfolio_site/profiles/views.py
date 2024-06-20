from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, Group


from .models import *
from .forms import *
from .decorators import loggeduser

#__________________________________________________________PORTFOLIO_VIEWS↓

# @login_required(login_url='login')
def portfolio_view(request,id=None):
    
    if id:
        portfolio = get_object_or_404(Portfolio,id=id)
        profile = get_object_or_404(UserProfile, user=portfolio.user_profile.user)

    else:
        profile = request.user.userprofile 
        portfolio = Portfolio.objects.get(user_profile=profile)
    
    custom_fields = CustomField.objects.filter(portfolio=portfolio)
    projects = Project.objects.filter(portfolio=portfolio)
    certificates = CertificateFiles.objects.filter(portfolio=portfolio)

    context = {
        'portfolio': portfolio,
        'custom_fields': custom_fields,
        'projects': projects,
        'certificates': certificates,
        'profile':profile,
    }
    return render(request, 'Portfolio/portfolio.html', context)



@login_required(login_url='login')
def edit_portfolio_view(request):
    user_profile = request.user.userprofile 
    portfolio = Portfolio.objects.get(user_profile=user_profile)
    custom_fields = CustomField.objects.filter(portfolio=portfolio)

    if request.method == 'POST':
        portfolio_form = PortfolioForm(request.POST, instance=portfolio)
        if portfolio_form.is_valid():
            portfolio = portfolio_form.save(commit=False)
            portfolio.user_profile = user_profile
            portfolio.save()
        else:
            print("Portfolio form errors:", portfolio_form.errors)

        for field in custom_fields:
            field_name_key = f'custom_field_name_{field.id}'
            field_value_key = f'custom_field_value_{field.id}'
            field_image_key = f'custom_field_image_{field.id}'

            field_name = request.POST.get(field_name_key)
            field_value = request.POST.get(field_value_key)
            field_image = request.FILES.get(field_image_key) 


            field.field_name = field_name
            field.field_value = field_value
            if field_image:
                field.field_image = field_image 
            field.save()
        return redirect('portfolio_view')

    else:
        portfolio_form = PortfolioForm(instance=portfolio)

    context = {
        'portfolio_form': portfolio_form,
        'custom_fields': custom_fields,
    }
    return render(request, 'Portfolio/edit_portfolio.html', context)

@login_required(login_url='login')
def add_custom_field(request):
    user_profile = request.user.userprofile 
    
    try:
        portfolio = Portfolio.objects.get(user_profile=user_profile)
    except Portfolio.DoesNotExist:
        portfolio = None

    if request.method == 'POST':
        custom_field_form = CustomFieldForm(request.POST, request.FILES)
        if custom_field_form.is_valid():
            custom_field = custom_field_form.save(commit=False)
            custom_field.portfolio = portfolio
            custom_field.save()
            return redirect('edit_portfolio')  
    else:
        custom_field_form = CustomFieldForm()
    
    context = {
        'custom_field_form': custom_field_form,
    }
    return render(request, 'Portfolio/add_custom_field.html', context)

@login_required(login_url='login')
def delete_custom_field(request, field_id):
    try:
        custom_field = CustomField.objects.get(id=field_id)
        portfolio = custom_field.portfolio


        if portfolio.user_profile.user == request.user:
            custom_field.delete()
            messages.success(request, 'Custom field deleted successfully.')
        else:
            messages.error(request, 'You do not have permission to delete this custom field.')

    except CustomField.DoesNotExist:
        messages.error(request, 'Custom field does not exist.')

    return redirect('edit_portfolio')

#__________________________________________________________Certificate_view↓
# @login_required(login_url='login')
def certificate_detail(request, id):
    certificate = get_object_or_404(CertificateFiles, id=id)
    
    context = {
        'certificate': certificate
    }
    return render(request, 'Portfolio/certificate_detail.html', context)


@login_required(login_url='login')
def certificate_add(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    portfolio = get_object_or_404(Portfolio, user_profile=user_profile)
    
    if request.method == 'POST':
        form = CertificateFilesForm(request.POST, request.FILES)
        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.portfolio = portfolio
            certificate.save()
            return redirect('portfolio_view')
        else:
            messages.error(request, 'There was an error with the form.')

    else:
        form = CertificateFilesForm()
    
    context = {
        'form': form
    }
    return render(request, 'Portfolio/certificate_form.html', context)

@login_required(login_url='login')
def certificate_edit(request, id):
    certificate = get_object_or_404(CertificateFiles, id=id, portfolio__user_profile__user=request.user)
    
    if request.method == 'POST':
        form = CertificateFilesForm(request.POST, request.FILES, instance=certificate)
        if form.is_valid():
            form.save()
            return redirect('portfolio_view')
        else:
            messages.error(request, 'There was an error with the form.')

    else:
        form = CertificateFilesForm(instance=certificate)
    
    context = {
        'form': form
    }
    return render(request, 'Portfolio/certificate_form.html', context)

@login_required(login_url='login')
def certificate_delete(request, id):
    certificate = get_object_or_404(CertificateFiles, id=id, portfolio__user_profile__user=request.user)
    
    if request.method == 'POST':
        certificate.delete()
        return redirect('portfolio_view')
    
    context = {
        'certificate': certificate
    }
    return render(request, 'Portfolio/certificate_delete.html', context)
#__________________________________________________________Certificate_view↑

#__________________________________________________________PORTFOLIO_VIEWS↑

#__________________________________________________________PROJECT_VIEWS↓

@login_required(login_url='login')
def add_project(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            portfolio, created = Portfolio.objects.get_or_create(user_profile=user_profile)
            project.portfolio = portfolio
            project.user_profile = user_profile
            project.save()
            return redirect('portfolio_view')
        else:
            messages.error(request, 'There was an error with the form.')

    else:
        form = ProjectForm()

    return render(request, 'Project/add_project.html', {'form': form})

@login_required(login_url='login')
def edit_project(request, project_id):

    project = get_object_or_404(Project, id=project_id, user_profile__user=request.user)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        
        if form.is_valid():
            form.save()
            return redirect('portfolio_view')
        else:
            messages.error(request, 'There was an error with the form.')

    else:
        form = ProjectForm(instance=project)
    return render(request, 'Project/edit_project.html', {'form': form})

@login_required(login_url='login')
def edit_project_image_view(request, id, image_id):
   
    project = get_object_or_404(Project, id=id)
    project_image = get_object_or_404(ProjectImage, id=image_id, project=project)

    if request.method == 'POST':
        form = ProjectImageForm(request.POST, request.FILES, instance=project_image)
        if form.is_valid():
            form.save()
            return redirect('project_detail', id=project.id)
    else:
        form = ProjectImageForm(instance=project_image)
    
    context = {
        'form': form,
        'project': project,
        'image': project_image
    }
    return render(request, 'Project/edit_project_image.html', context)


@login_required(login_url='login')
def delete_project_image_view(request, id, image_id):
   
    project = get_object_or_404(Project, id=id)
    project_image = get_object_or_404(ProjectImage, id=image_id, project=project)

    if request.method == 'POST':
        project_image.delete()
        return redirect('project_detail', id=project.id)
    
    context = {
        'project': project,
        'image': project_image
    }
    return render(request, 'Project/delete_project_image.html', context)

@login_required(login_url='login')
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, user_profile__user=request.user)
   
    if request.method == 'POST':
        project.delete()
        return redirect('portfolio_view')
  
    return render(request, 'Project/delete_project.html', {'project': project})



def project_detail_view(request, id):
    project = get_object_or_404(Project, id=id)
   
    if request.method == 'POST':
        form = ProjectImageForm(request.POST, request.FILES)
        if form.is_valid():
            project_image = form.save(commit=False)
            project_image.project = project
            project_image.save()
            return redirect('project_detail', id=project.id)
    else:
        form = ProjectImageForm()
    context = {
        'project': project,
        'images': project.images.all(),
        'form': form
    }
    return render(request, 'Project/project_detail.html', context)


#__________________________________________________________PROJECT_VIEWS↑

#__________________________________________________________PROFILE_VIEWS↓

@login_required(login_url='login')
def profile_view(request):
    user_profile = request.user.userprofile

    return render(request, 'profiles/profile.html', {'user_profile': user_profile})


@login_required(login_url='login')
def edit_profile(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view') 
        else:
            messages.error(request, 'There was an error with the form.')

    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'profiles/edit_profile.html', {'form': form})

#__________________________________________________________PROFILE_VIEWS↑

#__________________________________________________________USER_ACCOUNTS↓

def Register_user(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='Intern')
            user.groups.add(group)
            name = f"{user.first_name} {user.last_name}"
            email = user.email
            UserProfile.objects.create(user=user, name=name, email=email)

            Portfolio.objects.create(user_profile=user.userprofile, bio='Enter your Bio')

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
   
    return render(request, 'User/register.html', {'form': form})


def loginUser(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('base')
        else:
            messages.info(request, 'Username or password is wrong')
            return redirect('login')

    return render(request, 'User/login.html')


def logoutUser(request):
    logout(request)
    return redirect('base')

#_________________________________________________________USER_ACCOUNTS↑


#__________________________________________________________UNAUTHENTICATED_VIEWS↓
def dash_view(request):
    user_profiles = UserProfile.objects.prefetch_related('portfolio_set').all()
    project_images = ProjectImage.objects.all()
    context = {
        'user_profiles': user_profiles,
        'project_images': project_images
    }
    return render(request, 'dash.html',context)

@loggeduser
def base_view(request):
    context={} 
    return render(request, 'base.html', context)


def project_view(request):
    project_images = ProjectImage.objects.all()
    projects = Project.objects.all()

    context = {
        'project_images': project_images,
        'projects': projects,
        }
    return render(request, 'project.html', context)

def search(request):
    query = request.GET.get('q', '')  
    portfolios = Portfolio.objects.filter(user_profile__name__icontains=query) 
    
    context = {
        'query': query,
        'portfolios': portfolios,
    }
    return render(request, 'search.html', context)

#_______________________________________________________________UNAUTHENTICATED_VIEWS↑