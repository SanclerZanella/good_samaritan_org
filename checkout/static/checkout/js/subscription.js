stripeElements();

function stripeElements() {
  var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
  stripe = Stripe(stripePublicKey);

  if ($('#card-element')) {
    let elements = stripe.elements();

    // Card Element styles
    let style = {
        base: {
            color: '#000',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#aab7c4'
            }
        },
        invalid: {
            color: '#dc3545',
            iconColor: '#dc3545'
        }
    };


    var card = elements.create('card', { style: style });

    card.mount('#card-element');

    card.on('focus', function () {
      let el = document.getElementById('card-errors');
      el.classList.add('focused');
    });

    card.on('blur', function () {
      let el = document.getElementById('card-errors');
      el.classList.remove('focused');
    });

    card.on('change', function (event) {
      displayError(event);
    });
  }
  
  let paymentForm = $('#sponsor-form');
  if (paymentForm) {

    paymentForm.submit((evt) => {
        evt.preventDefault();
        var data = {
            'name': $('#id_full_name').val(),
            'csrfToken': $('input[name="csrfmiddlewaretoken"]').val(),
            'email': $('#id_email').val(),
            'address1': $('#id_street_address1').val(),
            'address2': $('#id_street_address2').val(),
            'town_or_city': $('#id_town_or_city').val(),
            'country': $('#id_country').val(),
        }

        // create new payment method & create subscription
        createPaymentMethod({ card }, data);
    });
  }

}

function createPaymentMethod({ card }, data) {

    // Set up payment method for recurring usage
    let billingName = data['name'];
    let token = data['csrfToken']
  
    stripe
      .createPaymentMethod({
        type: 'card',
        card: card,
        billing_details: {
          name: billingName,
        },
      })
      .then((result) => {
        if (result.error) {
          displayError(result);
        } else {
         const paymentParams = {
            price_id: $('#priceId').val(),
            payment_method: result.paymentMethod.id,
            data_form: data
        };

        fetch('/checkout/subscription_checkout/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-CSRFToken': token,
          },
          credentials: 'same-origin',
          body: JSON.stringify(paymentParams),
        }).then((result) => {
          if (result.error) {
            // The card had an error when trying to attach it to a customer
            throw result;
          }
          return result;
        }).then((result) => {
          if (result.status === 200) {
  
            window.location.href = result.url;
          };
        })
        }
      });
}

function displayError(event) {
 
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
}
