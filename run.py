from app import createApp 
import os
from dotenv import load_dotenv
load_dotenv()

app=createApp()
 
# if __name__=='__main__':
#     app.run(port=os.getenv('PORT'),debug=True)