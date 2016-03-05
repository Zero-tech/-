import sae
sae.add_vendor_dir('vendor')
import sys
import os
app_root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(app_root, 'vendor'))
print sys.path
import sae
from myapp import app
application = sae.create_wsgi_app(app)
