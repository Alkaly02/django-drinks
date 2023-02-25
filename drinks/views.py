from django.http import HttpResponse, JsonResponse
from .models import Drink
from .serializers import DrinkSerializer
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(["GET", "POST"])
def drink_list(request):
    if request.method == "GET":
        drinks = Drink.objects.all()
        serialisez_drinks = DrinkSerializer(drinks, many=True)
        return JsonResponse(
            {"drinks": serialisez_drinks.data}, status=status.HTTP_200_OK
        )
    if request.method == "POST":
        serialisez_drinks_post = DrinkSerializer(data=request.data)
        if serialisez_drinks_post.is_valid():
            serialisez_drinks_post.save()
            return JsonResponse(
                {"drink": serialisez_drinks_post.data}, status=status.HTTP_201_CREATED
            )


@api_view(["GET", "PUT", "DELETE"])
def drink_detail(request, id):
    try:
        drink = Drink.objects.get(pk=id)
    except Drink.DoesNotExist:
        return JsonResponse(
            {"failed": True, "message": "Pas de drink correspondant"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serialized_drink = DrinkSerializer(drink)
        return JsonResponse({"drink": serialized_drink.data}, status=status.HTTP_200_OK)
    if request.method == "PUT":
        serialized_drink_put = DrinkSerializer(drink, data=request.data)
        if serialized_drink_put.is_valid():
            serialized_drink_put.save()
            return JsonResponse(
                {"drink": serialized_drink_put.data}, status=status.HTTP_202_ACCEPTED
            )
    if request.method == "DELETE":
        drink.delete()
        return JsonResponse({"success": True, "message": "Drink deletede"})
