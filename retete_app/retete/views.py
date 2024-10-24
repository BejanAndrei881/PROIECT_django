from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RecipientForm, CreateUser
from .models import Recipient, SavedRecipient, Categorie
from django.contrib.auth.decorators import login_required


def home_page(request):
    search_query = request.GET.get('search', '')
    recipes = Recipient.objects.filter(title__icontains=search_query, is_private=False)
    context = {
        'recipes': recipes,
        'search_query': search_query,
    }
    return render(request, 'retete.html', context)


def vizualizare_retete(request):
    categorii = Categorie.objects.all()
    selected_category = request.GET.get('categorie') 
    if selected_category:
        recipes = Recipient.objects.filter(is_private=False,
            categorie__id=selected_category)
    else:
        recipes = Recipient.objects.filter(is_private=False)

    if request.user.is_authenticated:
        saved_recipes = SavedRecipient.objects.filter(user=request.user).values_list('recipe_id', flat=True)
    else:
        saved_recipes = []

    context = {
        'recipes': recipes,
        'saved_recipes': saved_recipes,
        'categorii': categorii,
        'selected_category': selected_category,
    }
    return render(request, 'vizualizare.html', context)


def list_recipes(request):
    recipes = Recipient.objects.all()
    return render(request, 'lista_retete.html', {'recipes': recipes})


@login_required
def adauga_reteta(request):
    if request.method == "POST":
        form = RecipientForm(request.POST, request.FILES)
        if form.is_valid():
            reteta = form.save(commit=False)
            reteta.user = request.user

            if request.POST.get('action') == 'salveaza_privata':
                reteta.is_private = True
            else:
                reteta.is_private = False

            reteta.save()
            return redirect('vizualizare_retete')
    else:
        form = RecipientForm()

    return render(request, 'add.html', {'form': form})


def salveaza_reteta(request, recipe_id):
    if request.method == "POST" and request.user.is_authenticated:
        recipe = get_object_or_404(Recipient, id=recipe_id)

        if not SavedRecipient.objects.filter(user=request.user, recipe=recipe).exists():
            SavedRecipient.objects.create(user=request.user, recipe=recipe)

        return redirect('reteta_salvata')
    return redirect('home')


def retete_salvate(request):
    if request.user.is_authenticated:
        saved_recipes = SavedRecipient.objects.filter(user=request.user)
        categorii = Categorie.objects.all()
        selected_category = request.GET.get('categorie', None)
        if selected_category:
            saved_recipes = saved_recipes.filter(recipe__categorie_id=selected_category)
    else:
        saved_recipes = []
        categorii = []
        selected_category = None

    context = {
        'saved_recipes': saved_recipes,
        'categorii': categorii,
        'selected_category': selected_category,
    }

    return render(request, 'saved.html', context)


@login_required
def sterge_reteta(request, saved_recipe_id):
    saved_recipe = get_object_or_404(SavedRecipient, id=saved_recipe_id, user=request.user)
    saved_recipe.delete()
    return redirect('reteta_salvata')


def sterge_reteta_privata(request, id):
    recipe = get_object_or_404(Recipient, id=id, user=request.user, is_private=True)
    recipe.delete()
    return redirect('retetele_mele')

# def retetele_mele(request):
#     if request.user.is_authenticated:
#         private_recipes = Recipient.objects.filter(user=request.user, is_private=True)
#
#         categorii = Categorie.objects.all()
#         selected_category = request.GET.get('categorie', None)
#         if selected_category:
#             private_recipes = private_recipes.filter(categorie_id=selected_category)
#
#         context = {
#             'private_recipes': private_recipes,
#             'categorii': categorii,
#             'selected_category': selected_category,
#         }
#         return render(request, 'retetele_mele.html', context)
#     else:
#         return redirect('login')
#


def retetele_salvate_si_mele(request):
    if request.user.is_authenticated:

        saved_recipes = SavedRecipient.objects.filter(user=request.user)

        private_recipes = Recipient.objects.filter(user=request.user, is_private=True)
        categorii = Categorie.objects.all()
        selected_category = request.GET.get('categorie', None)
        if selected_category:
            saved_recipes = saved_recipes.filter(recipe__categorie_id=selected_category)
            private_recipes = private_recipes.filter(categorie_id=selected_category)

        context = {
            'saved_recipes': saved_recipes,
            'private_recipes': private_recipes,
            'categorii': categorii,
            'selected_category': selected_category,
        }
        return render(request, 'retetele_mele.html', context)
    else:

        return redirect('login')


def detalii_reteta(request, pk):
    reteta = get_object_or_404(Recipient, pk=pk)
    return render(request, 'detali_reteta.html', {'reteta': reteta})


def edita_reteta(request, recipe_id):
    recipe = get_object_or_404(Recipient, id=recipe_id)

    if request.method == "POST":
        form = RecipientForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('retetele_mele')
    else:
        form = RecipientForm(instance=recipe)

    context = {
        'form': form,
        'recipe': recipe,
    }
    return render(request, 'edita_reteta.html', context)


def register(request):
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CreateUser()
    return render(request, 'registration/register.html', {'form': form})
