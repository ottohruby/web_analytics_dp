from src import create_app
from src.config import Config

application = create_app()

if __name__ == '__main__':
  application.run(debug=True)