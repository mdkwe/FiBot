from flask import Flask
from config import Config
from main import main_bp
from company import company_bp

app = Flask(__name__)
app.config.from_object(Config)

# Register blueprints
app.register_blueprint(main_bp, url_prefix='/')
app.register_blueprint(company_bp, url_prefix='/company')

if __name__ == '__main__':
    app.run(debug=True)
