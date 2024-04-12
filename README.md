# UrbanShop

UrbanShop is an e-commerce web application built using Flask for the backend and HTML, CSS(Bootstrap)

## Features

- **Buy and Sell Items**: Users can buy and sell items on the platform.
- **Item Classification**: Items are tagged with classifications such as clothes, cars, houses, accessories.
- **Search and Filter**: Users can search for items and apply filters to find their desired items easily.
- **Item Availability**: Each item has a sold/available tag indicating its availability status.
- **Shopping Cart**: Users can add items to their cart for future purchase.
- **Payment**: Users can make payments for items in their cart.
- **Chat with Seller**: Users can chat with the seller to negotiate on price and delivery details.

## Getting Started

Follow these instructions to run UrbanShop locally.

### Prerequisites

- Python 3.x
- pip (Python package manager)
- Flask

### Installation

1. Clone the repository:
git clone https://github.com/your-username/UrbanShop.git

2. Navigate to the project directory:
cd UrbanShop

3. Virtual Enviroment:
source venv/bin/activate

4. Install dependencies:
pip install -r requirements.txt



### Running the Application

1. Set the Flask app:

## On Unix/Linux: 
export FLASK_APP=app

## On Windows (Command Prompt):
set FLASK_APP=app

## On Windows (PowerShell):
$env:FLASK_APP = "app"

2. Initialize the database:
flask init-db

3. Run the application:
flask run

The application should now be running locally. Access it by navigating to `http://localhost:5000` in your web browser.

## Contributing

Contributions are welcome! Please feel free to open issues or pull requests for bug fixes, improvements, or new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.