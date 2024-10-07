from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category, User, Review, ProductImage, Wishlist, Promotion
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer, ProductImageSerializer, WishlistSerializer, PromotionSerializer

# Product ViewSet
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
     
    @action(detail=True, methods=['POST'])
    def purchase(self, request, pk=None):
        product = self.get_object()
        quantity = int(request.data.get('quantity', 1))
        try:
            product.reduce_stock(quantity)
            return Response({'status': 'purchase successful'}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # Filters and search
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'price', 'stock_quantity']
    search_fields = ['name', 'category__name']
    ordering_fields = ['price', 'created_date']

# Category ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# Review ViewSet
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Associate the review with the logged-in user
        serializer.save(user=self.request.user)

    def get_permissions(self):
        # Allow only the creator of the review to update or delete it
        if self.action in ['update', 'partial_update', 'destroy']:
            review = self.get_object()
            if review.user != self.request.user:
                raise PermissionDenied("You do not have permission to modify this review.")
        return super().get_permissions()

#ProductImage ViewSet
class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    #permission_classes = [permissions.IsAuthenticated]

# Wishlist ViewSet
class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
   # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#Promotion ViewSet
class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
