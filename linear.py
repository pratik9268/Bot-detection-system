from scipy.stats import linregress
import joblib
loaded_model = joblib.load('RandomForest.pkl')
mobile_model=joblib.load('update_Mobile_model.pkl')
def s(x,y):
# x=[976, 961, 952, 945, 940, 940, 938, 938, 938, 938, 939, 31]
# y=[302, 320, 332, 340, 345, 346, 348, 347, 346, 344, 344, 61]
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    return r_value

def find(r_value):
    if r_value**2 > 0.95:
        l='linear'
        # print("The movement is linear.")
        return l
    else:
        l='non linear'
        # print("The movement is non-linear.")
        return l


def predict_user(honeypot, mouse_movement):
    honeypot = 1 if honeypot == "Yes" else 0
    mouse_movement=1 if mouse_movement=='non linear' else 0
    prediction = loaded_model.predict([[honeypot, mouse_movement]])
    # print(prediction)
    # return "Bot" if prediction[0] == 1 else "Human"
    return prediction

def predict_user_mobile(honeypot,touch_events):
    honeypot = 1 if honeypot == "Yes" else 0
    touch_events=1 if touch_events=='Yes' else 0
    prediction = mobile_model.predict([[honeypot, touch_events]])
    # if prediction =='Bot':
    #     print('Bot')
    # else:
    #     print('Human')
    return prediction
# print(predict_user("Yes",l)) 
