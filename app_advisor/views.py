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


class AllocatePortfolioView(APIView):
    def post(self, request):
        user_responses = request.data.get('user_responses')
        initial_investment = float(request.data.get('initial_investment'))

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