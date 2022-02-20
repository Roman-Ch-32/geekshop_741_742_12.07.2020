from basketapp.models import Basket


def basket(request):
    print('корзинка')
    baskets = []

    if request.user.is_authenticated:
        baskets = Basket.objects.filter(user=request.user)
    return {
        'baskets': baskets,
    }
