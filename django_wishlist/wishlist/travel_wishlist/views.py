from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

# Create your views here.
# Make login a requirement for this view
@login_required
def place_list(request):

    if request.method == 'POST':
        form = NewPlaceForm(request.POST)
        # Create a new Place from the form, but don't save it yet
        place = form.save(commit=False)
        # Only the signed in user's places should be displayed
        # Associate the place with the user so that when a new place is added it has a user assigned to it
        place.user = request.user
        if form.is_valid():
            place.save()
            return redirect('place_list')

    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})


@login_required
def places_visited(request):
    visited = Place.objects.filter(user=request.user).filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited })


@login_required
def place_was_visited(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        place = get_object_or_404(Place, pk=pk)
        print(place.user, request.user)
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()

    return redirect('place_list')


@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)

    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        # instance is the model object to update with the form data

        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors)

        return redirect('place_details', place_pk=place_pk)

    else:
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form})

        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})


@login_required
def delete_place(request):
    pk = request.POST.get('pk')
    place = get_object_or_404(Place, pk=pk)
    # The user can only delete items from their wish list
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()