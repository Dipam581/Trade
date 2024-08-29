from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import creationData, BuyModel, NotifyAndWishlistModel
from django.contrib.auth import logout
from .utils import send_mail
from Login.models import CustomUser
from django.contrib.auth.models import User
from django.db.models import Q
import razorpay

def option_of_trading(request):
    return render(request, 'option.html')

def logout_user(request):
    logout(request)
    return redirect("/login")

def send_mail_Test(request):
    send_mail()
    return redirect("/option")

def wishlist(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        try:
            NotifyAndWishlistModel.objects.filter(product_id = product_id).delete()
            messages.info(request, "This product is removed from your wishlist")
        except:
            print("Error Occured")

    context = request.session.get('context', {})
    html_object = []
    notify_data = NotifyAndWishlistModel.objects.filter(bider_id = context["uuid"])
    for no in notify_data:
        product_details = creationData.objects.filter(product_id = no.product_id)
        temp_obj = {
            "id": str(product_details[0].product_id),
            "name": product_details[0].name,
            "desc": product_details[0].description,
            "image": product_details[0].image
        }
        html_object.append(temp_obj)
    return render(request, 'wishlist.html',{"html_object" : html_object})


def add_product_for_bid(request):
    context = request.session.get('context', {})
    if request.method == "POST":
        if(request.POST.get("removeBid") and request.POST.get("removeBid").split("_")[0] == "removeBid"):
            product_id = request.POST.get(f"product_id_{request.POST.get("removeBid").split("_")[1]}")
            try:
                creationData.objects.filter(product_id= product_id).delete()
            except:
                print("Exception")
        else:
            item_name = request.POST.get("item")
            item_description = request.POST.get("description")
            item_amount = request.POST.get("amount")
            file = request._files['file']
            bidData = creationData(owner_id= context["uuid"], name= item_name, price= item_amount, description= item_description, image = file)
            bidData.save()
    
    owner_data = {}
    if (len(creationData.objects.filter(owner_id= context["uuid"]))):
        owner_data = creationData.objects.filter(owner_id= context["uuid"])

    return render(request, 'bid_creation.html', {'userContext': context["fullName"], 'ownerData': owner_data})


#Show all products
def show_all_products(request):
    context = request.session.get('context', {})
    listed_obj = creationData.objects.filter(~Q(owner_id=context["uuid"]))
    return render(request, 'all_products.html',{"listed_obj": listed_obj})

    
# process to buy
def buy_product(request, product_id = None):
    if request.method == "POST":

        context = request.session.get('context', {})
        productDetails = creationData.objects.filter(product_id = product_id)
        owner_id = productDetails[0].owner_id
        current_price = productDetails[0].price
        updated_price = request.POST.get("updatedPrice")
        
        buyModel = BuyModel(owner_id = str(owner_id), bider_id = context["uuid"], original_price = current_price, updated_price = updated_price, product_id= product_id)
        buyModel.save()

        owner_mail = CustomUser.objects.filter(unique_key=owner_id)[0]
        name = User.objects.get(username= owner_mail).first_name
        msg = f"Hi {name}, You have a sell request from a buyer. Please visit TradeSquare."

        send_mail(msg, owner_mail)
        return redirect("/deals")


    product = creationData.objects.filter(product_id=product_id)
    user = CustomUser.objects.get(unique_key= product[0].owner_id)

    userContext = {
        "email": user.user
    }
    return render(request,"buy_screen.html", {"selectedData": product, "userContext": userContext})


def added_wishlist(request,product_id):
    
    context = request.session.get('context', {})
    productDetails = creationData.objects.filter(product_id = product_id)
    owner_id = productDetails[0].owner_id
    print(context["uuid"], " --", product_id)
    verify_data = NotifyAndWishlistModel.objects.filter(product_id = product_id, bider_id = context["uuid"])
    
    if(not verify_data):
        notify_wish_Model = NotifyAndWishlistModel(product_id = product_id, owner_id = str(owner_id), bider_id = context["uuid"], isWishlisted = True)
        notify_wish_Model.save()
        messages.success(request, "This product is added tot your wishlist")
    else:
        messages.info(request, "You have already wishlisted this item")

    return redirect("/deals")


#Sell product by owner

def sell_product(request):
    if request.method == "POST":
        product_id = request.POST.get("id")
        updatedPrice = request.POST.get("updatedPrice")
        buyer_id = request.POST.get("buyer_id")
        results = BuyModel.objects.filter( Q(product_id=product_id) & Q(bider_id=buyer_id))
        results.update(updated_price= updatedPrice)
        results.update(updatedByOwner= True)

        bider_mail = CustomUser.objects.filter(unique_key=buyer_id)[0]
        msg = f"Dear buyer, You have some new update on your bidded product. Please visit TradeSquare to know more!"
        send_mail(msg, bider_mail)

    context = request.session.get('context', {})
    owner_products = BuyModel.objects.filter(owner_id= context["uuid"])
    sell_object = []
    for pro in owner_products:
        product_details = creationData.objects.filter(product_id = pro.product_id)
        temp_obj = {
            "id": str(product_details[0].product_id),
            "name": product_details[0].name,
            "desc": product_details[0].description,
            "image": product_details[0].image,
            "curr_price": pro.original_price,
            "up_price": pro.updated_price,
            "buyer_id": pro.bider_id
        }
        sell_object.append(temp_obj)

    return render(request,"sell_product_list.html",{"owner_products": sell_object})


#View orders
def view_Orders(request):
    context = request.session.get('context', {})

    if request.method == "POST":
        button_value = request.POST.get("submit_button")
        button_value_To_purchase = request.POST.get("confirm_button")

        if(button_value):
            product_id = request.POST.get(f"product_id_{button_value}")
            order_id = request.POST.get(f"order_id_{button_value}")
            product = creationData.objects.filter(product_id=product_id)
            user_email = CustomUser.objects.get(unique_key= product[0].owner_id).user
            buy_product = BuyModel.objects.filter(order_id= order_id)[0]
            userContext = {
                "email": user_email,
                "flag": buy_product.updatedByOwner,
                "updated_price": buy_product.updated_price,
                "fromOrder": True
            }
            return render(request,"payment.html", {"selectedData": product, "userContext": userContext})
        else:
            updatedPrice = request.POST.get("updatedPrice")
            amount_in_paise = int(updatedPrice) * 100
            client = razorpay.Client(auth=("rzp_test_EhJqnkheuy4JLE", "uYC2jTPgYlcFaP9AGVqaXjgz"))
            data = { "amount": amount_in_paise, "currency": "INR", "receipt": "order_rcptid_11" }
            payment = client.order.create(data=data)
            order_id = payment.get('id')
            return render(request, "pay.html", {"order_id": order_id, "updatedPrice": updatedPrice})

    logged_in_user_order = BuyModel.objects.filter(bider_id= context["uuid"])
    order_object = []
    for order in logged_in_user_order:
        product_details = creationData.objects.filter(product_id = order.product_id)
        temp_obj = {
            "id": str(product_details[0].product_id),
            "name": product_details[0].name,
            "desc": product_details[0].description,
            "image": product_details[0].image,
            "actionByOwner": order.updatedByOwner,
            "order_id": order.order_id
        }
        order_object.append(temp_obj)

    return render(request,"order.html",{"logged_in_user_order": order_object})


#Initiate payment and post buy stuffs

def payment_and_post_buy(request):
    if request.method == "POST":
        client = razorpay.Client(auth=("rzp_test_EhJqnkheuy4JLE", "uYC2jTPgYlcFaP9AGVqaXjgz"))
        data = { "amount": 100, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        order_id = payment.get('id')  # Get the generated order_id

        return render(request, "pay.html", {"order_id": order_id})

    return render(request, "pay.html")

    
    