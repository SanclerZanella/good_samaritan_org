stripeElements();

function stripeElements() {
  /*
    Render Card Element from Stripe and Submit Form
  */

  var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
  stripe = Stripe(stripePublicKey);

  // Render Card Element
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

    // Create Element
    var card = elements.create('card', { style: style });

    // Render Element
    card.mount('#card-element');

    // Add class to style on focus
    card.on('focus', function () {
      let el = document.getElementById('card-errors');
      el.classList.add('focused');
    });

    // Add class to style on blur
    card.on('blur', function () {
      let el = document.getElementById('card-errors');
      el.classList.remove('focused');
    });

    // Add class to style on change
    card.on('change', function (event) {
      displayError(event);
    });
  }
  
  // Handle Form Submission 
  let paymentForm = $('#sponsor-form');
  if (paymentForm) {

    // Form Submission
    paymentForm.submit((evt) => {
        
        // Prevent page to be reloaded
        evt.preventDefault();

        // Verify if details to profiles is checked
        let saveInfo = Boolean($('#id-save-info').prop('checked'));

        // Disable card element
        card.update({ 'disabled': true});

        // Submit data from form
        var data = {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'name': $.trim($('#id_full_name').val()),
            'email': $.trim($('#id_email').val()),
            'address1': $.trim($('#id_street_address1').val()),
            'address2': $.trim($('#id_street_address2').val()),
            'town_or_city': $.trim($('#id_town_or_city').val()),
            'country': $.trim($('#id_country').val()),
            'productId': $('#productId').val(),
            'save_info': saveInfo,
        };

        // Create new payment method & create subscription
        createPaymentMethod({ card }, data);
    });
  }

}

function createPaymentMethod({ card }, data) {
  /*
    Create new payment method & create subscription
  */

    // Disable submit button, Hide form and Show loading screen
    $('#submit-button').attr('disabled', true);
    $('#sponsor-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    // Set up payment method for recurring usage
    let token = data['csrfmiddlewaretoken'];

    // Create payment method
    stripe
      .createPaymentMethod({
        type: 'card',
        card: card,
        billing_details: {
          name: $.trim(data['name']),
          email: $.trim(data['email']),
          address:{
              line1: $.trim(data['address1']),
              line2: $.trim(data['address2']),
              city: $.trim(data['town_or_city']),
              country: $.trim(data['country']),
          },
        },
      })
      .then((result) => {

        // Display any error
        if (result.error) {
          displayError(result);

        } else {

         // Set payment parameters 
         const paymentParams = {
              price_id: $('#priceId').val(),
              payment_method: result.paymentMethod.id,
              data_form: data
          };
          
          // Send data to server for customer and subscription creation
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

            // Load Sponsor(subscription) success page
            if (result.status === 200) {
              window.location.href = result.url;
            }

          });

        }

      });
}

function displayError(event) {
  /*
    Display any error to erros element under the card element
  */
 
    // Render error message
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
