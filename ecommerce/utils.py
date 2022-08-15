from dateutil.relativedelta import *
from datetime import datetime
from django.conf import settings
from .models import Wallet, Source, Invoice, Line, CartItem, Cart
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

class EcommerceManager:
    '''
    This manager allows work through app specific logic and also call 
    API end points for our payment processing company, Stripe. 
    '''
    def __init__(self, user, *args, **kwargs):
        '''
        A whole bunch of intance variables.
        '''
        self.user = user
        self.up = self.user.userprofile
        self.token = kwargs.get("token")
        self.source_id = kwargs.get("source_id")
        self.invoice_id = kwargs.get("invoice_id")
        self.invoice_item_id = kwargs.get("invoice_item_id")
        self.currency = 'GBP' 
        self.description = 'Django demo'
        
    #-------- Application methods ---------#

    def stripe_id(self):
        '''
        Returns a user stripe id.
        The user's stripe id is stored in their linked wallet instance.
        '''
        wallet = self.wallet_object()
        if not wallet.stripe_id:
            self.post_profile()			
        return wallet.stripe_id

    def cart_object(self):
        '''
        Used to get or create linked Cart.
        Negates the need for signals.
        Returns Cart object.
        '''
        cart, created = Cart.objects.get_or_create(user = self.user)
        return cart

    def wallet_object(self):
        '''
        Used to get or create linked Wallet.
        Negates the need for signals.
        Returns Wallet object.
        '''
        wallet, created = Wallet.objects.get_or_create(user = self.user)
        return wallet

    def source_object(self, id):
        '''
        Used to get or create Source object.
        Returns Source object.
        '''
        source, created = Source.objects.get_or_create(stripe_id = id)
        if self.token:
            source.is_default = True
            source.save()
        wallet = self.wallet_object()
        wallet.sources.add(source)
        wallet.save()
        return source

    def line_object(self, id, item_obj):
        '''
        Used to get or create Line object.
        Returns Line object.
        '''
        line, created = Line.objects.get_or_create(stripe_id = id)
        line.item = item_obj.item
        line.user = self.user
        line.quantity = item_obj.quantity
        line.amount = item_obj.amount() / 100
        line.amount_currency = self.currency
        line.save()
        return line

    def invoice_object(self, id, items, source_id):
        '''
        Used to get or create Invoice object.
        Returns Invoice object.
        '''
        invoice, created = Invoice.objects.get_or_create(stripe_id = id)
        for item in items:
            invoice.lines.add(item)
            invoice.save()
        invoice.user = self.user
        invoice.source = Source.objects.get(stripe_id = source_id)
        invoice.save()
        wallet = self.wallet_object()
        wallet.invoices.add(invoice)
        wallet.save()
        return invoice

    def create_stripe_address(self):
        '''
        Used to create a 'Stripe' friendly address dict
        Returns a dict.
        '''
        address={
            "line1":self.up.address,
            "city":self.up.town,
            "state":self.up.county,
            "postal_code": self.up.post_code,
            "country": self.up.country_alpha_2
            }
        return address

    
    def get_source_data(self):
        '''
        Used to get Source object data
        Returns a dict.
        {"sources":{},"has_sources":False}
        '''
        source_data = {"sources":{},"has_sources":False}
        try:
            sources = self.list_sources()
            customer = self.get_profile()
            default_source = customer["default_source"]
            source_obj = self.source_object(default_source)
            source_obj.is_default = True
            source_obj.save()
            exclude_id = [source_obj.id]
            #manage default
            user_sources = self.wallet_object().sources.exclude(id__in=exclude_id)
            for source in user_sources:
                source.is_default = False
                source.save()
            source_list = []
            for source in sources["data"]:
                source_info = {"id": "", "stripe_id": "", "type": "", "card": "", "exp": "", "default": ""}
                date = datetime.strptime(f'{source["exp_month"]}/{source["exp_year"]}', '%m/%Y')
                date2 = date + relativedelta(months=+1)
                exp_date = date2 + relativedelta(days=-1)
                today = date.today()

                source_obj = self.source_object(source["id"])
                if today <= exp_date:
                    source_info["id"] = source_obj.id
                    source_info["stripe_id"] = source["id"]
                    source_info["type"] = source["brand"]
                    source_info["default"] = source_obj.is_default
                    source_info["card"] = f'**** {source["last4"]}'

                    if source["exp_month"] < 9:
                        mnt = f'0{source["exp_month"]}'
                    else:
                        mnt = source["exp_month"]

                    year = source["exp_year"] - 2000
                    source_info["exp"] = f'{mnt}/{year}'
                    
                source_list.append(source_info)
            source_data["has_sources"] = True
            source_data["sources"] = source_list
        except:
            return source_data
        return source_data
        
    def get_invoice_data(self):
        '''
        Used to get Invoice object data
        Returns a dict.
        {"invoices":{},"has_invoices":False}
        '''
        invoice_data = {"invoices":{},"has_invoices":False}
        try:
            invoices = self.list_invoices()
            invoice_list = []
            for invoice in invoices["data"]:
                invoice_info = {
                    "invoice_id": invoice["id"], 
                    "invoice_url": invoice["hosted_invoice_url"], 
                    "invoice_pdf": invoice["invoice_pdf"], 
                    "invoice_description": invoice["lines"]["data"][0]["description"],
                    "invoice_total": invoice["amount_paid"]/100,
                    "invoice_paid": invoice["paid"],
                    "invoice_date": datetime.fromtimestamp(int(invoice["created"])).strftime('%d-%m-%Y'),
                    }

                invoice_list.append(invoice_info)
            invoice_data["has_invoices"] = True
            invoice_data["invoices"] = invoice_list

        except:
            return invoice_data
        return invoice_data


    #-------- Stripe API methods ---------#

    ##Stripe Customer API
    def get_profile(self):
        '''
        Docs - https://stripe.com/docs/api/customers/retrieve?lang=python
        '''
        stripe_customer = stripe.Customer.retrieve(
            self.stripe_id(),
            )
        return stripe_customer


    def post_profile(self):
        '''
        Docs - https://stripe.com/docs/api/customers/create?lang=python
        '''
        stripe_customer = stripe.Customer.create(
            email = self.user.email, 
            name = self.up.full_name(),
            address = self.create_stripe_address()
            )
        wallet = self.wallet_object()
        wallet.stripe_id = stripe_customer["id"]
        wallet.save()
        return stripe_customer


    def put_profile(self):
        '''
        Docs - https://stripe.com/docs/api/customers/modify?lang=python
        '''
        stripe_customer = stripe.Customer.modify(
            self.stripe_id(),
            email = self.up.email(), 
            name = self.up.full_name(),
            address = self.create_stripe_address()
            )
        return stripe_customer

    ##Stripe Sources/Cards API
    def list_sources(self):
        '''
        Docs - https://stripe.com/docs/api/cards/list?lang=python
        '''
        try:
            sources = stripe.Customer.list_sources(self.stripe_id(),limit=3,object='card')
        except TypeError:
            sources = []
        return sources


    def get_source(self):
        '''
        Docs - https://stripe.com/docs/api/cards/retreive?lang=python
        '''
        source = stripe.Customer.retrieve_source(self.stripe_id(),self.source_id)
        return source


    def put_source(self, source_id):
        '''
        Docs - https://stripe.com/docs/api/cards/update?lang=python
        '''
        source = stripe.Customer.retrieve_source(self.stripe_id(),source_id)
        put_source = stripe.Customer.modify(
                    self.stripe_id(), 
                    default_source=source["id"],
                    )
        source_obj = self.source_object(source["id"])
        source_obj.is_default = True
        source_obj.save()
        return put_source


    def post_source(self):
        '''
        Docs - https://stripe.com/docs/api/cards/create?lang=python
        '''
        stripe_id = self.stripe_id()
        source = stripe.Customer.create_source(
            stripe_id,
            source=self.token
            )
        self.put_source(source["id"])
        return source


    ##Stripe Invoice item API
    def get_invoice_item(self):
        '''
        Docs - https://stripe.com/docs/api/invoiceitems/retrieve?lang=python
        '''
        invoice_item = stripe.InvoiceItem.retrieve(self.invoice_item_id)
        return invoice_item


    def put_invoice_item(self):
        '''
        Docs - https://stripe.com/docs/api/invoiceitems/modify?lang=python
        '''
        invoice_item = stripe.InvoiceItem.modify(self.invoice_item_id)
        return invoice_item


    def post_invoice_item(self, item):
        '''
        Docs - https://stripe.com/docs/api/invoiceitems/create?lang=python
        '''
        quantity = int(item.quantity)
        amount = int(item.amount())
        unit_amount = int(amount / quantity)
        line = stripe.InvoiceItem.create(
            customer= self.stripe_id(),
            unit_amount= unit_amount,
            quantity = int(item.quantity),
            currency=self.currency.lower(),
            description= item.item.title
            )
        line = self.line_object(line["id"], item)
        return line


    ##Stripe Invoice item API
    def list_invoices(self):
        '''
        Docs - https://stripe.com/docs/api/invoices/list?lang=python
        '''
        invoices = stripe.Invoice.list(self.stripe_id())
        return invoices


    def get_invoice(self):
        '''
        Docs - https://stripe.com/docs/api/invoices/retreive?lang=python
        '''
        invoice = stripe.Invoice.retrieve(self.invoice_id)
        invoice_info = {
                    "invoice_id": invoice["id"], 
                    "invoice_url": invoice["hosted_invoice_url"], 
                    "invoice_pdf": invoice["invoice_pdf"], 
                    "invoice_description": invoice["lines"]["data"][0]["description"],
                    "invoice_total": invoice["amount_paid"]/100,
                    "invoice_paid": invoice["paid"],
                    "invoice_date": datetime.fromtimestamp(int(invoice["created"])).strftime('%d-%m-%Y'),
                    }
        return invoice_info

    def put_invoice(self, method, invoice_id, **kwargs):
        '''
        Docs - https://stripe.com/docs/api/invoices/finalize?lang=python
        Docs - https://stripe.com/docs/api/invoices/pay?lang=python
        '''
        source_id = kwargs.get("source_id")
        match method:
            case 'finalize':
                invoice = stripe.Invoice.finalize_invoice(invoice_id)
            case 'pay':
                invoice = stripe.Invoice.pay(invoice_id,source=source_id)
        return invoice



    def post_invoice(self):
        '''
        Docs - https://stripe.com/docs/api/invoices/create?lang=python
        '''
        cart = self.cart_object()
        amount = cart.amount

        if self.token:
            source = self.post_source()
            self.source_id = source["id"]
        
        #create invoice items
        items = []
        for item in cart.items.all():
            items.append(self.post_invoice_item(item))
        
        #created invoice items will automatically be added to this invoice
        new_invoice = stripe.Invoice.create(
            customer=self.stripe_id(),
            collection_method="charge_automatically",
        )

        #manually finalize the invoice before making a payment request
        invoice = self.put_invoice('finalize', new_invoice.id)

        try:
            self.put_invoice('pay', invoice.id, source_id = self.source_id)
            invoice = self.invoice_object(invoice.id, items, self.source_id)

            
        except stripe.error.CardError as e:
            message = "Card Error"
            status = "500"
            return {"status": status, "message": message}

        except stripe.error.RateLimitError as e:
            message = "Rate limit error"
            status = "500"
            return {"status": status, "message": message}
        
        except stripe.error.InvalidRequestError as e:
            message = "Invalid parameter"
            status = "500"
            return {"status": status, "message": message}
        
        except stripe.error.AuthenticationError as e:
            message = "Not authenticated"
            status = "500"
            return {"status": status, "message": message}

        except stripe.error.APIConnectionError as e:
            message = "Network error"
            status = "500"
            return {"status": status, "message": message}
        
        except stripe.error.StripeError as e:
            message = "Something went wrong, you were not charged"
            status = "500"
            return {"status": status, "message": message}
        
        except Exception as e:
            message = "Serious error, we have been notified"
            status = "500"
            return {"status": status, "message": message}

        #clear carts
        CartItem.objects.clear_items(self.user)
        
        message = "Success! Your payment was successful"
        status = "200"
        return {"status": status, "message": message, "id":invoice.id}