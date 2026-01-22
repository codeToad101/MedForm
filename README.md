This is a demo Medical Intake form for public use!

There an in-line comments with potential features to be added and improvements to be made. Visuals are one such thing that could be improved. I recommend students work to understand the existing code before they progress to making improvements.

To run the app as-is, run in terminal:
flask --app wellness run

Ctrl + C to close when you're done viewing

NOTES:

To install dependencies, run in terminal:
pip install -r requirements.txt

For everything to work as intended, you must create a SQL DB (local or not) and pop its details @ route wellness/secret.py (can be edited). Be mindful of what that means depending on the kind of SQL DB you decide to use. I ran a local MySQL DB for my purposes. You must also pop an initial "Admin" in.

You may also need to create a python .venv with which to run the process. Do NOT push DB secrets/.env back to Git -- it is a safety issue (for you, not me).

I hope this will be of some use!

Let it be known that this project is a demo/template and is not HIPAA-compliant by default.
It is provided for educational purposes only and should not be used in production medical environments without proper legal, security, and compliance review. No warranty is provided, express or implied.
MIT Licensed