from django.contrib import admin
from .models import Category, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    list_editable = ['is_active']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'discount_price', 'stock', 'is_featured', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['category', 'is_featured', 'is_new_arrival', 'is_best_seller', 'is_on_sale', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_featured', 'is_active', 'stock', 'price']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'description', 'image')
        }),
        ('Pricing', {
            'fields': ('price', 'discount_price', 'stock')
        }),
        ('Features', {
            'fields': ('is_featured', 'is_new_arrival', 'is_best_seller', 'is_on_sale', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone', 
                    'total_amount', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    list_editable = ['status']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at']