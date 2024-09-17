from .models import Business, Category, Investor


def all_categories(request):
    return {'all_categories': Category.objects.all()}


def user_type(request):
    user_is_investor = False
    user_is_business = False

    if request.user.is_authenticated:
        if Investor.objects.filter(id=request.user.id).exists():
            user_is_investor = True
        elif Business.objects.filter(id=request.user.id).exists():
            user_is_business = True

    return {
        'user_is_investor': user_is_investor,
        'user_is_business': user_is_business,
    }