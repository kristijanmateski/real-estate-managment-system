from django.shortcuts import render, redirect

from app.forms import RealStateForm
from app.models import RealState, CharacteristicRealEstate


# Create your views here.

def index(request):
    houses = RealState.objects.filter(sold=False, area__gt=100).all()
    real_estate_context = []
    for house in houses:
        price = 0
        house_characteristics = CharacteristicRealEstate.objects.filter(real_state=house)
        for house_characteristic in house_characteristics:
            price += house_characteristic.characteristic.value
        real_estate_context.append({'house': house, 'price': price})

    return render(request, 'index.html', {'houses': real_estate_context})


def edit(request, real_id):
    house = RealState.objects.filter(id=real_id).first()
    if request.method == 'POST':
        form = RealStateForm(request.POST, instance=house, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = RealStateForm(instance=house)
    return render(request, 'edit.html', {'form': form, 'house': house})
