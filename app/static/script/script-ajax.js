document.addEventListener('DOMContentLoaded', () => {
    const button = document.querySelector('#checkout');
    
    button.addEventListener('click', event => {
        fetch('/checkout')
        .then((result) => {
            return result.json();
        })
        .then((data) => {
            var stripe = Stripe(data.checkout_public_key);
            stripe.redirectToCheckout({
                sessionId: data.checkout_session_id
            }).then(function (result) {
                // Handle any errors during redirection
                if (result.error) {
                    console.error(result.error.message);
                }
            });
        });
    });
});
