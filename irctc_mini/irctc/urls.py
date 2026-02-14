"""
URL Configuration for IRCTC Mini System
"""

from django.urls import path
from irctc.views import auth as auth_views
from irctc.views import train as train_views
from irctc.views import booking as booking_views
from irctc.views import analytics as analytics_views

app_name = "irctc"

urlpatterns = [
    # ==================== Authentication APIs ==================== #
    
    path("auth/register/", auth_views.RegisterView.as_view(), name="auth-register"),
    path("auth/login/", auth_views.LoginView.as_view(), name="auth-login"),
    path("auth/me/", auth_views.UserDetailView.as_view(), name="auth-user-detail"),
    path("auth/token/refresh/", auth_views.TokenRefreshView.as_view(), name="auth-token-refresh"),
    path("auth/logout/", auth_views.LogoutView.as_view(), name="auth-logout"),
    
    # ==================== Train APIs ==================== #
    
    path("trains/search/", train_views.TrainSearchView.as_view(), name="train-search"),
    path("trains/", train_views.TrainCreateView.as_view(), name="train-create"),
    path("trains/<int:id>/", train_views.TrainUpdateView.as_view(), name="train-update"),
    path("trains/list/", train_views.TrainListView.as_view(), name="train-list"),
    #path("trains/detail/<int:train_id>/", train_views.TrainDetailView.as_view(), name="train-detail"),
    
    # ==================== Booking APIs ==================== #
    
    path("bookings/", booking_views.BookingCreateView.as_view(), name="booking-create"),
    path("bookings/my/", booking_views.UserBookingsView.as_view(), name="user-bookings"),
    #path("bookings/<int:booking_id>/", booking_views.BookingDetailView.as_view(), name="booking-detail"),
    path("bookings/<int:booking_id>/cancel/", booking_views.BookingCancelView.as_view(), name="booking-cancel"),
    #path("bookings/all/", booking_views.AllBookingsView.as_view(), name="all-bookings"),
    
    # ==================== Analytics APIs ==================== #
    path("analytics/top-routes/", analytics_views.TopRoutesAnalyticsView.as_view(), name="top-routes"),
    path("analytics/my-searches/", analytics_views.UserSearchAnalyticsView.as_view(), name="my-searches"),
]