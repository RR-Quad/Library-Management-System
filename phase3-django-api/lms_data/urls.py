"""
URL configuration for the Library Management System API.

This module defines all API routes including:

• REST API endpoints for all resources
• Library statistics endpoint
• OpenAPI schema generation
• Swagger API documentation

The API follows RESTful conventions and uses Django REST Framework routers
for automatic endpoint generation.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from .views import (
    LibraryViewSet,
    BookViewSet,
    AuthorViewSet,
    CategoryViewSet,
    MemberViewSet,
    BorrowingViewSet,
    ReviewViewSet,
    StatisticsAPIView,
)


# =========================================================
# API Router
# =========================================================

"""
The DefaultRouter automatically generates the following endpoints
for each registered ViewSet:

GET      /resource/          -> list
POST     /resource/          -> create
GET      /resource/{id}/     -> retrieve
PUT      /resource/{id}/     -> update
PATCH    /resource/{id}/     -> partial update
DELETE   /resource/{id}/     -> delete
"""

router = DefaultRouter()

router.register(r"libraries", LibraryViewSet, basename="libraries")
router.register(r"books", BookViewSet, basename="books")
router.register(r"authors", AuthorViewSet, basename="authors")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"members", MemberViewSet, basename="members")
router.register(r"borrowings", BorrowingViewSet, basename="borrowings")
router.register(r"reviews", ReviewViewSet, basename="reviews")


# =========================================================
# URL Patterns
# =========================================================

urlpatterns = [

    # -----------------------------------------------------
    # Core API Endpoints
    # -----------------------------------------------------

    path("", include(router.urls)),

    # Library analytics and statistics
    path(
        "statistics/",
        StatisticsAPIView.as_view(),
        name="library-statistics"
    ),


    # -----------------------------------------------------
    # OpenAPI Schema
    # -----------------------------------------------------

    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema"
    ),


    # -----------------------------------------------------
    # API Documentation
    # -----------------------------------------------------

    # Swagger UI
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),

    # ReDoc Documentation
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]