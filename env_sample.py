import os


os.environ["DJANGO_SECRET"] = "Your Django Secret"
os.environ["STRIPE_PUBLIC_KEY"] = "Your Stripe Public Key"
os.environ["STRIPE_SECRET_KEY"] = "Your Stripe Client Secret"
os.environ["STRIPE_WH_SECRET"] = "Your Stripe Webhook Secret"
os.environ["EMAIL_HOST_PASS"] = "Your email host password"
os.environ["EMAIL_HOST_USER"] = "Your email"
os.environ["AWS_ACCESS_KEY_ID"] = "From downloaded amazon CSV file"
os.environ["AWS_SECRET_ACCESS_KEY"] = "From downloaded amazon CSV file"

# This variable should not be added in production
os.environ["DEVELOPMENT"] = "true"
