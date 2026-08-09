from django.contrib import admin
from .models import Category, Product, Order, OrderItem, UserProfile

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'quantity', 'price')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'original_price', 'stock', 'rating', 'is_featured', 'is_popular')
    list_filter = ('category', 'is_featured', 'is_popular')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'is_featured', 'is_popular')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'phone', 'city', 'total_amount', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('order_number', 'full_name', 'email', 'phone', 'city', 'pincode')
    inlines = [OrderItemInline]
    list_editable = ('status',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'state', 'pincode')
    search_fields = ('user__username', 'user__email', 'phone', 'city', 'pincode')
