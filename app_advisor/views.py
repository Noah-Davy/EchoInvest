from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import (
    calculate_risk_score,
    determine_risk_tolerance,
    recommend_portfolio,
    allocate_portfolio,
    get_previous_trading_day,
    calculate_portfolio_performance
)

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class AllocatePortfolioView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        try:
            user_responses = request.data.get('user_responses')
            initial_investment = float(request.data.get('initial_investment'))

            # Log the received data for debugging
            print("User Responses:", user_responses)
            print("Initial Investment:", initial_investment)

            # Backend logic moved to utils
            risk_score = calculate_risk_score(user_responses)
            risk_tolerance = determine_risk_tolerance(risk_score)
            recommended_portfolio = recommend_portfolio(risk_tolerance)
            allocated_portfolio = allocate_portfolio(recommended_portfolio, initial_investment)
            end_date = get_previous_trading_day()
            portfolio_performance = calculate_portfolio_performance(allocated_portfolio, initial_investment, end_date)

            return Response({
                'risk_score': risk_score,
                'risk_tolerance': risk_tolerance,
                'recommended_portfolio': recommended_portfolio,
                'allocated_portfolio': allocated_portfolio,
                'portfolio_performance': portfolio_performance
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error in AllocatePortfolioView: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)