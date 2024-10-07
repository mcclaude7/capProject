from rest_framework import serializers
from .models import Product, Category, Review, ProductImage, Wishlist, Promotion

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

# Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Display username

    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

# Product Image Serializer
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image_url']



# Wishlist Serializer
class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product']  

# Promotion Serializer
class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['id', 'product', 'discount_percentage', 'start_date', 'end_date']

# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)  # Add this line to include reviews
    images = ProductImageSerializer(many=True, read_only=True)  
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category','category_id', 'stock_quantity', 'image_url', 'created_date','reviews', 'images']
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value
    
    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value




