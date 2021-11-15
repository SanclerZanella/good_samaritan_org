import os


os.environ["DJANGO_SECRET"] = "Your Django Secret"
os.environ["STRIPE_PUBLIC_KEY"] = "Your Stripe Public Key"
os.environ["CLIENT_SECRET"] = "Your Stripe Client Secret"
os.environ["STRIPE_WH_SECRET"] = "Your Stripe Webhook Secret"
os.environ["EMAIL_HOST_PASS"] = "Your email host password"
os.environ["EMAIL_HOST_USER"] = "Your email"
os.environ["DATABASE_URL"] = "Remote Database URL"

# This variable should not be added in production
os.environ["DEVELOPMENT"] = "true"
